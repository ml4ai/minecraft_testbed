function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~dashboard-dashboard-module~docker-docker-module~replay-replay-module~stats-stats-module"], {
  /***/
  "./src/app/replay/replay.service.ts":
  /*!******************************************!*\
    !*** ./src/app/replay/replay.service.ts ***!
    \******************************************/

  /*! exports provided: ReplayService */

  /***/
  function srcAppReplayReplayServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "ReplayService", function () {
      return ReplayService;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! ../../environments/environment */
    "./src/environments/environment.ts");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/http.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var uuid__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! uuid */
    "./node_modules/uuid/dist/esm-browser/index.js");
    /* harmony import */


    var _logging_logging_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ../logging/logging.service */
    "./src/app/logging/logging.service.ts");
    /* harmony import */


    var ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! ngx-mqtt */
    "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js"); // import moment from 'moment';


    var moment = __webpack_require__(
    /*! moment */
    "./node_modules/moment/moment.js");

    var ReplayService = /*#__PURE__*/function () {
      function ReplayService(http, loggingService, mqttService) {
        _classCallCheck(this, ReplayService);

        this.http = http;
        this.loggingService = loggingService;
        this.mqttService = mqttService;
        this.replaysUrl = _environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].metadataAppUrl + '/replays'; // URL to web api

        this._isReplayCreated = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.isReplayCreated = this._isReplayCreated.asObservable();
        this.httpOptions = {
          headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpHeaders"]({
            'Content-Type': 'application/json'
          })
        };
      }
      /** GET replay from the server */


      _createClass(ReplayService, [{
        key: "readReplays",
        value: function readReplays() {
          var _this = this;

          return this.http.get(this.replaysUrl).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            _this.log('Read replays');
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('readReplays', [])));
        }
        /** GET replays by id. Return `undefined` when id not found */

      }, {
        key: "readReplayNo404",
        value: function readReplayNo404(id) {
          var _this2 = this;

          var url = "".concat(this.replaysUrl, "/?id=").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["map"])(function (replays) {
            return replays[0];
          }), // returns a {0|1} element array
          Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (h) {
            var outcome = h ? "Read" : "Did not find";

            _this2.log("".concat(outcome, " replay id=").concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError("getReplays id=".concat(id))));
        }
        /** GET replays by id. Will 404 if id not found */

      }, {
        key: "readReplay",
        value: function readReplay(id) {
          var _this3 = this;

          var url = "".concat(this.replaysUrl, "/").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this3.log("Read replay id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError("getReplays id=".concat(id))));
        }
        /* GET replays whose name contains export term */

      }, {
        key: "searchReplays",
        value: function searchReplays(term) {
          var _this4 = this;

          if (!term.trim()) {
            // if not export term, return empty replays array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])([]);
          }

          return this.http.get("".concat(this.replaysUrl, "/?name=").concat(term)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (x) {
            return x.length ? _this4.log("Found replays matching \"".concat(term, "\"")) : _this4.log("No replays matching \"".concat(term, "\""));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('searchReplays', [])));
        }
        /* GET the root trial of a replay using replay uuid */

      }, {
        key: "getReplayRootTrial",
        value: function getReplayRootTrial(uuid) {
          var _this5 = this;

          var url = "".concat(this.replaysUrl, "/root-trial/").concat(uuid);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this5.log("Get replay root uuid=".concat(uuid));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError("getReplayRoot uuid=".concat(uuid))));
        }
        /* GET list of Replay parents for a Replay */

      }, {
        key: "getReplayParents",
        value: function getReplayParents(uuid) {
          var _this6 = this;

          var url = "".concat(this.replaysUrl, "/parents/").concat(uuid);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this6.log("Get replay parents of uuid=".concat(uuid));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError("getReplayParents uuid=".concat(uuid))));
        }
        /** GET replay from the server */

      }, {
        key: "abortReplay",
        value: function abortReplay() {
          var _this7 = this;

          var url = "".concat(this.replaysUrl, "/run/abort");
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this7.log('Replay aborted!');
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('abortReplay', false)));
        }
        /* GET the existence of the replay in elasticsearch */

      }, {
        key: "getExistReplay",
        value: function getExistReplay(uuid, index) {
          var _this8 = this;

          var url = "".concat(this.replaysUrl, "/").concat(uuid, "/exist?index=").concat(index);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (exist) {
            return _this8.log("Replay ".concat(uuid, " ").concat(exist ? 'exists' : 'does not exist', " in elasticsearch index ").concat(index));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError("Replay ".concat(uuid, " exist in elasticsearch index ").concat(index))));
        } //////// Save methods //////////

        /** POST: add a new replays to the server */

      }, {
        key: "createReplay",
        value: function createReplay(replay) {
          var _this9 = this;

          return this.http.post(this.replaysUrl, replay, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (newReplay) {
            return _this9.log("added replay with id=".concat(newReplay.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "createReplayMessage",
        value: function createReplayMessage(replayMessage) {
          var _this10 = this;

          return this.mqttService.publish('replay', JSON.stringify(replayMessage), {
            qos: 2
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this10.log("Sent message over bus to create replay.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplayMessage')));
        }
        /** DELETE: delete the replays from the server */

      }, {
        key: "deleteReplay",
        value: function deleteReplay(replay) {
          var _this11 = this;

          var id = typeof replay === 'number' ? replay : replay.id;
          var url = "".concat(this.replaysUrl, "/").concat(id);
          return this.http["delete"](url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this11.log("Deleted replay id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('deleteReplay')));
        }
        /** PUT: update the replays on the server */

      }, {
        key: "updateReplay",
        value: function updateReplay(replay) {
          var _this12 = this;

          var id = replay.id;
          var url = "".concat(this.replaysUrl, "/").concat(id);
          return this.http.put(url, replay, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            return _this12.log("Updated replay id=".concat(replay.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('updateReplay')));
        }
        /** POST: run a replay using elasticsearch index */

      }, {
        key: "runReplay",
        value: function runReplay(message, index) {
          var _this13 = this;

          var url = "".concat(this.replaysUrl, "/run/?index=").concat(index);

          this._isReplayCreated.next(true);

          return this.http.post(url, message, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (newReplay) {
            if (newReplay === null) {
              _this13.log("Replay was not run.");

              _this13._isReplayCreated.next(false);
            } else {
              _this13.log("Replay running with id=".concat(newReplay.id));

              _this13._isReplayCreated.next(false);
            }
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "runQuickTrial",
        value: function runQuickTrial(uuid, ignore_message_list, ignore_source_list, ignore_topic_list, index) {
          var _this14 = this;

          var url = "".concat(this.replaysUrl, "/run/trial/").concat(uuid, "?index=").concat(index, "&quick=true");

          this._isReplayCreated.next(true);

          var body = {
            ignore_message_list: ignore_message_list,
            ignore_source_list: ignore_source_list,
            ignore_topic_list: ignore_topic_list
          };
          return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (messageApiResult) {
            if (messageApiResult.result === 'success') {
              _this14.log("".concat(messageApiResult.message));

              _this14._isReplayCreated.next(false);
            } else {
              _this14.log("Replay was not run: ".concat(messageApiResult.message));

              _this14._isReplayCreated.next(false);
            }
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "runQuickReplay",
        value: function runQuickReplay(uuid, ignore_message_list, ignore_source_list, ignore_topic_list, index) {
          var _this15 = this;

          var url = "".concat(this.replaysUrl, "/run/replay/").concat(uuid, "?index=").concat(index, "&quick=true");

          this._isReplayCreated.next(true);

          var body = {
            ignore_message_list: ignore_message_list,
            ignore_source_list: ignore_source_list,
            ignore_topic_list: ignore_topic_list
          };
          return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (messageApiResult) {
            if (messageApiResult.result === 'success') {
              _this15.log("".concat(messageApiResult.message));

              _this15._isReplayCreated.next(false);
            } else {
              _this15.log("Replay was not run: ".concat(messageApiResult.message));

              _this15._isReplayCreated.next(false);
            }
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "runBatchTrial",
        value: function runBatchTrial(replay_objects, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index) {
          var _this16 = this;

          var url = "".concat(this.replaysUrl, "/run/batch/trial?index=").concat(index);

          this._isReplayCreated.next(true);

          var body = {
            replay_objects: replay_objects,
            ignore_message_list: ignore_message_list,
            ignore_source_list: ignore_source_list,
            ignore_topic_list: ignore_topic_list,
            restart: restart
          };
          return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (messageApiResult) {
            if (messageApiResult.result === 'success') {
              _this16.log("".concat(messageApiResult.message));

              _this16._isReplayCreated.next(false);
            } else {
              _this16.log("Replay was not run: ".concat(messageApiResult.message));

              _this16._isReplayCreated.next(false);
            }
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "runBatchReplay",
        value: function runBatchReplay(replay_objects, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index) {
          var _this17 = this;

          var url = "".concat(this.replaysUrl, "/run/batch/replay?index=").concat(index);

          this._isReplayCreated.next(true);

          var body = {
            replay_objects: replay_objects,
            ignore_message_list: ignore_message_list,
            ignore_source_list: ignore_source_list,
            ignore_topic_list: ignore_topic_list,
            restart: restart
          };
          return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (messageApiResult) {
            if (messageApiResult.result === 'success') {
              _this17.log("".concat(messageApiResult.message));

              _this17._isReplayCreated.next(false);
            } else {
              _this17.log("Replay was not run: ".concat(messageApiResult.message));

              _this17._isReplayCreated.next(false);
            }
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
        }
      }, {
        key: "generateReplayMessage",
        value: function generateReplayMessage(trial_id, experiment_id, replay_parent_id, replay_parent_type, ignore_message_list, ignore_source_list, ignore_topic_list, sub_type, source, version) {
          return {
            header: {
              timestamp: moment().toDate().toISOString(),
              message_type: 'replay',
              version: _environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].testbedVersion
            },
            msg: {
              sub_type: sub_type,
              source: source,
              experiment_id: experiment_id,
              trial_id: trial_id,
              timestamp: moment().toDate().toISOString(),
              version: version,
              replay_id: Object(uuid__WEBPACK_IMPORTED_MODULE_5__["v4"])(),
              replay_parent_id: replay_parent_id,
              replay_parent_type: replay_parent_type
            },
            data: {
              ignore_message_list: ignore_message_list,
              ignore_source_list: ignore_source_list,
              ignore_topic_list: ignore_topic_list
            }
          };
        }
      }, {
        key: "generateExportMessage",
        value: function generateExportMessage(replay, parents, index, sub_type, source, version) {
          var root = parents[parents.length - 1];

          if (root === null) {
            this.log('Root item in replay parent tree was not a Trial!');
            return null;
          }

          return {
            header: {
              timestamp: moment().toDate().toISOString(),
              message_type: 'export',
              version: _environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].testbedVersion
            },
            msg: {
              sub_type: sub_type,
              source: source,
              experiment_id: root.experiment.experiment_id,
              trial_id: root.trial_id,
              timestamp: moment().toDate().toISOString(),
              version: version,
              replay_id: replay.replay_id,
              replay_parent_id: replay.replay_parent_id,
              replay_parent_type: replay.replay_parent_type
            },
            data: {
              index: index,
              ignore_message_list: replay.ignore_message_list,
              ignore_source_list: replay.ignore_source_list,
              ignore_topic_list: replay.ignore_topic_list,
              metadata: {
                replay: replay,
                parents: parents
              }
            }
          };
        }
      }, {
        key: "sendExportMessage",
        value: function sendExportMessage(replayExportMessage) {
          var _this18 = this;

          return this.mqttService.publish('metadata/replay/export', JSON.stringify(replayExportMessage), {
            qos: 2
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            _this18.log("Exported replay using message bus.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('replayExportMessage')));
        }
      }, {
        key: "sendRunMessage",
        value: function sendRunMessage(replay) {
          var _this19 = this;

          return this.mqttService.publish('metadata/replay/run', JSON.stringify(replay), {
            qos: 2
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(function (_) {
            _this19.log("Running replay using message bus.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('replayRunMessage')));
        }
        /**
         * Handle Http operation that failed.
         * Let the app continue.
         * @param operation - name of the operation that failed
         * @param result - optional value to return as the observable result
         */

      }, {
        key: "handleError",
        value: function handleError() {
          var _this20 = this;

          var operation = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'operation';
          var result = arguments.length > 1 ? arguments[1] : undefined;
          return function (error) {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption

            _this20.log("".concat(operation, " failed: ").concat(error.message)); // Let the app keep running by returning an empty result.


            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(result);
          };
        }
        /** Log a ReplayService message with the MessageService */

      }, {
        key: "log",
        value: function log(message) {
          this.loggingService.add("ReplayService: ".concat(message));
        }
      }]);

      return ReplayService;
    }();

    ReplayService.ɵfac = function ReplayService_Factory(t) {
      return new (t || ReplayService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_6__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__["MqttService"]));
    };

    ReplayService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: ReplayService,
      factory: ReplayService.ɵfac,
      providedIn: 'root'
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](ReplayService, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }], function () {
        return [{
          type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]
        }, {
          type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_6__["LoggingService"]
        }, {
          type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__["MqttService"]
        }];
      }, null);
    })();
    /***/

  },

  /***/
  "./src/app/trial/trial.service.ts":
  /*!****************************************!*\
    !*** ./src/app/trial/trial.service.ts ***!
    \****************************************/

  /*! exports provided: TrialService */

  /***/
  function srcAppTrialTrialServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "TrialService", function () {
      return TrialService;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/common/http */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/http.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../../environments/environment */
    "./src/environments/environment.ts");
    /* harmony import */


    var _logging_logging_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! ../logging/logging.service */
    "./src/app/logging/logging.service.ts");
    /* harmony import */


    var ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ngx-mqtt */
    "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js"); // import moment from 'moment';


    var moment = __webpack_require__(
    /*! moment */
    "./node_modules/moment/moment.js");

    var TrialService = /*#__PURE__*/function () {
      function TrialService(http, loggingService, mqttService) {
        _classCallCheck(this, TrialService);

        this.http = http;
        this.loggingService = loggingService;
        this.mqttService = mqttService;
        this.trialsUrl = _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].metadataAppUrl + '/trials'; // URL to web api

        this.httpOptions = {
          headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({
            'Content-Type': 'application/json'
          })
        };
      }
      /** GET trials from the server */


      _createClass(TrialService, [{
        key: "readTrials",
        value: function readTrials() {
          var _this21 = this;

          return this.http.get(this.trialsUrl).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this21.log('Read trials');
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('readTrials', [])));
        }
        /** GET trials by id. Return `undefined` when id not found */

      }, {
        key: "readTrialNo404",
        value: function readTrialNo404(id) {
          var _this22 = this;

          var url = "".concat(this.trialsUrl, "/?id=").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (trials) {
            return trials[0];
          }), // returns a {0|1} element array
          Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (h) {
            var outcome = h ? "Read" : "Did not find";

            _this22.log("".concat(outcome, " trial id=").concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials id=".concat(id))));
        }
        /** GET trials by uuid. Return `undefined` when id not found */

      }, {
        key: "readTrialUUID",
        value: function readTrialUUID(uuid) {
          var _this23 = this;

          var url = "".concat(this.trialsUrl, "/uuid/").concat(uuid);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this23.log("Read trial id=".concat(uuid));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials uuid=".concat(uuid))));
        }
        /** GET trials by id. Will 404 if id not found */

      }, {
        key: "readTrial",
        value: function readTrial(id) {
          var _this24 = this;

          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this24.log("Read trial id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials id=".concat(id))));
        }
        /* GET trials whose name contains export term */

      }, {
        key: "searchTrials",
        value: function searchTrials(term) {
          var _this25 = this;

          if (!term.trim()) {
            // if not export term, return empty trials array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])([]);
          }

          return this.http.get("".concat(this.trialsUrl, "/?name=").concat(term)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (x) {
            return x.length ? _this25.log("Found trials matching \"".concat(term, "\"")) : _this25.log("No trials matching \"".concat(term, "\""));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('searchTrials', [])));
        }
        /* GET the existence of the replay in elasticsearch */

      }, {
        key: "getExistReplay",
        value: function getExistReplay(uuid, index) {
          var _this26 = this;

          var url = "".concat(this.trialsUrl, "/").concat(uuid, "/exist?index=").concat(index);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (exist) {
            return _this26.log("Trial ".concat(uuid, " ").concat(exist ? 'exists' : 'does not exist', " in elasticsearch index ").concat(index));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("Trial ".concat(uuid, " exist in elasticsearch index ").concat(index))));
        } //////// Save methods //////////

        /** POST: add a new trials to the server */

      }, {
        key: "createTrial",
        value: function createTrial(trial) {
          var _this27 = this;

          return this.http.post(this.trialsUrl, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (newTrial) {
            return _this27.log("added trial with id=".concat(newTrial.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrial')));
        }
      }, {
        key: "createTrialMessage",
        value: function createTrialMessage(trialMessage) {
          var _this28 = this;

          return this.mqttService.publish('trial', JSON.stringify(trialMessage), {
            qos: 1
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this28.log("Sent message over bus to create trial.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrialMessage')));
        }
        /** DELETE: delete the trials from the server */

      }, {
        key: "deleteTrial",
        value: function deleteTrial(trial) {
          var _this29 = this;

          var id = typeof trial === 'number' ? trial : trial.id;
          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http["delete"](url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this29.log("Deleted trial id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('deleteTrial')));
        }
        /** PUT: update the trials on the server */

      }, {
        key: "updateTrial",
        value: function updateTrial(trial) {
          var _this30 = this;

          var id = trial.id;
          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http.put(url, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this30.log("Updated trial id=".concat(trial.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('updateTrial')));
        }
      }, {
        key: "generateTrialMessage",
        value: function generateTrialMessage(trial, sub_type, source, version, replay_id, replay_parent_id, replay_parent_type) {
          var trialMessage = {
            header: {
              timestamp: trial.date,
              message_type: 'trial',
              version: _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].testbedVersion
            },
            msg: {
              sub_type: sub_type,
              source: source,
              experiment_id: trial.experiment.experiment_id,
              trial_id: trial.trial_id,
              timestamp: moment().toDate().toISOString(),
              version: version,
              replay_id: replay_id,
              replay_parent_id: replay_parent_id,
              replay_parent_type: replay_parent_type
            },
            data: {
              name: trial.name,
              date: trial.date,
              experimenter: trial.experimenter,
              subjects: trial.subjects,
              trial_number: trial.trial_number,
              group_number: trial.group_number,
              study_number: trial.study_number,
              condition: trial.condition,
              notes: trial.notes,
              testbed_version: trial.testbed_version,
              experiment_name: trial.experiment.name,
              experiment_date: trial.experiment.date,
              experiment_author: trial.experiment.author,
              experiment_mission: trial.experiment.mission
            }
          };

          if (replay_id === null) {
            delete trialMessage.msg.replay_id;
          }

          if (replay_parent_id === null) {
            delete trialMessage.msg.replay_parent_id;
          }

          if (replay_parent_type === null) {
            delete trialMessage.msg.replay_parent_type;
          }

          return trialMessage;
        }
      }, {
        key: "generateExportMessage",
        value: function generateExportMessage(trial, index, sub_type, source, version, replay_id, replay_parent_id, replay_parent_type) {
          if (trial === null) {
            return null;
          }

          var trialExportMessage = {
            header: {
              timestamp: moment().toDate().toISOString(),
              message_type: 'export',
              version: index
            },
            msg: {
              sub_type: sub_type,
              source: source,
              experiment_id: trial.experiment.experiment_id,
              trial_id: trial.trial_id,
              timestamp: moment().toDate().toISOString(),
              version: version,
              replay_id: replay_id,
              replay_parent_id: replay_parent_id,
              replay_parent_type: replay_parent_type
            },
            data: {
              index: index,
              metadata: {
                trial: {
                  name: trial.name,
                  date: trial.date,
                  experimenter: trial.experimenter,
                  subjects: trial.subjects,
                  trial_number: trial.trial_number,
                  group_number: trial.group_number,
                  study_number: trial.study_number,
                  condition: trial.condition,
                  notes: trial.notes,
                  testbed_version: trial.testbed_version,
                  experiment_name: trial.experiment.name,
                  experiment_date: trial.experiment.date,
                  experiment_author: trial.experiment.author,
                  experiment_mission: trial.experiment.mission
                }
              }
            }
          };

          if (replay_id === null) {
            delete trialExportMessage.msg.replay_id;
          }

          if (replay_parent_id === null) {
            delete trialExportMessage.msg.replay_parent_id;
          }

          if (replay_parent_type === null) {
            delete trialExportMessage.msg.replay_parent_type;
          }

          return trialExportMessage;
        }
      }, {
        key: "sendExportMessage",
        value: function sendExportMessage(trialExportMessage) {
          var _this31 = this;

          if (trialExportMessage !== null) {
            return this.mqttService.publish('metadata/trial/export', JSON.stringify(trialExportMessage), {
              qos: 1
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
              _this31.log("Exported trial using message bus.");
            }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('trialExportMessage')));
          }
        }
        /**
         * Handle Http operation that failed.
         * Let the app continue.
         * @param operation - name of the operation that failed
         * @param result - optional value to return as the observable result
         */

      }, {
        key: "handleError",
        value: function handleError() {
          var _this32 = this;

          var operation = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'operation';
          var result = arguments.length > 1 ? arguments[1] : undefined;
          return function (error) {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption

            _this32.log("".concat(operation, " failed: ").concat(error.message)); // Let the app keep running by returning an empty result.


            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(result);
          };
        }
        /** Log a TrialService message with the MessageService */

      }, {
        key: "log",
        value: function log(message) {
          this.loggingService.add("TrialService: ".concat(message));
        }
      }]);

      return TrialService;
    }();

    TrialService.ɵfac = function TrialService_Factory(t) {
      return new (t || TrialService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_5__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__["MqttService"]));
    };

    TrialService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: TrialService,
      factory: TrialService.ɵfac,
      providedIn: 'root'
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](TrialService, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }], function () {
        return [{
          type: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"]
        }, {
          type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_5__["LoggingService"]
        }, {
          type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__["MqttService"]
        }];
      }, null);
    })();
    /***/

  }
}]);
//# sourceMappingURL=default~dashboard-dashboard-module~docker-docker-module~replay-replay-module~stats-stats-module-es5.js.map