import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoggingService } from '../logging/logging.service';
import { MqttService } from 'ngx-mqtt';
import {BehaviorSubject, Observable, of} from 'rxjs';
import { Trial } from '../trial/trial';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DockerService {
  private dockerUrl = environment.dockerUrl + '/docker';  // URL to web api
  private agentsUrl = environment.agentsUrl + '/agents';  // URL to web api

  private _isDockerOnline: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isDockerOnline = this._isDockerOnline.asObservable();
  private dockerOnline = false;

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  httpTextOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    responseType: 'text' as 'json'
  };

  constructor(
    private http: HttpClient,
    private loggingService: LoggingService,
    private mqttService: MqttService
  ) { }

  setDockerOnline(online: boolean) {
    this._isDockerOnline.next(online);
    if (this.dockerOnline !== online) {
      this.log(online ? 'docker is online.' : 'docker is offline!');
    }
    this.dockerOnline = online;
  }

  ping(): Observable<boolean> {
    return this.http.get<boolean>(this.dockerUrl + '/ping')
      .pipe(
        catchError(this.handleError<boolean>('ping', false))
      );
  }

  startContainer(id: string): Observable<any> {
    return this.http.put<any>(this.dockerUrl + `/containers/${id}/start`, null, this.httpOptions)
      .pipe(
        tap(_ => this.log(`Start container: ${id}`)),
        catchError(this.handleError<any>('startContainer'))
      );
  }

  stopContainer(id: string): Observable<any> {
    return this.http.put<any>(this.dockerUrl + `/containers/${id}/stop`, null, this.httpOptions)
      .pipe(
        tap(_ => this.log(`Stop container: ${id}`)),
        catchError(this.handleError<any>('stopContainer'))
      );
  }

  /** List containers from the server */
  containerList(): Observable<any[]> {
    return this.http.get<any[]>(this.dockerUrl + '/containers/ls')
      .pipe(
        catchError(this.handleError<any[]>('containerList', []))
      );
  }

  /** Containers log from the server */
  containerLog(id: string): Observable<any[]> {
    return this.http.get<any[]>(this.dockerUrl + `/containers/${id}/log`)
      .pipe(
        catchError(this.handleError<any[]>('containerLog', []))
      );
  }

  /** Containers log file from the server */
  containerLogDownload(id: string): Observable<any> {
    return this.http.get<any>(this.dockerUrl + `/containers/${id}/log/download`, {responseType: 'blob' as 'json'})
      .pipe(
        catchError(this.handleError<any>('containerLogDownload', ''))
      );
  }

  /** Containers log file from the server */
  containerLogsDownload(): Observable<any> {
    return this.http.get<any>(this.dockerUrl + `/containers/log/download`, {responseType: 'blob' as 'json'})
      .pipe(
        catchError(this.handleError<any>('containerLogDownload', ''))
      );
  }

  /** Container stats from the server */
  containerStats(id: string): Observable<any> {
    return this.http.get<any[]>(this.dockerUrl + `/containers/${id}/stats`)
      .pipe(
        catchError(this.handleError<any>('containerStats', {}))
      );
  }

  agentList(): Observable<string[]> {
    console.log(this.agentsUrl);
    return this.http.get<any[]>(this.agentsUrl)
      .pipe(
        catchError(this.handleError<any[]>('agentList', []))
      );
  }

  agentUp(agent: string): Observable<any> {
    return this.http.post<string>(this.agentsUrl + `/${agent}/up`, null, this.httpTextOptions)
      .pipe(
        tap(_ => this.log(`Agent up: ${agent}`)),
        catchError(this.handleError<string>('agentUp'))
      );
  }

  agentDown(agent: string): Observable<any> {
    return this.http.post<any>(this.agentsUrl + `/${agent}/down`, null, this.httpTextOptions)
      .pipe(
        tap(_ => this.log(`Agent down: ${agent}`)),
        catchError(this.handleError<any>('agentDown'))
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

  /** Log a TrialService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`DockerService: ${message}`);
  }
}
