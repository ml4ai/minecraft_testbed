import { Injectable } from '@angular/core';
import { from, Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { LoggingService } from '../../logging/logging.service';

@Injectable({
  providedIn: 'root'
})
export class MetadataAppService {
  private metadataAppUrl = environment.metadataAppUrl + '/health';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private client: HttpClient,
    private loggingService: LoggingService
  ) { }

  getHealth(): Observable<any> {
    return this.client.get<any>(this.metadataAppUrl)
      .pipe(
        catchError(this.handleError<any>('getHealth', null))
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
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /** Log an ExperimentService message with the MessageService */
  private log(message: string) {
    this.loggingService.add(`MetadataAppService: ${message}`);
  }

}
