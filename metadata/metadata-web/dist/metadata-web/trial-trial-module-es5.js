function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["trial-trial-module"], {
  /***/
  "./src/app/experiment/experiment.service.ts":
  /*!**************************************************!*\
    !*** ./src/app/experiment/experiment.service.ts ***!
    \**************************************************/

  /*! exports provided: ExperimentService */

  /***/
  function srcAppExperimentExperimentServiceTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "ExperimentService", function () {
      return ExperimentService;
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

    var ExperimentService = /*#__PURE__*/function () {
      function ExperimentService(http, loggingService, mqttService) {
        _classCallCheck(this, ExperimentService);

        this.http = http;
        this.loggingService = loggingService;
        this.mqttService = mqttService;
        this.experimentsUrl = _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].metadataAppUrl + '/experiments'; // URL to web api

        this.httpOptions = {
          headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({
            'Content-Type': 'application/json'
          })
        };
      }
      /** GET experiments from the server */


      _createClass(ExperimentService, [{
        key: "readExperiments",
        value: function readExperiments() {
          var _this = this;

          return this.http.get(this.experimentsUrl).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this.log('Read experiments');
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('readExperiments', [])));
        }
        /** GET experiments by id. Return `undefined` when id not found */

      }, {
        key: "readExperimentNo404",
        value: function readExperimentNo404(id) {
          var _this2 = this;

          var url = "".concat(this.experimentsUrl, "/?id=").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (experiments) {
            return experiments[0];
          }), // returns a {0|1} element array
          Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (h) {
            var outcome = h ? "Read" : "Did not find";

            _this2.log("".concat(outcome, " experiment id=").concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getExperiments id=".concat(id))));
        }
        /** GET experiments by id. Will 404 if id not found */

      }, {
        key: "readExperiment",
        value: function readExperiment(id) {
          var _this3 = this;

          var url = "".concat(this.experimentsUrl, "/").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this3.log("Read experiment id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getExperiments id=".concat(id))));
        }
        /** GET experiments by uuid. Will 404 if id not found */

      }, {
        key: "readExperimentUUID",
        value: function readExperimentUUID(experimentId) {
          var _this4 = this;

          var url = "".concat(this.experimentsUrl, "/uuid/").concat(experimentId);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this4.log("Read experiment experimentId=".concat(experimentId));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getExperiments experimentId=".concat(experimentId))));
        }
        /* GET experiments whose name contains export term */

      }, {
        key: "searchExperiments",
        value: function searchExperiments(term) {
          var _this5 = this;

          if (!term.trim()) {
            // if not export term, return empty experiments array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])([]);
          }

          return this.http.get("".concat(this.experimentsUrl, "/?name=").concat(term)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (x) {
            return x.length ? _this5.log("Found experiments matching \"".concat(term, "\"")) : _this5.log("No experiments matching \"".concat(term, "\""));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('searchExperiments', [])));
        } //////// Save methods //////////

        /** POST: add a new experiments to the server */

      }, {
        key: "createExperiment",
        value: function createExperiment(experiment) {
          var _this6 = this;

          return this.http.post(this.experimentsUrl, experiment, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (newExperiment) {
            return _this6.log("Added experiment with id=".concat(newExperiment.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createExperiment')));
        }
      }, {
        key: "createExperimentMessage",
        value: function createExperimentMessage(experimentMessage) {
          var _this7 = this;

          return this.mqttService.publish('experiment', JSON.stringify(experimentMessage), {
            qos: 1
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this7.log("Sent message over bus to create experiment.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createExperimentMessage')));
        }
        /** DELETE: delete the experiments from the server */

      }, {
        key: "deleteExperiment",
        value: function deleteExperiment(experiment) {
          var _this8 = this;

          var id = typeof experiment === 'number' ? experiment : experiment.id;
          var url = "".concat(this.experimentsUrl, "/").concat(id);
          return this.http["delete"](url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this8.log("Deleted experiment id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('deleteExperiment')));
        }
        /** PUT: update the experiments on the server */

      }, {
        key: "updateExperiment",
        value: function updateExperiment(experiment) {
          var _this9 = this;

          var id = experiment.id;
          var url = "".concat(this.experimentsUrl, "/").concat(id);
          return this.http.put(url, experiment, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this9.log("Updated experiment id=".concat(experiment.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('updateExperiment')));
        }
      }, {
        key: "generateExperimentMessage",
        value: function generateExperimentMessage(experiment, messageType, sub_type, source, version) {
          var experimentMessage = {
            header: {
              timestamp: experiment.date,
              message_type: messageType,
              version: _environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].testbedVersion
            },
            msg: {
              sub_type: sub_type,
              source: source,
              experiment_id: experiment.experiment_id,
              timestamp: moment().toDate().toISOString(),
              version: version
            },
            data: {
              name: experiment.name,
              date: experiment.date,
              author: experiment.author,
              mission: experiment.mission
            }
          };
          return experimentMessage;
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
          var _this10 = this;

          var operation = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'operation';
          var result = arguments.length > 1 ? arguments[1] : undefined;
          return function (error) {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption

            _this10.log("".concat(operation, " failed: ").concat(error.message)); // Let the app keep running by returning an empty result.


            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(result);
          };
        }
        /** Log an ExperimentService message with the MessageService */

      }, {
        key: "log",
        value: function log(message) {
          this.loggingService.add("ExperimentService: ".concat(message));
        }
      }]);

      return ExperimentService;
    }();

    ExperimentService.ɵfac = function ExperimentService_Factory(t) {
      return new (t || ExperimentService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_5__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_6__["MqttService"]));
    };

    ExperimentService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: ExperimentService,
      factory: ExperimentService.ɵfac,
      providedIn: 'root'
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](ExperimentService, [{
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

  },

  /***/
  "./src/app/trial/create-trial/create-trial.component.ts":
  /*!**************************************************************!*\
    !*** ./src/app/trial/create-trial/create-trial.component.ts ***!
    \**************************************************************/

  /*! exports provided: CreateTrialComponent */

  /***/
  function srcAppTrialCreateTrialCreateTrialComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "CreateTrialComponent", function () {
      return CreateTrialComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/material/dialog */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/dialog.js");
    /* harmony import */


    var uuid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! uuid */
    "./node_modules/uuid/dist/esm-browser/index.js");
    /* harmony import */


    var _json_trial_json_trial_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../json-trial/json-trial.component */
    "./src/app/trial/json-trial/json-trial.component.ts");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! ../../../environments/environment */
    "./src/environments/environment.ts");
    /* harmony import */


    var _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ../../experiment/experiment.service */
    "./src/app/experiment/experiment.service.ts");
    /* harmony import */


    var _logging_logging_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! ../../logging/logging.service */
    "./src/app/logging/logging.service.ts");
    /* harmony import */


    var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! @angular/material/form-field */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/form-field.js");
    /* harmony import */


    var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! @angular/material/slide-toggle */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/slide-toggle.js");
    /* harmony import */


    var _angular_material_input__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! @angular/material/input */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/input.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");
    /* harmony import */


    var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! @angular/material/tooltip */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/tooltip.js");
    /* harmony import */


    var _angular_material_icon__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
    /*! @angular/material/icon */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/icon.js");
    /* harmony import */


    var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
    /*! @angular/material/datepicker */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/datepicker.js");
    /* harmony import */


    var _angular_material_select__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
    /*! @angular/material/select */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/select.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _angular_material_core__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
    /*! @angular/material/core */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/core.js");

    function CreateTrialComponent_mat_option_86_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "mat-option", 29);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var experiment_r2 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("value", experiment_r2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", experiment_r2.name, " ");
      }
    }

    var CreateTrialComponent = /*#__PURE__*/function () {
      function CreateTrialComponent(formBuilder, dialogRef, experimentService, jsonDialog, loggingService, data) {
        _classCallCheck(this, CreateTrialComponent);

        this.formBuilder = formBuilder;
        this.dialogRef = dialogRef;
        this.experimentService = experimentService;
        this.jsonDialog = jsonDialog;
        this.loggingService = loggingService;
        this.data = data;
        this.experiments = [];
        this.createTrialForm = this.formBuilder.group({
          trial_id: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          date: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experimenter: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          subjects: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          trial_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          group_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          study_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          condition: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          notes: [''],
          testbed_version: [_environments_environment__WEBPACK_IMPORTED_MODULE_5__["environment"].testbedVersion, _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experiment: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          useMessageBus: [false]
        });
        this.uuidPattern = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
      }

      _createClass(CreateTrialComponent, [{
        key: "readExperiments",
        value: function readExperiments() {
          var _this11 = this;

          this.experimentService.readExperiments().subscribe(function (experiments) {
            _this11.experiments = experiments;
          });
        }
      }, {
        key: "openJsonTrialDialog",
        value: function openJsonTrialDialog() {
          var _this12 = this;

          var dialogResult = this.createTrialForm.value;
          var subjectsText = this.createTrialForm.get('subjects').value;

          if (subjectsText !== '') {
            dialogResult.subjects = subjectsText.split(/[\r\n]+/);
          } else {
            dialogResult.subjects = [];
          }

          var notesText = this.createTrialForm.get('notes').value;

          if (notesText !== '') {
            dialogResult.notes = notesText.split(/[\r\n]+/);
          } else {
            dialogResult.notes = [];
          }

          delete dialogResult.useMessageBus;
          var jsonDialogRef = this.jsonDialog.open(_json_trial_json_trial_component__WEBPACK_IMPORTED_MODULE_4__["JsonTrialComponent"], {
            // width: '250px',
            data: JSON.stringify(dialogResult, null, 2),
            panelClass: 'full-width-2-dialog'
          });
          jsonDialogRef.afterClosed().subscribe(function (result) {
            if (result) {
              try {
                var trial = JSON.parse(result.json); // let experiment = {
                //   name: trial.experiment
                // }

                var experiment = _this12.experiments.find(function (e) {
                  return e.name === trial.experiment;
                });

                _this12.createTrialForm.patchValue({
                  trial_id: trial.trial_id,
                  name: trial.name,
                  date: trial.date,
                  experimenter: trial.experimenter,
                  subjects: trial.subjects.length > 0 ? trial.subjects.join('\r\n') : trial.subjects,
                  trial_number: trial.trial_number,
                  group_number: trial.group_number,
                  study_number: trial.study_number,
                  condition: trial.condition,
                  notes: trial.notes.length > 0 ? trial.notes.join('\r\n') : trial.notes,
                  testbed_version: trial.testbed_version,
                  experiment: experiment
                });
              } catch (e) {
                _this12.log(e);
              }
            }
          });
        }
      }, {
        key: "onCreateClick",
        value: function onCreateClick() {
          var dialogResult = this.createTrialForm.value;
          var subjectsText = this.createTrialForm.get('subjects').value;

          if (subjectsText !== '') {
            dialogResult.subjects = subjectsText.split(/[\r\n]+/);
          } else {
            dialogResult.subjects = [];
          }

          var notesText = this.createTrialForm.get('notes').value;

          if (notesText !== '') {
            dialogResult.notes = notesText.split(/[\r\n]+/);
          } else {
            dialogResult.notes = [];
          }

          this.dialogRef.close(dialogResult);
        }
      }, {
        key: "onCancelClick",
        value: function onCancelClick() {
          this.dialogRef.close();
        }
      }, {
        key: "onGenerateUUIDClick",
        value: function onGenerateUUIDClick() {
          this.createTrialForm.patchValue({
            trial_id: Object(uuid__WEBPACK_IMPORTED_MODULE_3__["v4"])()
          });
        }
      }, {
        key: "toggleUseMessageBusChange",
        value: function toggleUseMessageBusChange(event) {// if (event.checked) {
          //   this.createTrialForm.controls['trial_id'].reset('', {
          //     onlySelf: true
          //   });
          // } else {
          //   this.createTrialForm.controls['trial_id'].reset('', {
          //     onlySelf: true
          //   });
          // }
        }
      }, {
        key: "ngOnInit",
        value: function ngOnInit() {
          this.readExperiments();
        }
      }, {
        key: "compareFnExperiments",
        value: function compareFnExperiments(e1, e2) {
          return e1 && e2 ? e1.name === e2.name : e1 === e2;
        }
        /** Log a TrialService message with the MessageService */

      }, {
        key: "log",
        value: function log(message) {
          this.loggingService.add("CreateTrialComponent: ".concat(message));
        }
      }]);

      return CreateTrialComponent;
    }();

    CreateTrialComponent.ɵfac = function CreateTrialComponent_Factory(t) {
      return new (t || CreateTrialComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_experiment_experiment_service__WEBPACK_IMPORTED_MODULE_6__["ExperimentService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialog"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_7__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]));
    };

    CreateTrialComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: CreateTrialComponent,
      selectors: [["app-create-trial"]],
      decls: 94,
      vars: 7,
      consts: [["mat-dialog-title", ""], ["mat-dialog-content", "", "layout", "row", "layout-align", "center center", 3, "formGroup"], ["floatLabel", "always", "appearance", "none"], [1, "header-row"], ["color", "primary", "formControlName", "useMessageBus", 3, "change"], ["matInput", "", "hidden", ""], ["mat-fab", "", "color", "primary", "matTooltip", "Use JSON to populate form.", 3, "click"], ["aria-label", "Create"], ["appearance", "fill"], ["matInput", "", "formControlName", "trial_id", "placeholder", "UUID", "required", "", "autocomplete", "off", 3, "pattern"], ["mat-icon-button", "", "matSuffix", "", 3, "click"], ["aria-label", "UUID"], ["matInput", "", "formControlName", "name", "placeholder", "Name", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "date", "required", "", "autocomplete", "off", 3, "matDatepicker"], ["matSuffix", "", 3, "for"], ["date", ""], ["matInput", "", "formControlName", "experimenter", "placeholder", "Experimenter", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "subjects", "placeholder", "Subjects...", "autocomplete", "off"], ["matInput", "", "formControlName", "trial_number", "placeholder", "Trial Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "group_number", "placeholder", "Trial Group Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "study_number", "placeholder", "Trial Study Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "condition", "placeholder", "Trial Condition", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "notes", "placeholder", "Notes...", "autocomplete", "off"], ["matInput", "", "formControlName", "testbed_version", "placeholder", "Testbed Version", "required", "", "autocomplete", "off"], ["formControlName", "experiment", "placeholder", "Experiment", "required", "", 3, "compareWith"], [3, "value", 4, "ngFor", "ngForOf"], ["mat-dialog-actions", "", "align", "end"], ["mat-raised-button", "", "color", "accent", 3, "click"], ["mat-raised-button", "", "color", "primary", 3, "disabled", "click"], [3, "value"]],
      template: function CreateTrialComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "h1", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, "Create");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "fieldset");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "legend");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "Trial");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "div", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "mat-slide-toggle", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("change", function CreateTrialComponent_Template_mat_slide_toggle_change_8_listener($event) {
            return ctx.toggleUseMessageBusChange($event);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](9, "Use Message Bus");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](10, "textarea", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "button", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CreateTrialComponent_Template_button_click_11_listener() {
            return ctx.openJsonTrialDialog();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "mat-icon", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](13, "text_snippet");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](16, "Trial UUID");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](17, "input", 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](18, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](19, "Please use a valid UUID.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](20, "button", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CreateTrialComponent_Template_button_click_20_listener() {
            return ctx.onGenerateUUIDClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](21, "mat-icon", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](22, "autorenew");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](23, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](24, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](25, "Trial Name");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](26, "input", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](28, "Name is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](29, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](31, "Trial Date");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](32, "input", 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](33, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](34, "Date is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](35, "mat-datepicker-toggle", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](36, "mat-datepicker", null, 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](38, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](39, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](40, "Trial Experimenter");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](41, "input", 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](42, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](43, "Experimenter is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](44, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](45, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](46, "Trial Subjects");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](47, "textarea", 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](48, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](49, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](50, "Trial Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](51, "input", 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](52, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](53, "Trial Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](54, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](55, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](56, "Trial Group Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](57, "input", 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](58, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](59, "Trial Group Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](60, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](61, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](62, "Trial Study Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](63, "input", 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](64, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](65, "Trial Study Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](66, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](67, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](68, "Trial Condition");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](69, "input", 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](70, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](71, "Trial Condition is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](72, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](73, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](74, "Trial Notes");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](75, "textarea", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](76, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](77, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](78, "Trial Testbed Version");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](79, "input", 23);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](80, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](81, "Testbed version is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](82, "mat-form-field", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](83, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](84, "Trial Experiment");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](85, "mat-select", 24);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](86, CreateTrialComponent_mat_option_86_Template, 2, 2, "mat-option", 25);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](87, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](88, "Experiment is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](89, "div", 26);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](90, "button", 27);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CreateTrialComponent_Template_button_click_90_listener() {
            return ctx.onCancelClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](91, "Cancel");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](92, "button", 28);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CreateTrialComponent_Template_button_click_92_listener() {
            return ctx.onCreateClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](93, "Create");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          var _r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](37);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.createTrialForm);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("pattern", ctx.uuidPattern);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("matDatepicker", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("for", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](50);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("compareWith", ctx.compareFnExperiments);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.experiments);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", !ctx.createTrialForm.valid);
        }
      },
      directives: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogTitle"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogContent"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatusGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormGroupDirective"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MatFormField"], _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__["MatSlideToggle"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControlName"], _angular_material_input__WEBPACK_IMPORTED_MODULE_10__["MatInput"], _angular_material_button__WEBPACK_IMPORTED_MODULE_11__["MatButton"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_12__["MatTooltip"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_13__["MatIcon"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MatLabel"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["DefaultValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["RequiredValidator"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["PatternValidator"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MatError"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MatSuffix"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_14__["MatDatepickerInput"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_14__["MatDatepickerToggle"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_14__["MatDatepicker"], _angular_material_select__WEBPACK_IMPORTED_MODULE_15__["MatSelect"], _angular_common__WEBPACK_IMPORTED_MODULE_16__["NgForOf"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogActions"], _angular_material_core__WEBPACK_IMPORTED_MODULE_17__["MatOption"]],
      styles: ["mat-form-field[_ngcontent-%COMP%] {\n  width: 100%;\n}\n\n.header-row[_ngcontent-%COMP%] {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvdHJpYWwvY3JlYXRlLXRyaWFsL0M6XFxVc2Vyc1xcQ2hhcmxpZSBLYXBvcG91bG9zXFxQcm9qZWN0c1xcQXB0aW1hXFx0ZXN0YmVkXFxtZXRhZGF0YVxcbWV0YWRhdGEtd2ViL3NyY1xcYXBwXFx0cmlhbFxcY3JlYXRlLXRyaWFsXFxjcmVhdGUtdHJpYWwuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3RyaWFsL2NyZWF0ZS10cmlhbC9jcmVhdGUtdHJpYWwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxXQUFXO0FDQ2I7O0FERUE7RUFDRSxhQUFhO0VBQ2IsOEJBQThCO0VBQzlCLG1CQUFtQjtBQ0NyQiIsImZpbGUiOiJzcmMvYXBwL3RyaWFsL2NyZWF0ZS10cmlhbC9jcmVhdGUtdHJpYWwuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJtYXQtZm9ybS1maWVsZCB7XHJcbiAgd2lkdGg6IDEwMCU7XHJcbn1cclxuXHJcbi5oZWFkZXItcm93IHtcclxuICBkaXNwbGF5OiBmbGV4O1xyXG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2VlbjtcclxuICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG59XHJcbiIsIm1hdC1mb3JtLWZpZWxkIHtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbi5oZWFkZXItcm93IHtcbiAgZGlzcGxheTogZmxleDtcbiAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuIl19 */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](CreateTrialComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-create-trial',
          templateUrl: './create-trial.component.html',
          styleUrls: ['./create-trial.component.scss']
        }]
      }], function () {
        return [{
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]
        }, {
          type: _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_6__["ExperimentService"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialog"]
        }, {
          type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_7__["LoggingService"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]]
          }]
        }];
      }, null);
    })();
    /***/

  },

  /***/
  "./src/app/trial/delete-trial/delete-trial.component.ts":
  /*!**************************************************************!*\
    !*** ./src/app/trial/delete-trial/delete-trial.component.ts ***!
    \**************************************************************/

  /*! exports provided: DeleteTrialComponent */

  /***/
  function srcAppTrialDeleteTrialDeleteTrialComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "DeleteTrialComponent", function () {
      return DeleteTrialComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/material/dialog */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/dialog.js");
    /* harmony import */


    var uuid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! uuid */
    "./node_modules/uuid/dist/esm-browser/index.js");
    /* harmony import */


    var _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../../experiment/experiment.service */
    "./src/app/experiment/experiment.service.ts");
    /* harmony import */


    var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/material/form-field */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/form-field.js");
    /* harmony import */


    var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! @angular/material/input */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/input.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");
    /* harmony import */


    var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! @angular/material/icon */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/icon.js");
    /* harmony import */


    var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! @angular/material/datepicker */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/datepicker.js");
    /* harmony import */


    var _angular_material_select__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! @angular/material/select */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/select.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _angular_material_core__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! @angular/material/core */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/core.js");

    function DeleteTrialComponent_mat_option_78_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "mat-option", 23);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var experiment_r2 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("value", experiment_r2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", experiment_r2.name, " ");
      }
    }

    var DeleteTrialComponent = /*#__PURE__*/function () {
      function DeleteTrialComponent(formBuilder, dialogRef, experimentService, data) {
        _classCallCheck(this, DeleteTrialComponent);

        this.formBuilder = formBuilder;
        this.dialogRef = dialogRef;
        this.experimentService = experimentService;
        this.data = data;
        this.deleteTrialForm = this.formBuilder.group({
          id: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          trial_id: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          date: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experimenter: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          subjects: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          trial_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          group_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          study_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          condition: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          notes: [''],
          testbed_version: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experiment: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required]
        });
        this.uuidPattern = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
      }

      _createClass(DeleteTrialComponent, [{
        key: "readExperiments",
        value: function readExperiments() {
          var _this13 = this;

          this.experimentService.readExperiments().subscribe(function (experiments) {
            _this13.experiments = experiments;
          });
        }
      }, {
        key: "onDeleteClick",
        value: function onDeleteClick() {
          this.dialogRef.close(this.deleteTrialForm.getRawValue());
        }
      }, {
        key: "onCancelClick",
        value: function onCancelClick() {
          this.dialogRef.close();
        }
      }, {
        key: "onGenerateUUIDClick",
        value: function onGenerateUUIDClick() {
          this.deleteTrialForm.patchValue({
            trial_id: Object(uuid__WEBPACK_IMPORTED_MODULE_3__["v4"])()
          });
        }
      }, {
        key: "ngOnInit",
        value: function ngOnInit() {
          this.readExperiments();
          this.deleteTrialForm.setValue({
            id: this.data.id,
            trial_id: this.data.trial_id,
            name: this.data.name,
            date: this.data.date,
            experimenter: this.data.experimenter,
            subjects: this.data.subjects.length > 0 ? this.data.subjects.join('\r\n') : this.data.subjects,
            trial_number: this.data.trial_number,
            group_number: this.data.group_number,
            study_number: this.data.study_number,
            condition: this.data.condition,
            notes: this.data.notes.length > 0 ? this.data.notes.join('\r\n') : this.data.notes,
            testbed_version: this.data.testbed_version,
            experiment: this.data.experiment
          });
          this.deleteTrialForm.disable();
        }
      }, {
        key: "compareFnExperiments",
        value: function compareFnExperiments(e1, e2) {
          return e1 && e2 ? e1.id === e2.id : e1 === e2;
        }
      }]);

      return DeleteTrialComponent;
    }();

    DeleteTrialComponent.ɵfac = function DeleteTrialComponent_Factory(t) {
      return new (t || DeleteTrialComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__["ExperimentService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]));
    };

    DeleteTrialComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DeleteTrialComponent,
      selectors: [["app-delete-trial"]],
      decls: 86,
      vars: 8,
      consts: [["mat-dialog-title", ""], ["mat-dialog-content", "", "layout", "row", "layout-align", "center center", 3, "formGroup"], ["appearance", "fill"], ["matInput", "", "formControlName", "trial_id", "placeholder", "UUID", "required", "", "autocomplete", "off", 3, "pattern"], ["mat-icon-button", "", "matSuffix", "", 3, "disabled", "click"], ["aria-label", "UUID"], ["matInput", "", "formControlName", "name", "placeholder", "Name", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "date", "required", "", "autocomplete", "off", 3, "matDatepicker"], ["matSuffix", "", 3, "for"], ["date", ""], ["matInput", "", "formControlName", "experimenter", "placeholder", "Experimenter", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "subjects", "placeholder", "Subjects...", "autocomplete", "off"], ["matInput", "", "formControlName", "trial_number", "placeholder", "Trial Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "group_number", "placeholder", "Trial Group Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "study_number", "placeholder", "Trial Study Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "condition", "placeholder", "Trial Condition", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "notes", "placeholder", "Notes...", "autocomplete", "off"], ["matInput", "", "formControlName", "testbed_version", "placeholder", "Testbed Version", "required", "", "autocomplete", "off"], ["formControlName", "experiment", "placeholder", "Experiment", "required", "", 3, "compareWith"], [3, "value", 4, "ngFor", "ngForOf"], ["mat-dialog-actions", "", "align", "end"], ["mat-raised-button", "", "color", "accent", 3, "click"], ["mat-raised-button", "", "color", "primary", 3, "click"], [3, "value"]],
      template: function DeleteTrialComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "h1", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, "Delete");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "fieldset");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "legend");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](8, "Trial UUID");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "input", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11, "Please use a valid UUID.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "button", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DeleteTrialComponent_Template_button_click_12_listener() {
            return ctx.onGenerateUUIDClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "mat-icon", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](14, "autorenew");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](16, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](17, "Trial Name");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](18, "input", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](19, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](20, "Name is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](21, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](23, "Trial Date");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](24, "input", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](25, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](26, "Date is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](27, "mat-datepicker-toggle", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](28, "mat-datepicker", null, 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](31, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](32, "Trial Experimenter");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](33, "input", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](34, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](35, "Experimenter is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](36, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](37, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](38, "Trial Subjects");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](39, "textarea", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](40, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](41, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](42, "Trial Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](43, "input", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](44, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](45, "Trial Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](46, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](47, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](48, "Trial Group Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](49, "input", 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](50, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](51, "Trial Group Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](52, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](53, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](54, "Trial Study Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](55, "input", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](56, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](57, "Trial Study Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](58, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](59, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](60, "Trial Condition");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](61, "input", 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](62, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](63, "Trial Condition is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](64, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](65, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](66, "Trial Notes");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](67, "textarea", 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](68, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](69, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](70, "Trial Testbed Version");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](71, "input", 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](72, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](73, "Testbed version is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](74, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](75, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](76, "Trial Experiment");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](77, "mat-select", 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](78, DeleteTrialComponent_mat_option_78_Template, 2, 2, "mat-option", 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](79, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](80, "Experiment is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](81, "div", 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](82, "button", 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DeleteTrialComponent_Template_button_click_82_listener() {
            return ctx.onCancelClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](83, "Cancel");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](84, "button", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DeleteTrialComponent_Template_button_click_84_listener() {
            return ctx.onDeleteClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](85, "Delete");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          var _r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](29);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.deleteTrialForm);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("Trial: ", ctx.data.id, "");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("pattern", ctx.uuidPattern);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.deleteTrialForm.disabled);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("matDatepicker", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("for", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](50);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("compareWith", ctx.compareFnExperiments);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.experiments);
        }
      },
      directives: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogTitle"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogContent"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatusGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormGroupDirective"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatFormField"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatLabel"], _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInput"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["DefaultValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControlName"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["RequiredValidator"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["PatternValidator"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatError"], _angular_material_button__WEBPACK_IMPORTED_MODULE_7__["MatButton"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatSuffix"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIcon"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerInput"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerToggle"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepicker"], _angular_material_select__WEBPACK_IMPORTED_MODULE_10__["MatSelect"], _angular_common__WEBPACK_IMPORTED_MODULE_11__["NgForOf"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogActions"], _angular_material_core__WEBPACK_IMPORTED_MODULE_12__["MatOption"]],
      styles: ["mat-form-field[_ngcontent-%COMP%] {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvdHJpYWwvZGVsZXRlLXRyaWFsL0M6XFxVc2Vyc1xcQ2hhcmxpZSBLYXBvcG91bG9zXFxQcm9qZWN0c1xcQXB0aW1hXFx0ZXN0YmVkXFxtZXRhZGF0YVxcbWV0YWRhdGEtd2ViL3NyY1xcYXBwXFx0cmlhbFxcZGVsZXRlLXRyaWFsXFxkZWxldGUtdHJpYWwuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3RyaWFsL2RlbGV0ZS10cmlhbC9kZWxldGUtdHJpYWwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxXQUFXO0FDQ2IiLCJmaWxlIjoic3JjL2FwcC90cmlhbC9kZWxldGUtdHJpYWwvZGVsZXRlLXRyaWFsLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsibWF0LWZvcm0tZmllbGQge1xyXG4gIHdpZHRoOiAxMDAlO1xyXG59XHJcbiIsIm1hdC1mb3JtLWZpZWxkIHtcbiAgd2lkdGg6IDEwMCU7XG59XG4iXX0= */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](DeleteTrialComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-delete-trial',
          templateUrl: './delete-trial.component.html',
          styleUrls: ['./delete-trial.component.scss']
        }]
      }], function () {
        return [{
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]
        }, {
          type: _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__["ExperimentService"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]]
          }]
        }];
      }, null);
    })();
    /***/

  },

  /***/
  "./src/app/trial/json-trial/json-trial.component.ts":
  /*!**********************************************************!*\
    !*** ./src/app/trial/json-trial/json-trial.component.ts ***!
    \**********************************************************/

  /*! exports provided: JsonTrialComponent */

  /***/
  function srcAppTrialJsonTrialJsonTrialComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "JsonTrialComponent", function () {
      return JsonTrialComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/material/dialog */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/dialog.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/material/form-field */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/form-field.js");
    /* harmony import */


    var _angular_material_input__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @angular/material/input */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/input.js");
    /* harmony import */


    var _angular_cdk_text_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/cdk/text-field */
    "./node_modules/@angular/cdk/__ivy_ngcc__/fesm2015/text-field.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");

    var JsonTrialComponent = /*#__PURE__*/function () {
      function JsonTrialComponent(formBuilder, dialogRef, data) {
        _classCallCheck(this, JsonTrialComponent);

        this.formBuilder = formBuilder;
        this.dialogRef = dialogRef;
        this.data = data;
        this.jsonTrialForm = this.formBuilder.group({
          json: ['']
        });
      }

      _createClass(JsonTrialComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          this.jsonTrialForm.setValue({
            json: this.data
          });
        }
      }, {
        key: "onParseClick",
        value: function onParseClick() {
          var dialogResult = this.jsonTrialForm.value;
          this.dialogRef.close(dialogResult);
        }
      }, {
        key: "onCancelClick",
        value: function onCancelClick() {
          this.dialogRef.close();
        }
      }]);

      return JsonTrialComponent;
    }();

    JsonTrialComponent.ɵfac = function JsonTrialComponent_Factory(t) {
      return new (t || JsonTrialComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MatDialogRef"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MAT_DIALOG_DATA"]));
    };

    JsonTrialComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: JsonTrialComponent,
      selectors: [["app-json-trial"]],
      decls: 16,
      vars: 2,
      consts: [["mat-dialog-title", ""], ["mat-dialog-content", "", "layout", "row", "layout-align", "center center", 3, "formGroup"], ["color", "accent", "appearance", "fill"], ["matInput", "", "cdkTextareaAutosize", "", "cdkAutosizeMinRows", "20", "cdkAutosizeMaxRows", "20", "md-detect-hidden", "", "formControlName", "json", "placeholder", "{ }", "autocomplete", "off"], ["autosize", "cdkTextareaAutosize"], ["mat-dialog-actions", "", "align", "end"], ["mat-raised-button", "", "color", "accent", 3, "click"], ["mat-raised-button", "", "color", "primary", 3, "disabled", "click"]],
      template: function JsonTrialComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "h1", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, "Parse");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "fieldset");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "legend");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "JSON Trial");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](8, "JSON");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "textarea", 3, 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "div", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "button", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function JsonTrialComponent_Template_button_click_12_listener() {
            return ctx.onCancelClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](13, "Cancel");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "button", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function JsonTrialComponent_Template_button_click_14_listener() {
            return ctx.onParseClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](15, "Parse");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.jsonTrialForm);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", !ctx.jsonTrialForm.valid);
        }
      },
      directives: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MatDialogTitle"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MatDialogContent"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__["NgControlStatusGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormGroupDirective"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_3__["MatFormField"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_3__["MatLabel"], _angular_material_input__WEBPACK_IMPORTED_MODULE_4__["MatInput"], _angular_cdk_text_field__WEBPACK_IMPORTED_MODULE_5__["CdkTextareaAutosize"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__["DefaultValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControlName"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MatDialogActions"], _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButton"]],
      styles: ["mat-form-field[_ngcontent-%COMP%] {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvdHJpYWwvanNvbi10cmlhbC9DOlxcVXNlcnNcXENoYXJsaWUgS2Fwb3BvdWxvc1xcUHJvamVjdHNcXEFwdGltYVxcdGVzdGJlZFxcbWV0YWRhdGFcXG1ldGFkYXRhLXdlYi9zcmNcXGFwcFxcdHJpYWxcXGpzb24tdHJpYWxcXGpzb24tdHJpYWwuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3RyaWFsL2pzb24tdHJpYWwvanNvbi10cmlhbC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFdBQVc7QUNDYiIsImZpbGUiOiJzcmMvYXBwL3RyaWFsL2pzb24tdHJpYWwvanNvbi10cmlhbC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIm1hdC1mb3JtLWZpZWxkIHtcclxuICB3aWR0aDogMTAwJTtcclxufVxyXG4iLCJtYXQtZm9ybS1maWVsZCB7XG4gIHdpZHRoOiAxMDAlO1xufVxuIl19 */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](JsonTrialComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-json-trial',
          templateUrl: './json-trial.component.html',
          styleUrls: ['./json-trial.component.scss']
        }]
      }], function () {
        return [{
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MatDialogRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_1__["MAT_DIALOG_DATA"]]
          }]
        }];
      }, null);
    })();
    /***/

  },

  /***/
  "./src/app/trial/trial-routing.module.ts":
  /*!***********************************************!*\
    !*** ./src/app/trial/trial-routing.module.ts ***!
    \***********************************************/

  /*! exports provided: TrialRoutingModule */

  /***/
  function srcAppTrialTrialRoutingModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "TrialRoutingModule", function () {
      return TrialRoutingModule;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/router */
    "./node_modules/@angular/router/__ivy_ngcc__/fesm2015/router.js");
    /* harmony import */


    var _trials_trials_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./trials/trials.component */
    "./src/app/trial/trials/trials.component.ts");

    var routes = [{
      path: '',
      component: _trials_trials_component__WEBPACK_IMPORTED_MODULE_2__["TrialsComponent"]
    }];

    var TrialRoutingModule = function TrialRoutingModule() {
      _classCallCheck(this, TrialRoutingModule);
    };

    TrialRoutingModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: TrialRoutingModule
    });
    TrialRoutingModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function TrialRoutingModule_Factory(t) {
        return new (t || TrialRoutingModule)();
      },
      imports: [[_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)], _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](TrialRoutingModule, {
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](TrialRoutingModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)],
          exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
        }]
      }], null, null);
    })();
    /***/

  },

  /***/
  "./src/app/trial/trial.module.ts":
  /*!***************************************!*\
    !*** ./src/app/trial/trial.module.ts ***!
    \***************************************/

  /*! exports provided: TrialModule */

  /***/
  function srcAppTrialTrialModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "TrialModule", function () {
      return TrialModule;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _trial_routing_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./trial-routing.module */
    "./src/app/trial/trial-routing.module.ts");
    /* harmony import */


    var _trials_trials_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./trials/trials.component */
    "./src/app/trial/trials/trials.component.ts");
    /* harmony import */


    var _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../angular-material/angular-material-module */
    "./src/app/angular-material/angular-material-module.ts");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _create_trial_create_trial_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ./create-trial/create-trial.component */
    "./src/app/trial/create-trial/create-trial.component.ts");
    /* harmony import */


    var _update_trial_update_trial_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! ./update-trial/update-trial.component */
    "./src/app/trial/update-trial/update-trial.component.ts");
    /* harmony import */


    var _delete_trial_delete_trial_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! ./delete-trial/delete-trial.component */
    "./src/app/trial/delete-trial/delete-trial.component.ts");
    /* harmony import */


    var _json_trial_json_trial_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! ./json-trial/json-trial.component */
    "./src/app/trial/json-trial/json-trial.component.ts");

    var TrialModule = function TrialModule() {
      _classCallCheck(this, TrialModule);
    };

    TrialModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: TrialModule
    });
    TrialModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function TrialModule_Factory(t) {
        return new (t || TrialModule)();
      },
      imports: [[_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _trial_routing_module__WEBPACK_IMPORTED_MODULE_2__["TrialRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_4__["AngularMaterialModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"]]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](TrialModule, {
        declarations: [_trials_trials_component__WEBPACK_IMPORTED_MODULE_3__["TrialsComponent"], _create_trial_create_trial_component__WEBPACK_IMPORTED_MODULE_6__["CreateTrialComponent"], _update_trial_update_trial_component__WEBPACK_IMPORTED_MODULE_7__["UpdateTrialComponent"], _delete_trial_delete_trial_component__WEBPACK_IMPORTED_MODULE_8__["DeleteTrialComponent"], _json_trial_json_trial_component__WEBPACK_IMPORTED_MODULE_9__["JsonTrialComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _trial_routing_module__WEBPACK_IMPORTED_MODULE_2__["TrialRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_4__["AngularMaterialModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](TrialModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          declarations: [_trials_trials_component__WEBPACK_IMPORTED_MODULE_3__["TrialsComponent"], _create_trial_create_trial_component__WEBPACK_IMPORTED_MODULE_6__["CreateTrialComponent"], _update_trial_update_trial_component__WEBPACK_IMPORTED_MODULE_7__["UpdateTrialComponent"], _delete_trial_delete_trial_component__WEBPACK_IMPORTED_MODULE_8__["DeleteTrialComponent"], _json_trial_json_trial_component__WEBPACK_IMPORTED_MODULE_9__["JsonTrialComponent"]],
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _trial_routing_module__WEBPACK_IMPORTED_MODULE_2__["TrialRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_4__["AngularMaterialModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"]]
        }]
      }], null, null);
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
          var _this14 = this;

          return this.http.get(this.trialsUrl).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this14.log('Read trials');
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('readTrials', [])));
        }
        /** GET trials by id. Return `undefined` when id not found */

      }, {
        key: "readTrialNo404",
        value: function readTrialNo404(id) {
          var _this15 = this;

          var url = "".concat(this.trialsUrl, "/?id=").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (trials) {
            return trials[0];
          }), // returns a {0|1} element array
          Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (h) {
            var outcome = h ? "Read" : "Did not find";

            _this15.log("".concat(outcome, " trial id=").concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials id=".concat(id))));
        }
        /** GET trials by uuid. Return `undefined` when id not found */

      }, {
        key: "readTrialUUID",
        value: function readTrialUUID(uuid) {
          var _this16 = this;

          var url = "".concat(this.trialsUrl, "/uuid/").concat(uuid);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this16.log("Read trial id=".concat(uuid));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials uuid=".concat(uuid))));
        }
        /** GET trials by id. Will 404 if id not found */

      }, {
        key: "readTrial",
        value: function readTrial(id) {
          var _this17 = this;

          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this17.log("Read trial id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("getTrials id=".concat(id))));
        }
        /* GET trials whose name contains export term */

      }, {
        key: "searchTrials",
        value: function searchTrials(term) {
          var _this18 = this;

          if (!term.trim()) {
            // if not export term, return empty trials array.
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])([]);
          }

          return this.http.get("".concat(this.trialsUrl, "/?name=").concat(term)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (x) {
            return x.length ? _this18.log("Found trials matching \"".concat(term, "\"")) : _this18.log("No trials matching \"".concat(term, "\""));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('searchTrials', [])));
        }
        /* GET the existence of the replay in elasticsearch */

      }, {
        key: "getExistReplay",
        value: function getExistReplay(uuid, index) {
          var _this19 = this;

          var url = "".concat(this.trialsUrl, "/").concat(uuid, "/exist?index=").concat(index);
          return this.http.get(url).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (exist) {
            return _this19.log("Trial ".concat(uuid, " ").concat(exist ? 'exists' : 'does not exist', " in elasticsearch index ").concat(index));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError("Trial ".concat(uuid, " exist in elasticsearch index ").concat(index))));
        } //////// Save methods //////////

        /** POST: add a new trials to the server */

      }, {
        key: "createTrial",
        value: function createTrial(trial) {
          var _this20 = this;

          return this.http.post(this.trialsUrl, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (newTrial) {
            return _this20.log("added trial with id=".concat(newTrial.id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrial')));
        }
      }, {
        key: "createTrialMessage",
        value: function createTrialMessage(trialMessage) {
          var _this21 = this;

          return this.mqttService.publish('trial', JSON.stringify(trialMessage), {
            qos: 1
          }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this21.log("Sent message over bus to create trial.");
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('createTrialMessage')));
        }
        /** DELETE: delete the trials from the server */

      }, {
        key: "deleteTrial",
        value: function deleteTrial(trial) {
          var _this22 = this;

          var id = typeof trial === 'number' ? trial : trial.id;
          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http["delete"](url, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this22.log("Deleted trial id=".concat(id));
          }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(this.handleError('deleteTrial')));
        }
        /** PUT: update the trials on the server */

      }, {
        key: "updateTrial",
        value: function updateTrial(trial) {
          var _this23 = this;

          var id = trial.id;
          var url = "".concat(this.trialsUrl, "/").concat(id);
          return this.http.put(url, trial, this.httpOptions).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
            return _this23.log("Updated trial id=".concat(trial.id));
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
          var _this24 = this;

          if (trialExportMessage !== null) {
            return this.mqttService.publish('metadata/trial/export', JSON.stringify(trialExportMessage), {
              qos: 1
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["tap"])(function (_) {
              _this24.log("Exported trial using message bus.");
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
          var _this25 = this;

          var operation = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'operation';
          var result = arguments.length > 1 ? arguments[1] : undefined;
          return function (error) {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
            // TODO: better job of transforming error for user consumption

            _this25.log("".concat(operation, " failed: ").concat(error.message)); // Let the app keep running by returning an empty result.


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

  },

  /***/
  "./src/app/trial/trials/trials.component.ts":
  /*!**************************************************!*\
    !*** ./src/app/trial/trials/trials.component.ts ***!
    \**************************************************/

  /*! exports provided: TrialsComponent */

  /***/
  function srcAppTrialTrialsTrialsComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "TrialsComponent", function () {
      return TrialsComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_material_sort__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/material/sort */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/sort.js");
    /* harmony import */


    var _angular_material_table__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/material/table */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/table.js");
    /* harmony import */


    var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! @angular/material/paginator */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/paginator.js");
    /* harmony import */


    var _create_trial_create_trial_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../create-trial/create-trial.component */
    "./src/app/trial/create-trial/create-trial.component.ts");
    /* harmony import */


    var _update_trial_update_trial_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! ../update-trial/update-trial.component */
    "./src/app/trial/update-trial/update-trial.component.ts");
    /* harmony import */


    var _delete_trial_delete_trial_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ../delete-trial/delete-trial.component */
    "./src/app/trial/delete-trial/delete-trial.component.ts");
    /* harmony import */


    var _environments_environment__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! ../../../environments/environment */
    "./src/environments/environment.ts");
    /* harmony import */


    var _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! @angular/cdk/portal */
    "./node_modules/@angular/cdk/__ivy_ngcc__/fesm2015/portal.js");
    /* harmony import */


    var _progress_spinner_progress_spinner_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! ../../progress-spinner/progress-spinner.component */
    "./src/app/progress-spinner/progress-spinner.component.ts");
    /* harmony import */


    var rxjs_operators__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! rxjs/operators */
    "./node_modules/rxjs/_esm2015/operators/index.js");
    /* harmony import */


    var _trial_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! ../trial.service */
    "./src/app/trial/trial.service.ts");
    /* harmony import */


    var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! @angular/flex-layout */
    "./node_modules/@angular/flex-layout/__ivy_ngcc__/esm2015/flex-layout.js");
    /* harmony import */


    var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
    /*! @angular/material/dialog */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/dialog.js");
    /* harmony import */


    var _logging_logging_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
    /*! ../../logging/logging.service */
    "./src/app/logging/logging.service.ts");
    /* harmony import */


    var _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
    /*! @angular/cdk/overlay */
    "./node_modules/@angular/cdk/__ivy_ngcc__/fesm2015/overlay.js");
    /* harmony import */


    var ngx_mqtt__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
    /*! ngx-mqtt */
    "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js");
    /* harmony import */


    var _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
    /*! @angular/flex-layout/flex */
    "./node_modules/@angular/flex-layout/__ivy_ngcc__/esm2015/flex.js");
    /* harmony import */


    var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
    /*! @angular/material/form-field */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/form-field.js");
    /* harmony import */


    var _angular_material_input__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
    /*! @angular/material/input */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/input.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");
    /* harmony import */


    var _angular_material_icon__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
    /*! @angular/material/icon */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/icon.js");

    function TrialsComponent_th_11_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " ID ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_12_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r30 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r30.id, " ");
      }
    }

    function TrialsComponent_th_14_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Trial ID ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_15_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r31 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r31.trial_id, " ");
      }
    }

    function TrialsComponent_th_17_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Name ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_18_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r32 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r32.name, " ");
      }
    }

    function TrialsComponent_th_20_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Date ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_21_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r33 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r33.date, " ");
      }
    }

    function TrialsComponent_th_23_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Experimenter ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_24_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r34 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r34.experimenter, " ");
      }
    }

    function TrialsComponent_th_26_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Subjects ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_27_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r35 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r35.subjects, " ");
      }
    }

    function TrialsComponent_th_29_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Trial Number ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_30_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r36 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r36.trial_number, " ");
      }
    }

    function TrialsComponent_th_32_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Group Number ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_33_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r37 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r37.group_number, " ");
      }
    }

    function TrialsComponent_th_35_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Study Number ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_36_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r38 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r38.study_number, " ");
      }
    }

    function TrialsComponent_th_38_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Condition ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_39_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r39 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r39.condition, " ");
      }
    }

    function TrialsComponent_th_41_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Notes ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_42_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r40 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r40.notes, " ");
      }
    }

    function TrialsComponent_th_44_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Testbed Version ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_45_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r41 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r41.testbed_version, " ");
      }
    }

    function TrialsComponent_th_47_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Experiment ID ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_48_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var trial_r42 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", trial_r42.experiment !== null ? trial_r42.experiment.experiment_id : "NULL", " ");
      }
    }

    function TrialsComponent_th_50_Template(rf, ctx) {
      if (rf & 1) {
        var _r44 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 28);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "button", 29);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function TrialsComponent_th_50_Template_button_click_1_listener() {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r44);

          var ctx_r43 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

          return ctx_r43.openCreateTrialDialog();
        });

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "mat-icon", 30);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, "add_circle");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_td_51_Template(rf, ctx) {
      if (rf & 1) {
        var _r48 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 31);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "button", 32);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function TrialsComponent_td_51_Template_button_click_2_listener() {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r48);

          var i_r46 = ctx.index;
          var row_r45 = ctx.$implicit;

          var ctx_r47 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

          return ctx_r47.openUpdateTrialDialog(ctx_r47.paginator.pageIndex == 0 ? i_r46 : i_r46 + ctx_r47.paginator.pageIndex * ctx_r47.paginator.pageSize, row_r45.id, row_r45.trial_id, row_r45.name, row_r45.date, row_r45.experimenter, row_r45.subjects, row_r45.trial_number, row_r45.group_number, row_r45.study_number, row_r45.condition, row_r45.notes, row_r45.testbed_version, row_r45.experiment);
        });

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "mat-icon", 33);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4, "edit");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "button", 32);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function TrialsComponent_td_51_Template_button_click_5_listener() {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r48);

          var i_r46 = ctx.index;
          var row_r45 = ctx.$implicit;

          var ctx_r49 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

          return ctx_r49.openDeleteTrialDialog(ctx_r49.paginator.pageIndex == 0 ? i_r46 : i_r46 + ctx_r49.paginator.pageIndex * ctx_r49.paginator.pageSize, row_r45.id, row_r45.trial_id, row_r45.name, row_r45.date, row_r45.experimenter, row_r45.subjects, row_r45.trial_number, row_r45.group_number, row_r45.study_number, row_r45.condition, row_r45.notes, row_r45.testbed_version, row_r45.experiment);
        });

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-icon", 34);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7, "delete");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }
    }

    function TrialsComponent_tr_52_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "tr", 35);
      }
    }

    function TrialsComponent_tr_53_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "tr", 36);
      }
    }

    var _c0 = function _c0() {
      return [5, 10, 20];
    };

    var TrialsComponent = /*#__PURE__*/function () {
      function TrialsComponent(trialService, mediaObserver, createDialog, updateDialog, deleteDialog, loggingService, overlay, mqttService) {
        var _this26 = this;

        _classCallCheck(this, TrialsComponent);

        this.trialService = trialService;
        this.mediaObserver = mediaObserver;
        this.createDialog = createDialog;
        this.updateDialog = updateDialog;
        this.deleteDialog = deleteDialog;
        this.loggingService = loggingService;
        this.overlay = overlay;
        this.mqttService = mqttService;
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatTableDataSource"](this.trials);
        this.currentScreenWidth = '';
        this.trialCreatedSubscription = this.mqttService.observe('metadata/trial/created').subscribe(function (message) {
          var json = new TextDecoder('utf-8').decode(message.payload); // let trial = <Trial>JSON.parse(json);

          _this26.log('Trial created: ' + json);

          _this26.read();
        }); // this.flexMediaWatcher = mediaObserver.media$.subscribe((change: MediaChange) => {
        //   if (change.mqAlias !== this.currentScreenWidth) {
        //     this.currentScreenWidth = change.mqAlias;
        //     this.setupTable();
        //   }
        // });

        this.overlayRef = this.overlay.create({
          positionStrategy: this.overlay.position().global().centerHorizontally().centerVertically(),
          hasBackdrop: true
        });
        this.flexMediaWatcher = mediaObserver.asObservable().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_10__["filter"])(function (changes) {
          return changes.length > 0;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_10__["map"])(function (changes) {
          return changes[0];
        })).subscribe(function (change) {
          if (change.mqAlias !== _this26.currentScreenWidth) {
            _this26.currentScreenWidth = change.mqAlias;

            _this26.setupTable();
          }
        });
      }

      _createClass(TrialsComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          this.read();
        }
      }, {
        key: "ngOnDestroy",
        value: function ngOnDestroy() {
          this.flexMediaWatcher.unsubscribe();
          this.trialCreatedSubscription.unsubscribe();
        }
      }, {
        key: "setupTable",
        value: function setupTable() {
          this.displayedColumns = ['id', 'trial_id', 'name', 'date', 'experimenter', 'subjects', 'trial_number', 'group_number', 'study_number', 'condition', 'notes', 'testbed_version', 'experiment_id_experiments', 'actions'];

          if (this.currentScreenWidth === 'xs') {
            this.displayedColumns = ['name', 'experiment_id_experiments', 'actions'];
          }
        }
      }, {
        key: "applyFilter",
        value: function applyFilter(event) {
          var filterValue = event.target.value;
          this.dataSource.filter = filterValue.trim().toLowerCase();
        }
      }, {
        key: "showOverlay",
        value: function showOverlay() {
          var _this27 = this;

          this.overlayRef.attach(new _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_8__["ComponentPortal"](_progress_spinner_progress_spinner_component__WEBPACK_IMPORTED_MODULE_9__["ProgressSpinnerComponent"]));
          setTimeout(function () {
            _this27.overlayRef.detach();

            _this27.read();
          }, 3000);
        }
      }, {
        key: "create",
        value: function create(trial) {
          var _this28 = this;

          if (!trial) {
            return;
          }

          this.trialService.createTrial(trial).subscribe(function (t) {
            if (t) {
              _this28.log("Trial has been created: ".concat(t.id));

              _this28.trials.push(t);

              _this28.dataSource.data = _this28.trials;
              _this28.dataSource.sort = _this28.sort;
              _this28.dataSource.paginator = _this28.paginator;
            }
          });
          this.table.renderRows();
        }
      }, {
        key: "createMessage",
        value: function createMessage(trial) {
          if (!trial) {
            return;
          }

          this.trialService.createTrialMessage(trial).subscribe(function (_) {// this.log(`Trial message has been created using message bus.`);
            // this.showOverlay();
          }); // this.table.renderRows();
        }
      }, {
        key: "read",
        value: function read() {
          var _this29 = this;

          this.trialService.readTrials().subscribe(function (trials) {
            _this29.trials = trials;
            _this29.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatTableDataSource"](_this29.trials);
            _this29.dataSource.sort = _this29.sort;
            _this29.dataSource.paginator = _this29.paginator;
          });
        }
      }, {
        key: "update",
        value: function update(index, trial) {
          var _this30 = this;

          if (!trial) {
            return;
          }

          if (!trial.id) {
            return;
          }

          this.trialService.updateTrial(trial).subscribe(function (t) {
            if (t) {
              _this30.log("Trial has been updated: ".concat(t.id));

              _this30.trials[index] = t;
              _this30.dataSource.data = _this30.trials;
              _this30.dataSource.sort = _this30.sort;
              _this30.dataSource.paginator = _this30.paginator;
            }
          });
          this.table.renderRows();
        }
      }, {
        key: "delete",
        value: function _delete(index, trial) {
          var _this31 = this;

          if (!trial) {
            return;
          }

          this.trialService.deleteTrial(trial.id).subscribe(function (success) {
            if (success) {
              _this31.log("Trial has been deleted: ".concat(trial.id));

              _this31.dataSource.data.splice(index, 1);

              _this31.dataSource.data = _this31.trials;
              _this31.dataSource.sort = _this31.sort;
              _this31.dataSource.paginator = _this31.paginator;
            }
          });
          this.table.renderRows();
        }
      }, {
        key: "openCreateTrialDialog",
        value: function openCreateTrialDialog() {
          var _this32 = this;

          // const dialogRef = this.createDialog.open(CreateTrialComponent, {
          //   // width: '250px',
          //   // data: {name: this.name, animal: this.animal}
          // });
          //
          // dialogRef.afterClosed().subscribe(result => {
          //   this.create(result);
          // });
          var dialogRef = this.createDialog.open(_create_trial_create_trial_component__WEBPACK_IMPORTED_MODULE_4__["CreateTrialComponent"], {
            // width: '250px',
            // data: {name: this.name, animal: this.animal}
            panelClass: 'full-width-1-dialog'
          });
          dialogRef.afterClosed().subscribe(function (result) {
            if (!result) {
              return;
            }

            if (result.useMessageBus) {
              var trialMessage = _this32.trialService.generateTrialMessage(result, 'create', 'metadata-web', _environments_environment__WEBPACK_IMPORTED_MODULE_7__["environment"].testbedVersion, null, null, null);

              _this32.createMessage(trialMessage);
            } else {
              var trial = {
                id: -1,
                trial_id: result.trial_id,
                name: result.name,
                date: result.date,
                experimenter: result.experimenter,
                subjects: result.subjects,
                trial_number: result.trial_number,
                group_number: result.group_number,
                study_number: result.study_number,
                condition: result.condition,
                notes: result.notes,
                testbed_version: result.testbed_version,
                experiment: result.experiment
              };

              _this32.create(trial);
            }
          });
        }
      }, {
        key: "openUpdateTrialDialog",
        value: function openUpdateTrialDialog(index, id, trial_id, name, date, experimenter, subjects, trial_number, group_number, study_number, condition, notes, testbed_version, experiment) {
          var _this33 = this;

          var dialogRef = this.updateDialog.open(_update_trial_update_trial_component__WEBPACK_IMPORTED_MODULE_5__["UpdateTrialComponent"], {
            data: {
              id: id,
              trial_id: trial_id,
              name: name,
              date: date,
              experimenter: experimenter,
              subjects: subjects,
              trial_number: trial_number,
              group_number: group_number,
              study_number: study_number,
              condition: condition,
              notes: notes,
              testbed_version: testbed_version,
              experiment: experiment
            }
          });
          dialogRef.afterClosed().subscribe(function (result) {
            if (!result) {
              return;
            }

            _this33.update(index, result);
          });
        }
      }, {
        key: "openDeleteTrialDialog",
        value: function openDeleteTrialDialog(index, id, trial_id, name, date, experimenter, subjects, trial_number, group_number, study_number, condition, notes, testbed_version, experiment) {
          var _this34 = this;

          var dialogRef = this.deleteDialog.open(_delete_trial_delete_trial_component__WEBPACK_IMPORTED_MODULE_6__["DeleteTrialComponent"], {
            data: {
              id: id,
              trial_id: trial_id,
              name: name,
              date: date,
              experimenter: experimenter,
              trial_number: trial_number,
              group_number: group_number,
              study_number: study_number,
              condition: condition,
              subjects: subjects,
              notes: notes,
              testbed_version: testbed_version,
              experiment: experiment
            }
          });
          dialogRef.afterClosed().subscribe(function (result) {
            _this34["delete"](index, result);
          });
        }
      }, {
        key: "log",
        value: function log(message) {
          this.loggingService.add("TrialComponent: ".concat(message));
        }
      }]);

      return TrialsComponent;
    }();

    TrialsComponent.ɵfac = function TrialsComponent_Factory(t) {
      return new (t || TrialsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_trial_service__WEBPACK_IMPORTED_MODULE_11__["TrialService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__["MediaObserver"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_logging_logging_service__WEBPACK_IMPORTED_MODULE_14__["LoggingService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_15__["Overlay"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_16__["MqttService"]));
    };

    TrialsComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: TrialsComponent,
      selectors: [["app-trials"]],
      viewQuery: function TrialsComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatTable"], true);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstaticViewQuery"](_angular_material_sort__WEBPACK_IMPORTED_MODULE_1__["MatSort"], true);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstaticViewQuery"](_angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__["MatPaginator"], true);
        }

        if (rf & 2) {
          var _t;

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.table = _t.first);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.sort = _t.first);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.paginator = _t.first);
        }
      },
      decls: 57,
      vars: 8,
      consts: [[1, "container"], ["fxLayout", "column"], ["matInput", "", "placeholder", "Filter", "autocomplete", "off", 3, "keyup"], [1, "table-container"], ["mat-table", "", "matSort", "", 1, "mat-elevation-z8", 3, "dataSource"], ["matColumnDef", "id"], ["mat-header-cell", "", "mat-sort-header", "", 4, "matHeaderCellDef"], ["mat-cell", "", 4, "matCellDef"], ["matColumnDef", "trial_id"], ["matColumnDef", "name"], ["matColumnDef", "date"], ["matColumnDef", "experimenter"], ["matColumnDef", "subjects"], ["matColumnDef", "trial_number"], ["matColumnDef", "group_number"], ["matColumnDef", "study_number"], ["matColumnDef", "condition"], ["matColumnDef", "notes"], ["matColumnDef", "testbed_version"], ["matColumnDef", "experiment_id_experiments"], ["matColumnDef", "actions"], ["mat-header-cell", "", "class", "create-button", 4, "matHeaderCellDef"], ["mat-header-row", "", 4, "matHeaderRowDef", "matHeaderRowDefSticky"], ["mat-row", "", 4, "matRowDef", "matRowDefColumns"], [1, "no-results"], ["showFirstLastButtons", "", 3, "pageSizeOptions"], ["mat-header-cell", "", "mat-sort-header", ""], ["mat-cell", ""], ["mat-header-cell", "", 1, "create-button"], ["mat-icon-button", "", 3, "click"], ["aria-label", "Create"], [1, "mat-cell-buttons"], ["mat-icon-button", "", "color", "accent", 3, "click"], ["aria-label", "Edit"], ["aria-label", "Delete"], ["mat-header-row", ""], ["mat-row", ""]],
      template: function TrialsComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "h2");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "Trials");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "mat-form-field");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6, "Filter Table");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "input", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("keyup", function TrialsComponent_Template_input_keyup_7_listener($event) {
            return ctx.applyFilter($event);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](9, "table", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](10, 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](11, TrialsComponent_th_11_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](12, TrialsComponent_td_12_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](13, 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](14, TrialsComponent_th_14_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](15, TrialsComponent_td_15_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](16, 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](17, TrialsComponent_th_17_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](18, TrialsComponent_td_18_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](19, 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](20, TrialsComponent_th_20_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](21, TrialsComponent_td_21_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](22, 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](23, TrialsComponent_th_23_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](24, TrialsComponent_td_24_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](25, 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](26, TrialsComponent_th_26_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](27, TrialsComponent_td_27_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](28, 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](29, TrialsComponent_th_29_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](30, TrialsComponent_td_30_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](31, 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](32, TrialsComponent_th_32_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](33, TrialsComponent_td_33_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](34, 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](35, TrialsComponent_th_35_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](36, TrialsComponent_td_36_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](37, 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](38, TrialsComponent_th_38_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](39, TrialsComponent_td_39_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](40, 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](41, TrialsComponent_th_41_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](42, TrialsComponent_td_42_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](43, 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](44, TrialsComponent_th_44_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](45, TrialsComponent_td_45_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](46, 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](47, TrialsComponent_th_47_Template, 2, 0, "th", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](48, TrialsComponent_td_48_Template, 2, 1, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](49, 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](50, TrialsComponent_th_50_Template, 4, 0, "th", 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](51, TrialsComponent_td_51_Template, 8, 0, "td", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](52, TrialsComponent_tr_52_Template, 1, 0, "tr", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](53, TrialsComponent_tr_53_Template, 1, 0, "tr", 23);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](54, "div", 24);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](55, " No results ");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](56, "mat-paginator", 25);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("dataSource", ctx.dataSource);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](43);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("matHeaderRowDef", ctx.displayedColumns)("matHeaderRowDefSticky", true);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("matRowDefColumns", ctx.displayedColumns);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("display", ctx.dataSource.data.length == 0 ? "" : "none");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("pageSizeOptions", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](7, _c0));
        }
      },
      directives: [_angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_17__["DefaultLayoutDirective"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__["MatFormField"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__["MatLabel"], _angular_material_input__WEBPACK_IMPORTED_MODULE_19__["MatInput"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatTable"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_1__["MatSort"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatColumnDef"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatHeaderCellDef"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatCellDef"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatHeaderRowDef"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatRowDef"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__["MatPaginator"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatHeaderCell"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_1__["MatSortHeader"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatCell"], _angular_material_button__WEBPACK_IMPORTED_MODULE_20__["MatButton"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_21__["MatIcon"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatHeaderRow"], _angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatRow"]],
      styles: [".table-container[_ngcontent-%COMP%] {\n  overflow: auto;\n}\n\ntable[_ngcontent-%COMP%] {\n  width: 100%;\n}\n\nth.mat-sort-header-sorted[_ngcontent-%COMP%] {\n  color: black;\n}\n\n.container[_ngcontent-%COMP%] {\n  margin: 2em;\n}\n\n.no-results[_ngcontent-%COMP%] {\n  display: flex;\n  justify-content: center;\n  padding: 14px;\n  font-size: 14px;\n  font-style: italic;\n}\n\n.create-button[_ngcontent-%COMP%] {\n  text-align: center;\n}\n\n.mat-cell-buttons[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n}\n\n.mat-cell[_ngcontent-%COMP%] {\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  max-width: 0;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvdHJpYWwvdHJpYWxzL0M6XFxVc2Vyc1xcQ2hhcmxpZSBLYXBvcG91bG9zXFxQcm9qZWN0c1xcQXB0aW1hXFx0ZXN0YmVkXFxtZXRhZGF0YVxcbWV0YWRhdGEtd2ViL3NyY1xcYXBwXFx0cmlhbFxcdHJpYWxzXFx0cmlhbHMuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3RyaWFsL3RyaWFscy90cmlhbHMuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFFRSxjQUFjO0FDQWhCOztBREdBO0VBQ0UsV0FBVztBQ0FiOztBREdBO0VBQ0UsWUFBWTtBQ0FkOztBREdBO0VBQ0UsV0FBVztBQ0FiOztBREdBO0VBQ0UsYUFBYTtFQUNiLHVCQUF1QjtFQUN2QixhQUFhO0VBQ2IsZUFBZTtFQUNmLGtCQUFrQjtBQ0FwQjs7QURHQTtFQUNFLGtCQUFrQjtBQ0FwQjs7QURHQTtFQUNFLGFBQWE7RUFDYixtQkFBbUI7RUFDbkIsOEJBQThCO0FDQWhDOztBREdBO0VBQ0UsbUJBQW1CO0VBQ25CLGdCQUFnQjtFQUNoQix1QkFBdUI7RUFDdkIsWUFBWTtBQ0FkIiwiZmlsZSI6InNyYy9hcHAvdHJpYWwvdHJpYWxzL3RyaWFscy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi50YWJsZS1jb250YWluZXIge1xyXG4gIC8vbWF4LWhlaWdodDogMzAwcHg7XHJcbiAgb3ZlcmZsb3c6IGF1dG87XHJcbn1cclxuXHJcbnRhYmxlIHtcclxuICB3aWR0aDogMTAwJTtcclxufVxyXG5cclxudGgubWF0LXNvcnQtaGVhZGVyLXNvcnRlZCB7XHJcbiAgY29sb3I6IGJsYWNrO1xyXG59XHJcblxyXG4uY29udGFpbmVyIHtcclxuICBtYXJnaW46IDJlbTtcclxufVxyXG5cclxuLm5vLXJlc3VsdHMge1xyXG4gIGRpc3BsYXk6IGZsZXg7XHJcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XHJcbiAgcGFkZGluZzogMTRweDtcclxuICBmb250LXNpemU6IDE0cHg7XHJcbiAgZm9udC1zdHlsZTogaXRhbGljO1xyXG59XHJcblxyXG4uY3JlYXRlLWJ1dHRvbiB7XHJcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xyXG59XHJcblxyXG4ubWF0LWNlbGwtYnV0dG9ucyB7XHJcbiAgZGlzcGxheTogZmxleDtcclxuICBmbGV4LWRpcmVjdGlvbjogcm93O1xyXG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2VlbjtcclxufVxyXG5cclxuLm1hdC1jZWxsIHtcclxuICB3aGl0ZS1zcGFjZTogbm93cmFwO1xyXG4gIG92ZXJmbG93OiBoaWRkZW47XHJcbiAgdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XHJcbiAgbWF4LXdpZHRoOiAwO1xyXG59XHJcbiIsIi50YWJsZS1jb250YWluZXIge1xuICBvdmVyZmxvdzogYXV0bztcbn1cblxudGFibGUge1xuICB3aWR0aDogMTAwJTtcbn1cblxudGgubWF0LXNvcnQtaGVhZGVyLXNvcnRlZCB7XG4gIGNvbG9yOiBibGFjaztcbn1cblxuLmNvbnRhaW5lciB7XG4gIG1hcmdpbjogMmVtO1xufVxuXG4ubm8tcmVzdWx0cyB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBwYWRkaW5nOiAxNHB4O1xuICBmb250LXNpemU6IDE0cHg7XG4gIGZvbnQtc3R5bGU6IGl0YWxpYztcbn1cblxuLmNyZWF0ZS1idXR0b24ge1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbi5tYXQtY2VsbC1idXR0b25zIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IHJvdztcbiAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuO1xufVxuXG4ubWF0LWNlbGwge1xuICB3aGl0ZS1zcGFjZTogbm93cmFwO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0ZXh0LW92ZXJmbG93OiBlbGxpcHNpcztcbiAgbWF4LXdpZHRoOiAwO1xufVxuIl19 */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](TrialsComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-trials',
          templateUrl: './trials.component.html',
          styleUrls: ['./trials.component.scss']
        }]
      }], function () {
        return [{
          type: _trial_service__WEBPACK_IMPORTED_MODULE_11__["TrialService"]
        }, {
          type: _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__["MediaObserver"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"]
        }, {
          type: _logging_logging_service__WEBPACK_IMPORTED_MODULE_14__["LoggingService"]
        }, {
          type: _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_15__["Overlay"]
        }, {
          type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_16__["MqttService"]
        }];
      }, {
        table: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"],
          args: [_angular_material_table__WEBPACK_IMPORTED_MODULE_2__["MatTable"]]
        }],
        sort: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"],
          args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_1__["MatSort"], {
            "static": true
          }]
        }],
        paginator: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"],
          args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__["MatPaginator"], {
            "static": true
          }]
        }]
      });
    })();
    /***/

  },

  /***/
  "./src/app/trial/update-trial/update-trial.component.ts":
  /*!**************************************************************!*\
    !*** ./src/app/trial/update-trial/update-trial.component.ts ***!
    \**************************************************************/

  /*! exports provided: UpdateTrialComponent */

  /***/
  function srcAppTrialUpdateTrialUpdateTrialComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "UpdateTrialComponent", function () {
      return UpdateTrialComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");
    /* harmony import */


    var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! @angular/material/dialog */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/dialog.js");
    /* harmony import */


    var uuid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! uuid */
    "./node_modules/uuid/dist/esm-browser/index.js");
    /* harmony import */


    var _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../../experiment/experiment.service */
    "./src/app/experiment/experiment.service.ts");
    /* harmony import */


    var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/material/form-field */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/form-field.js");
    /* harmony import */


    var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! @angular/material/input */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/input.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");
    /* harmony import */


    var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! @angular/material/icon */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/icon.js");
    /* harmony import */


    var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! @angular/material/datepicker */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/datepicker.js");
    /* harmony import */


    var _angular_material_select__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! @angular/material/select */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/select.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _angular_material_core__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! @angular/material/core */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/core.js");

    function UpdateTrialComponent_mat_option_78_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "mat-option", 23);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var experiment_r2 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("value", experiment_r2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", experiment_r2.name, " ");
      }
    }

    var UpdateTrialComponent = /*#__PURE__*/function () {
      function UpdateTrialComponent(formBuilder, dialogRef, experimentService, data) {
        _classCallCheck(this, UpdateTrialComponent);

        this.formBuilder = formBuilder;
        this.dialogRef = dialogRef;
        this.experimentService = experimentService;
        this.data = data;
        this.updateTrialForm = this.formBuilder.group({
          id: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          trial_id: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          date: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experimenter: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          subjects: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          trial_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          group_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          study_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          condition: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          notes: [''],
          testbed_version: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required],
          experiment: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_1__["Validators"].required]
        });
        this.uuidPattern = new RegExp(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
      }

      _createClass(UpdateTrialComponent, [{
        key: "readExperiments",
        value: function readExperiments() {
          var _this35 = this;

          this.experimentService.readExperiments().subscribe(function (experiments) {
            _this35.experiments = experiments;
          });
        }
      }, {
        key: "onUpdateClick",
        value: function onUpdateClick() {
          var dialogResult = this.updateTrialForm.value;
          var subjectsText = this.updateTrialForm.get('subjects').value;

          if (subjectsText !== '') {
            dialogResult.subjects = subjectsText.split(/[\r\n]+/);
          } else {
            dialogResult.subjects = [];
          }

          var notesText = this.updateTrialForm.get('notes').value;

          if (notesText !== '') {
            dialogResult.notes = notesText.split(/[\r\n]+/);
          } else {
            dialogResult.notes = [];
          }

          this.dialogRef.close(dialogResult);
        }
      }, {
        key: "onCancelClick",
        value: function onCancelClick() {
          this.dialogRef.close();
        }
      }, {
        key: "onGenerateUUIDClick",
        value: function onGenerateUUIDClick() {
          this.updateTrialForm.patchValue({
            trial_id: Object(uuid__WEBPACK_IMPORTED_MODULE_3__["v4"])()
          });
        }
      }, {
        key: "ngOnInit",
        value: function ngOnInit() {
          this.readExperiments();
          this.updateTrialForm.setValue({
            id: this.data.id,
            trial_id: this.data.trial_id,
            name: this.data.name,
            date: this.data.date,
            experimenter: this.data.experimenter,
            subjects: this.data.subjects.length > 0 ? this.data.subjects.join('\r\n') : this.data.subjects,
            trial_number: this.data.trial_number,
            group_number: this.data.group_number,
            study_number: this.data.study_number,
            condition: this.data.condition,
            notes: this.data.notes.length > 0 ? this.data.notes.join('\r\n') : this.data.notes,
            testbed_version: this.data.testbed_version,
            experiment: this.data.experiment
          });
        }
      }, {
        key: "compareFnExperiments",
        value: function compareFnExperiments(e1, e2) {
          return e1 && e2 ? e1.id === e2.id : e1 === e2;
        }
      }]);

      return UpdateTrialComponent;
    }();

    UpdateTrialComponent.ɵfac = function UpdateTrialComponent_Factory(t) {
      return new (t || UpdateTrialComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__["ExperimentService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]));
    };

    UpdateTrialComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: UpdateTrialComponent,
      selectors: [["app-update-trial"]],
      decls: 86,
      vars: 8,
      consts: [["mat-dialog-title", ""], ["mat-dialog-content", "", "layout", "row", "layout-align", "center center", 3, "formGroup"], ["appearance", "fill"], ["matInput", "", "formControlName", "trial_id", "placeholder", "UUID", "required", "", "autocomplete", "off", 3, "pattern"], ["mat-icon-button", "", "matSuffix", "", 3, "click"], ["aria-label", "UUID"], ["matInput", "", "formControlName", "name", "placeholder", "Name", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "date", "required", "", "autocomplete", "off", 3, "matDatepicker"], ["matSuffix", "", 3, "for"], ["date", ""], ["matInput", "", "formControlName", "experimenter", "placeholder", "Experimenter", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "subjects", "placeholder", "Subjects...", "autocomplete", "off"], ["matInput", "", "formControlName", "trial_number", "placeholder", "Trial Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "group_number", "placeholder", "Trial Group Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "study_number", "placeholder", "Trial Study Number", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "condition", "placeholder", "Trial Condition", "required", "", "autocomplete", "off"], ["matInput", "", "formControlName", "notes", "placeholder", "Notes...", "autocomplete", "off"], ["matInput", "", "formControlName", "testbed_version", "placeholder", "Testbed Version", "required", "", "autocomplete", "off"], ["formControlName", "experiment", "placeholder", "Experiment", "required", "", 3, "compareWith"], [3, "value", 4, "ngFor", "ngForOf"], ["mat-dialog-actions", "", "align", "end"], ["mat-raised-button", "", "color", "accent", 3, "click"], ["mat-raised-button", "", "color", "primary", 3, "disabled", "click"], [3, "value"]],
      template: function UpdateTrialComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "h1", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, "Update");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "fieldset");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "legend");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](8, "Trial UUID");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "input", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11, "Please use a valid UUID.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "button", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function UpdateTrialComponent_Template_button_click_12_listener() {
            return ctx.onGenerateUUIDClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "mat-icon", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](14, "autorenew");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](16, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](17, "Trial Name");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](18, "input", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](19, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](20, "Name is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](21, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](23, "Trial Date");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](24, "input", 7);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](25, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](26, "Date is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](27, "mat-datepicker-toggle", 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](28, "mat-datepicker", null, 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](31, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](32, "Trial Experimenter");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](33, "input", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](34, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](35, "Experimenter is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](36, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](37, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](38, "Trial Subjects");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](39, "textarea", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](40, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](41, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](42, "Trial Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](43, "input", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](44, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](45, "Trial Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](46, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](47, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](48, "Trial Group Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](49, "input", 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](50, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](51, "Trial Group Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](52, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](53, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](54, "Trial Study Number");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](55, "input", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](56, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](57, "Trial Study Number is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](58, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](59, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](60, "Trial Condition");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](61, "input", 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](62, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](63, "Trial Condition is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](64, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](65, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](66, "Trial Notes");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](67, "textarea", 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](68, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](69, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](70, "Trial Testbed Version");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](71, "input", 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](72, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](73, "Testbed version is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](74, "mat-form-field", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](75, "mat-label");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](76, "Trial Experiment");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](77, "mat-select", 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](78, UpdateTrialComponent_mat_option_78_Template, 2, 2, "mat-option", 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](79, "mat-error");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](80, "Experiment is required.");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](81, "div", 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](82, "button", 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function UpdateTrialComponent_Template_button_click_82_listener() {
            return ctx.onCancelClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](83, "Cancel");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](84, "button", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function UpdateTrialComponent_Template_button_click_84_listener() {
            return ctx.onUpdateClick();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](85, "Update");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          var _r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](29);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.updateTrialForm);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("Trial: ", ctx.data.id, "");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("pattern", ctx.uuidPattern);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("matDatepicker", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("for", _r0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](50);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("compareWith", ctx.compareFnExperiments);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.experiments);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", !ctx.updateTrialForm.valid);
        }
      },
      directives: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogTitle"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogContent"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatusGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormGroupDirective"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatFormField"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatLabel"], _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInput"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["DefaultValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormControlName"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["RequiredValidator"], _angular_forms__WEBPACK_IMPORTED_MODULE_1__["PatternValidator"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatError"], _angular_material_button__WEBPACK_IMPORTED_MODULE_7__["MatButton"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatSuffix"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIcon"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerInput"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerToggle"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepicker"], _angular_material_select__WEBPACK_IMPORTED_MODULE_10__["MatSelect"], _angular_common__WEBPACK_IMPORTED_MODULE_11__["NgForOf"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogActions"], _angular_material_core__WEBPACK_IMPORTED_MODULE_12__["MatOption"]],
      styles: ["mat-form-field[_ngcontent-%COMP%] {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvdHJpYWwvdXBkYXRlLXRyaWFsL0M6XFxVc2Vyc1xcQ2hhcmxpZSBLYXBvcG91bG9zXFxQcm9qZWN0c1xcQXB0aW1hXFx0ZXN0YmVkXFxtZXRhZGF0YVxcbWV0YWRhdGEtd2ViL3NyY1xcYXBwXFx0cmlhbFxcdXBkYXRlLXRyaWFsXFx1cGRhdGUtdHJpYWwuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3RyaWFsL3VwZGF0ZS10cmlhbC91cGRhdGUtdHJpYWwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxXQUFXO0FDQ2IiLCJmaWxlIjoic3JjL2FwcC90cmlhbC91cGRhdGUtdHJpYWwvdXBkYXRlLXRyaWFsLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsibWF0LWZvcm0tZmllbGQge1xyXG4gIHdpZHRoOiAxMDAlO1xyXG59XHJcbiIsIm1hdC1mb3JtLWZpZWxkIHtcbiAgd2lkdGg6IDEwMCU7XG59XG4iXX0= */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](UpdateTrialComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-update-trial',
          templateUrl: './update-trial.component.html',
          styleUrls: ['./update-trial.component.scss']
        }]
      }], function () {
        return [{
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_1__["FormBuilder"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"]
        }, {
          type: _experiment_experiment_service__WEBPACK_IMPORTED_MODULE_4__["ExperimentService"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]]
          }]
        }];
      }, null);
    })();
    /***/

  }
}]);
//# sourceMappingURL=trial-trial-module-es5.js.map