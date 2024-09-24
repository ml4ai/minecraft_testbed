import { Component, EventEmitter, Inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { WebsocketService } from '../websocket.service';
import { SessionService } from '../Services/session.service';
import { APP_BASE_HREF } from '@angular/common';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  avatarName;
  password;

  mapEmitter:EventEmitter<string> = new EventEmitter<string>();

  constructor(private websocket: WebsocketService, private sessionService: SessionService, private router: Router
    ) {
      console.log(document.location);
      console.log(document.location.host);
     }

  ngOnInit(): void {

    
  }

  login(){

    const logindata = {

      name: this.avatarName,
      password : this.password

    };

    this.websocket.socket.emit('authenticate', logindata );

  }



}
