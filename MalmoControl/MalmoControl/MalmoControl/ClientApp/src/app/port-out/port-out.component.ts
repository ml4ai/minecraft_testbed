import { Component, Inject} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { OpenExternalPortDTO } from '../Interface/DTO';

@Component({
  selector: 'app-port-out',
  templateUrl: './port-out.component.html',
  styleUrls: ['./port-out.component.css']
})
export class PortOutComponent {

  externalPort = '4000';
  internalPort = 'GetMeFromMinecraft';
  dockerNetwork = 'malmonet';
  instanceNumber = '';
  baseUrl;

  constructor(private http: HttpClient, @Inject('BASE_URL') baseUrl: string) {

    this.baseUrl = baseUrl;

  }

  public openExternalPort() {

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };

    const openExternalPortDto: OpenExternalPortDTO = { 'internalPort': this.internalPort,
    'instanceNumber': this.instanceNumber, 'externalPort': this.externalPort, 'dockerNetwork': this.dockerNetwork  };


    console.log('Opening ports -->' + this.externalPort + ':' + this.internalPort );
    this.http.put<OpenExternalPortDTO>(this.baseUrl + 'api/Malmo/openExternalPort', openExternalPortDto, httpOptions)
    .subscribe((returned) => console.log(returned));
  }

}
