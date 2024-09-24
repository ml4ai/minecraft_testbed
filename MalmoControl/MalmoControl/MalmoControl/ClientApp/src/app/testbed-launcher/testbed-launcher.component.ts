import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-testbed-launcher',
  templateUrl: './testbed-launcher.component.html',
  styleUrls: ['./testbed-launcher.component.css']
})
export class TestbedLauncherComponent implements OnInit {
  components = ['Minecraft', 'ELK', 'Metadata DB'];

  constructor() { }

  ngOnInit(): void {
  }

  execute() {
    
  }

}
