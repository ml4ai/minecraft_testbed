import { Injectable } from '@angular/core';
import {Observable, from, Subject, BehaviorSubject, of} from 'rxjs';
import {Client, CountResponse, SearchResponse} from 'elasticsearch';
import { environment } from '../../../environments/environment';
import { BlobBuilder } from './blob-builder';
import { ReadableStream } from 'web-streams-polyfill/ponyfill';
import * as StreamSaver from 'streamsaver';
import { LineReader } from 'line-reader-browser';
import { LoggingService } from '../../logging/logging.service';
import { Experiment } from '../../experiment/experiment';
import { Trial } from '../../trial/trial';
import { TrialExportMessage } from '../../trial/trial-export-message';
import { FirstLineReader } from './first-line-reader';
import { ExportQueryType } from './export-query-type';
import { ReplayExportMessage } from '../../replay/replay-export-message';
// import moment from 'moment';
import { TimeWindowExportMessage } from './time-window-export-message';
import { catchError, tap } from 'rxjs/operators';
import { MqttService } from 'ngx-mqtt';

const moment = require('moment');

@Injectable({
  providedIn: 'root'
})
export class ElasticsearchService {
  private client: Client;

  private indexArray: string[] = [];
  private _indices: BehaviorSubject<any[]> = new BehaviorSubject<any[]>(this.indexArray);
  public indices = this._indices.asObservable();

  private _isExportingTrial: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isExportingTrial = this._isExportingTrial.asObservable();
  private _isExportingReplay: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isExportingReplay = this._isExportingReplay.asObservable();

  private _isImportingTrial: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isImportingTrial = this._isImportingTrial.asObservable();
  private _isImportingReplay: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isImportingReplay = this._isImportingReplay.asObservable();

  private _isElasticsearchBusy: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public isElasticsearchBusy = this._isElasticsearchBusy.asObservable();

  // private blobBuilder: BlobBuilder;

  constructor(
    private loggingService: LoggingService,
    private mqttService: MqttService
  ) {
    // this.blobBuilder = new BlobBuilder();
    this.client = new Client({
      host: environment.elasticsearchUrl,
      requestTimeout: environment.elasticsearchRequestTimeout
    });

    this.catIndices();
  }

  public catIndices(): void {
    // return from(<Promise<SearchResponse<{}>>>this.client.cat.indices({
    //   format: 'JSON'
    // }));
    this.client.cat.indices({
      format: 'JSON'
    }).then(results => {
      this._indices.next(results);
    }).catch(error => {
      this.log(`Error: ${JSON.stringify(error)}`);
      this._indices.next([]);
    });
  }

  public getIndices(): Observable<any> {
    return from(this.client.indices.get({
      index: '_all'
    }) as Promise<any>);
  }

  public ping(): Observable<any> {
    return from(this.client.ping({
      requestTimeout: 5000,
    }) as Promise<any>);
  }

  public createIndex(index: string): Observable<any> {
    return from(this.client.indices.create({
      index,
      body: {
        settings: {
          'index.lifecycle.name': 'logstash-policy',
          'index.lifecycle.rollover_alias': 'logstash',
          'index.refresh_interval': '5s',
          number_of_shards: 1
        },
        mappings: {
          dynamic: false,
          properties: {
            header: {
              properties: {
                message_type: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                }
              }
            },
            msg: {
              properties: {
                trial_id: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                experiment_id: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                replay_id: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                replay_parent_id: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                replay_parent_type: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                source: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                sub_type: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                timestamp: {
                  type: 'date'
                },
                name: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                testbed_version: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                }
              }
            },
            topic: {
              type: 'text',
              norms: false,
              fields: {
                keyword: {
                  type: 'keyword',
                  ignore_above: 256
                }
              }
            },
            '@timestamp': {
              type: 'date'
            },
            '@version': {
              type: 'keyword'
            },
            error: {
              properties: {
                reason: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                plugin_id: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                },
                plugin_type: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                }
              }
            }
          }
        }
      }
    }) as Promise<any>);
  }

  // public getReplays(): Observable<any> {
  //   return from(<Promise<any>>this.searchReplays());
  // }

  public async getReplays(index: string) {
    const ITEMS_PER_PAGE = 1000;

    const json = {
      index,
      size: 0,
      body: {
        aggs: {
          replays: {
            composite: {
              size: ITEMS_PER_PAGE,
              sources: [
                {'msg.replay_id': {terms: {field: 'msg.replay_id.keyword'}}}
              ],
              after: undefined
            }
          }
        }
      }
    };

    const uniqueReplays = [];

    while (true) {
      const result = await this.client.search(json);
      const currentUniqueReplays = result.aggregations.replays.buckets.map(bucket => bucket.key);

      uniqueReplays.push(...currentUniqueReplays);

      const after = result.aggregations.replays.after_key;

      if (after) {
        // continue paginating unique items
        json.body.aggs.replays.composite.after = after;
      } else {
        return uniqueReplays;
      }
    }
  }

  private async import(index: string, file: File) {
    const dataset = [];

    // const chunkSize: number;
    const lineReader = new LineReader(file);

    // Context is optional. It can be used to inside processLineFn
    const context = {};
    await lineReader.forEachLine(processLineFn, context)
      .then(result => console.log('Done!', result));

    // Context is same Object as passed while calling forEachLine
    function processLineFn(_line: string, _index: number, _context: any) {
      if (_index === 0) {
        const header = JSON.parse(_line);
        if ('@timestamp' in header) {
          dataset.push(_line);
        }
      } else {
        dataset.push(_line);
      }
    }

    // await this.client.indices.create({
    //   index: index
    // }, {ignore: [400]});

    const body = dataset.flatMap(doc => [{index: {_index: index}}, doc]);

    // this.client.bulk({refresh: true, body}, function(err, resp) {
    //   if (resp.errors) {
    //     resp.items.forEach((action, i) => {
    //       const operation = Object.keys(action)[0];
    //       if (action[operation].error) {
    //         const erroredDocument = {
    //           // If the status is 429 it means that you can retry the document,
    //           // otherwise it's very likely a mapping error, and you should
    //           // fix the document before to try it again.
    //           status: action[operation].status,
    //           error: action[operation].error,
    //           operation: body[i * 2],
    //           document: body[i * 2 + 1]
    //         };
    //         this.log(JSON.stringify(erroredDocument));
    //       }
    //     });
    //   }
    //   return dataset.length;
    // }.bind(this));

    const erroredDocuments = [];
    const bulkResponse = await this.client.bulk({ refresh: true, body });
    if (bulkResponse.errors) {
      // The items array has the same order of the dataset we just indexed.
      // The presence of the `error` key indicates that the operation
      // that we did for the document has failed.
      bulkResponse.items.forEach((action, i) => {
        const operation = Object.keys(action)[0];
        if (action[operation].error) {
          erroredDocuments.push({
            // If the status is 429 it means that you can retry the document,
            // otherwise it's very likely a mapping error, and you should
            // fix the document before to try it again.
            status: action[operation].status,
            error: action[operation].error,
            operation: body[i * 2],
            document: body[i * 2 + 1]
          });
        }
      });
      erroredDocuments.forEach((document, i) => {
        this.log(JSON.stringify(document));
      });
    }

    return {
      total: dataset.length,
      success: dataset.length - erroredDocuments.length,
      error: erroredDocuments.length
    };
  }

  // Add the trial here for inserting into the file.
  private async export(index: string, exportQueryType: ExportQueryType, id: string, filename: string, exportMessage: TrialExportMessage | ReplayExportMessage) {
    const blobBuilder = new BlobBuilder();
    // let observations = [];
    const responseQueue = [];
    let query = {};
    switch (exportQueryType) {
      case ExportQueryType.TRIAL:
        query = {
          index,
          scroll: '30s',
          size: 1000,
          body: {
            sort: [{
              '@timestamp': {
                order: 'asc'
              }
            }],
            query: {
              bool: {
                must: [{
                  match: {
                    'msg.trial_id.keyword': id
                  }
                }],
                must_not: [{
                  exists: {
                    field: 'msg.replay_id'
                  }
                }]
              }
            }
          }
        };
        break;
      case ExportQueryType.REPLAY:
        query = {
          index,
          // Keep the export results "scrollable" for 30 seconds
          scroll: '30s',
          size: 1000,
          body: {
            sort: [{
              '@timestamp': {
                order: 'asc'
              }
            }],
            query: {
              match: {
                'msg.replay_id.keyword': id
              }
            }
          }
        };
        break;
    }

    // Start things off by searching, setting a scroll timeout, and pushing
    // our first response into the queue to be processed
    const response = await this.client.search(query);

    responseQueue.push(response);

    while (responseQueue.length > 0) {
      const body = responseQueue.shift();

      // Collect the hits from this response
      body.hits.hits.forEach(hit => {
        // observations.push(hit._source)
        blobBuilder.append(JSON.stringify(hit._source));
      });

      // Check to see if we have collected all of the results
      // if (body.hits.total.value === observations.length) {
      if (body.hits.total.value === blobBuilder.getLength()) {
        // return observations;
        // let observationsResponse = new Response(blobBuilder.getBlob(), { 'status' : 200 , 'statusText' : 'OK' });
        // return observationsResponse;
        // return blobBuilder.getBlob();
        break;
      }

      // Get the next response if there are more quotes to fetch
      responseQueue.push(
        await this.client.scroll({
          scrollId: body._scroll_id,
          scroll: '30s'
        })
      );
    }

    // Add header to beginning of blob.
    // For now replay export passes in a null.
    if (exportMessage !== null) {
      blobBuilder.prepend(JSON.stringify(exportMessage));
    }

    // console.log('sleep called');

    const blob = blobBuilder.getBlob();
    if (environment.mitmUrl !== 'default') {
      StreamSaver.mitm = environment.mitmUrl + '/StreamSaver.js/mitm.html?version=' + StreamSaver.version.full;
    }
    const fileStream = StreamSaver.createWriteStream(filename + '.metadata', {
      size: blob.size // Makes the percentage visible in the download
    });

    const readableStream = blob.stream();

    // more optimized pipe version
    // (Safari may have pipeTo but it's useless without the WritableStream)
    if (window.WritableStream && readableStream.pipeTo) {
      return readableStream.pipeTo(fileStream)
        .then(() => {
          if (exportMessage !== null) {
            this.log(`Exported ${blobBuilder.getLength() - 1} documents successfully.`);
          } else {
            this.log(`Exported ${blobBuilder.getLength()} documents successfully.`);
          }
        });
    }

    // Write (pipe) manually
    (window as any).writer = fileStream.getWriter();

    const reader = readableStream.getReader();
    const pump = () => reader.read()
      .then(res => res.done
        ? (window as any).writer.close() : (window as any).writer.write(res.value).then(pump)).finally(() => {
        this.log('Exported ' + blobBuilder.getLength() + ' documents successfully.');
      });

    // // abort so it dose not look stuck
    // window.onunload = () => {
    //   fileStream.abort()
    //   // also possible to call abort on the writer you got from `getWriter()`
    //   (<any>window).writer.abort()
    // }
    //
    // window.onbeforeunload = () => {
    //     return 'Are you sure you want to leave?';
    // }

    // added await due to lint.
    await pump();
    // return observations;
    // return new Response(blobBuilder.getBlob(), { 'status' : 500 , 'statusText' : 'INCOMPLETE' });
  }

  private async exportTime(beginDateTime: string, endDateTime: string, index: string, filename: string) {
    const blobBuilder = new BlobBuilder();
    const responseQueue = [];
    const query = {
      index,
      // Keep the export results "scrollable" for 30 seconds
      scroll: '30s',
      size: 1000,
      body: {
        sort: [{
          '@timestamp': {
            order: 'asc'
          }
        }],
        query: {
          range: {
            'msg.timestamp': {
              gte: beginDateTime,
              lte: endDateTime
            }
          }
        }
      }
    };
    // this.log(`query: ${JSON.stringify(query)}`);
    // Start things off by searching, setting a scroll timeout, and pushing
    // our first response into the queue to be processed
    const response = await this.client.search(query);

    responseQueue.push(response);

    while (responseQueue.length > 0) {
      const body = responseQueue.shift();

      // Collect the hits from this response
      body.hits.hits.forEach(hit => {
        // observations.push(hit._source)
        blobBuilder.append(JSON.stringify(hit._source));
      });

      // Check to see if we have collected all of the results
      if (body.hits.total.value === blobBuilder.getLength()) {
        break;
      }

      // Get the next response if there are more quotes to fetch
      responseQueue.push(
        await this.client.scroll({
          scrollId: body._scroll_id,
          scroll: '30s'
        })
      );
    }

    // console.log('sleep called');

    const blob = blobBuilder.getBlob();
    if (environment.mitmUrl !== 'default') {
      StreamSaver.mitm = environment.mitmUrl + '/StreamSaver.js/mitm.html?version=' + StreamSaver.version.full;
    }
    const fileStream = StreamSaver.createWriteStream(filename + '.metadata', {
      size: blob.size // Makes the percentage visible in the download
    });

    const readableStream = blob.stream();

    // more optimized pipe version
    // (Safari may have pipeTo but it's useless without the WritableStream)
    if (window.WritableStream && readableStream.pipeTo) {
      return readableStream.pipeTo(fileStream)
        .then(() => {
          this.log(`Exported ${blobBuilder.getLength()} documents successfully.`);
        });
    }

    // Write (pipe) manually
    (window as any).writer = fileStream.getWriter();

    const reader = readableStream.getReader();
    const pump = () => reader.read()
      .then(res => res.done
        ? (window as any).writer.close() : (window as any).writer.write(res.value).then(pump)).finally(() => {
        this.log('Exported ' + blobBuilder.getLength() + ' documents successfully.');
      });

    // added await due to lint.
    await pump();
  }

  // private sleep(milliseconds) {
  //   console.log('sleep start');
  //   const date = Date.now();
  //   let currentDate = null;
  //   do {
  //     currentDate = Date.now();
  //   } while (currentDate - date < milliseconds);
  //   console.log('sleep end');
  // }

  public getDocumentCount(index: string, type: string, id: string): Promise<CountResponse> {
    return this.client.count({
      index,
      body: {
        query: {
          match: type === 'TRIAL' ? {
            'msg.trial_id.keyword': id
          } : {
            'msg.replay_id.keyword': id
          }
        }
      }
    });
  }

  public getMessageCount(index: string, type: string, id: string, messageType: string, subType: string): Promise<CountResponse> {
    return this.client.count({
      index,
      body: {
        query: {
          bool: {
            must: [
              {
                match: type === 'TRIAL' ? {
                  'msg.trial_id.keyword': id
                } : {
                  'msg.replay_id.keyword': id
                }
              },
              {
                match: {
                  'header.message_type': messageType
                }
              },
              {
                match: {
                  'msg.sub_type': subType
                }
              }
            ]
          }
        }
      }
    });
  }

  public exportTrial(index: string, trialId: string, filename: string, trialExportMessage: TrialExportMessage) {
    this._isExportingTrial.next(true);
    this._isElasticsearchBusy.next(true);
    return this.export(index, ExportQueryType.TRIAL, trialId, filename, trialExportMessage).finally(() => {
      this._isExportingTrial.next(false);
      this._isElasticsearchBusy.next(false);
    });
  }

  public async exportReplay(index: string, replayId: string, filename: string, replayExportMessage: ReplayExportMessage) {
    this._isExportingReplay.next(true);
    this._isElasticsearchBusy.next(true);
    return this.export(index, ExportQueryType.REPLAY, replayId, filename, replayExportMessage).finally(() => {
      this._isExportingReplay.next(false);
      this._isElasticsearchBusy.next(false);
    });
  }

  public sendExportMessage(timeWindowExportMessage: TimeWindowExportMessage) {
    if (timeWindowExportMessage !== null) {
      return this.mqttService.publish('metadata/time_window/export', JSON.stringify(timeWindowExportMessage), {qos: 1}).pipe(
        tap(_ => {
          this.log(`Exported time window using message bus.`);
        }),
        catchError(this.handleError<void>('timeWindowExportMessage'))
      );
    }
  }

  public generateExportTimeWindowMessage(beginDateTime: string, endDateTime: string, index: string, sub_type: string, source: string, version: string): TimeWindowExportMessage {
    const timeWindowExportMessage = {
      header: {
        timestamp: moment().toDate().toISOString(),
        message_type: 'export',
        version: index
      },
      msg: {
        sub_type,
        source,
        experiment_id: null,
        trial_id: null,
        timestamp: moment().toDate().toISOString(),
        version,
        replay_id: null,
        replay_parent_id: null,
        replay_parent_type: null
      },
      data: {
        index,
        metadata: {
          begin_date_time: beginDateTime,
          end_date_time: endDateTime
        }
      }
    };
    return timeWindowExportMessage;
  }

  public exportTimeWindow(beginTimeWindow: string, endTimeWindow: string, index: string, filename: string) {
    this._isExportingTrial.next(true);
    this._isElasticsearchBusy.next(true);
    return this.exportTime(beginTimeWindow, endTimeWindow, index, filename).finally(() => {
      this._isExportingTrial.next(false);
      this._isElasticsearchBusy.next(false);
    });
  }

  public importTrial(index: string, file: File) {
    this._isImportingTrial.next(true);
    this._isElasticsearchBusy.next(true);
    return this.import(index, file).finally(() => {
      this._isImportingTrial.next(false);
      this._isElasticsearchBusy.next(false);
    });
  }

  public importReplay(index: string, file: File) {
    this._isImportingReplay.next(true);
    this._isElasticsearchBusy.next(true);
    return this.import(index, file).finally(() => {
      this._isImportingReplay.next(false);
      this._isElasticsearchBusy.next(false);
    });
  }

  private buildExportHeader(index: string, experiment: Experiment, trial: Trial, replayId: string, filename: string) {
    //
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

  private log(message: string) {
    this.loggingService.add(`ElasticsearchService: ${message}`);
  }

}
