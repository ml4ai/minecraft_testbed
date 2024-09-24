(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~dashboard-dashboard-module~docker-docker-module~replay-replay-module~stats-stats-module"],{

/***/ "./src/app/replay/replay.service.ts":
/*!******************************************!*\
  !*** ./src/app/replay/replay.service.ts ***!
  \******************************************/
/*! exports provided: ReplayService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ReplayService", function() { return ReplayService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/http.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! uuid */ "./node_modules/uuid/dist/esm-browser/index.js");
/* harmony import */ var _logging_logging_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../logging/logging.service */ "./src/app/logging/logging.service.ts");
/* harmony import */ var ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ngx-mqtt */ "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js");










// import moment from 'moment';
const moment = __webpack_require__(/*! moment */ "./node_modules/moment/moment.js");
class ReplayService {
    constructor(http, loggingService, mqttService) {
        this.http = http;
        this.loggingService = loggingService;
        this.mqttService = mqttService;
        this.replaysUrl = _environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].metadataAppUrl + '/replays'; // URL to web api
        this._isReplayCreated = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.isReplayCreated = this._isReplayCreated.asObservable();
        this.httpOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpHeaders"]({ 'Content-Type': 'application/json' })
        };
    }
    /** GET replay from the server */
    readReplays() {
        return this.http.get(this.replaysUrl)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => {
            this.log('Read replays');
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('readReplays', [])));
    }
    /** GET replays by id. Return `undefined` when id not found */
    readReplayNo404(id) {
        const url = `${this.replaysUrl}/?id=${id}`;
        return this.http.get(url)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["map"])(replays => replays[0]), // returns a {0|1} element array
        Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(h => {
            const outcome = h ? `Read` : `Did not find`;
            this.log(`${outcome} replay id=${id}`);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError(`getReplays id=${id}`)));
    }
    /** GET replays by id. Will 404 if id not found */
    readReplay(id) {
        const url = `${this.replaysUrl}/${id}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Read replay id=${id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError(`getReplays id=${id}`)));
    }
    /* GET replays whose name contains export term */
    searchReplays(term) {
        if (!term.trim()) {
            // if not export term, return empty replays array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])([]);
        }
        return this.http.get(`${this.replaysUrl}/?name=${term}`).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(x => x.length ?
            this.log(`Found replays matching "${term}"`) :
            this.log(`No replays matching "${term}"`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('searchReplays', [])));
    }
    /* GET the root trial of a replay using replay uuid */
    getReplayRootTrial(uuid) {
        const url = `${this.replaysUrl}/root-trial/${uuid}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Get replay root uuid=${uuid}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError(`getReplayRoot uuid=${uuid}`)));
    }
    /* GET list of Replay parents for a Replay */
    getReplayParents(uuid) {
        const url = `${this.replaysUrl}/parents/${uuid}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Get replay parents of uuid=${uuid}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError(`getReplayParents uuid=${uuid}`)));
    }
    /** GET replay from the server */
    abortReplay() {
        const url = `${this.replaysUrl}/run/abort`;
        return this.http.get(url)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log('Replay aborted!')), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('abortReplay', false)));
    }
    /* GET the existence of the replay in elasticsearch */
    getExistReplay(uuid, index) {
        const url = `${this.replaysUrl}/${uuid}/exist?index=${index}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(exist => this.log(`Replay ${uuid} ${exist ? 'exists' : 'does not exist'} in elasticsearch index ${index}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError(`Replay ${uuid} exist in elasticsearch index ${index}`)));
    }
    //////// Save methods //////////
    /** POST: add a new replays to the server */
    createReplay(replay) {
        return this.http.post(this.replaysUrl, replay, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((newReplay) => this.log(`added replay with id=${newReplay.id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    createReplayMessage(replayMessage) {
        return this.mqttService.publish('replay', JSON.stringify(replayMessage), { qos: 2 }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Sent message over bus to create replay.`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplayMessage')));
    }
    /** DELETE: delete the replays from the server */
    deleteReplay(replay) {
        const id = typeof replay === 'number' ? replay : replay.id;
        const url = `${this.replaysUrl}/${id}`;
        return this.http.delete(url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Deleted replay id=${id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('deleteReplay')));
    }
    /** PUT: update the replays on the server */
    updateReplay(replay) {
        const id = replay.id;
        const url = `${this.replaysUrl}/${id}`;
        return this.http.put(url, replay, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => this.log(`Updated replay id=${replay.id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('updateReplay')));
    }
    /** POST: run a replay using elasticsearch index */
    runReplay(message, index) {
        const url = `${this.replaysUrl}/run/?index=${index}`;
        this._isReplayCreated.next(true);
        return this.http.post(url, message, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((newReplay) => {
            if (newReplay === null) {
                this.log(`Replay was not run.`);
                this._isReplayCreated.next(false);
            }
            else {
                this.log(`Replay running with id=${newReplay.id}`);
                this._isReplayCreated.next(false);
            }
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    runQuickTrial(uuid, ignore_message_list, ignore_source_list, ignore_topic_list, index) {
        const url = `${this.replaysUrl}/run/trial/${uuid}?index=${index}&quick=true`;
        this._isReplayCreated.next(true);
        const body = {
            ignore_message_list,
            ignore_source_list,
            ignore_topic_list,
        };
        return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((messageApiResult) => {
            if (messageApiResult.result === 'success') {
                this.log(`${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
            else {
                this.log(`Replay was not run: ${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    runQuickReplay(uuid, ignore_message_list, ignore_source_list, ignore_topic_list, index) {
        const url = `${this.replaysUrl}/run/replay/${uuid}?index=${index}&quick=true`;
        this._isReplayCreated.next(true);
        const body = {
            ignore_message_list,
            ignore_source_list,
            ignore_topic_list,
        };
        return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((messageApiResult) => {
            if (messageApiResult.result === 'success') {
                this.log(`${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
            else {
                this.log(`Replay was not run: ${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    runBatchTrial(replay_objects, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index) {
        const url = `${this.replaysUrl}/run/batch/trial?index=${index}`;
        this._isReplayCreated.next(true);
        const body = {
            replay_objects,
            ignore_message_list,
            ignore_source_list,
            ignore_topic_list,
            restart,
        };
        return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((messageApiResult) => {
            if (messageApiResult.result === 'success') {
                this.log(`${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
            else {
                this.log(`Replay was not run: ${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    runBatchReplay(replay_objects, ignore_message_list, ignore_source_list, ignore_topic_list, restart, index) {
        const url = `${this.replaysUrl}/run/batch/replay?index=${index}`;
        this._isReplayCreated.next(true);
        const body = {
            replay_objects,
            ignore_message_list,
            ignore_source_list,
            ignore_topic_list,
            restart,
        };
        return this.http.post(url, body, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])((messageApiResult) => {
            if (messageApiResult.result === 'success') {
                this.log(`${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
            else {
                this.log(`Replay was not run: ${messageApiResult.message}`);
                this._isReplayCreated.next(false);
            }
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('createReplay')));
    }
    generateReplayMessage(trial_id, experiment_id, replay_parent_id, replay_parent_type, ignore_message_list, ignore_source_list, ignore_topic_list, sub_type, source, version) {
        return {
            header: {
                timestamp: moment().toDate().toISOString(),
                message_type: 'replay',
                version: _environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].testbedVersion
            },
            msg: {
                sub_type,
                source,
                experiment_id,
                trial_id,
                timestamp: moment().toDate().toISOString(),
                version,
                replay_id: Object(uuid__WEBPACK_IMPORTED_MODULE_5__["v4"])(),
                replay_parent_id,
                replay_parent_type
            },
            data: {
                ignore_message_list,
                ignore_source_list,
                ignore_topic_list
            }
        };
    }
    generateExportMessage(replay, parents, index, sub_type, source, version) {
        const root = parents[parents.length - 1];
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
                sub_type,
                source,
                experiment_id: root.experiment.experiment_id,
                trial_id: root.trial_id,
                timestamp: moment().toDate().toISOString(),
                version,
                replay_id: replay.replay_id,
                replay_parent_id: replay.replay_parent_id,
                replay_parent_type: replay.replay_parent_type
            },
            data: {
                index,
                ignore_message_list: replay.ignore_message_list,
                ignore_source_list: replay.ignore_source_list,
                ignore_topic_list: replay.ignore_topic_list,
                metadata: {
                    replay,
                    parents
                }
            }
        };
    }
    sendExportMessage(replayExportMessage) {
        return this.mqttService.publish('metadata/replay/export', JSON.stringify(replayExportMessage), { qos: 2 }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => {
            this.log(`Exported replay using message bus.`);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('replayExportMessage')));
    }
    sendRunMessage(replay) {
        return this.mqttService.publish('metadata/replay/run', JSON.stringify(replay), { qos: 2 }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["tap"])(_ => {
            this.log(`Running replay using message bus.`);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(this.handleError('replayRunMessage')));
    }
    /**
     * Handle Http operation that failed.
     * Let the app continue.
     * @param operation - name of the operation that failed
     * @param result - optional value to return as the observable result
     */
    handleError(operation = 'operation', result) {
        return (error) => {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption
            this.log(`${operation} failed: ${error.message}`);
            // Let the app keep running by returning an empty result.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(result);
        };
    }
    /** Log a ReplayService message with the MessageService */
    log(message) {
        this.loggingService.add(`ReplayService: ${message}`);
    }
}
ReplayService.ɵfac = function ReplayService_Factory(t) { return new (t || ReplayService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_6__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__["MqttService"])); };
ReplayService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({ token: ReplayService, factory: ReplayService.ɵfac, providedIn: 'root' });
/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](ReplayService, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
                providedIn: 'root'
            }]
    }], function () { return [{ type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] }, { type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_6__["LoggingService"] }, { type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_7__["MqttService"] }]; }, null); })();


/***/ }),

/***/ "./src/app/trial/trial.service.ts":
/*!****************************************!*\
  !*** ./src/app/trial/trial.service.ts ***!
  \****************************************/
/*! exports provided: TrialService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TrialService", function() { return TrialService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/http.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _logging_logging_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../logging/logging.service */ "./src/app/logging/logging.service.ts");
/* harmony import */ var ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ngx-mqtt */ "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js");









// import moment from 'moment';
const moment = __webpack_require__(/*! moment */ "./node_modules/moment/moment.js");
class TrialService {
    constructor(http, loggingService, mqttService) {
        this.http = http;
        this.loggingService = loggingService;
        this.mqttService = mqttService;
        this.trialsUrl = _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].metadataAppUrl + '/trials'; // URL to web api
        this.httpOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({ 'Content-Type': 'application/json' })
        };
    }
    /** GET trials from the server */
    readTrials() {
        return this.http.get(this.trialsUrl)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log('Read trials')), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('readTrials', [])));
    }
    /** GET trials by id. Return `undefined` when id not found */
    readTrialNo404(id) {
        const url = `${this.trialsUrl}/?id=${id}`;
        return this.http.get(url)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(trials => trials[0]), // returns a {0|1} element array
        Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(h => {
            const outcome = h ? `Read` : `Did not find`;
            this.log(`${outcome} trial id=${id}`);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError(`getTrials id=${id}`)));
    }
    /** GET trials by uuid. Return `undefined` when id not found */
    readTrialUUID(uuid) {
        const url = `${this.trialsUrl}/uuid/${uuid}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log(`Read trial id=${uuid}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError(`getTrials uuid=${uuid}`)));
    }
    /** GET trials by id. Will 404 if id not found */
    readTrial(id) {
        const url = `${this.trialsUrl}/${id}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log(`Read trial id=${id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError(`getTrials id=${id}`)));
    }
    /* GET trials whose name contains export term */
    searchTrials(term) {
        if (!term.trim()) {
            // if not export term, return empty trials array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])([]);
        }
        return this.http.get(`${this.trialsUrl}/?name=${term}`).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(x => x.length ?
            this.log(`Found trials matching "${term}"`) :
            this.log(`No trials matching "${term}"`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('searchTrials', [])));
    }
    /* GET the existence of the replay in elasticsearch */
    getExistReplay(uuid, index) {
        const url = `${this.trialsUrl}/${uuid}/exist?index=${index}`;
        return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(exist => this.log(`Trial ${uuid} ${exist ? 'exists' : 'does not exist'} in elasticsearch index ${index}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError(`Trial ${uuid} exist in elasticsearch index ${index}`)));
    }
    //////// Save methods //////////
    /** POST: add a new trials to the server */
    createTrial(trial) {
        return this.http.post(this.trialsUrl, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])((newTrial) => this.log(`added trial with id=${newTrial.id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrial')));
    }
    createTrialMessage(trialMessage) {
        return this.mqttService.publish('trial', JSON.stringify(trialMessage), { qos: 1 }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log(`Sent message over bus to create trial.`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrialMessage')));
    }
    /** DELETE: delete the trials from the server */
    deleteTrial(trial) {
        const id = typeof trial === 'number' ? trial : trial.id;
        const url = `${this.trialsUrl}/${id}`;
        return this.http.delete(url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log(`Deleted trial id=${id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('deleteTrial')));
    }
    /** PUT: update the trials on the server */
    updateTrial(trial) {
        const id = trial.id;
        const url = `${this.trialsUrl}/${id}`;
        return this.http.put(url, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => this.log(`Updated trial id=${trial.id}`)), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('updateTrial')));
    }
    generateTrialMessage(trial, sub_type, source, version, replay_id, replay_parent_id, replay_parent_type) {
        const trialMessage = {
            header: {
                timestamp: trial.date,
                message_type: 'trial',
                version: _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].testbedVersion
            },
            msg: {
                sub_type,
                source,
                experiment_id: trial.experiment.experiment_id,
                trial_id: trial.trial_id,
                timestamp: moment().toDate().toISOString(),
                version,
                replay_id,
                replay_parent_id,
                replay_parent_type
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
    generateExportMessage(trial, index, sub_type, source, version, replay_id, replay_parent_id, replay_parent_type) {
        if (trial === null) {
            return null;
        }
        const trialExportMessage = {
            header: {
                timestamp: moment().toDate().toISOString(),
                message_type: 'export',
                version: index
            },
            msg: {
                sub_type,
                source,
                experiment_id: trial.experiment.experiment_id,
                trial_id: trial.trial_id,
                timestamp: moment().toDate().toISOString(),
                version,
                replay_id,
                replay_parent_id,
                replay_parent_type
            },
            data: {
                index,
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
    sendExportMessage(trialExportMessage) {
        if (trialExportMessage !== null) {
            return this.mqttService.publish('metadata/trial/export', JSON.stringify(trialExportMessage), { qos: 1 }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(_ => {
                this.log(`Exported trial using message bus.`);
            }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('trialExportMessage')));
        }
    }
    /**
     * Handle Http operation that failed.
     * Let the app continue.
     * @param operation - name of the operation that failed
     * @param result - optional value to return as the observable result
     */
    handleError(operation = 'operation', result) {
        return (error) => {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption
            this.log(`${operation} failed: ${error.message}`);
            // Let the app keep running by returning an empty result.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(result);
        };
    }
    /** Log a TrialService message with the MessageService */
    log(message) {
        this.loggingService.add(`TrialService: ${message}`);
    }
}
TrialService.ɵfac = function TrialService_Factory(t) { return new (t || TrialService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_5__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__["MqttService"])); };
TrialService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({ token: TrialService, factory: TrialService.ɵfac, providedIn: 'root' });
/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](TrialService, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
                providedIn: 'root'
            }]
    }], function () { return [{ type: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"] }, { type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_5__["LoggingService"] }, { type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__["MqttService"] }]; }, null); })();


/***/ })

}]);
//# sourceMappingURL=default~dashboard-dashboard-module~docker-docker-module~replay-replay-module~stats-stats-module-es2015.js.map