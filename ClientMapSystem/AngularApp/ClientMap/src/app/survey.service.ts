import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';import { Survey } from './survey';
import { SURVEYS } from './test-surveys';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class SurveyService {

  private surveyUrl = 'https://iad1.qualtrics.com/API/v3/surveys/';

  httpOptions = {
    headers: new HttpHeaders({'X-API-TOKEN': 'BFzUdjstVdryWHXFUopQnqu85iBTMa4xK7pN0MD9', 'Content-Type': 'application/json'})
  };
  constructor(private http: HttpClient) { }

  getSurveys(): Observable<Survey[]> {
    return this.http.get<Survey[]>(this.surveyUrl, this.httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    return throwError(
      'Something bad happened; please try again later.');
  }
  
}
