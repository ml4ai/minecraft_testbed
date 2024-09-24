import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Experiment } from './experiment';
import { ExperimentMessage } from './experiment-message';
import { LoggingService } from '../logging/logging.service';
import { environment } from '../../environments/environment';
import { MqttService } from 'ngx-mqtt';
import { Trial } from '../trial/trial';
import { TrialMessage } from '../trial/trial-message';
// import moment from 'moment';

const moment = require('moment');

@Injectable({
  providedIn: 'root'
})
export class ExperimentService {
  private experimentsUrl = environment.metadataAppUrl + '/experiments';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private loggingService: LoggingService,
    private mqttService: MqttService
  ) { }

  /** GET experiments from the server */
  readExperiments(): Observable<Experiment[]> {
    return this.http.get<Experiment[]>(this.experimentsUrl)
      .pipe(
        tap(_ => this.log('Read experiments')),
        catchError(this.handleError<Experiment[]>('readExperiments', []))
      );
  }

  /** GET experiments by id. Return `undefined` when id not found */
  readExperimentNo404<Data>(id: number): Observable<Experiment> {
    const url = `${this.experimentsUrl}/?id=${id}`;
    return this.http.get<Experiment[]>(url)
      .pipe(
        map(experiments => experiments[0]), // returns a {0|1} element array
        tap(h => {
          const outcome = h ? `Read` : `Did not find`;
          this.log(`${outcome} experiment id=${id}`);
        }),
        catchError(this.handleError<Experiment>(`getExperiments id=${id}`))
      );
  }

  /** GET experiments by id. Will 404 if id not found */
  readExperiment(id: number): Observable<Experiment> {
    const url = `${this.experimentsUrl}/${id}`;
    return this.http.get<Experiment>(url).pipe(
      tap(_ => this.log(`Read experiment id=${id}`)),
      catchError(this.handleError<Experiment>(`getExperiments id=${id}`))
    );
  }

  /** GET experiments by uuid. Will 404 if id not found */
  readExperimentUUID(experimentId: string): Observable<Experiment> {
    const url = `${this.experimentsUrl}/uuid/${experimentId}`;
    return this.http.get<Experiment>(url).pipe(
      tap(_ => this.log(`Read experiment experimentId=${experimentId}`)),
      catchError(this.handleError<Experiment>(`getExperiments experimentId=${experimentId}`))
    );
  }

  /* GET experiments whose name contains export term */
  searchExperiments(term: string): Observable<Experiment[]> {
    if (!term.trim()) {
      // if not export term, return empty experiments array.
      return of([]);
    }
    return this.http.get<Experiment[]>(`${this.experimentsUrl}/?name=${term}`).pipe(
      tap(x => x.length ?
        this.log(`Found experiments matching "${term}"`) :
        this.log(`No experiments matching "${term}"`)),
      catchError(this.handleError<Experiment[]>('searchExperiments', []))
    );
  }

  //////// Save methods //////////

  /** POST: add a new experiments to the server */
  createExperiment(experiment: Experiment): Observable<Experiment> {
    return this.http.post<Experiment>(this.experimentsUrl, experiment, this.httpOptions).pipe(
      tap((newExperiment: Experiment) => this.log(`Added experiment with id=${newExperiment.id}`)),
      catchError(this.handleError<Experiment>('createExperiment'))
    );
  }

  createExperimentMessage(experimentMessage: ExperimentMessage): Observable<void> {
    return this.mqttService.publish('experiment', JSON.stringify(experimentMessage), { qos: 1 }).pipe(
      tap(_ => this.log(`Sent message over bus to create experiment.`)),
      catchError(this.handleError<void>('createExperimentMessage'))
    );
  }

  /** DELETE: delete the experiments from the server */
  deleteExperiment(experiment: Experiment | number): Observable<Experiment> {
    const id = typeof experiment === 'number' ? experiment : experiment.id;
    const url = `${this.experimentsUrl}/${id}`;

    return this.http.delete<Experiment>(url, this.httpOptions).pipe(
      tap(_ => this.log(`Deleted experiment id=${id}`)),
      catchError(this.handleError<Experiment>('deleteExperiment'))
    );
  }

  /** PUT: update the experiments on the server */
  updateExperiment(experiment: Experiment): Observable<any> {
    const id = experiment.id;
    const url = `${this.experimentsUrl}/${id}`;

    return this.http.put(url, experiment, this.httpOptions).pipe(
      tap(_ => this.log(`Updated experiment id=${experiment.id}`)),
      catchError(this.handleError<any>('updateExperiment'))
    );
  }

  public generateExperimentMessage(experiment: Experiment, messageType: string, sub_type: string, source: string, version: string): ExperimentMessage {
    const experimentMessage = {
      header: {
        timestamp: experiment.date,
        message_type: messageType,
        version: environment.testbedVersion
      },
      msg: {
        sub_type,
        source,
        experiment_id: experiment.experiment_id,
        timestamp: moment().toDate().toISOString(),
        version
      },
      data: {
        name: experiment.name,
        date: experiment.date,
        author: experiment.author,
        mission: experiment.mission
      }
    };
    return experimentMessage;
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

  /** Log an ExperimentService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`ExperimentService: ${message}`);
  }
}
