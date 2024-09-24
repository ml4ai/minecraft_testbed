import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatBottomSheet, MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { LoggingService } from '../logging.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-bottom-sheet-container',
  templateUrl: './bottom-sheet-container.component.html',
  styleUrls: ['./bottom-sheet-container.component.scss']
})
export class BottomSheetContainerComponent implements OnInit, OnDestroy {
  newMessageCountSubscription: Subscription;
  newMessageCount: number;

  constructor(
    private _bottomSheet: MatBottomSheet,
    private loggingService: LoggingService) { }

  openBottomSheet(): void {
    this._bottomSheet.open(BottomSheetContainerSheet, {
      panelClass: 'bottom-sheet-container'
    });
  }

  closeBottomSheet(): void {
    this._bottomSheet.dismiss();
  }

  ngOnInit(): void {
    this.newMessageCountSubscription = this.loggingService.newMessageCount.subscribe(count => this.newMessageCount = count);
  }

  ngOnDestroy(): void {
    this.newMessageCountSubscription.unsubscribe();
  }

}

@Component({
  selector: 'bottom-sheet-container-sheet',
  templateUrl: './bottom-sheet-container-sheet.html',
  styleUrls: ['./bottom-sheet-container-sheet.scss']
})
export class BottomSheetContainerSheet implements OnInit, OnDestroy {
  afterOpenedSubscription: Subscription;

  constructor(
    private _bottomSheetRef: MatBottomSheetRef<BottomSheetContainerSheet>,
    private loggingService: LoggingService,
  ) { }

  close(): void {
    this._bottomSheetRef.dismiss();
  }

  ngOnInit(): void {
    this.afterOpenedSubscription = this._bottomSheetRef.afterOpened().subscribe(() => this.loggingService.clearNewMessageCount());
  }

  ngOnDestroy(): void {
    this.afterOpenedSubscription.unsubscribe();
  }
}
