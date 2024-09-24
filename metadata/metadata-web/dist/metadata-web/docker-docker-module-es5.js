function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["docker-docker-module"], {
  /***/
  "./src/app/docker/docker-routing.module.ts":
  /*!*************************************************!*\
    !*** ./src/app/docker/docker-routing.module.ts ***!
    \*************************************************/

  /*! exports provided: DockerRoutingModule */

  /***/
  function srcAppDockerDockerRoutingModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "DockerRoutingModule", function () {
      return DockerRoutingModule;
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


    var _docker_docker_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./docker/docker.component */
    "./src/app/docker/docker/docker.component.ts");

    var routes = [{
      path: '',
      component: _docker_docker_component__WEBPACK_IMPORTED_MODULE_2__["DockerComponent"]
    }];

    var DockerRoutingModule = function DockerRoutingModule() {
      _classCallCheck(this, DockerRoutingModule);
    };

    DockerRoutingModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: DockerRoutingModule
    });
    DockerRoutingModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function DockerRoutingModule_Factory(t) {
        return new (t || DockerRoutingModule)();
      },
      imports: [[_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)], _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](DockerRoutingModule, {
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](DockerRoutingModule, [{
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
  "./src/app/docker/docker.module.ts":
  /*!*****************************************!*\
    !*** ./src/app/docker/docker.module.ts ***!
    \*****************************************/

  /*! exports provided: DockerModule */

  /***/
  function srcAppDockerDockerModuleTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "DockerModule", function () {
      return DockerModule;
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


    var _docker_docker_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ./docker/docker.component */
    "./src/app/docker/docker/docker.component.ts");
    /* harmony import */


    var _docker_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ./docker-routing.module */
    "./src/app/docker/docker-routing.module.ts");
    /* harmony import */


    var _dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! ../dashboard/dashboard.module */
    "./src/app/dashboard/dashboard.module.ts");
    /* harmony import */


    var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/flex-layout */
    "./node_modules/@angular/flex-layout/__ivy_ngcc__/esm2015/flex-layout.js");
    /* harmony import */


    var _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! ../angular-material/angular-material-module */
    "./src/app/angular-material/angular-material-module.ts");
    /* harmony import */


    var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! @angular/forms */
    "./node_modules/@angular/forms/__ivy_ngcc__/fesm2015/forms.js");

    var DockerModule = function DockerModule() {
      _classCallCheck(this, DockerModule);
    };

    DockerModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: DockerModule
    });
    DockerModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      factory: function DockerModule_Factory(t) {
        return new (t || DockerModule)();
      },
      imports: [[_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _docker_routing_module__WEBPACK_IMPORTED_MODULE_3__["DockerRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_6__["AngularMaterialModule"], _dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_4__["DashboardModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["ExtendedModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["FlexModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_7__["FormsModule"]]]
    });

    (function () {
      (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](DockerModule, {
        declarations: [_docker_docker_component__WEBPACK_IMPORTED_MODULE_2__["DockerComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _docker_routing_module__WEBPACK_IMPORTED_MODULE_3__["DockerRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_6__["AngularMaterialModule"], _dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_4__["DashboardModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["ExtendedModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["FlexModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_7__["FormsModule"]]
      });
    })();
    /*@__PURE__*/


    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](DockerModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          declarations: [_docker_docker_component__WEBPACK_IMPORTED_MODULE_2__["DockerComponent"]],
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _docker_routing_module__WEBPACK_IMPORTED_MODULE_3__["DockerRoutingModule"], _angular_material_angular_material_module__WEBPACK_IMPORTED_MODULE_6__["AngularMaterialModule"], _dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_4__["DashboardModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["ExtendedModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["FlexModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_7__["FormsModule"]]
        }]
      }], null, null);
    })();
    /***/

  },

  /***/
  "./src/app/docker/docker/docker.component.ts":
  /*!***************************************************!*\
    !*** ./src/app/docker/docker/docker.component.ts ***!
    \***************************************************/

  /*! exports provided: DockerComponent */

  /***/
  function srcAppDockerDockerDockerComponentTs(module, __webpack_exports__, __webpack_require__) {
    "use strict";

    __webpack_require__.r(__webpack_exports__);
    /* harmony export (binding) */


    __webpack_require__.d(__webpack_exports__, "DockerComponent", function () {
      return DockerComponent;
    });
    /* harmony import */


    var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
    /*! @angular/core */
    "./node_modules/@angular/core/__ivy_ngcc__/fesm2015/core.js");
    /* harmony import */


    var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
    /*! rxjs */
    "./node_modules/rxjs/_esm2015/index.js");
    /* harmony import */


    var _docker_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
    /*! ../docker.service */
    "./src/app/docker/docker.service.ts");
    /* harmony import */


    var ngx_mqtt__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
    /*! ngx-mqtt */
    "./node_modules/ngx-mqtt/__ivy_ngcc__/fesm2015/ngx-mqtt.js");
    /* harmony import */


    var _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
    /*! @angular/flex-layout/flex */
    "./node_modules/@angular/flex-layout/__ivy_ngcc__/esm2015/flex.js");
    /* harmony import */


    var _angular_material_card__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
    /*! @angular/material/card */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/card.js");
    /* harmony import */


    var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
    /*! @angular/common */
    "./node_modules/@angular/common/__ivy_ngcc__/fesm2015/common.js");
    /* harmony import */


    var _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
    /*! @angular/flex-layout/extended */
    "./node_modules/@angular/flex-layout/__ivy_ngcc__/esm2015/extended.js");
    /* harmony import */


    var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
    /*! @angular/material/icon */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/icon.js");
    /* harmony import */


    var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
    /*! @angular/material/tooltip */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/tooltip.js");
    /* harmony import */


    var _angular_material_list__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
    /*! @angular/material/list */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/list.js");
    /* harmony import */


    var _angular_material_divider__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
    /*! @angular/material/divider */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/divider.js");
    /* harmony import */


    var _angular_material_button__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
    /*! @angular/material/button */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/button.js");
    /* harmony import */


    var _angular_material_core__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
    /*! @angular/material/core */
    "./node_modules/@angular/material/__ivy_ngcc__/fesm2015/core.js");

    var _c0 = ["containerList"];

    function DockerComponent_mat_list_option_19_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "mat-list-option", 24);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "mat-icon", 25);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "lens");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var item_r8 = ctx.$implicit;

        var ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("value", item_r8.value)("selected", ctx_r1.isSelected(item_r8.value.Id));

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("color", item_r8.value.State === "running" ? "primary" : "warn");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("matTooltip", item_r8.value.Status);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](item_r8.value.Names[0].substring(1));

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate2"]("CPU: ", item_r8.value.State === "running" ? ctx_r1.calcCpuPercent(item_r8.value.Id) + "%" : "0", " MEM: ", item_r8.value.State === "running" ? ctx_r1.calcMemPercent(item_r8.value.Id) + "%" : "0", "");
      }
    }

    function DockerComponent_p_39_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "p", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "span", 28);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "Id: ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r2.selectedContainer.Id);
      }
    }

    function DockerComponent_p_40_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "p", 27);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "span", 28);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "Image: ");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r3.selectedContainer.Image);
      }
    }

    function DockerComponent_div_41_div_2_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var line_r10 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", line_r10, " ");
      }
    }

    function DockerComponent_div_41_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 29);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 30);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DockerComponent_div_41_div_2_Template, 2, 1, "div", 22);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r4.selectedContainerLog);
      }
    }

    function DockerComponent_mat_list_item_69_Template(rf, ctx) {
      if (rf & 1) {
        var _r13 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "mat-list-item");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 26);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "button", 31);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_mat_list_item_69_Template_button_click_3_listener() {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r13);

          var item_r11 = ctx.$implicit;

          var ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

          return ctx_r12.agentDown(item_r11);
        });

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "mat-icon", 32);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "stop");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "button", 31);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_mat_list_item_69_Template_button_click_6_listener() {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r13);

          var item_r11 = ctx.$implicit;

          var ctx_r14 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

          return ctx_r14.agentUp(item_r11);
        });

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "mat-icon", 33);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](8, "play_arrow");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var item_r11 = ctx.$implicit;

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](item_r11);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate1"]("matTooltip", "Down ", item_r11, "");

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate1"]("matTooltip", "Up ", item_r11, "");
      }
    }

    function DockerComponent_div_72_Template(rf, ctx) {
      if (rf & 1) {
        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 34);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      }

      if (rf & 2) {
        var ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

        _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx_r7.agentLog, " ");
      }
    }

    var DockerComponent = /*#__PURE__*/function () {
      function DockerComponent(dockerService, // private agentService: AgentService,
      mqttService) {
        var _this = this;

        _classCallCheck(this, DockerComponent);

        this.dockerService = dockerService;
        this.mqttService = mqttService;
        this.containers = {};
        this.statistics = {};
        this.selectedContainer = null;
        this.selectedContainerLog = [];
        this.agents = [];
        this.agentLog = ''; // 'b1124ca78a7a Extracting [==================================================>]  40.41MB/40.41MB';

        this.metadataAgentLogSubscription = this.mqttService.observe('metadata/agent/log').subscribe(function (message) {
          var output = new TextDecoder('utf-8').decode(message.payload); // const logMessage = JSON.parse(output);
          // const decodedString = atob(logMessage.encoded_string);

          console.log(output);
          _this.agentLog = output;
        });
      }

      _createClass(DockerComponent, [{
        key: "ngOnInit",
        value: function ngOnInit() {
          var _this2 = this;

          this.containerStatusTimer();
          this.agentList();
          this.dockerOnlineSubscription = this.dockerService.isDockerOnline.subscribe(function (isOnline) {
            return _this2.dockerOnline = isOnline;
          });
        }
      }, {
        key: "ngOnDestroy",
        value: function ngOnDestroy() {
          this.dockerOnlineSubscription.unsubscribe();
          this.metadataAgentLogSubscription.unsubscribe();
        }
      }, {
        key: "containerStatusTimer",
        value: function containerStatusTimer() {
          var _this3 = this;

          var source = Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["timer"])(0, 10000);
          source.subscribe(function (val) {
            _this3.ping();

            _this3.containerList();
          });
        }
      }, {
        key: "ping",
        value: function ping() {
          var _this4 = this;

          this.dockerService.ping().subscribe(function (online) {
            _this4.dockerOnline = online;
          });
        }
      }, {
        key: "containerList",
        value: function containerList() {
          var _this5 = this;

          this.dockerService.containerList().subscribe(function (containers) {
            // Remove any old containers that are not in new list
            var currentContainerIds = Object.keys(_this5.containers);
            currentContainerIds.forEach(function (id) {
              if (containers.findIndex(function (c) {
                return c.Id === id;
              }) === -1) {
                delete _this5.containers[id];
                delete _this5.statistics[id];
              }
            }); // Update container list

            containers.forEach(function (container) {
              _this5.containers[container.Id] = container;

              if (_this5.selectedContainer && _this5.selectedContainer.Id === container.Id) {
                _this5.selectedContainer = container;
              } // Stats


              _this5.containerStats(container.Id);
            });
          });
        }
      }, {
        key: "agentList",
        value: function agentList() {
          var _this6 = this;

          this.dockerService.agentList().subscribe(function (agents) {
            console.log('agents: ' + agents);
            _this6.agents = agents;
          });
        }
      }, {
        key: "containerLog",
        value: function containerLog(Id) {
          var _this7 = this;

          this.dockerService.containerLog(Id).subscribe(function (log) {
            _this7.selectedContainerLog = log;
          });
        }
      }, {
        key: "onSelectionChange",
        value: function onSelectionChange($event) {
          var _a;

          this.selectedContainer = (_a = $event.option) === null || _a === void 0 ? void 0 : _a.value;
          this.containerLog(this.selectedContainer.Id);
        }
      }, {
        key: "isSelected",
        value: function isSelected(Id) {
          if (this.selectedContainer) {
            return this.selectedContainer.Id === Id;
          }
        }
      }, {
        key: "compare",
        value: function compare(c1, c2) {
          return c1 && c2 && c1.Id === c2.Id;
        }
      }, {
        key: "startContainer",
        value: function startContainer(id) {
          var _this8 = this;

          this.agentLog = '';
          this.dockerService.startContainer(id).subscribe(function (container) {
            _this8.selectedContainer = container;
            _this8.containers[id] = container;
          });
        }
      }, {
        key: "stopContainer",
        value: function stopContainer(id) {
          var _this9 = this;

          this.agentLog = '';
          this.dockerService.stopContainer(id).subscribe(function (container) {
            _this9.selectedContainer = container;
            _this9.containers[id] = container;
          });
        }
      }, {
        key: "containerLogDownload",
        value: function containerLogDownload(Id) {
          this.dockerService.containerLogDownload(Id).subscribe(function (response) {
            var dataType = response.type;
            var binaryData = [];
            binaryData.push(response);
            var downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {
              type: dataType
            }));
            downloadLink.setAttribute('download', "".concat(Id, ".txt"));
            document.body.appendChild(downloadLink);
            downloadLink.click();
          });
        }
      }, {
        key: "containerLogsDownload",
        value: function containerLogsDownload() {
          this.dockerService.containerLogsDownload().subscribe(function (response) {
            var dataType = response.type;
            var binaryData = [];
            binaryData.push(response);
            var downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {
              type: dataType
            }));
            downloadLink.setAttribute('download', 'dockerlogs.zip');
            document.body.appendChild(downloadLink);
            downloadLink.click();
          });
        }
      }, {
        key: "containerStats",
        value: function containerStats(Id) {
          var _this10 = this;

          this.dockerService.containerStats(Id).subscribe(function (stats) {
            _this10.statistics[Id] = stats[0];
          });
        }
      }, {
        key: "calcCpuPercent",
        value: function calcCpuPercent(Id) {
          // cpu_delta = cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage
          // system_cpu_delta = cpu_stats.system_cpu_usage - precpu_stats.system_cpu_usage
          // number_cpus = length(cpu_stats.cpu_usage.percpu_usage) or cpu_stats.online_cpus
          // (cpu_delta / system_cpu_delta) * number_cpus * 100.0
          var stats = this.statistics[Id];

          if (stats) {
            var cpu_delta = stats.cpu_stats.cpu_usage.total_usage - stats.precpu_stats.cpu_usage.total_usage;
            var system_cpu_delta = (stats.cpu_stats.system_cpu_usage ? stats.cpu_stats.system_cpu_usage : 0) - (stats.precpu_stats.system_cpu_usage ? stats.precpu_stats.system_cpu_usage : 0);
            var number_cpus = stats.cpu_stats.online_cpus ? stats.cpu_stats.online_cpus : stats.cpu_stats.cpu_usage.percpu_usage ? stats.cpu_stats.cpu_usage.percpu_usage.length : 1;
            return (cpu_delta / system_cpu_delta * (number_cpus * 100.0)).toFixed(2);
          }
        }
      }, {
        key: "calcMemPercent",
        value: function calcMemPercent(Id) {
          // used_memory = memory_stats.usage - memory_stats.stats.cache
          // available_memory = memory_stats.limit
          // (used_memory / available_memory) * 100.0
          var stats = this.statistics[Id];

          if (stats) {
            var used_memory = stats.memory_stats.usage ? stats.memory_stats.usage : 0 - stats.memory_stats.stats ? stats.memory_stats.stats.cache ? stats.memory_stats.stats.cache : 0 : 0;
            var available_memory = stats.memory_stats.limit;
            return (used_memory / available_memory * 100.0).toFixed(2);
          }
        }
      }, {
        key: "agentUp",
        value: function agentUp(agent) {
          this.agentLog = "Calling up on agent: ".concat(agent);
          this.dockerService.agentUp(agent).subscribe(function (output) {// console.log(output);
          });
        }
      }, {
        key: "agentDown",
        value: function agentDown(agent) {
          this.agentLog = "Calling down on agent: ".concat(agent);
          this.dockerService.agentDown(agent).subscribe(function (output) {// console.log(output);
          });
        }
      }]);

      return DockerComponent;
    }();

    DockerComponent.ɵfac = function DockerComponent_Factory(t) {
      return new (t || DockerComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_docker_service__WEBPACK_IMPORTED_MODULE_2__["DockerService"]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](ngx_mqtt__WEBPACK_IMPORTED_MODULE_3__["MqttService"]));
    };

    DockerComponent.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DockerComponent,
      selectors: [["app-docker"]],
      viewQuery: function DockerComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c0, true);
        }

        if (rf & 2) {
          var _t;

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.matSelectionList = _t.first);
        }
      },
      decls: 73,
      vars: 29,
      consts: [[1, "container"], ["fxLayout", "row wrap", "fxLayoutAlign", "center top", 3, "fxLayout.lt-md"], ["fxLayoutAlign", "stretch", 3, "fxFlex.gt-sm"], ["ngClass", "dashboard-card", 3, "ngClass.lt-md"], ["mat-card-avatar", ""], ["aria-label", "Containers"], [3, "color", "matTooltip"], [3, "multiple", "compareWith", "selectionChange"], ["containerList", ""], [3, "value", "selected", 4, "ngFor", "ngForOf"], ["inset", ""], ["align", "end"], ["mat-mini-fab", "", "color", "primary", "aria-label", "Download container log.", "matTooltip", "Download all container logs", 3, "disabled", "click"], ["aria-label", "Container Details"], ["class", "lighter", 4, "ngIf"], ["class", "log-content", 4, "ngIf"], ["mat-mini-fab", "", "color", "primary", "aria-label", "Refresh last 100 lines of container log.", "matTooltip", "Refresh last 100 line of log", 3, "disabled", "click"], ["mat-mini-fab", "", "color", "primary", "aria-label", "Download container log.", "matTooltip", "Download container log", 3, "disabled", "click"], ["mat-raised-button", "", "color", "primary", "matTooltip", "Stop container", 3, "disabled", "click"], ["mat-raised-button", "", "color", "primary", "matTooltip", "Start container", 3, "disabled", "click"], ["aria-label", "Agents"], ["agentList", ""], [4, "ngFor", "ngForOf"], ["class", "agent-output caption", 4, "ngIf"], [3, "value", "selected"], ["mat-list-icon", "", 3, "color", "matTooltip"], ["mat-line", ""], [1, "lighter"], [1, "bold"], [1, "log-content"], [1, "log-list"], ["mat-mini-fab", "", "color", "primary", 3, "matTooltip", "click"], ["aria-label", "Down"], ["aria-label", "Up"], [1, "agent-output", "caption"]],
      template: function DockerComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "h2");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "Docker");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "div", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "mat-card", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "mat-card-header");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "div", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "mat-icon", 5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](9, "web_stories");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "mat-card-title");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11, "Containers");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "mat-card-subtitle");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](13, "Status");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "mat-icon", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](15, "lens");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](16, "mat-card-content");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](17, "mat-selection-list", 7, 8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("selectionChange", function DockerComponent_Template_mat_selection_list_selectionChange_17_listener($event) {
            return ctx.onSelectionChange($event);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](19, DockerComponent_mat_list_option_19_Template, 7, 7, "mat-list-option", 9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](20, "keyvalue");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](21, "mat-divider", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "mat-card-actions", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](23, "button", 12);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_Template_button_click_23_listener() {
            return ctx.containerLogsDownload();
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](24, "mat-icon");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](25, "download");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](26, "div", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "mat-card", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](28, "mat-card-header");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](29, "div", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "mat-icon", 13);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](31, "notes");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](32, "mat-card-title");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](33, "Container");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](34, "mat-card-subtitle");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](35);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](36, "mat-icon", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](37, "lens");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](38, "mat-card-content");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](39, DockerComponent_p_39_Template, 4, 1, "p", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](40, DockerComponent_p_40_Template, 4, 1, "p", 14);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](41, DockerComponent_div_41_Template, 3, 1, "div", 15);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](42, "mat-divider", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](43, "mat-card-actions", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](44, "button", 16);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_Template_button_click_44_listener() {
            return ctx.containerLog(ctx.selectedContainer.Id);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](45, "mat-icon");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](46, "refresh");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](47, "button", 17);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_Template_button_click_47_listener() {
            return ctx.containerLogDownload(ctx.selectedContainer.Id);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](48, "mat-icon");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](49, "download");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](50, "button", 18);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_Template_button_click_50_listener() {
            return ctx.stopContainer(ctx.selectedContainer.Id);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](51, "Stop");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](52, "button", 19);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DockerComponent_Template_button_click_52_listener() {
            return ctx.startContainer(ctx.selectedContainer.Id);
          });

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](53, "Start");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](54, "div", 2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](55, "mat-card", 3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](56, "mat-card-header");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](57, "div", 4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](58, "mat-icon", 20);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](59, "group");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](60, "mat-card-title");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](61, "Agents");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](62, "mat-card-subtitle");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](63, "Status");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](64, "mat-icon", 6);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](65, "lens");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](66, "mat-card-content");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](67, "mat-action-list", null, 21);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](69, DockerComponent_mat_list_item_69_Template, 9, 3, "mat-list-item", 22);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](70, "mat-divider", 10);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](71, "mat-card-actions", 11);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](72, DockerComponent_div_72_Template, 2, 1, "div", 23);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }

        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("fxLayout.lt-md", "column wrap");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("fxFlex.gt-sm", 100 / 2 + "%");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass.lt-md", "dashboard-card-narrow");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("color", ctx.dockerOnline ? "primary" : "warn");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("matTooltip", ctx.dockerOnline ? "Docker online" : "Docker offline");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("multiple", false)("compareWith", ctx.compare);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](20, 27, ctx.containers));

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", !ctx.dockerOnline);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("fxFlex.gt-sm", 100 / 2 + "%");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass.lt-md", "dashboard-card-narrow");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](8);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx.selectedContainer === null ? "Details" : ctx.selectedContainer.Names[0].substring(1));

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("color", ctx.selectedContainer === null || ctx.selectedContainer.State === "running" ? "primary" : "warn");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("matTooltip", ctx.selectedContainer === null ? "" : ctx.selectedContainer.Status);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.selectedContainer !== null);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.selectedContainer !== null);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.selectedContainer !== null);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.selectedContainer === null);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.selectedContainer === null);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.selectedContainer === null || ctx.selectedContainer.State !== "running");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.selectedContainer === null || ctx.selectedContainer.State !== "exited");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("fxFlex.gt-sm", 100 / 2 + "%");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass.lt-md", "dashboard-card-narrow");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](9);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("color", ctx.dockerOnline ? "primary" : "warn");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpropertyInterpolate"]("matTooltip", ctx.dockerOnline ? "Docker online" : "Docker offline");

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.agents);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);

          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.agentLog != "");
        }
      },
      directives: [_angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_4__["DefaultLayoutDirective"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_4__["DefaultLayoutAlignDirective"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_4__["DefaultFlexDirective"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCard"], _angular_common__WEBPACK_IMPORTED_MODULE_6__["NgClass"], _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_7__["DefaultClassDirective"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardHeader"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardAvatar"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIcon"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardTitle"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardSubtitle"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__["MatTooltip"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardContent"], _angular_material_list__WEBPACK_IMPORTED_MODULE_10__["MatSelectionList"], _angular_common__WEBPACK_IMPORTED_MODULE_6__["NgForOf"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_11__["MatDivider"], _angular_material_card__WEBPACK_IMPORTED_MODULE_5__["MatCardActions"], _angular_material_button__WEBPACK_IMPORTED_MODULE_12__["MatButton"], _angular_common__WEBPACK_IMPORTED_MODULE_6__["NgIf"], _angular_material_list__WEBPACK_IMPORTED_MODULE_10__["MatList"], _angular_material_list__WEBPACK_IMPORTED_MODULE_10__["MatListOption"], _angular_material_list__WEBPACK_IMPORTED_MODULE_10__["MatListIconCssMatStyler"], _angular_material_core__WEBPACK_IMPORTED_MODULE_13__["MatLine"], _angular_material_list__WEBPACK_IMPORTED_MODULE_10__["MatListItem"]],
      pipes: [_angular_common__WEBPACK_IMPORTED_MODULE_6__["KeyValuePipe"]],
      styles: [".bold[_ngcontent-%COMP%] {\n  font-weight: bold;\n}\n\n.lighter[_ngcontent-%COMP%] {\n  font-weight: lighter;\n}\n\n.container[_ngcontent-%COMP%] {\n  margin: 2em;\n}\n\n.mat-card[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: column;\n  height: 600px;\n  overflow: hidden;\n}\n\n.mat-card-content[_ngcontent-%COMP%] {\n  overflow: auto;\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n}\n\n.mat-mini-fab[_ngcontent-%COMP%] {\n  margin: 0 8px;\n}\n\n[_nghost-%COMP%]     .mat-card-header-text {\n  flex: 1;\n}\n\n.mat-card-avatar[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%] {\n  width: 40px;\n  height: 40px;\n  font-size: 40px;\n}\n\n.dashboard-card-narrow[_ngcontent-%COMP%] {\n  margin: 0.5em;\n  flex: 1;\n}\n\n.dashboard-card[_ngcontent-%COMP%] {\n  margin: 2em;\n  flex: 1;\n}\n\n.mat-icon[_ngcontent-%COMP%] {\n  cursor: pointer;\n}\n\n.log-content[_ngcontent-%COMP%] {\n  overflow-y: auto;\n  display: flex;\n  background-color: black;\n  color: #33FF00;\n  -ms-scroll-snap-type: y mandatory;\n      scroll-snap-type: y mandatory;\n  margin-right: 8px;\n  margin-bottom: 8px;\n  flex: 1;\n}\n\n.log-list[_ngcontent-%COMP%] {\n  padding: 8px 16px;\n  display: flex;\n  flex-direction: column;\n  flex: 1 0 auto;\n  font-family: \"Courier New\";\n  font-size: smaller;\n}\n\n.log-list[_ngcontent-%COMP%]   div[_ngcontent-%COMP%] {\n  scroll-snap-align: start;\n}\n\n.agent-output[_ngcontent-%COMP%] {\n  background: black;\n  width: 100%;\n  display: flex;\n  padding: 0 0.5em;\n  color: white;\n  text-align: left;\n  font-size: x-small;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvZG9ja2VyL2RvY2tlci9DOlxcVXNlcnNcXENoYXJsaWUgS2Fwb3BvdWxvc1xcUHJvamVjdHNcXEFwdGltYVxcdGVzdGJlZFxcbWV0YWRhdGFcXG1ldGFkYXRhLXdlYi9zcmNcXGFwcFxcZG9ja2VyXFxkb2NrZXJcXGRvY2tlci5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvZG9ja2VyL2RvY2tlci9kb2NrZXIuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxpQkFBaUI7QUNDbkI7O0FERUE7RUFDRSxvQkFBb0I7QUNDdEI7O0FERUE7RUFDRSxXQUFXO0FDQ2I7O0FERUE7RUFDRSxhQUFhO0VBQ2Isc0JBQXNCO0VBQ3RCLGFBQWE7RUFDYixnQkFBZ0I7QUNDbEI7O0FERUM7RUFDRSxjQUFjO0VBQ2QsYUFBYTtFQUNiLHNCQUFzQjtFQUN0QixPQUFPO0FDQ1Y7O0FEZUE7RUFDRSxhQUFhO0FDWmY7O0FEZUE7RUFDRSxPQUFPO0FDWlQ7O0FEZUE7RUFDRSxXQUFXO0VBQ1gsWUFBWTtFQUNaLGVBQWU7QUNaakI7O0FEZUE7RUFDRSxhQUFhO0VBQ2IsT0FBTztBQ1pUOztBRGVBO0VBQ0UsV0FBVztFQUNYLE9BQU87QUNaVDs7QURlQTtFQUNFLGVBQWU7QUNaakI7O0FEZUE7RUFDRSxnQkFBZ0I7RUFDaEIsYUFBYTtFQUNiLHVCQUF1QjtFQUN2QixjQUFjO0VBQ2QsaUNBQTZCO01BQTdCLDZCQUE2QjtFQUc3QixpQkFBaUI7RUFDakIsa0JBQWtCO0VBQ2xCLE9BQU87QUNkVDs7QURpQkE7RUFDRSxpQkFBaUI7RUFDakIsYUFBYTtFQUNiLHNCQUFzQjtFQUN0QixjQUFjO0VBRWQsMEJBQTBCO0VBQzFCLGtCQUFrQjtBQ2ZwQjs7QURRQTtFQVVJLHdCQUF3QjtBQ2Q1Qjs7QURrQkE7RUFDRSxpQkFBaUI7RUFDakIsV0FBVztFQUNYLGFBQWE7RUFDYixnQkFBZ0I7RUFDaEIsWUFBWTtFQUNaLGdCQUFnQjtFQUNoQixrQkFBa0I7QUNmcEIiLCJmaWxlIjoic3JjL2FwcC9kb2NrZXIvZG9ja2VyL2RvY2tlci5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5ib2xkIHtcclxuICBmb250LXdlaWdodDogYm9sZDtcclxufVxyXG5cclxuLmxpZ2h0ZXIge1xyXG4gIGZvbnQtd2VpZ2h0OiBsaWdodGVyO1xyXG59XHJcblxyXG4uY29udGFpbmVyIHtcclxuICBtYXJnaW46IDJlbTtcclxufVxyXG5cclxuLm1hdC1jYXJkIHtcclxuICBkaXNwbGF5OiBmbGV4O1xyXG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgaGVpZ2h0OiA2MDBweDtcclxuICBvdmVyZmxvdzogaGlkZGVuO1xyXG4gfVxyXG5cclxuIC5tYXQtY2FyZC1jb250ZW50IHtcclxuICAgb3ZlcmZsb3c6IGF1dG87XHJcbiAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgIGZsZXg6IDE7XHJcbiAgIC8vLmNvbnRhaW5lci1idXR0b24tY29udGFpbmVyIHtcclxuICAgLy8gIGRpc3BsYXk6IGZsZXg7XHJcbiAgIC8vICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XHJcbiAgIC8vICBidXR0b24ge1xyXG4gICAvLyAgICAvL2FsaWduLXNlbGY6IGVuZDtcclxuICAgLy8gICAgbWFyZ2luLWJvdHRvbTogMWVtO1xyXG4gICAvLyAgICBjdXJzb3I6IHBvaW50ZXI7XHJcbiAgIC8vXHJcbiAgIC8vICAgIC5tYXQtaWNvbiB7XHJcbiAgIC8vICAgICAgY3Vyc29yOiBwb2ludGVyO1xyXG4gICAvLyAgICB9XHJcbiAgIC8vICB9XHJcbiAgIC8vfVxyXG4gfVxyXG5cclxuLm1hdC1taW5pLWZhYiB7XHJcbiAgbWFyZ2luOiAwIDhweDtcclxufVxyXG5cclxuOmhvc3QgOjpuZy1kZWVwIC5tYXQtY2FyZC1oZWFkZXItdGV4dCB7XHJcbiAgZmxleDogMTtcclxufVxyXG5cclxuLm1hdC1jYXJkLWF2YXRhciBtYXQtaWNvbiB7XHJcbiAgd2lkdGg6IDQwcHg7XHJcbiAgaGVpZ2h0OiA0MHB4O1xyXG4gIGZvbnQtc2l6ZTogNDBweDtcclxufVxyXG5cclxuLmRhc2hib2FyZC1jYXJkLW5hcnJvdyB7XHJcbiAgbWFyZ2luOiAwLjVlbTtcclxuICBmbGV4OiAxO1xyXG59XHJcblxyXG4uZGFzaGJvYXJkLWNhcmQge1xyXG4gIG1hcmdpbjogMmVtO1xyXG4gIGZsZXg6IDE7XHJcbn1cclxuXHJcbi5tYXQtaWNvbiB7XHJcbiAgY3Vyc29yOiBwb2ludGVyO1xyXG59XHJcblxyXG4ubG9nLWNvbnRlbnQge1xyXG4gIG92ZXJmbG93LXk6IGF1dG87XHJcbiAgZGlzcGxheTogZmxleDtcclxuICBiYWNrZ3JvdW5kLWNvbG9yOiBibGFjaztcclxuICBjb2xvcjogIzMzRkYwMDtcclxuICBzY3JvbGwtc25hcC10eXBlOiB5IG1hbmRhdG9yeTtcclxuICAvL2ZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgLy9mbGV4OiAxIDEgYXV0bztcclxuICBtYXJnaW4tcmlnaHQ6IDhweDtcclxuICBtYXJnaW4tYm90dG9tOiA4cHg7XHJcbiAgZmxleDogMTtcclxufVxyXG5cclxuLmxvZy1saXN0IHtcclxuICBwYWRkaW5nOiA4cHggMTZweDtcclxuICBkaXNwbGF5OiBmbGV4O1xyXG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgZmxleDogMSAwIGF1dG87XHJcbiAgLy9vdmVyZmxvdzogYXV0bztcclxuICBmb250LWZhbWlseTogXCJDb3VyaWVyIE5ld1wiO1xyXG4gIGZvbnQtc2l6ZTogc21hbGxlcjtcclxuICAvL292ZXJmbG93LXg6IGF1dG87XHJcbiAgZGl2IHtcclxuICAgIHNjcm9sbC1zbmFwLWFsaWduOiBzdGFydDtcclxuICB9XHJcbn1cclxuXHJcbi5hZ2VudC1vdXRwdXQge1xyXG4gIGJhY2tncm91bmQ6IGJsYWNrO1xyXG4gIHdpZHRoOiAxMDAlO1xyXG4gIGRpc3BsYXk6IGZsZXg7XHJcbiAgcGFkZGluZzogMCAwLjVlbTtcclxuICBjb2xvcjogd2hpdGU7XHJcbiAgdGV4dC1hbGlnbjogbGVmdDtcclxuICBmb250LXNpemU6IHgtc21hbGw7XHJcbn1cclxuIiwiLmJvbGQge1xuICBmb250LXdlaWdodDogYm9sZDtcbn1cblxuLmxpZ2h0ZXIge1xuICBmb250LXdlaWdodDogbGlnaHRlcjtcbn1cblxuLmNvbnRhaW5lciB7XG4gIG1hcmdpbjogMmVtO1xufVxuXG4ubWF0LWNhcmQge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBoZWlnaHQ6IDYwMHB4O1xuICBvdmVyZmxvdzogaGlkZGVuO1xufVxuXG4ubWF0LWNhcmQtY29udGVudCB7XG4gIG92ZXJmbG93OiBhdXRvO1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBmbGV4OiAxO1xufVxuXG4ubWF0LW1pbmktZmFiIHtcbiAgbWFyZ2luOiAwIDhweDtcbn1cblxuOmhvc3QgOjpuZy1kZWVwIC5tYXQtY2FyZC1oZWFkZXItdGV4dCB7XG4gIGZsZXg6IDE7XG59XG5cbi5tYXQtY2FyZC1hdmF0YXIgbWF0LWljb24ge1xuICB3aWR0aDogNDBweDtcbiAgaGVpZ2h0OiA0MHB4O1xuICBmb250LXNpemU6IDQwcHg7XG59XG5cbi5kYXNoYm9hcmQtY2FyZC1uYXJyb3cge1xuICBtYXJnaW46IDAuNWVtO1xuICBmbGV4OiAxO1xufVxuXG4uZGFzaGJvYXJkLWNhcmQge1xuICBtYXJnaW46IDJlbTtcbiAgZmxleDogMTtcbn1cblxuLm1hdC1pY29uIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4ubG9nLWNvbnRlbnQge1xuICBvdmVyZmxvdy15OiBhdXRvO1xuICBkaXNwbGF5OiBmbGV4O1xuICBiYWNrZ3JvdW5kLWNvbG9yOiBibGFjaztcbiAgY29sb3I6ICMzM0ZGMDA7XG4gIHNjcm9sbC1zbmFwLXR5cGU6IHkgbWFuZGF0b3J5O1xuICBtYXJnaW4tcmlnaHQ6IDhweDtcbiAgbWFyZ2luLWJvdHRvbTogOHB4O1xuICBmbGV4OiAxO1xufVxuXG4ubG9nLWxpc3Qge1xuICBwYWRkaW5nOiA4cHggMTZweDtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZmxleDogMSAwIGF1dG87XG4gIGZvbnQtZmFtaWx5OiBcIkNvdXJpZXIgTmV3XCI7XG4gIGZvbnQtc2l6ZTogc21hbGxlcjtcbn1cblxuLmxvZy1saXN0IGRpdiB7XG4gIHNjcm9sbC1zbmFwLWFsaWduOiBzdGFydDtcbn1cblxuLmFnZW50LW91dHB1dCB7XG4gIGJhY2tncm91bmQ6IGJsYWNrO1xuICB3aWR0aDogMTAwJTtcbiAgZGlzcGxheTogZmxleDtcbiAgcGFkZGluZzogMCAwLjVlbTtcbiAgY29sb3I6IHdoaXRlO1xuICB0ZXh0LWFsaWduOiBsZWZ0O1xuICBmb250LXNpemU6IHgtc21hbGw7XG59XG4iXX0= */"]
    });
    /*@__PURE__*/

    (function () {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](DockerComponent, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'app-docker',
          templateUrl: './docker.component.html',
          styleUrls: ['./docker.component.scss']
        }]
      }], function () {
        return [{
          type: _docker_service__WEBPACK_IMPORTED_MODULE_2__["DockerService"]
        }, {
          type: ngx_mqtt__WEBPACK_IMPORTED_MODULE_3__["MqttService"]
        }];
      }, {
        matSelectionList: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"],
          args: ['containerList']
        }]
      });
    })();
    /***/

  }
}]);
//# sourceMappingURL=docker-docker-module-es5.js.map