import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoggingService } from '../logging/logging.service';
import { MqttService } from 'ngx-mqtt';
import {BehaviorSubject, Observable, of} from 'rxjs';
import { Replay } from './replay';
import { catchError, map, tap } from 'rxjs/operators';
import { ReplayMessage } from './replay-message';
import { ReplayExportMessage } from './replay-export-message';
import { Trial } from '../trial/trial';
import { v4 as uuidv4 } from 'uuid';
import {MessageApiResult} from '../dashboard/run-replay/MessageApiResult';
import {IgnoreListItem} from './ignore-list-item';
import {ReplayObject} from '../dashboard/batch-run-replay/replayObject';
// import moment from 'moment';

const moment = require('moment');

@Injectable({
  providedIn: 'root'
})
export class ReplayService {
  private replaysUrl = environment.metadataAppUrl + '/replays';  // URL to web api

  private _isReplayCreated: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isReplayCreated = this._isReplayCreated.asObservable();

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private loggingService: LoggingService,
    private mqttService: MqttService
  ) { }

  /** GET replay from the server */
  readReplays(): Observable<Replay[]> {
    return this.http.get<Replay[]>(this.replaysUrl)
      .pipe(
        tap(_ => {
          this.log('Read replays');
        }),
        catchError(this.handleError<Replay[]>('readReplays', []))
      );
  }

  /** GET replays by id. Return `undefined` when id not found */
  readReplayNo404<Data>(id: number): Observable<Replay> {
    const url = `${this.replaysUrl}/?id=${id}`;
    return this.http.get<Replay[]>(url)
      .pipe(
        map(replays => replays[0]), // returns a {0|1} element array
        tap(h => {
          const outcome = h ? `Read` : `Did not find`;
          this.log(`${outcome} replay id=${id}`);
        }),
        catchError(this.handleError<Replay>(`getReplays id=${id}`))
      );
  }

  /** GET replays by id. Will 404 if id not found */
  readReplay(id: number): Observable<Replay> {
    const url = `${this.replaysUrl}/${id}`;
    return this.http.get<Replay>(url).pipe(
      tap(_ => this.log(`Read replay id=${id}`)),
      catchError(this.handleError<Replay>(`getReplays id=${id}`))
    );
  }

  /* GET replays whose name contains export term */
  searchReplays(term: string): Observable<Replay[]> {
    if (!term.trim()) {
      // if not export term, return empty replays array.
      return of([]);
    }
    return this.http.get<Replay[]>(`${this.replaysUrl}/?name=${term}`).pipe(
      tap(x => x.length ?
        this.log(`Found replays matching "${term}"`) :
        this.log(`No replays matching "${term}"`)),
      catchError(this.handleError<Replay[]>('searchReplays', []))
    );
  }

  /* GET the root trial of a replay using replay uuid */
  getReplayRootTrial(uuid: string): Observable<any> {
    const url = `${this.replaysUrl}/root-trial/${uuid}`;
    return this.http.get<Trial>(url).pipe(
      tap(_ => this.log(`Get replay root uuid=${uuid}`)),
      catchError(this.handleError<Trial>(`getReplayRoot uuid=${uuid}`))
    );
  }

  /* GET list of Replay parents for a Replay */
  getReplayParents(uuid: string): Observable<any> {
    const url = `${this.replaysUrl}/parents/${uuid}`;
    return this.http.get<Trial>(url).pipe(
      tap(_ => this.log(`Get replay parents of uuid=${uuid}`)),
      catchError(this.handleError<Trial>(`getReplayParents uuid=${uuid}`))
    );
  }

  /** GET replay from the server */
  abortReplay(): Observable<boolean> {
    const url = `${this.replaysUrl}/run/abort`;
    return this.http.get<boolean>(url)
      .pipe(
        tap(_ => this.log('Replay aborted!')),
        catchError(this.handleError<boolean>('abortReplay', false))
      );
  }

  /* GET the existence of the replay in elasticsearch */
  getExistReplay(uuid: string, index: string): Observable<any> {
    const url = `${this.replaysUrl}/${uuid}/exist?index=${index}`;
    return this.http.get<boolean>(url).pipe(
      tap(exist => this.log(`Replay ${uuid} ${exist ? 'exists' : 'does not exist'} in elasticsearch index ${index}`)),
      catchError(this.handleError<boolean>(`Replay ${uuid} exist in elasticsearch index ${index}`))
    );
  }

  //////// Save methods //////////

  /** POST: add a new replays to the server */
  createReplay(replay: Replay): Observable<Replay> {
    return this.http.post<Replay>(this.replaysUrl, replay, this.httpOptions).pipe(
      tap((newReplay: Replay) => this.log(`added replay with id=${newReplay.id}`)),
      catchError(this.handleError<Replay>('createReplay'))
    );
  }

  createReplayMessage(replayMessage: ReplayMessage): Observable<void> {
    return this.mqttService.publish('replay', JSON.stringify(replayMessage), { qos: 2 }).pipe(
      tap(_ => this.log(`Sent message over bus to create replay.`)),
      catchError(this.handleError<void>('createReplayMessage'))
    );
  }

  /** DELETE: delete the replays from the server */
  deleteReplay(replay: Replay | number): Observable<Replay> {
    const id = typeof replay === 'number' ? replay : replay.id;
    const url = `${this.replaysUrl}/${id}`;

    return this.http.delete<Replay>(url, this.httpOptions).pipe(
      tap(_ => this.log(`Deleted replay id=${id}`)),
      catchError(this.handleError<Replay>('deleteReplay'))
    );
  }

  /** PUT: update the replays on the server */
  updateReplay(replay: Replay): Observable<any> {
    const id = replay.id;
    const url = `${this.replaysUrl}/${id}`;

    return this.http.put(url, replay, this.httpOptions).pipe(
      tap(_ => this.log(`Updated replay id=${replay.id}`)),
      catchError(this.handleError<any>('updateReplay'))
    );
  }

  /** POST: run a replay using elasticsearch index */
  runReplay(message: ReplayMessage, index: string): Observable<any> {
    const url = `${this.replaysUrl}/run/?index=${index}`;
    this._isReplayCreated.next(true);
    return this.http.post<Replay>(url, message, this.httpOptions).pipe(
      tap((newReplay: Replay) => {
        if (newReplay === null) {
          this.log(`Replay was not run.`);
          this._isReplayCreated.next(false);
        } else {
          this.log(`Replay running with id=${newReplay.id}`);
          this._isReplayCreated.next(false);
        }
      }),
      catchError(this.handleError<ReplayMessage>('createReplay'))
    );
  }

  runQuickTrial(uuid: string, ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[], index: string): Observable<any> {
    const url = `${this.replaysUrl}/run/trial/${uuid}?index=${index}&quick=true`;
    this._isReplayCreated.next(true);
    const body = {
      ignore_message_list,
      ignore_source_list,
      ignore_topic_list,
    };
    return this.http.post<MessageApiResult>(url, body, this.httpOptions).pipe(
      tap((messageApiResult: MessageApiResult) => {
        if (messageApiResult.result === 'success'){
          this.log(`${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        } else {
          this.log(`Replay was not run: ${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        }
      }),
      catchError(this.handleError<MessageApiResult>('createReplay'))
    );
  }

  runQuickReplay(uuid: string, ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[], index: string): Observable<any> {
    const url = `${this.replaysUrl}/run/replay/${uuid}?index=${index}&quick=true`;
    this._isReplayCreated.next(true);
    const body = {
      ignore_message_list,
      ignore_source_list,
      ignore_topic_list,
    };
    return this.http.post<MessageApiResult>(url, body, this.httpOptions).pipe(
      tap((messageApiResult: MessageApiResult) => {
        if (messageApiResult.result === 'success'){
          this.log(`${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        } else {
          this.log(`Replay was not run: ${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        }
      }),
      catchError(this.handleError<MessageApiResult>('createReplay'))
    );
  }

  runBatchTrial(replay_objects: ReplayObject[], ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[], restart: boolean, index: string): Observable<any> {
    const url = `${this.replaysUrl}/run/batch/trial?index=${index}`;
    this._isReplayCreated.next(true);
    const body = {
      replay_objects,
      ignore_message_list,
      ignore_source_list,
      ignore_topic_list,
      restart,
    };
    return this.http.post<MessageApiResult>(url, body, this.httpOptions).pipe(
      tap((messageApiResult: MessageApiResult) => {
        if (messageApiResult.result === 'success'){
          this.log(`${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        } else {
          this.log(`Replay was not run: ${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        }
      }),
      catchError(this.handleError<MessageApiResult>('createReplay'))
    );
  }

  runBatchReplay(replay_objects: ReplayObject[], ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[], restart: boolean, index: string): Observable<any> {
    const url = `${this.replaysUrl}/run/batch/replay?index=${index}`;
    this._isReplayCreated.next(true);
    const body = {
      replay_objects,
      ignore_message_list,
      ignore_source_list,
      ignore_topic_list,
      restart,
    };
    return this.http.post<MessageApiResult>(url, body, this.httpOptions).pipe(
      tap((messageApiResult: MessageApiResult) => {
        if (messageApiResult.result === 'success'){
          this.log(`${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        } else {
          this.log(`Replay was not run: ${messageApiResult.message}`);
          this._isReplayCreated.next(false);
        }
      }),
      catchError(this.handleError<MessageApiResult>('createReplay'))
    );
  }

  public generateReplayMessage(trial_id: string, experiment_id: string, replay_parent_id: string, replay_parent_type: string, ignore_message_list: IgnoreListItem[], ignore_source_list: string[], ignore_topic_list: string[], sub_type: string, source: string, version: string): ReplayMessage {
    return {
      header: {
        timestamp: moment().toDate().toISOString(),
        message_type: 'replay',
        version: environment.testbedVersion
      },
      msg: {
        sub_type,
        source,
        experiment_id,
        trial_id,
        timestamp: moment().toDate().toISOString(),
        version,
        replay_id: uuidv4(),
        replay_parent_id,
        replay_parent_type
      },
      data: {
        ignore_message_list,
        ignore_source_list,
        ignore_topic_list
      }
    };
  }

  public generateExportMessage(replay: Replay, parents: Trial[] | Replay[], index: string, sub_type: string, source: string, version: string): ReplayExportMessage {
    const root = parents[parents.length - 1] as Trial;
    if (root === null) {
      this.log('Root item in replay parent tree was not a Trial!');
      return null;
    }
    return {
      header: {
        timestamp: moment().toDate().toISOString(),
        message_type: 'export',
        version: environment.testbedVersion
      },
      msg: {
        sub_type,
        source,
        experiment_id: root.experiment.experiment_id,
        trial_id: root.trial_id,
        timestamp: moment().toDate().toISOString(),
        version,
        replay_id: replay.replay_id,
        replay_parent_id: replay.replay_parent_id,
        replay_parent_type: replay.replay_parent_type
      },
      data: {
        index,
        ignore_message_list: replay.ignore_message_list,
        ignore_source_list: replay.ignore_source_list,
        ignore_topic_list: replay.ignore_topic_list,
        metadata: {
          replay,
          parents
        }
      }
    };
  }

  public sendExportMessage(replayExportMessage: ReplayExportMessage) {
    return this.mqttService.publish('metadata/replay/export', JSON.stringify(replayExportMessage), { qos: 2 }).pipe(
      tap(_ => {
        this.log(`Exported replay using message bus.`);
      }),
      catchError(this.handleError<void>('replayExportMessage'))
    );
  }

  public sendRunMessage(replay: Replay) {
    return this.mqttService.publish('metadata/replay/run', JSON.stringify(replay), { qos: 2 }).pipe(
      tap(_ => {
        this.log(`Running replay using message bus.`);
      }),
      catchError(this.handleError<void>('replayRunMessage'))
    );
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

  /** Log a ReplayService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`ReplayService: ${message}`);
  }
}
