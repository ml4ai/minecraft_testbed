import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AgentService {

  public agent_running = 'False';

  constructor() { }
}
