import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
// import moment from 'moment';

const moment = require('moment');

@Injectable({
  providedIn: 'root'
})
export class LoggingService {
  private _newMessageCount: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public newMessageCount = this._newMessageCount.asObservable();

  private msgArray: string[] = [];
  private _messages: BehaviorSubject<string[]> = new BehaviorSubject<string[]>(this.msgArray);
  public messages = this._messages.asObservable();

  private _message: Subject<string> = new Subject<string>(); // BehaviorSubject
  public message = this._message.asObservable();

  add(message: string) {
    this._newMessageCount.next(this._newMessageCount.value + 1);
    this._message.next(message);
    this.msgArray.push('[' + moment().format() + '] ' + message);
    this._messages.next(this.msgArray);
  }

  clearNewMessageCount(): void {
    this._newMessageCount.next(0);
  }

  clear(): void {
    this._newMessageCount.next(0);
    this.msgArray = [];
    this._messages.next(this.msgArray);
    // this.messages = [];
  }
}
