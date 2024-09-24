import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoggingService } from '../logging/logging.service';
import { Observable, of } from 'rxjs';
import { Trial } from '../trial/trial';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { TrialMessage } from '../trial/trial-message';
import { TrialExportMessage } from '../trial/trial-export-message';
import { MqttService } from 'ngx-mqtt';
// import moment from 'moment';

const moment = require('moment');

@Injectable({
  providedIn: 'root'
})
export class TrialService {
  private trialsUrl = environment.metadataAppUrl + '/trials';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private loggingService: LoggingService,
    private mqttService: MqttService
  ) { }

  /** GET trials from the server */
  readTrials(): Observable<Trial[]> {
    return this.http.get<Trial[]>(this.trialsUrl)
      .pipe(
        tap(_ => this.log('Read trials')),
        catchError(this.handleError<Trial[]>('readTrials', []))
      );
  }

  /** GET trials by id. Return `undefined` when id not found */
  readTrialNo404<Data>(id: number): Observable<Trial> {
    const url = `${this.trialsUrl}/?id=${id}`;
    return this.http.get<Trial[]>(url)
      .pipe(
        map(trials => trials[0]), // returns a {0|1} element array
        tap(h => {
          const outcome = h ? `Read` : `Did not find`;
          this.log(`${outcome} trial id=${id}`);
        }),
        catchError(this.handleError<Trial>(`getTrials id=${id}`))
      );
  }

  /** GET trials by uuid. Return `undefined` when id not found */
  readTrialUUID(uuid: string): Observable<Trial> {
    const url = `${this.trialsUrl}/uuid/${uuid}`;
    return this.http.get<Trial>(url).pipe(
      tap(_ => this.log(`Read trial id=${uuid}`)),
      catchError(this.handleError<Trial>(`getTrials uuid=${uuid}`))
    );
  }

  /** GET trials by id. Will 404 if id not found */
  readTrial(id: number): Observable<Trial> {
    const url = `${this.trialsUrl}/${id}`;
    return this.http.get<Trial>(url).pipe(
      tap(_ => this.log(`Read trial id=${id}`)),
      catchError(this.handleError<Trial>(`getTrials id=${id}`))
    );
  }

  /* GET trials whose name contains export term */
  searchTrials(term: string): Observable<Trial[]> {
    if (!term.trim()) {
      // if not export term, return empty trials array.
      return of([]);
    }
    return this.http.get<Trial[]>(`${this.trialsUrl}/?name=${term}`).pipe(
      tap(x => x.length ?
        this.log(`Found trials matching "${term}"`) :
        this.log(`No trials matching "${term}"`)),
      catchError(this.handleError<Trial[]>('searchTrials', []))
    );
  }

  /* GET the existence of the replay in elasticsearch */
  getExistReplay(uuid: string, index: string): Observable<any> {
    const url = `${this.trialsUrl}/${uuid}/exist?index=${index}`;
    return this.http.get<boolean>(url).pipe(
      tap(exist => this.log(`Trial ${uuid} ${exist ? 'exists' : 'does not exist'} in elasticsearch index ${index}`)),
      catchError(this.handleError<boolean>(`Trial ${uuid} exist in elasticsearch index ${index}`))
    );
  }

  //////// Save methods //////////

  /** POST: add a new trials to the server */
  createTrial(trial: Trial): Observable<Trial> {
    return this.http.post<Trial>(this.trialsUrl, trial, this.httpOptions).pipe(
      tap((newTrial: Trial) => this.log(`added trial with id=${newTrial.id}`)),
      catchError(this.handleError<Trial>('createTrial'))
    );
  }

  createTrialMessage(trialMessage: TrialMessage): Observable<void> {
    return this.mqttService.publish('trial', JSON.stringify(trialMessage), { qos: 1 }).pipe(
      tap(_ => this.log(`Sent message over bus to create trial.`)),
      catchError(this.handleError<void>('createTrialMessage'))
    );
  }

  /** DELETE: delete the trials from the server */
  deleteTrial(trial: Trial | number): Observable<Trial> {
    const id = typeof trial === 'number' ? trial : trial.id;
    const url = `${this.trialsUrl}/${id}`;

    return this.http.delete<Trial>(url, this.httpOptions).pipe(
      tap(_ => this.log(`Deleted trial id=${id}`)),
      catchError(this.handleError<Trial>('deleteTrial'))
    );
  }

  /** PUT: update the trials on the server */
  updateTrial(trial: Trial): Observable<any> {
    const id = trial.id;
    const url = `${this.trialsUrl}/${id}`;

    return this.http.put(url, trial, this.httpOptions).pipe(
      tap(_ => this.log(`Updated trial id=${trial.id}`)),
      catchError(this.handleError<any>('updateTrial'))
    );
  }

  public generateTrialMessage(trial: Trial, sub_type: string, source: string, version: string, replay_id: string, replay_parent_id: string, replay_parent_type: string): TrialMessage {
    const trialMessage = {
      header: {
        timestamp: trial.date,
        message_type: 'trial',
        version: environment.testbedVersion
      },
      msg: {
        sub_type,
        source,
        experiment_id: trial.experiment.experiment_id,
        trial_id: trial.trial_id,
        timestamp: moment().toDate().toISOString(),
        version,
        replay_id,
        replay_parent_id,
        replay_parent_type
      },
      data: {
        name: trial.name,
        date: trial.date,
        experimenter: trial.experimenter,
        subjects: trial.subjects,
        trial_number: trial.trial_number,
        group_number: trial.group_number,
        study_number: trial.study_number,
        condition: trial.condition,
        notes: trial.notes,
        testbed_version: trial.testbed_version,
        experiment_name: trial.experiment.name,
        experiment_date: trial.experiment.date,
        experiment_author: trial.experiment.author,
        experiment_mission: trial.experiment.mission
      }
    };
    if (replay_id === null) {
      delete trialMessage.msg.replay_id;
    }
    if (replay_parent_id === null) {
      delete trialMessage.msg.replay_parent_id;
    }
    if (replay_parent_type === null) {
      delete trialMessage.msg.replay_parent_type;
    }
    return trialMessage;
  }

  public generateExportMessage(trial: Trial, index: string, sub_type: string, source: string, version: string, replay_id: string, replay_parent_id: string, replay_parent_type: string): TrialExportMessage {
    if (trial === null) {
      return null;
    }
    const trialExportMessage = {
      header: {
        timestamp: moment().toDate().toISOString(),
        message_type: 'export',
        version: index
      },
      msg: {
        sub_type,
        source,
        experiment_id: trial.experiment.experiment_id,
        trial_id: trial.trial_id,
        timestamp: moment().toDate().toISOString(),
        version,
        replay_id,
        replay_parent_id,
        replay_parent_type
      },
      data: {
        index,
        metadata: {
          trial: {
            name: trial.name,
            date: trial.date,
            experimenter: trial.experimenter,
            subjects: trial.subjects,
            trial_number: trial.trial_number,
            group_number: trial.group_number,
            study_number: trial.study_number,
            condition: trial.condition,
            notes: trial.notes,
            testbed_version: trial.testbed_version,
            experiment_name: trial.experiment.name,
            experiment_date: trial.experiment.date,
            experiment_author: trial.experiment.author,
            experiment_mission: trial.experiment.mission
          }
        }
      }
    };
    if (replay_id === null) {
      delete trialExportMessage.msg.replay_id;
    }
    if (replay_parent_id === null) {
      delete trialExportMessage.msg.replay_parent_id;
    }
    if (replay_parent_type === null) {
      delete trialExportMessage.msg.replay_parent_type;
    }
    return trialExportMessage;
  }

  public sendExportMessage(trialExportMessage: TrialExportMessage) {
    if (trialExportMessage !== null) {
      return this.mqttService.publish('metadata/trial/export', JSON.stringify(trialExportMessage), {qos: 1}).pipe(
        tap(_ => {
          this.log(`Exported trial using message bus.`);
        }),
        catchError(this.handleError<void>('trialExportMessage'))
      );
    }
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /** Log a TrialService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`TrialService: ${message}`);
  }
}
