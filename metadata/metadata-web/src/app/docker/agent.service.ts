import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private agentsUrl = environment.agentsUrl + '/agents';  // URL to web api

  constructor(private _zone: NgZone) {}

  agentUp(agent: string): Observable<any> {
    const url = this.agentsUrl + `/${agent}/up`;
    return new Observable(observer => {
      const eventSource = this.getEventSource(url);
      eventSource.onmessage = event => {
        this._zone.run(() => {
          observer.next(event);
        });
      };
      eventSource.onerror = error => {
        this._zone.run(() => {
          observer.error(error);
        });
      };
    });
  }
  private getEventSource(url: string): EventSource {
    return new EventSource(url);
  }

  agentUp2(agent: string): Observable<string> {
    const url = this.agentsUrl + `/${agent}/up`;
    return new Observable<string>(obs => {
      const es = new EventSource(url);
      es.addEventListener('message', (evt) => {
        console.log(evt.data);
        obs.next(evt.data);
      });
      return () => es.close();
    });
  }
}

