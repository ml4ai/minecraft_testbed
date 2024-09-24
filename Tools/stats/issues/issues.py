#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Chuck Kapopoulos"
__version__ = "0.1.0"
__license__ = "Aptima, Inc."

import argparse
import sys
import gitlab
import json
import csv
import yaml
from datetime import datetime
from dateutil.relativedelta import relativedelta
import iso8601


def main(prior_issue_date: datetime = None, current_issue_date: datetime = None, next_issue_date: datetime = None):
    """ Main entry point of the app """
    with open("config.yaml", "r") as configFile:
        config = yaml.safe_load(configFile)
    # print(json.dumps(config['projects']))

    project_rows = []
    latest_time = None
    time = None
    for configProject in config['projects']:
        gl = gitlab.Gitlab(url=config['url'], private_token=configProject['token'])
        project = gl.projects.get(configProject['id'])
        if prior_issue_date is None:
            issues = project.issues.list(scope='all', all=True)
        else:
            issues = project.issues.list(scope='all', all=True)  # created_after=prior_issue_date.isoformat()
        time, rows = create_rows(project, issues, prior_issue_date, current_issue_date, next_issue_date)
        project_rows.extend(rows)
        if latest_time is None:
            latest_time = time
        else:
            if time > latest_time:
                latest_time = time
        # print(configProject['name'])
    if time is None:
        filename = 'issues.csv'
    else:
        filename = 'issues_' + time.strftime('%Y%m%d-%H.%M.%S.%f')[:-3] + '.csv'
    create_csv(project_rows, filename)
    print('File ' + filename + ' created!')


def create_rows(project, issues, prior_issue_date, current_issue_date, next_issue_date):
    rows = []
    latest_updated_at = None
    updated_at = None
    for issue in issues:
        updated_at = iso8601.parse_date(issue.updated_at)
        if latest_updated_at is None:
            latest_updated_at = updated_at
        else:
            if updated_at > latest_updated_at:
                latest_updated_at = updated_at

        notes = issue.notes.list()
        discussions = issue.discussions.list()
        created_at = iso8601.parse_date(issue.updated_at)
        due_date = iso8601.parse_date(issue.due_date) if issue.due_date is not None else (
                current_issue_date + relativedelta(months=1)).replace(
            tzinfo=iso8601.UTC)
        updated_at = iso8601.parse_date(issue.updated_at)
        status_new = 'yes' if issue.state == 'opened' and created_at > prior_issue_date.replace(
            tzinfo=iso8601.UTC) else 'no'
        if due_date is None:
            status_action_pending = 'yes'
        else:
            status_action_pending = 'yes' if issue.state == 'opened' and (
                    current_issue_date.replace(tzinfo=iso8601.UTC) <= due_date < next_issue_date.replace(
                        tzinfo=iso8601.UTC)) else 'no'
        status_closed = 'yes' if issue.state == 'closed' and updated_at > prior_issue_date.replace(
            tzinfo=iso8601.UTC) and (
                                         updated_at <= current_issue_date.replace(tzinfo=iso8601.UTC)) else 'no'
        status_changed = 'yes' if issue.state == 'opened' and updated_at > prior_issue_date.replace(
            tzinfo=iso8601.UTC) and (
                                          updated_at <= current_issue_date.replace(tzinfo=iso8601.UTC)) else 'no'

        row = [project.name, issue.id, issue.iid, issue.title, issue.web_url,
               'None' if not issue.description else issue.description,
               issue.author['name'], issue.created_at, issue.updated_at, due_date.isoformat().replace('+00:00', 'Z'),
               [a['name'] for a in issue.assignees], len(notes), len(discussions),
               [note['author']['name'] for discussion in discussions for note in discussion.attributes['notes']],
               issue.labels, issue.state, status_new, status_action_pending, status_closed, status_changed]
        rows.append(row)
    return updated_at, rows


def create_csv(rows, filename):
    header = ['project', 'id', 'iid', 'title', 'web_url', 'description', 'author', 'created_at', 'updated_at',
              'due_date', 'assignee names', 'note count',
              'commenter count', 'commenter names', 'issue labels', 'state', 'status: new', 'status: action pending',
              'status: closed', 'status: changed']

    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    if len(sys.argv) == 1:
        main()
    else:
        parser = argparse.ArgumentParser(description='Issues report.')
        parser.add_argument('-p', '--prior', help='Prior Issue Date', required=True)
        parser.add_argument('-c', '--current', help='Current Issue Date', required=True)
        parser.add_argument('-n', '--next', help='Next Issue Date', required=True)
        args = vars(parser.parse_args())

        prior_issue = datetime.strptime(args['prior'], '%Y-%m-%d')
        current_issue = datetime.strptime(args['current'], '%Y-%m-%d')
        next_issue = datetime.strptime(args['next'], '%Y-%m-%d')
        main(prior_issue_date=prior_issue, current_issue_date=current_issue, next_issue_date=next_issue)
