webpackHotUpdate("main",{

/***/ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/components/BasePage.vue?vue&type=script&lang=js&":
/*!**********************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib??ref--0-0!./node_modules/vue-loader/lib??vue-loader-options!./src/components/BasePage.vue?vue&type=script&lang=js& ***!
  \**********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _TopNav_vue__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./TopNav.vue */ "./src/components/TopNav.vue");
/* harmony import */ var _Menu_vue__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Menu.vue */ "./src/components/Menu.vue");
/* harmony import */ var _Footer_vue__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Footer.vue */ "./src/components/Footer.vue");
/* harmony import */ var _Popup_vue__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Popup.vue */ "./src/components/Popup.vue");
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//




/* harmony default export */ __webpack_exports__["default"] = ({
  name: "BasePage",
  components: {
    'top-nav': _TopNav_vue__WEBPACK_IMPORTED_MODULE_0__["default"],
    'left-menu': _Menu_vue__WEBPACK_IMPORTED_MODULE_1__["default"],
    'main-footer': _Footer_vue__WEBPACK_IMPORTED_MODULE_2__["default"],
    'popup': _Popup_vue__WEBPACK_IMPORTED_MODULE_3__["default"]
  },
  mounted: function mounted() {
    if (this.$route.params.shift_id) {
      this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id);
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/components/Cell.vue?vue&type=script&lang=js&":
/*!******************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib??ref--0-0!./node_modules/vue-loader/lib??vue-loader-options!./src/components/Cell.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! core-js/modules/es6.function.name */ "./node_modules/core-js/modules/es6.function.name.js");
/* harmony import */ var core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var core_js_modules_es6_array_find__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! core-js/modules/es6.array.find */ "./node_modules/core-js/modules/es6.array.find.js");
/* harmony import */ var core_js_modules_es6_array_find__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_array_find__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! vue/dist/vue.esm.js */ "./node_modules/vue/dist/vue.esm.js");
/* harmony import */ var v_tooltip__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! v-tooltip */ "../node_modules/v-tooltip/dist/v-tooltip.esm.js");
/* harmony import */ var _CellComment_vue__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./CellComment.vue */ "./src/components/CellComment.vue");
/* harmony import */ var clockpicker_dist_bootstrap_clockpicker_min__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! clockpicker/dist/bootstrap-clockpicker.min */ "./node_modules/clockpicker/dist/bootstrap-clockpicker.min.js");
/* harmony import */ var clockpicker_dist_bootstrap_clockpicker_min__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(clockpicker_dist_bootstrap_clockpicker_min__WEBPACK_IMPORTED_MODULE_5__);


//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//




vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_2__["default"].directive('tooltip', v_tooltip__WEBPACK_IMPORTED_MODULE_3__["VTooltip"]);
vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_2__["default"].directive('close-popover', v_tooltip__WEBPACK_IMPORTED_MODULE_3__["VClosePopover"]);
vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_2__["default"].component('v-popover', v_tooltip__WEBPACK_IMPORTED_MODULE_3__["VPopover"]);
vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_2__["default"].component('CellComment', _CellComment_vue__WEBPACK_IMPORTED_MODULE_4__["default"]);
/* harmony default export */ __webpack_exports__["default"] = ({
  name: 'Cell',
  props: ['fieldName', 'rowIndex', 'linked'],
  data: function data() {
    return {
      classes: 'general-value number-cell form-control',
      minValue: null,
      maxValue: null,
      type: null,
      placeholder: '',
      showCellTypeTooltip: false
    };
  },
  watch: {
    mode: function mode(value) {
      var _this = this;

      if (this.type === 'time') {
        if (value === 'edit') {
          console.log('edit');
          $(this.$el).find('input').clockpicker({
            autoclose: true,
            'default': 'now',
            donetext: false,
            afterDone: function afterDone() {
              _this.value = $(_this.$el).find('input').val();
            }
          });
        } else {
          console.log('not-edit');
          $(this.$el).find('input').clockpicker('remove');
        }
      }
    }
  },
  computed: {
    tableName: function tableName() {
      if (typeof this.$parent.props !== 'undefined') {
        return this.$parent.props.name;
      } else {
        return '';
      }
    },
    activeColor: function activeColor() {
      return this.critical ? 'red' : '';
    },
    critical: function critical() {
      return this.minValue && this.value < this.minValue || this.maxValue && this.value > this.maxValue;
    },
    value: {
      get: function get() {
        return this.$store.getters['journalState/cellValue'](this.tableName, this.fieldName, this.rowIndex);
      },
      set: function set(val) {
        this.$store.commit('journalState/SAVE_CELL_VALUE', {
          tableName: this.tableName,
          fieldName: this.fieldName,
          index: this.rowIndex,
          value: val
        });
      }
    },
    mode: function mode() {
      return this.$store.getters['journalState/journalInfo'].mode;
    }
  },
  methods: {
    send: function send() {
      this.$socket.sendObj({
        'type': 'shift_data',
        'cell_location': {
          'group_id': this.$store.getters['journalState/journalInfo'].id,
          'table_name': this.tableName,
          'field_name': this.fieldName,
          'index': this.rowIndex
        },
        'value': this.value
      });
    },
    onInput: function onInput(e) {
      this.value = e.target.value;
      this.send();
    },
    onChanged: function onChanged() {},
    filterInput: function filterInput(e) {
      if (this.type === 'number') {
        var keycode = e.which; // if non number character was pressed

        if (!(e.shiftKey == false && (keycode == 45 && this.value == '' || keycode == 46 || keycode == 8 || keycode == 37 || keycode == 39 || keycode >= 48 && keycode <= 57))) {
          this.showCellTypeTooltip = true;
          event.preventDefault();
        } else {
          this.showCellTypeTooltip = false;
        }
      }
    },
    changeFocus: function changeFocus(e) {
      function getIndex(tds, focusedTd) {
        var index = 0;

        for (var i = 0; i < tds.length; i++) {
          var td = tds[i];

          if (td === focusedTd) {
            break;
          }

          index += parseInt(td.getAttribute('colspan'), 10) || 1;
        }

        return index;
      }

      function getTd(tds, index) {
        var nextRowIndex = 0;

        for (var i = 0; i < tds.length; i++) {
          var td = tds[i];

          if (nextRowIndex === index) {
            return td;
          }

          nextRowIndex += parseInt(td.getAttribute('colspan'), 10) || 1;
        }
      }

      var focusedTd = this.$el.parentElement;
      var tr = focusedTd.parentElement;
      var rowIndex = getIndex(tr.children, focusedTd);

      switch (e.key) {
        case 'ArrowUp':
          var prevTr = tr.previousElementSibling;

          if (prevTr) {
            getTd(prevTr.children, rowIndex).children[0].children[0].children[0].select();
          }

          break;

        case 'ArrowDown':
          var nextTr = tr.nextElementSibling;

          if (nextTr) {
            getTd(nextTr.children, rowIndex).children[0].children[0].children[0].select();
          }

          break;

        case 'ArrowLeft':
          var prevTd = focusedTd.previousElementSibling;

          if (prevTd) {
            prevTd.children[0].children[0].children[0].select();
          }

          break;

        case 'ArrowRight':
          var nextTd = focusedTd.nextElementSibling;

          if (nextTd) {
            nextTd.children[0].children[0].children[0].select();
          }

          break;
      }
    }
  },
  mounted: function mounted() {
    // initializing data
    var desc = this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName);
    this.placeholder = desc['units'] || '';
    this.minValue = desc['min_normal'] || null;
    this.maxValue = desc['max_normal'] || null;
    this.type = desc['type'] || 'text';

    if (this.linked) {
      // auto fill cell
      this.value = this.$store.getters['journalState/' + this.linked];
      this.send();
    } // if (this.type === 'date') {
    //     setTimeout(() => {
    //         $(this.$el).datepicker({
    //             format: 'yyyy-mm-dd',
    //             autoclose: true,
    //             endDate: '+0d',
    //         })
    //     }, 0)
    // }

  }
});
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/components/JournalPanel.vue?vue&type=script&lang=js&":
/*!**************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib??ref--0-0!./node_modules/vue-loader/lib??vue-loader-options!./src/components/JournalPanel.vue?vue&type=script&lang=js& ***!
  \**************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var core_js_modules_es6_regexp_split__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! core-js/modules/es6.regexp.split */ "./node_modules/core-js/modules/es6.regexp.split.js");
/* harmony import */ var core_js_modules_es6_regexp_split__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_regexp_split__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! axios */ "./node_modules/axios/index.js");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var vue_full_calendar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! vue-full-calendar */ "./node_modules/vue-full-calendar/index.js");
/* harmony import */ var _Modal_vue__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Modal.vue */ "./src/components/Modal.vue");

//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



/* harmony default export */ __webpack_exports__["default"] = ({
  name: 'journal-panel',
  data: function data() {
    return {
      showCalendar: false,
      employeeName: 'Employee name',
      employeePosition: 'position',
      events: null,
      fullCalendarConfig: {
        locale: 'ru',
        buttonText: {
          today: 'Сегодня',
          month: 'Месяц',
          week: 'Неделя',
          day: 'День',
          list: 'Список'
        },
        timeFormat: 'H(:mm)',
        header: {
          left: 'prev,next today',
          center: 'title',
          right: 'month, listMonth'
        },
        selectable: true,
        selectHelper: true,
        select: function select(start, end, allDay) {},
        eventClick: function eventClick(calEvent, jsEvent, view) {
          console.log("event click");
        },
        editable: false
      }
    };
  },
  computed: {
    employeeFormatted: function employeeFormatted() {
      return this.employeeName + " : " + this.employeePosition;
    },
    mode: function mode() {
      return this.$store.getters['journalState/journalInfo'].mode;
    },
    shiftDate: function shiftDate() {
      return this.$store.getters['journalState/journalInfo'].date;
    },
    shiftOrder: function shiftOrder() {
      return this.$store.getters['journalState/journalInfo'].order;
    }
  },
  methods: {
    changeMode: function changeMode(mode) {
      var permission = mode + '_cells';
      var permissions = this.$store.getters['journalState/journalInfo'].permissions;

      for (var i = 0; i < permissions.length; i++) {
        if (permission === permissions[i]) {
          this.$store.commit('journalState/SET_PAGE_MODE', mode);
        }
      }
    }
  },
  mounted: function mounted() {
    var plant = location.pathname.split('/')[1];
    var journal_name = location.pathname.split('/')[2];
    var self = this;
    axios__WEBPACK_IMPORTED_MODULE_1___default.a.get('http://localhost:8000/' + plant + '/' + journal_name + '/get_shifts/', {
      withCredentials: true
    }).then(function (response) {
      self.events = response.data;
      $(".fc-month-button").click();
    }).catch(function (e) {
      console.log(e);
    });
  },
  components: {
    modal: _Modal_vue__WEBPACK_IMPORTED_MODULE_3__["default"],
    FullCalendar: vue_full_calendar__WEBPACK_IMPORTED_MODULE_2__["FullCalendar"]
  }
});
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker.js":
false,

/***/ "./node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js":
false,

/***/ "./node_modules/css-loader/index.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js?!./src/components/BasePage.vue?vue&type=style&index=0&id=10e8a5a0&scoped=true&lang=css&":
/*!***********************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/css-loader!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib??vue-loader-options!./src/components/BasePage.vue?vue&type=style&index=0&id=10e8a5a0&scoped=true&lang=css& ***!
  \***********************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(/*! ../../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", ""]);

// exports


/***/ }),

/***/ "./node_modules/css-loader/index.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js?!./src/components/JournalPanel.vue?vue&type=style&index=0&lang=css&":
/*!***************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/css-loader!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib??vue-loader-options!./src/components/JournalPanel.vue?vue&type=style&index=0&lang=css& ***!
  \***************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(/*! ../../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", ""]);

// exports


/***/ }),

/***/ "./node_modules/reconnecting-websocket/dist/reconnecting-websocket.mjs":
false,

/***/ "./node_modules/vue-loader/lib/loaders/templateLoader.js?!./node_modules/vue-loader/lib/index.js?!./src/components/Cell.vue?vue&type=template&id=c13496dc&":
/*!**********************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/Cell.vue?vue&type=template&id=c13496dc& ***!
  \**********************************************************************************************************************************************************************************************/
/*! exports provided: render, staticRenderFns */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return staticRenderFns; });
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c(
    "v-popover",
    { attrs: { offset: "16", disabled: _vm.mode !== "validate" } },
    [
      _c("input", {
        directives: [
          {
            name: "tooltip",
            rawName: "v-tooltip",
            value: {
              content: "Введите число",
              show: _vm.showCellTypeTooltip,
              trigger: "manual"
            },
            expression:
              "{content: 'Введите число', show: showCellTypeTooltip, trigger: 'manual'}"
          }
        ],
        class: _vm.classes,
        style: { color: _vm.activeColor },
        attrs: {
          name: _vm.fieldName,
          "row-index": _vm.rowIndex,
          readonly: _vm.mode !== "edit",
          placeholder: _vm.placeholder,
          type: _vm.type
        },
        domProps: { value: _vm.value },
        on: {
          keypress: _vm.filterInput,
          keydown: _vm.changeFocus,
          change: _vm.onChanged,
          input: _vm.onInput,
          blur: function($event) {
            _vm.showCellTypeTooltip = false
          }
        }
      }),
      _vm._v(" "),
      _vm.$store.getters["journalState/cellComment"](
        _vm.tableName,
        _vm.fieldName,
        _vm.rowIndex
      )
        ? _c("i", { staticClass: "far fa-envelope comment-notification" })
        : _vm._e(),
      _vm._v(" "),
      _c(
        "template",
        { slot: "popover" },
        [
          _c("CellComment", {
            attrs: {
              "table-name": _vm.tableName,
              "field-name": _vm.fieldName,
              "row-index": _vm.rowIndex
            }
          })
        ],
        1
      )
    ],
    2
  )
}
var staticRenderFns = []
render._withStripped = true



/***/ }),

/***/ "./src/assets/js/index.js":
/*!********************************!*\
  !*** ./src/assets/js/index.js ***!
  \********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($, jQuery, _) {/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lodash */ "./node_modules/lodash/lodash.js");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var vue__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! vue */ "./node_modules/vue/dist/vue.esm.js");
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! bootstrap */ "./node_modules/bootstrap/dist/js/bootstrap.js");
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(bootstrap__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var jquery_confirm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! jquery-confirm */ "./node_modules/jquery-confirm/dist/jquery-confirm.min.js");
/* harmony import */ var jquery_confirm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(jquery_confirm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var promise_polyfill_src_polyfill__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! promise-polyfill/src/polyfill */ "./node_modules/promise-polyfill/src/polyfill.js");
/* harmony import */ var fullcalendar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! fullcalendar */ "./node_modules/fullcalendar/dist/fullcalendar.js");
/* harmony import */ var fullcalendar__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(fullcalendar__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var bootstrap_grid__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! bootstrap-grid */ "./node_modules/bootstrap-grid/dist/grid.min.css");
/* harmony import */ var bootstrap_grid__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(bootstrap_grid__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var waypoints_lib_jquery_waypoints_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! waypoints/lib/jquery.waypoints.js */ "./node_modules/waypoints/lib/jquery.waypoints.js");
/* harmony import */ var waypoints_lib_jquery_waypoints_js__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(waypoints_lib_jquery_waypoints_js__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var typeface_roboto_condensed__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! typeface-roboto-condensed */ "./node_modules/typeface-roboto-condensed/index.css");
/* harmony import */ var typeface_roboto_condensed__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(typeface_roboto_condensed__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var typeface_roboto__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! typeface-roboto */ "./node_modules/typeface-roboto/index.css");
/* harmony import */ var typeface_roboto__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(typeface_roboto__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _fortawesome_fontawesome__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @fortawesome/fontawesome */ "./node_modules/@fortawesome/fontawesome/index.es.js");
/* harmony import */ var _fortawesome_fontawesome_free_brands__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @fortawesome/fontawesome-free-brands */ "./node_modules/@fortawesome/fontawesome-free-brands/index.es.js");
/* harmony import */ var _feedback__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./feedback */ "./src/assets/js/feedback.js");
/* harmony import */ var _header__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./header */ "./src/assets/js/header.js");
/* harmony import */ var _header__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_header__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _vue_env__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./vue-env */ "./src/assets/js/vue-env.js");
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./common */ "./src/assets/js/common.js");
//- require('offline-plugin/runtime').install();  // offline service-worker plugin
// ------------------------------------- Libs -------------------------------------

window.$ = $;
window.jQuery = jQuery;

window._ = _;


window.Vue = vue__WEBPACK_IMPORTED_MODULE_2__["default"];





 // import 'waypoints'; import Waypoint from 'waypoints'; window.Waypoint = Waypoint;


 // import 'material-design-icons';


 // ---------------------------------- Modules -------------------------------------
// import '../scss/index.scss';





/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), __webpack_require__(/*! lodash */ "./node_modules/lodash/lodash.js")))

/***/ }),

/***/ "./src/main.js":
/*!*********************!*\
  !*** ./src/main.js ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue/dist/vue.esm.js */ "./node_modules/vue/dist/vue.esm.js");
/* harmony import */ var _App_vue__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./App.vue */ "./src/App.vue");
/* harmony import */ var _router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./router */ "./src/router.js");
/* harmony import */ var _store_store__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./store/store */ "./src/store/store.js");
/* harmony import */ var vue_native_websocket__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! vue-native-websocket */ "../node_modules/vue-native-websocket/dist/build.js");
/* harmony import */ var vue_native_websocket__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(vue_native_websocket__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _register_sw__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./register-sw */ "./src/register-sw.js");
/* harmony import */ var _register_sw__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_register_sw__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _assets_js_index__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./assets/js/index */ "./src/assets/js/index.js");







vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_0__["default"].config.productionTip = false;
var dataEndpoint = 'ws://' + window.location.hostname + ':8000/e-logs/';
vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_0__["default"].use(vue_native_websocket__WEBPACK_IMPORTED_MODULE_4___default.a, dataEndpoint, {
  store: _store_store__WEBPACK_IMPORTED_MODULE_3__["default"],
  format: 'json',
  reconnection: true,
  connectManually: true,
  passToStoreHandler: function passToStoreHandler(eventName, event) {
    if (!(eventName === 'SOCKET_onmessage')) {
      return;
    }

    var data = JSON.parse(event.data);
    this.store.commit('journalState/SAVE_CELL_VALUE', {
      tableName: data['cell_location']['table_name'],
      fieldName: data['cell_location']['field_name'],
      index: data['cell_location']['index'],
      value: data['value']
    });
  }
});
window.mv = new vue_dist_vue_esm_js__WEBPACK_IMPORTED_MODULE_0__["default"]({
  el: '#app',
  router: _router__WEBPACK_IMPORTED_MODULE_2__["default"],
  store: _store_store__WEBPACK_IMPORTED_MODULE_3__["default"],
  render: function render(h) {
    return h(_App_vue__WEBPACK_IMPORTED_MODULE_1__["default"]);
  },
  mounted: function mounted() {}
});

/***/ }),

/***/ "./src/store/modules/journalState.js":
/*!*******************************************!*\
  !*** ./src/store/modules/journalState.js ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! core-js/modules/es6.function.name */ "./node_modules/core-js/modules/es6.function.name.js");
/* harmony import */ var core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_function_name__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var core_js_modules_web_dom_iterable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! core-js/modules/web.dom.iterable */ "./node_modules/core-js/modules/web.dom.iterable.js");
/* harmony import */ var core_js_modules_web_dom_iterable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_web_dom_iterable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var core_js_modules_es6_object_keys__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! core-js/modules/es6.object.keys */ "./node_modules/core-js/modules/es6.object.keys.js");
/* harmony import */ var core_js_modules_es6_object_keys__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_object_keys__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var core_js_modules_es6_array_iterator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! core-js/modules/es6.array.iterator */ "./node_modules/core-js/modules/es6.array.iterator.js");
/* harmony import */ var core_js_modules_es6_array_iterator__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_array_iterator__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var core_js_modules_es6_promise__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! core-js/modules/es6.promise */ "./node_modules/core-js/modules/es6.promise.js");
/* harmony import */ var core_js_modules_es6_promise__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es6_promise__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var core_js_modules_es7_promise_finally__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! core-js/modules/es7.promise.finally */ "./node_modules/core-js/modules/es7.promise.finally.js");
/* harmony import */ var core_js_modules_es7_promise_finally__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es7_promise_finally__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! axios */ "./node_modules/axios/index.js");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var vue_cookies__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! vue-cookies */ "./node_modules/vue-cookies/vue-cookies.js");
/* harmony import */ var vue_cookies__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(vue_cookies__WEBPACK_IMPORTED_MODULE_7__);








var journalState = {
  namespaced: true,
  state: {
    plantsInfo: [],
    journalInfo: {},
    loaded: false,
    socket: {
      isConnected: false,
      reconnectError: false
    }
  },
  getters: {
    loaded: function loaded(state) {
      return state.loaded;
    },
    journalInfo: function journalInfo(state) {
      return state.journalInfo;
    },
    tables: function tables(state) {
      if (state.loaded) {
        return Object.keys(state.journalInfo.journal.tables);
      } else {
        return [];
      }
    },
    plants: function plants(state) {
      return state.plantsInfo;
    },
    plantName: function plantName(state) {
      if (state.loaded) {
        return state.journalInfo.plant.name;
      } else {
        return '';
      }
    },
    plantVerboseName: function plantVerboseName(state) {
      if (state.loaded) {
        return state.journalInfo.plant.name;
      } else {
        return '';
      }
    },
    journalName: function journalName(state) {
      if (state.loaded) {
        return state.journalInfo.journal.name;
      } else {
        return '';
      }
    },
    journalVerboseName: function journalVerboseName(state) {
      if (state.loaded) {
        return state.journalInfo.journal.name;
      } else {
        return '';
      }
    },
    tableVerboseName: function tableVerboseName(state) {
      return function (tableName) {
        if (state.loaded) {
          return tableName;
        } else {
          return '';
        }
      };
    },
    fieldVerboseName: function fieldVerboseName(state) {
      return function (tableName, fieldName) {
        if (state.loaded) {
          return fieldName;
        } else {
          return '';
        }
      };
    },
    shiftOrder: function shiftOrder(state) {
      if (state.loaded) {
        return state.journalInfo.order;
      } else {
        return -1;
      }
    },
    cellValue: function cellValue(state) {
      return function (tableName, fieldName, rowIndex) {
        if (state.loaded) {
          var fields = state.journalInfo.journal.tables[tableName].fields;

          if (!(fieldName in fields)) {
            console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
            return '';
          }

          var cells = fields[fieldName].cells;

          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].value;
            } else {
              console.log('WARNING! Trying to get cell value with unexistent index: ' + fieldName + ' ' + rowIndex);
              return '';
            }
          } else {
            return '';
          }
        }
      };
    },
    cellComment: function cellComment(state) {
      return function (tableName, fieldName, rowIndex) {
        if (state.loaded) {
          var fields = state.journalInfo.journal.tables[tableName].fields;

          if (!(fieldName in fields)) {
            console.log('WARNING! Trying to get cell comment of unexistent field: ' + fieldName);
            return '';
          }

          var cells = fields[fieldName].cells;

          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].comment;
            } else {
              console.log('WARNING! Trying to get cell comment with unexistent index: ' + fieldName + ' ' + rowIndex);
              return '';
            }
          } else {
            return '';
          }
        }
      };
    },
    fieldCells: function fieldCells(state) {
      return function (tableName, fieldName) {
        if (state.loaded) {
          var fields = state.journalInfo.journal.tables[tableName].fields;

          if (fieldName in fields) {
            return state.journalInfo.journal.tables[tableName].fields[fieldName].cells;
          } else return [];
        } else {
          return [];
        }
      };
    },
    maxRowIndex: function maxRowIndex(state) {
      return function (tableName) {
        if (state.loaded) {
          var max = -1;
          var fields = state.journalInfo.journal.tables[tableName].fields;

          for (var field in fields) {
            for (var index in fields[field].cells) {
              index = parseInt(index);
              max = max < index ? index : max;
            }
          }

          return max + 1;
        } else {
          return -1;
        }
      };
    },
    rowIsEmpty: function rowIsEmpty(state) {
      return function (tableName, index) {
        if (state.loaded) {
          var fields = state.journalInfo.journal.tables[tableName].fields;

          for (var field in fields) {
            if ('cells' in fields[field]) {
              if (index in fields[field].cells) {
                return false;
              }
            }
          }

          return true;
        }
      };
    },
    tableTitle: function tableTitle(state) {
      return function (tableName) {
        return 'Заголовок таблицы';
      };
    },
    fieldDescription: function fieldDescription(state) {
      return function (tableName, fieldName) {
        if (state.loaded) {
          var fields = state.journalInfo.journal.tables[tableName].fields;

          if (!(fieldName in fields)) {
            console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
            return {};
          }

          return fields[fieldName].field_description || '';
        } else {
          return '';
        }
      };
    }
  },
  mutations: {
    UPDATE_JOURNAL_INFO: function UPDATE_JOURNAL_INFO(state, journalInfo) {
      state.journalInfo = journalInfo;
    },
    UPDATE_PLANTS_INFO: function UPDATE_PLANTS_INFO(state, plantsInfo) {
      state.plantsInfo = plantsInfo;
    },
    SET_LOADED: function SET_LOADED(state, loaded) {
      state.loaded = loaded;
    },
    SAVE_CELL_VALUE: function SAVE_CELL_VALUE(state, payload) {
      if (state.loaded) {
        var fields = state.journalInfo.journal.tables[payload.tableName].fields;

        if (!(payload.fieldName in fields)) {
          console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
          console.log('  Creating field ' + payload.fieldName + '...');
          fields[payload.fieldName] = {};
          fields[payload.fieldName]['cells'] = {};
        }

        var cells = fields[payload.fieldName].cells;

        if (payload.value) {
          if (payload.index in cells) {
            // update cell
            cells[payload.index]['value'] = payload.value;
          } else {
            // create cell
            Vue.set(cells, payload.index, {});
            Vue.set(cells[payload.index], 'value', payload.value);
          }
        } else {
          Vue.delete(cells, payload.index);
        }
      }
    },
    SAVE_CELL_COMMENT: function SAVE_CELL_COMMENT(state, payload) {
      if (state.loaded) {
        var fields = state.journalInfo.journal.tables[payload.tableName].fields;

        if (!(payload.fieldName in fields)) {
          console.log('WARNING! Trying to save comment of unexistent field: ' + payload.fieldName);
          console.log('  Creating field ' + payload.fieldName + '...');
          fields[payload.fieldName] = {};
          fields[payload.fieldName]['cells'] = {};
        }

        var cells = fields[payload.fieldName].cells;

        if (payload.comment) {
          if (payload.index in cells) {
            // update cell
            cells[payload.index]['comment'] = payload.comment;
          } else {
            // create cell
            Vue.set(cells, payload.index, {});
            Vue.set(cells[payload.index], 'comment', payload.comment);
          }
        } else {
          Vue.delete(cells, payload.index);
        }
      }
    },
    SET_PAGE_MODE: function SET_PAGE_MODE(state, mode) {
      if (state.loaded) {
        state.journalInfo.mode = mode;
      }
    },
    SOCKET_ONOPEN: function SOCKET_ONOPEN(state, event) {
      Vue.prototype.$socket = event.currentTarget;
      state.socket.isConnected = true;
    },
    SOCKET_ONCLOSE: function SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false;
    },
    SOCKET_ONERROR: function SOCKET_ONERROR(state, event) {
      console.error(state, event);
    },
    SOCKET_ONMESSAGE: function SOCKET_ONMESSAGE(state, message) {},
    SOCKET_RECONNECT: function SOCKET_RECONNECT(state, count) {
      console.info(state, count);
    },
    SOCKET_RECONNECT_ERROR: function SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    }
  },
  actions: {
    loadJournal: function loadJournal(_ref, payload) {
      var commit = _ref.commit,
          state = _ref.state,
          getters = _ref.getters;
      return new Promise(function (res, rej) {
        axios__WEBPACK_IMPORTED_MODULE_6___default.a.get('http://localhost:8000/api/shifts/' + payload, {
          withCredentials: true
        }).then(function (response) {
          commit('UPDATE_JOURNAL_INFO', response.data);
          commit('SET_LOADED', true);
        }).then(function () {
          res();
        }).catch(function (err) {
          console.log(err);
        });
      });
    },
    loadPlants: function loadPlants(_ref2) {
      var commit = _ref2.commit,
          state = _ref2.state,
          getters = _ref2.getters;
      axios__WEBPACK_IMPORTED_MODULE_6___default.a.get('http://localhost:8000/api/menu_info/').then(function (response) {
        commit('UPDATE_PLANTS_INFO', response.data.plants);
      });
    }
  }
};
/* harmony default export */ __webpack_exports__["default"] = (journalState);

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vc3JjL2NvbXBvbmVudHMvQmFzZVBhZ2UudnVlIiwid2VicGFjazovLy9zcmMvY29tcG9uZW50cy9DZWxsLnZ1ZSIsIndlYnBhY2s6Ly8vc3JjL2NvbXBvbmVudHMvSm91cm5hbFBhbmVsLnZ1ZSIsIndlYnBhY2s6Ly8vLi9zcmMvY29tcG9uZW50cy9CYXNlUGFnZS52dWU/ZmNkNCIsIndlYnBhY2s6Ly8vLi9zcmMvY29tcG9uZW50cy9Kb3VybmFsUGFuZWwudnVlP2NhYzkiLCJ3ZWJwYWNrOi8vLy4vc3JjL2NvbXBvbmVudHMvQ2VsbC52dWU/ZjlmZSIsIndlYnBhY2s6Ly8vLi9zcmMvYXNzZXRzL2pzL2luZGV4LmpzIiwid2VicGFjazovLy8uL3NyYy9tYWluLmpzIiwid2VicGFjazovLy8uL3NyYy9zdG9yZS9tb2R1bGVzL2pvdXJuYWxTdGF0ZS5qcyJdLCJuYW1lcyI6WyJ3aW5kb3ciLCIkIiwialF1ZXJ5IiwiXyIsIlZ1ZSIsImNvbmZpZyIsInByb2R1Y3Rpb25UaXAiLCJkYXRhRW5kcG9pbnQiLCJsb2NhdGlvbiIsImhvc3RuYW1lIiwidXNlIiwiVnVlTmF0aXZlU29jayIsInN0b3JlIiwiZm9ybWF0IiwicmVjb25uZWN0aW9uIiwiY29ubmVjdE1hbnVhbGx5IiwicGFzc1RvU3RvcmVIYW5kbGVyIiwiZXZlbnROYW1lIiwiZXZlbnQiLCJkYXRhIiwiSlNPTiIsInBhcnNlIiwiY29tbWl0IiwidGFibGVOYW1lIiwiZmllbGROYW1lIiwiaW5kZXgiLCJ2YWx1ZSIsIm12IiwiZWwiLCJyb3V0ZXIiLCJyZW5kZXIiLCJoIiwiQXBwIiwibW91bnRlZCIsImpvdXJuYWxTdGF0ZSIsIm5hbWVzcGFjZWQiLCJzdGF0ZSIsInBsYW50c0luZm8iLCJqb3VybmFsSW5mbyIsImxvYWRlZCIsInNvY2tldCIsImlzQ29ubmVjdGVkIiwicmVjb25uZWN0RXJyb3IiLCJnZXR0ZXJzIiwidGFibGVzIiwiT2JqZWN0Iiwia2V5cyIsImpvdXJuYWwiLCJwbGFudHMiLCJwbGFudE5hbWUiLCJwbGFudCIsIm5hbWUiLCJwbGFudFZlcmJvc2VOYW1lIiwiam91cm5hbE5hbWUiLCJqb3VybmFsVmVyYm9zZU5hbWUiLCJ0YWJsZVZlcmJvc2VOYW1lIiwiZmllbGRWZXJib3NlTmFtZSIsInNoaWZ0T3JkZXIiLCJvcmRlciIsImNlbGxWYWx1ZSIsInJvd0luZGV4IiwiZmllbGRzIiwiY29uc29sZSIsImxvZyIsImNlbGxzIiwibGVuZ3RoIiwiY2VsbENvbW1lbnQiLCJjb21tZW50IiwiZmllbGRDZWxscyIsIm1heFJvd0luZGV4IiwibWF4IiwiZmllbGQiLCJwYXJzZUludCIsInJvd0lzRW1wdHkiLCJ0YWJsZVRpdGxlIiwiZmllbGREZXNjcmlwdGlvbiIsImZpZWxkX2Rlc2NyaXB0aW9uIiwibXV0YXRpb25zIiwiVVBEQVRFX0pPVVJOQUxfSU5GTyIsIlVQREFURV9QTEFOVFNfSU5GTyIsIlNFVF9MT0FERUQiLCJTQVZFX0NFTExfVkFMVUUiLCJwYXlsb2FkIiwic2V0IiwiZGVsZXRlIiwiU0FWRV9DRUxMX0NPTU1FTlQiLCJTRVRfUEFHRV9NT0RFIiwibW9kZSIsIlNPQ0tFVF9PTk9QRU4iLCJwcm90b3R5cGUiLCIkc29ja2V0IiwiY3VycmVudFRhcmdldCIsIlNPQ0tFVF9PTkNMT1NFIiwiU09DS0VUX09ORVJST1IiLCJlcnJvciIsIlNPQ0tFVF9PTk1FU1NBR0UiLCJtZXNzYWdlIiwiU09DS0VUX1JFQ09OTkVDVCIsImNvdW50IiwiaW5mbyIsIlNPQ0tFVF9SRUNPTk5FQ1RfRVJST1IiLCJhY3Rpb25zIiwibG9hZEpvdXJuYWwiLCJQcm9taXNlIiwicmVzIiwicmVqIiwiYXhpb3MiLCJnZXQiLCJ3aXRoQ3JlZGVudGlhbHMiLCJ0aGVuIiwicmVzcG9uc2UiLCJjYXRjaCIsImVyciIsImxvYWRQbGFudHMiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFpQkE7QUFDQTtBQUNBO0FBQ0E7QUFFQTtBQUNBLGtCQURBO0FBRUE7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QTJCLFFBQTNCQSxLQUEyQjtBQUFBLFVBQXBCTyxPQUFvQixRQUFwQkEsT0FBb0I7QUFDeEQsYUFBTyxJQUFJNEQsT0FBSixDQUFZLFVBQUNDLEdBQUQsRUFBTUMsR0FBTixFQUFjO0FBQzdCQyxvREFBS0EsQ0FDQUMsR0FETCxDQUNTLHNDQUFzQ3pCLE9BRC9DLEVBQ3dEO0FBQ2hEMEIsMkJBQWlCO0FBRCtCLFNBRHhELEVBSUtDLElBSkwsQ0FJVSxvQkFBWTtBQUNkdkYsaUJBQU8scUJBQVAsRUFBOEJ3RixTQUFTM0YsSUFBdkM7QUFDQUcsaUJBQU8sWUFBUCxFQUFxQixJQUFyQjtBQUNILFNBUEwsRUFRS3VGLElBUkwsQ0FRVSxZQUFNO0FBQ1JMO0FBQ0gsU0FWTCxFQVdLTyxLQVhMLENBV1csVUFBQ0MsR0FBRCxFQUFTO0FBQ1psRCxrQkFBUUMsR0FBUixDQUFZaUQsR0FBWjtBQUNILFNBYkw7QUFjSCxPQWZNLENBQVA7QUFnQkgsS0FsQkk7QUFtQkxDLGdCQUFZLDJCQUFzQztBQUFBLFVBQTFCM0YsTUFBMEIsU0FBMUJBLE1BQTBCO0FBQUEsVUFBbEJjLEtBQWtCLFNBQWxCQSxLQUFrQjtBQUFBLFVBQVhPLE9BQVcsU0FBWEEsT0FBVztBQUM5QytELGtEQUFLQSxDQUNBQyxHQURMLENBQ1Msc0NBRFQsRUFFS0UsSUFGTCxDQUVVLG9CQUFZO0FBQ2R2RixlQUFPLG9CQUFQLEVBQTZCd0YsU0FBUzNGLElBQVQsQ0FBYzZCLE1BQTNDO0FBQ0gsT0FKTDtBQUtIO0FBekJJO0FBcFFRLENBQXJCO0FBaVNlZCwyRUFBZixFIiwiZmlsZSI6Im1haW4uMmQ4Y2E2OWRhMDRiM2RlMGMyOTguaG90LXVwZGF0ZS5qcyIsInNvdXJjZXNDb250ZW50IjpbIjx0ZW1wbGF0ZT5cbiAgICA8ZGl2IGNsYXNzPVwiZWxvZ3MtY29udGFpbmVyXCI+XG4gICAgICAgIDx0b3AtbmF2PjwvdG9wLW5hdj5cbiAgICAgICAgPGRpdiBjbGFzcz1cIm1haW4tY29udGFpbmVyXCI+XG4gICAgICAgICAgICA8bmF2IGNsYXNzPVwiY29sdW1uLWxlZnRcIj5cbiAgICAgICAgICAgICAgICA8bGVmdC1tZW51PjwvbGVmdC1tZW51PlxuICAgICAgICAgICAgPC9uYXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzPVwiY29sdW1uLWNvbnRlbnRcIiBpZD1cImVsb2dzLWFwcFwiPlxuICAgICAgICAgICAgICAgIDxyb3V0ZXItdmlldz48L3JvdXRlci12aWV3PlxuICAgICAgICAgICAgICAgIDxtYWluLWZvb3Rlcj48L21haW4tZm9vdGVyPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8cG9wdXA+PC9wb3B1cD5cbiAgICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQ+XG5pbXBvcnQgVG9wTmF2IGZyb20gJy4vVG9wTmF2LnZ1ZSdcbmltcG9ydCBNZW51IGZyb20gJy4vTWVudS52dWUnXG5pbXBvcnQgRm9vdGVyIGZyb20gJy4vRm9vdGVyLnZ1ZSdcbmltcG9ydCBQb3B1cCBmcm9tICcuL1BvcHVwLnZ1ZSc7XG5cbmV4cG9ydCBkZWZhdWx0IHtcbiAgICBuYW1lOiBcIkJhc2VQYWdlXCIsXG4gICAgY29tcG9uZW50czoge1xuICAgICAgICAndG9wLW5hdic6IFRvcE5hdixcbiAgICAgICAgJ2xlZnQtbWVudSc6IE1lbnUsXG4gICAgICAgICdtYWluLWZvb3Rlcic6IEZvb3RlcixcbiAgICAgICAgJ3BvcHVwJzogUG9wdXAsXG4gICAgfSxcbiAgICBtb3VudGVkICgpIHtcbiAgICAgICAgaWYgKHRoaXMuJHJvdXRlLnBhcmFtcy5zaGlmdF9pZCkge1xuICAgICAgICAgICAgdGhpcy4kc3RvcmUuZGlzcGF0Y2goJ2pvdXJuYWxTdGF0ZS9sb2FkSm91cm5hbCcsIHRoaXMuJHJvdXRlLnBhcmFtcy5zaGlmdF9pZClcbiAgICAgICAgfVxuICAgIH1cbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuXG48L3N0eWxlPiIsIjx0ZW1wbGF0ZT5cbiAgICA8di1wb3BvdmVyXG4gICAgICAgICAgICBvZmZzZXQ9XCIxNlwiXG4gICAgICAgICAgICA6ZGlzYWJsZWQ9XCJtb2RlICE9PSAndmFsaWRhdGUnXCI+XG4gICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgIDpjbGFzcz1cImNsYXNzZXNcIlxuICAgICAgICAgICAgICAgIDpuYW1lPVwiZmllbGROYW1lXCJcbiAgICAgICAgICAgICAgICA6cm93LWluZGV4PVwicm93SW5kZXhcIlxuICAgICAgICAgICAgICAgIDp2YWx1ZT1cInZhbHVlXCJcbiAgICAgICAgICAgICAgICBAa2V5cHJlc3M9XCJmaWx0ZXJJbnB1dFwiXG4gICAgICAgICAgICAgICAgQGtleWRvd249XCJjaGFuZ2VGb2N1c1wiXG4gICAgICAgICAgICAgICAgQGNoYW5nZT1cIm9uQ2hhbmdlZFwiXG4gICAgICAgICAgICAgICAgQGlucHV0PVwib25JbnB1dFwiXG4gICAgICAgICAgICAgICAgQGJsdXI9XCJzaG93Q2VsbFR5cGVUb29sdGlwPWZhbHNlXCJcbiAgICAgICAgICAgICAgICA6cmVhZG9ubHk9XCJtb2RlICE9PSAnZWRpdCdcIlxuICAgICAgICAgICAgICAgIDpwbGFjZWhvbGRlcj1cInBsYWNlaG9sZGVyXCJcbiAgICAgICAgICAgICAgICA6c3R5bGU9XCJ7IGNvbG9yOiBhY3RpdmVDb2xvciB9XCJcbiAgICAgICAgICAgICAgICA6dHlwZT1cInR5cGVcIlxuICAgICAgICAgICAgICAgIHYtdG9vbHRpcD1cIntjb250ZW50OiAn0JLQstC10LTQuNGC0LUg0YfQuNGB0LvQvicsIHNob3c6IHNob3dDZWxsVHlwZVRvb2x0aXAsIHRyaWdnZXI6ICdtYW51YWwnfVwiXG4gICAgICAgID5cbiAgICAgICAgPGlcbiAgICAgICAgICAgICAgICB2LWlmPVwiJHN0b3JlLmdldHRlcnNbJ2pvdXJuYWxTdGF0ZS9jZWxsQ29tbWVudCddKHRhYmxlTmFtZSwgZmllbGROYW1lLCByb3dJbmRleClcIlxuICAgICAgICAgICAgICAgIGNsYXNzPVwiZmFyIGZhLWVudmVsb3BlIGNvbW1lbnQtbm90aWZpY2F0aW9uXCI+PC9pPlxuICAgICAgICA8dGVtcGxhdGUgc2xvdD1cInBvcG92ZXJcIj5cbiAgICAgICAgICAgIDxDZWxsQ29tbWVudFxuICAgICAgICAgICAgICAgICAgICA6dGFibGUtbmFtZT1cInRhYmxlTmFtZVwiXG4gICAgICAgICAgICAgICAgICAgIDpmaWVsZC1uYW1lPVwiZmllbGROYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgOnJvdy1pbmRleD1cInJvd0luZGV4XCIvPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgIDwvdi1wb3BvdmVyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdD5cbiAgICBpbXBvcnQgVnVlIGZyb20gJ3Z1ZS9kaXN0L3Z1ZS5lc20uanMnXG4gICAgaW1wb3J0IHtWVG9vbHRpcCwgVlBvcG92ZXIsIFZDbG9zZVBvcG92ZXJ9IGZyb20gJ3YtdG9vbHRpcCdcbiAgICBpbXBvcnQgQ2VsbENvbW1lbnQgZnJvbSAnLi9DZWxsQ29tbWVudC52dWUnXG4gICAgaW1wb3J0ICdjbG9ja3BpY2tlci9kaXN0L2Jvb3RzdHJhcC1jbG9ja3BpY2tlci5taW4nXG5cbiAgICBWdWUuZGlyZWN0aXZlKCd0b29sdGlwJywgVlRvb2x0aXApO1xuICAgIFZ1ZS5kaXJlY3RpdmUoJ2Nsb3NlLXBvcG92ZXInLCBWQ2xvc2VQb3BvdmVyKTtcbiAgICBWdWUuY29tcG9uZW50KCd2LXBvcG92ZXInLCBWUG9wb3Zlcik7XG4gICAgVnVlLmNvbXBvbmVudCgnQ2VsbENvbW1lbnQnLCBDZWxsQ29tbWVudCk7XG5cblxuICAgIGV4cG9ydCBkZWZhdWx0IHtcbiAgICAgICAgbmFtZTogJ0NlbGwnLFxuICAgICAgICBwcm9wczogW1xuICAgICAgICAgICAgJ2ZpZWxkTmFtZScsXG4gICAgICAgICAgICAncm93SW5kZXgnLFxuICAgICAgICAgICAgJ2xpbmtlZCdcbiAgICAgICAgXSxcbiAgICAgICAgZGF0YSgpIHtcbiAgICAgICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICAgICAgY2xhc3NlczogJ2dlbmVyYWwtdmFsdWUgbnVtYmVyLWNlbGwgZm9ybS1jb250cm9sJyxcbiAgICAgICAgICAgICAgICBtaW5WYWx1ZTogbnVsbCxcbiAgICAgICAgICAgICAgICBtYXhWYWx1ZTogbnVsbCxcbiAgICAgICAgICAgICAgICB0eXBlOiBudWxsLFxuICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyOiAnJyxcbiAgICAgICAgICAgICAgICBzaG93Q2VsbFR5cGVUb29sdGlwOiBmYWxzZVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICB3YXRjaDoge1xuICAgICAgICAgICAgbW9kZSAodmFsdWUpIHtcbiAgICAgICAgICAgICAgICBpZiAodGhpcy50eXBlID09PSAndGltZScpIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHZhbHVlID09PSAnZWRpdCcpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdlZGl0JylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKHRoaXMuJGVsKS5maW5kKCdpbnB1dCcpLmNsb2NrcGlja2VyKHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXV0b2Nsb3NlOiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnZGVmYXVsdCc6ICdub3cnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb25ldGV4dDogZmFsc2UsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFmdGVyRG9uZTogKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy52YWx1ZSA9ICQodGhpcy4kZWwpLmZpbmQoJ2lucHV0JykudmFsKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ25vdC1lZGl0JylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKHRoaXMuJGVsKS5maW5kKCdpbnB1dCcpLmNsb2NrcGlja2VyKCdyZW1vdmUnKVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBjb21wdXRlZDoge1xuICAgICAgICAgICAgdGFibGVOYW1lOiBmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICAgICAgaWYgKHR5cGVvZiB0aGlzLiRwYXJlbnQucHJvcHMgIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB0aGlzLiRwYXJlbnQucHJvcHMubmFtZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJ1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBhY3RpdmVDb2xvcjogZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgICAgIHJldHVybiB0aGlzLmNyaXRpY2FsID8gJ3JlZCcgOiAnJztcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBjcml0aWNhbDogZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgICAgIHJldHVybiAodGhpcy5taW5WYWx1ZSAmJiAodGhpcy52YWx1ZSA8IHRoaXMubWluVmFsdWUpKSB8fFxuICAgICAgICAgICAgICAgICAgICAodGhpcy5tYXhWYWx1ZSAmJiAodGhpcy52YWx1ZSA+IHRoaXMubWF4VmFsdWUpKTtcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICB2YWx1ZToge1xuICAgICAgICAgICAgICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2NlbGxWYWx1ZSddKHRoaXMudGFibGVOYW1lLCB0aGlzLmZpZWxkTmFtZSwgdGhpcy5yb3dJbmRleCk7XG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICBzZXQ6IGZ1bmN0aW9uICh2YWwpIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy4kc3RvcmUuY29tbWl0KCdqb3VybmFsU3RhdGUvU0FWRV9DRUxMX1ZBTFVFJywge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGFibGVOYW1lOiB0aGlzLnRhYmxlTmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGZpZWxkTmFtZTogdGhpcy5maWVsZE5hbWUsXG4gICAgICAgICAgICAgICAgICAgICAgICBpbmRleDogdGhpcy5yb3dJbmRleCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiB2YWxcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIG1vZGUoKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHRoaXMuJHN0b3JlLmdldHRlcnNbJ2pvdXJuYWxTdGF0ZS9qb3VybmFsSW5mbyddLm1vZGU7XG4gICAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgICBtZXRob2RzOiB7XG4gICAgICAgICAgICBzZW5kKCkge1xuICAgICAgICAgICAgICAgIHRoaXMuJHNvY2tldC5zZW5kT2JqKHtcbiAgICAgICAgICAgICAgICAgICAgJ3R5cGUnOiAnc2hpZnRfZGF0YScsXG4gICAgICAgICAgICAgICAgICAgICdjZWxsX2xvY2F0aW9uJzoge1xuICAgICAgICAgICAgICAgICAgICAgICAgJ2dyb3VwX2lkJzogdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2pvdXJuYWxJbmZvJ10uaWQsXG4gICAgICAgICAgICAgICAgICAgICAgICAndGFibGVfbmFtZSc6IHRoaXMudGFibGVOYW1lLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ2ZpZWxkX25hbWUnOiB0aGlzLmZpZWxkTmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICdpbmRleCc6IHRoaXMucm93SW5kZXhcbiAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgJ3ZhbHVlJzogdGhpcy52YWx1ZVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIG9uSW5wdXQoZSkge1xuICAgICAgICAgICAgICAgIHRoaXMudmFsdWUgPSBlLnRhcmdldC52YWx1ZTtcbiAgICAgICAgICAgICAgICB0aGlzLnNlbmQoKTtcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBvbkNoYW5nZWQoKSB7XG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgZmlsdGVySW5wdXQoZSkge1xuICAgICAgICAgICAgICAgIGlmICh0aGlzLnR5cGUgPT09ICdudW1iZXInKSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCBrZXljb2RlID0gZS53aGljaFxuICAgICAgICAgICAgICAgICAgICAvLyBpZiBub24gbnVtYmVyIGNoYXJhY3RlciB3YXMgcHJlc3NlZFxuICAgICAgICAgICAgICAgICAgICBpZiAoIShlLnNoaWZ0S2V5ID09IGZhbHNlICYmICgoa2V5Y29kZSA9PSA0NSAmJiB0aGlzLnZhbHVlID09ICcnKSB8fCBrZXljb2RlID09IDQ2XG4gICAgICAgICAgICAgICAgICAgICAgICB8fCBrZXljb2RlID09IDggfHwga2V5Y29kZSA9PSAzNyB8fCBrZXljb2RlID09IDM5IHx8IChrZXljb2RlID49IDQ4ICYmIGtleWNvZGUgPD0gNTcpKSkpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2hvd0NlbGxUeXBlVG9vbHRpcCA9IHRydWU7XG4gICAgICAgICAgICAgICAgICAgICAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zaG93Q2VsbFR5cGVUb29sdGlwID0gZmFsc2U7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9LFxuXG4gICAgICAgICAgICBjaGFuZ2VGb2N1cyhlKSB7XG4gICAgICAgICAgICAgICAgZnVuY3Rpb24gZ2V0SW5kZXgodGRzLCBmb2N1c2VkVGQpIHtcbiAgICAgICAgICAgICAgICAgICAgbGV0IGluZGV4ID0gMFxuICAgICAgICAgICAgICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRkcy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgICAgICAgICAgICAgbGV0IHRkID0gdGRzW2ldO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKHRkID09PSBmb2N1c2VkVGQpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIGluZGV4ICs9IChwYXJzZUludCh0ZC5nZXRBdHRyaWJ1dGUoJ2NvbHNwYW4nKSwgMTApIHx8IDEpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBpbmRleDtcbiAgICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgICBmdW5jdGlvbiBnZXRUZCh0ZHMsIGluZGV4KSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCBuZXh0Um93SW5kZXggPSAwXG4gICAgICAgICAgICAgICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBsZXQgdGQgPSB0ZHNbaV07XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAobmV4dFJvd0luZGV4ID09PSBpbmRleCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiB0ZDtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIG5leHRSb3dJbmRleCArPSAocGFyc2VJbnQodGQuZ2V0QXR0cmlidXRlKCdjb2xzcGFuJyksIDEwKSB8fCAxKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgICAgIGxldCBmb2N1c2VkVGQgPSB0aGlzLiRlbC5wYXJlbnRFbGVtZW50O1xuICAgICAgICAgICAgICAgIGxldCB0ciA9IGZvY3VzZWRUZC5wYXJlbnRFbGVtZW50O1xuICAgICAgICAgICAgICAgIGxldCByb3dJbmRleCA9IGdldEluZGV4KHRyLmNoaWxkcmVuLCBmb2N1c2VkVGQpO1xuXG4gICAgICAgICAgICAgICAgc3dpdGNoIChlLmtleSkge1xuICAgICAgICAgICAgICAgICAgICBjYXNlICdBcnJvd1VwJzpcbiAgICAgICAgICAgICAgICAgICAgICAgIGxldCBwcmV2VHIgPSB0ci5wcmV2aW91c0VsZW1lbnRTaWJsaW5nO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKHByZXZUcikge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdldFRkKHByZXZUci5jaGlsZHJlbiwgcm93SW5kZXgpLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLnNlbGVjdCgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ0Fycm93RG93bic6XG4gICAgICAgICAgICAgICAgICAgICAgICBsZXQgbmV4dFRyID0gdHIubmV4dEVsZW1lbnRTaWJsaW5nO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKG5leHRUcikge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdldFRkKG5leHRUci5jaGlsZHJlbiwgcm93SW5kZXgpLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLnNlbGVjdCgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ0Fycm93TGVmdCc6XG4gICAgICAgICAgICAgICAgICAgICAgICBsZXQgcHJldlRkID0gZm9jdXNlZFRkLnByZXZpb3VzRWxlbWVudFNpYmxpbmc7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAocHJldlRkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcHJldlRkLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLnNlbGVjdCgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ0Fycm93UmlnaHQnOlxuICAgICAgICAgICAgICAgICAgICAgICAgbGV0IG5leHRUZCA9IGZvY3VzZWRUZC5uZXh0RWxlbWVudFNpYmxpbmc7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAobmV4dFRkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgbmV4dFRkLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLmNoaWxkcmVuWzBdLnNlbGVjdCgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBtb3VudGVkKCkge1xuICAgICAgICAgICAgLy8gaW5pdGlhbGl6aW5nIGRhdGFcbiAgICAgICAgICAgIGxldCBkZXNjID0gdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2ZpZWxkRGVzY3JpcHRpb24nXSh0aGlzLnRhYmxlTmFtZSwgdGhpcy5maWVsZE5hbWUpO1xuICAgICAgICAgICAgdGhpcy5wbGFjZWhvbGRlciA9IGRlc2NbJ3VuaXRzJ10gfHwgJyc7XG4gICAgICAgICAgICB0aGlzLm1pblZhbHVlID0gZGVzY1snbWluX25vcm1hbCddIHx8IG51bGw7XG4gICAgICAgICAgICB0aGlzLm1heFZhbHVlID0gZGVzY1snbWF4X25vcm1hbCddIHx8IG51bGw7XG4gICAgICAgICAgICB0aGlzLnR5cGUgPSBkZXNjWyd0eXBlJ10gfHwgJ3RleHQnO1xuXG4gICAgICAgICAgICBpZiAodGhpcy5saW5rZWQpIHtcbiAgICAgICAgICAgICAgICAvLyBhdXRvIGZpbGwgY2VsbFxuICAgICAgICAgICAgICAgIHRoaXMudmFsdWUgPSB0aGlzLiRzdG9yZS5nZXR0ZXJzWydqb3VybmFsU3RhdGUvJyArIHRoaXMubGlua2VkXTtcbiAgICAgICAgICAgICAgICB0aGlzLnNlbmQoKTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgLy8gaWYgKHRoaXMudHlwZSA9PT0gJ2RhdGUnKSB7XG4gICAgICAgICAgICAvLyAgICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgICAgICAvLyAgICAgICAgICQodGhpcy4kZWwpLmRhdGVwaWNrZXIoe1xuICAgICAgICAgICAgLy8gICAgICAgICAgICAgZm9ybWF0OiAneXl5eS1tbS1kZCcsXG4gICAgICAgICAgICAvLyAgICAgICAgICAgICBhdXRvY2xvc2U6IHRydWUsXG4gICAgICAgICAgICAvLyAgICAgICAgICAgICBlbmREYXRlOiAnKzBkJyxcbiAgICAgICAgICAgIC8vICAgICAgICAgfSlcbiAgICAgICAgICAgIC8vICAgICB9LCAwKVxuICAgICAgICAgICAgLy8gfVxuICAgICAgICB9XG4gICAgfVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBsYW5nPVwic2Nzc1wiPlxuICAgIC50b29sdGlwIHtcbiAgICAgICAgZGlzcGxheTogYmxvY2sgIWltcG9ydGFudDtcbiAgICAgICAgei1pbmRleDogMTAwMDA7XG5cbiAgICAgICAgLnRvb2x0aXAtaW5uZXIge1xuICAgICAgICAgICAgbWF4LXdpZHRoOiA0NTBweDtcbiAgICAgICAgICAgIGJhY2tncm91bmQ6IGJsYWNrO1xuICAgICAgICAgICAgY29sb3I6IHdoaXRlO1xuICAgICAgICAgICAgYm9yZGVyLXJhZGl1czogMTZweDtcbiAgICAgICAgICAgIHBhZGRpbmc6IDVweCAxMHB4IDRweDtcbiAgICAgICAgfVxuXG4gICAgICAgIC50b29sdGlwLWFycm93IHtcbiAgICAgICAgICAgIHdpZHRoOiAwO1xuICAgICAgICAgICAgaGVpZ2h0OiAwO1xuICAgICAgICAgICAgYm9yZGVyLXN0eWxlOiBzb2xpZDtcbiAgICAgICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICAgICAgICAgIG1hcmdpbjogNXB4O1xuICAgICAgICAgICAgYm9yZGVyLWNvbG9yOiBibGFjaztcbiAgICAgICAgICAgIHotaW5kZXg6IDE7XG4gICAgICAgIH1cblxuICAgICAgICAmW3gtcGxhY2VtZW50Xj1cInRvcFwiXSB7XG4gICAgICAgICAgICBtYXJnaW4tYm90dG9tOiA1cHg7XG5cbiAgICAgICAgICAgIC50b29sdGlwLWFycm93IHtcbiAgICAgICAgICAgICAgICBib3JkZXItd2lkdGg6IDVweCA1cHggMCA1cHg7XG4gICAgICAgICAgICAgICAgYm9yZGVyLWxlZnQtY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgYm9yZGVyLXJpZ2h0LWNvbG9yOiB0cmFuc3BhcmVudCAhaW1wb3J0YW50O1xuICAgICAgICAgICAgICAgIGJvcmRlci1ib3R0b20tY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgYm90dG9tOiAtNXB4O1xuICAgICAgICAgICAgICAgIGxlZnQ6IGNhbGMoNTAlIC0gNXB4KTtcbiAgICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAwO1xuICAgICAgICAgICAgICAgIG1hcmdpbi1ib3R0b206IDA7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICAmW3gtcGxhY2VtZW50Xj1cImJvdHRvbVwiXSB7XG4gICAgICAgICAgICBtYXJnaW4tdG9wOiA1cHg7XG5cbiAgICAgICAgICAgIC50b29sdGlwLWFycm93IHtcbiAgICAgICAgICAgICAgICBib3JkZXItd2lkdGg6IDAgNXB4IDVweCA1cHg7XG4gICAgICAgICAgICAgICAgYm9yZGVyLWxlZnQtY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgYm9yZGVyLXJpZ2h0LWNvbG9yOiB0cmFuc3BhcmVudCAhaW1wb3J0YW50O1xuICAgICAgICAgICAgICAgIGJvcmRlci10b3AtY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgdG9wOiAtNXB4O1xuICAgICAgICAgICAgICAgIGxlZnQ6IGNhbGMoNTAlIC0gNXB4KTtcbiAgICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAwO1xuICAgICAgICAgICAgICAgIG1hcmdpbi1ib3R0b206IDA7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICAmW3gtcGxhY2VtZW50Xj1cInJpZ2h0XCJdIHtcbiAgICAgICAgICAgIG1hcmdpbi1sZWZ0OiA1cHg7XG5cbiAgICAgICAgICAgIC50b29sdGlwLWFycm93IHtcbiAgICAgICAgICAgICAgICBib3JkZXItd2lkdGg6IDVweCA1cHggNXB4IDA7XG4gICAgICAgICAgICAgICAgYm9yZGVyLWxlZnQtY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgYm9yZGVyLXRvcC1jb2xvcjogdHJhbnNwYXJlbnQgIWltcG9ydGFudDtcbiAgICAgICAgICAgICAgICBib3JkZXItYm90dG9tLWNvbG9yOiB0cmFuc3BhcmVudCAhaW1wb3J0YW50O1xuICAgICAgICAgICAgICAgIGxlZnQ6IC01cHg7XG4gICAgICAgICAgICAgICAgdG9wOiBjYWxjKDUwJSAtIDVweCk7XG4gICAgICAgICAgICAgICAgbWFyZ2luLWxlZnQ6IDA7XG4gICAgICAgICAgICAgICAgbWFyZ2luLXJpZ2h0OiAwO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgJlt4LXBsYWNlbWVudF49XCJsZWZ0XCJdIHtcbiAgICAgICAgICAgIG1hcmdpbi1yaWdodDogNXB4O1xuXG4gICAgICAgICAgICAudG9vbHRpcC1hcnJvdyB7XG4gICAgICAgICAgICAgICAgYm9yZGVyLXdpZHRoOiA1cHggMCA1cHggNXB4O1xuICAgICAgICAgICAgICAgIGJvcmRlci10b3AtY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgYm9yZGVyLXJpZ2h0LWNvbG9yOiB0cmFuc3BhcmVudCAhaW1wb3J0YW50O1xuICAgICAgICAgICAgICAgIGJvcmRlci1ib3R0b20tY29sb3I6IHRyYW5zcGFyZW50ICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICAgICAgcmlnaHQ6IC01cHg7XG4gICAgICAgICAgICAgICAgdG9wOiBjYWxjKDUwJSAtIDVweCk7XG4gICAgICAgICAgICAgICAgbWFyZ2luLWxlZnQ6IDA7XG4gICAgICAgICAgICAgICAgbWFyZ2luLXJpZ2h0OiAwO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgJi5wb3BvdmVyIHtcbiAgICAgICAgICAgICRjb2xvcjogI2Y5ZjlmOTtcblxuICAgICAgICAgICAgLnBvcG92ZXItaW5uZXIge1xuICAgICAgICAgICAgICAgIGJhY2tncm91bmQ6ICRjb2xvcjtcbiAgICAgICAgICAgICAgICBjb2xvcjogYmxhY2s7XG4gICAgICAgICAgICAgICAgcGFkZGluZzogMHB4O1xuICAgICAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDVweDtcbiAgICAgICAgICAgICAgICBib3gtc2hhZG93OiAwIDVweCAzMHB4IHJnYmEoYmxhY2ssIC4xKTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgLnBvcG92ZXItYXJyb3cge1xuICAgICAgICAgICAgICAgIGJvcmRlci1jb2xvcjogJGNvbG9yO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgJlthcmlhLWhpZGRlbj0ndHJ1ZSddIHtcbiAgICAgICAgICAgIHZpc2liaWxpdHk6IGhpZGRlbjtcbiAgICAgICAgICAgIG9wYWNpdHk6IDA7XG4gICAgICAgICAgICB0cmFuc2l0aW9uOiBvcGFjaXR5IC4xNXMsIHZpc2liaWxpdHkgLjE1cztcbiAgICAgICAgfVxuXG4gICAgICAgICZbYXJpYS1oaWRkZW49J2ZhbHNlJ10ge1xuICAgICAgICAgICAgdmlzaWJpbGl0eTogdmlzaWJsZTtcbiAgICAgICAgICAgIG9wYWNpdHk6IDE7XG4gICAgICAgICAgICB0cmFuc2l0aW9uOiBvcGFjaXR5IC4xNXM7XG4gICAgICAgIH1cbiAgICB9XG48L3N0eWxlPiIsIjx0ZW1wbGF0ZT5cbiAgICA8ZGl2IGNsYXNzPVwiam91cm5hbF9fcGFuZWxcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRhdGUtc2VsZWN0b3JcIj5cbiAgICAgICAgICAgIDxsYWJlbD7QktGL0LHQtdGA0LjRgtC1INC00LDRgtGDINC4INGB0LzQtdC90YM8L2xhYmVsPlxuICAgICAgICAgICAgPGlucHV0IGlkPVwic2hpZnRfZmllbGRcIlxuICAgICAgICAgICAgICAgICAgIHR5cGU9XCJ0ZXh0XCJcbiAgICAgICAgICAgICAgICAgICA6dmFsdWU9XCJzaGlmdERhdGUgKyAnLCAnICsgc2hpZnRPcmRlciArICct0LDRjyDRgdC80LXQvdCwJ1wiXG4gICAgICAgICAgICAgICAgICAgQGNsaWNrPVwic2hvd0NhbGVuZGFyPXRydWVcIlxuICAgICAgICAgICAgICAgICAgIGNsYXNzPVwiZGF0ZS1zZWxlY3Rvcl9fZGF0ZVwiXG4gICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9XCLQktGL0LHQtdGA0LjRgtC1INC00LDRgtGDLi4uXCJcbiAgICAgICAgICAgICAgICAgICBkYXRhLXRvZ2dsZT1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgICBkYXRhLXRhcmdldD1cIiNteU1vZGFsXCJcbiAgICAgICAgICAgID5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJtb2RlLWJ1dHRvbnNcIj5cbiAgICAgICAgICAgIDxidXR0b24gOmNsYXNzPVwiWydidG4nLCAnYnRuLXZpZXcnLCB7ICdidG4tLWFjdGl2ZSc6IG1vZGU9PT0ndmlldycgfV1cIlxuICAgICAgICAgICAgICAgICAgICBAY2xpY2s9XCJjaGFuZ2VNb2RlKCd2aWV3JylcIj5cbiAgICAgICAgICAgICAgICDQn9GA0L7RgdC80L7RgtGAXG4gICAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICAgIDxidXR0b24gOmNsYXNzPVwiWydidG4nLCAnYnRuLWVkaXQnLCB7ICdidG4tLWFjdGl2ZSc6IG1vZGU9PT0nZWRpdCcgfV1cIlxuICAgICAgICAgICAgICAgICAgICBAY2xpY2s9XCJjaGFuZ2VNb2RlKCdlZGl0JylcIj5cbiAgICAgICAgICAgICAgICDQoNC10LTQsNC60YLQuNGA0L7QstCw0L3QuNC1XG4gICAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICAgIDxidXR0b24gOmNsYXNzPVwiWydidG4nLCAnYnRuLXZhbGlkYXRlJywgeyAnYnRuLS1hY3RpdmUnOiBtb2RlPT09J3ZhbGlkYXRlJyB9XVwiXG4gICAgICAgICAgICAgICAgICAgIEBjbGljaz1cImNoYW5nZU1vZGUoJ3ZhbGlkYXRlJylcIj5cbiAgICAgICAgICAgICAgICDQktCw0LvQuNC00LDRhtC40Y9cbiAgICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgICAgPGltZyBzdHlsZT1cImhlaWdodDogMzBweDsgd2lkdGg6IDMwcHg7XCJcbiAgICAgICAgICAgICAgICAgOnRpdGxlPVwiZW1wbG95ZWVGb3JtYXR0ZWRcIlxuICAgICAgICAgICAgICAgICBzcmM9XCIuLi9hc3NldHMvaW1hZ2VzL25vLWF2YXRhci5wbmdcIj5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxtb2RhbCB2LXNob3c9XCJzaG93Q2FsZW5kYXJcIiBAY2xvc2U9XCJzaG93Q2FsZW5kYXIgPSBmYWxzZVwiID5cbiAgICAgICAgICAgIDxmdWxsLWNhbGVuZGFyIDpldmVudHM9XCJldmVudHNcIiA6Y29uZmlnPVwiZnVsbENhbGVuZGFyQ29uZmlnXCIgcmVmPVwiY2FsZW5kYXJcIiAvPlxuICAgICAgICA8L21vZGFsPlxuICAgIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbjxzY3JpcHQ+XG4gICAgaW1wb3J0IGF4aW9zIGZyb20gJ2F4aW9zJ1xuICAgIGltcG9ydCB7IEZ1bGxDYWxlbmRhciB9IGZyb20gJ3Z1ZS1mdWxsLWNhbGVuZGFyJ1xuICAgIGltcG9ydCBtb2RhbCBmcm9tIFwiLi9Nb2RhbC52dWVcIlxuXG4gICAgZXhwb3J0IGRlZmF1bHQge1xuICAgICAgICBuYW1lOiAnam91cm5hbC1wYW5lbCcsXG4gICAgICAgIGRhdGEoKSB7XG4gICAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgICAgIHNob3dDYWxlbmRhcjogZmFsc2UsXG4gICAgICAgICAgICAgICAgZW1wbG95ZWVOYW1lOiAnRW1wbG95ZWUgbmFtZScsXG4gICAgICAgICAgICAgICAgZW1wbG95ZWVQb3NpdGlvbjogJ3Bvc2l0aW9uJyxcbiAgICAgICAgICAgICAgICBldmVudHM6IG51bGwsXG4gICAgICAgICAgICAgICAgZnVsbENhbGVuZGFyQ29uZmlnOiB7XG4gICAgICAgICAgICAgICAgICAgIGxvY2FsZTogJ3J1JyxcbiAgICAgICAgICAgICAgICAgICAgYnV0dG9uVGV4dDoge1xuICAgICAgICAgICAgICAgICAgICAgICAgdG9kYXk6ICAgICfQodC10LPQvtC00L3RjycsXG4gICAgICAgICAgICAgICAgICAgICAgICBtb250aDogICAgJ9Cc0LXRgdGP0YYnLFxuICAgICAgICAgICAgICAgICAgICAgICAgd2VlazogICAgICfQndC10LTQtdC70Y8nLFxuICAgICAgICAgICAgICAgICAgICAgICAgZGF5OiAgICAgICfQlNC10L3RjCcsXG4gICAgICAgICAgICAgICAgICAgICAgICBsaXN0OiAgICAgJ9Ch0L/QuNGB0L7QuidcbiAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgdGltZUZvcm1hdDogJ0goOm1tKScsXG4gICAgICAgICAgICAgICAgICAgIGhlYWRlcjoge1xuICAgICAgICAgICAgICAgICAgICAgICAgbGVmdDogJ3ByZXYsbmV4dCB0b2RheScsXG4gICAgICAgICAgICAgICAgICAgICAgICBjZW50ZXI6ICd0aXRsZScsXG4gICAgICAgICAgICAgICAgICAgICAgICByaWdodDogJ21vbnRoLCBsaXN0TW9udGgnXG4gICAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAgIHNlbGVjdGFibGU6IHRydWUsXG4gICAgICAgICAgICAgICAgICAgIHNlbGVjdEhlbHBlcjogdHJ1ZSxcbiAgICAgICAgICAgICAgICAgICAgc2VsZWN0OiBmdW5jdGlvbiAoc3RhcnQsIGVuZCwgYWxsRGF5KSB7XG4gICAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAgIGV2ZW50Q2xpY2s6IGZ1bmN0aW9uIChjYWxFdmVudCwganNFdmVudCwgdmlldykge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coXCJldmVudCBjbGlja1wiKTtcbiAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgZWRpdGFibGU6IGZhbHNlLFxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgY29tcHV0ZWQ6IHtcbiAgICAgICAgICAgIGVtcGxveWVlRm9ybWF0dGVkKCkge1xuICAgICAgICAgICAgICAgIHJldHVybiB0aGlzLmVtcGxveWVlTmFtZSArIFwiIDogXCIgKyB0aGlzLmVtcGxveWVlUG9zaXRpb247XG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgbW9kZSgpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2pvdXJuYWxJbmZvJ10ubW9kZTtcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBzaGlmdERhdGUoKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHRoaXMuJHN0b3JlLmdldHRlcnNbJ2pvdXJuYWxTdGF0ZS9qb3VybmFsSW5mbyddLmRhdGU7XG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgc2hpZnRPcmRlcigpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2pvdXJuYWxJbmZvJ10ub3JkZXI7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIG1ldGhvZHM6IHtcbiAgICAgICAgICAgIGNoYW5nZU1vZGUobW9kZSkge1xuICAgICAgICAgICAgICAgIGxldCBwZXJtaXNzaW9uID0gbW9kZSArICdfY2VsbHMnXG4gICAgICAgICAgICAgICAgbGV0IHBlcm1pc3Npb25zID0gdGhpcy4kc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2pvdXJuYWxJbmZvJ10ucGVybWlzc2lvbnNcbiAgICAgICAgICAgICAgICBmb3IgKGxldCBpPTA7IGk8cGVybWlzc2lvbnMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHBlcm1pc3Npb24gPT09IHBlcm1pc3Npb25zW2ldKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLiRzdG9yZS5jb21taXQoJ2pvdXJuYWxTdGF0ZS9TRVRfUEFHRV9NT0RFJywgbW9kZSk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgICBtb3VudGVkKCkge1xuICAgICAgICAgICAgbGV0IHBsYW50ID0gbG9jYXRpb24ucGF0aG5hbWUuc3BsaXQoJy8nKVsxXTtcbiAgICAgICAgICAgIGxldCBqb3VybmFsX25hbWUgPSBsb2NhdGlvbi5wYXRobmFtZS5zcGxpdCgnLycpWzJdO1xuICAgICAgICAgICAgbGV0IHNlbGYgPSB0aGlzO1xuICAgICAgICAgICAgYXhpb3MuZ2V0KCdodHRwOi8vbG9jYWxob3N0OjgwMDAvJyArIHBsYW50ICsgJy8nICsgam91cm5hbF9uYW1lICsnL2dldF9zaGlmdHMvJyxcbiAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgIHdpdGhDcmVkZW50aWFsczogdHJ1ZVxuICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBzZWxmLmV2ZW50cyA9IHJlc3BvbnNlLmRhdGE7XG4gICAgICAgICAgICAgICAgICAgICQoXCIuZmMtbW9udGgtYnV0dG9uXCIpLmNsaWNrKCk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAuY2F0Y2goZSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGUpXG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgIH0sXG4gICAgICAgIGNvbXBvbmVudHM6IHtcbiAgICAgICAgICAgIG1vZGFsLFxuICAgICAgICAgICAgRnVsbENhbGVuZGFyXG4gICAgICAgIH1cbiAgICB9XG48L3NjcmlwdD5cbjxzdHlsZT5cbjwvc3R5bGU+XG4iLCJleHBvcnRzID0gbW9kdWxlLmV4cG9ydHMgPSByZXF1aXJlKFwiLi4vLi4vbm9kZV9tb2R1bGVzL2Nzcy1sb2FkZXIvbGliL2Nzcy1iYXNlLmpzXCIpKGZhbHNlKTtcbi8vIGltcG9ydHNcblxuXG4vLyBtb2R1bGVcbmV4cG9ydHMucHVzaChbbW9kdWxlLmlkLCBcIlxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblxcblwiLCBcIlwiXSk7XG5cbi8vIGV4cG9ydHNcbiIsImV4cG9ydHMgPSBtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoXCIuLi8uLi9ub2RlX21vZHVsZXMvY3NzLWxvYWRlci9saWIvY3NzLWJhc2UuanNcIikoZmFsc2UpO1xuLy8gaW1wb3J0c1xuXG5cbi8vIG1vZHVsZVxuZXhwb3J0cy5wdXNoKFttb2R1bGUuaWQsIFwiXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXCIsIFwiXCJdKTtcblxuLy8gZXhwb3J0c1xuIiwidmFyIHJlbmRlciA9IGZ1bmN0aW9uKCkge1xuICB2YXIgX3ZtID0gdGhpc1xuICB2YXIgX2ggPSBfdm0uJGNyZWF0ZUVsZW1lbnRcbiAgdmFyIF9jID0gX3ZtLl9zZWxmLl9jIHx8IF9oXG4gIHJldHVybiBfYyhcbiAgICBcInYtcG9wb3ZlclwiLFxuICAgIHsgYXR0cnM6IHsgb2Zmc2V0OiBcIjE2XCIsIGRpc2FibGVkOiBfdm0ubW9kZSAhPT0gXCJ2YWxpZGF0ZVwiIH0gfSxcbiAgICBbXG4gICAgICBfYyhcImlucHV0XCIsIHtcbiAgICAgICAgZGlyZWN0aXZlczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIG5hbWU6IFwidG9vbHRpcFwiLFxuICAgICAgICAgICAgcmF3TmFtZTogXCJ2LXRvb2x0aXBcIixcbiAgICAgICAgICAgIHZhbHVlOiB7XG4gICAgICAgICAgICAgIGNvbnRlbnQ6IFwi0JLQstC10LTQuNGC0LUg0YfQuNGB0LvQvlwiLFxuICAgICAgICAgICAgICBzaG93OiBfdm0uc2hvd0NlbGxUeXBlVG9vbHRpcCxcbiAgICAgICAgICAgICAgdHJpZ2dlcjogXCJtYW51YWxcIlxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIGV4cHJlc3Npb246XG4gICAgICAgICAgICAgIFwie2NvbnRlbnQ6ICfQktCy0LXQtNC40YLQtSDRh9C40YHQu9C+Jywgc2hvdzogc2hvd0NlbGxUeXBlVG9vbHRpcCwgdHJpZ2dlcjogJ21hbnVhbCd9XCJcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIGNsYXNzOiBfdm0uY2xhc3NlcyxcbiAgICAgICAgc3R5bGU6IHsgY29sb3I6IF92bS5hY3RpdmVDb2xvciB9LFxuICAgICAgICBhdHRyczoge1xuICAgICAgICAgIG5hbWU6IF92bS5maWVsZE5hbWUsXG4gICAgICAgICAgXCJyb3ctaW5kZXhcIjogX3ZtLnJvd0luZGV4LFxuICAgICAgICAgIHJlYWRvbmx5OiBfdm0ubW9kZSAhPT0gXCJlZGl0XCIsXG4gICAgICAgICAgcGxhY2Vob2xkZXI6IF92bS5wbGFjZWhvbGRlcixcbiAgICAgICAgICB0eXBlOiBfdm0udHlwZVxuICAgICAgICB9LFxuICAgICAgICBkb21Qcm9wczogeyB2YWx1ZTogX3ZtLnZhbHVlIH0sXG4gICAgICAgIG9uOiB7XG4gICAgICAgICAga2V5cHJlc3M6IF92bS5maWx0ZXJJbnB1dCxcbiAgICAgICAgICBrZXlkb3duOiBfdm0uY2hhbmdlRm9jdXMsXG4gICAgICAgICAgY2hhbmdlOiBfdm0ub25DaGFuZ2VkLFxuICAgICAgICAgIGlucHV0OiBfdm0ub25JbnB1dCxcbiAgICAgICAgICBibHVyOiBmdW5jdGlvbigkZXZlbnQpIHtcbiAgICAgICAgICAgIF92bS5zaG93Q2VsbFR5cGVUb29sdGlwID0gZmFsc2VcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pLFxuICAgICAgX3ZtLl92KFwiIFwiKSxcbiAgICAgIF92bS4kc3RvcmUuZ2V0dGVyc1tcImpvdXJuYWxTdGF0ZS9jZWxsQ29tbWVudFwiXShcbiAgICAgICAgX3ZtLnRhYmxlTmFtZSxcbiAgICAgICAgX3ZtLmZpZWxkTmFtZSxcbiAgICAgICAgX3ZtLnJvd0luZGV4XG4gICAgICApXG4gICAgICAgID8gX2MoXCJpXCIsIHsgc3RhdGljQ2xhc3M6IFwiZmFyIGZhLWVudmVsb3BlIGNvbW1lbnQtbm90aWZpY2F0aW9uXCIgfSlcbiAgICAgICAgOiBfdm0uX2UoKSxcbiAgICAgIF92bS5fdihcIiBcIiksXG4gICAgICBfYyhcbiAgICAgICAgXCJ0ZW1wbGF0ZVwiLFxuICAgICAgICB7IHNsb3Q6IFwicG9wb3ZlclwiIH0sXG4gICAgICAgIFtcbiAgICAgICAgICBfYyhcIkNlbGxDb21tZW50XCIsIHtcbiAgICAgICAgICAgIGF0dHJzOiB7XG4gICAgICAgICAgICAgIFwidGFibGUtbmFtZVwiOiBfdm0udGFibGVOYW1lLFxuICAgICAgICAgICAgICBcImZpZWxkLW5hbWVcIjogX3ZtLmZpZWxkTmFtZSxcbiAgICAgICAgICAgICAgXCJyb3ctaW5kZXhcIjogX3ZtLnJvd0luZGV4XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSlcbiAgICAgICAgXSxcbiAgICAgICAgMVxuICAgICAgKVxuICAgIF0sXG4gICAgMlxuICApXG59XG52YXIgc3RhdGljUmVuZGVyRm5zID0gW11cbnJlbmRlci5fd2l0aFN0cmlwcGVkID0gdHJ1ZVxuXG5leHBvcnQgeyByZW5kZXIsIHN0YXRpY1JlbmRlckZucyB9IiwiLy8tIHJlcXVpcmUoJ29mZmxpbmUtcGx1Z2luL3J1bnRpbWUnKS5pbnN0YWxsKCk7ICAvLyBvZmZsaW5lIHNlcnZpY2Utd29ya2VyIHBsdWdpblxuXG5cbi8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gTGlicyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG5pbXBvcnQgJ2pxdWVyeSc7IHdpbmRvdy4kID0gJDsgd2luZG93LmpRdWVyeSA9IGpRdWVyeTtcbmltcG9ydCAnbG9kYXNoJzsgd2luZG93Ll8gPSBfO1xuaW1wb3J0ICd2dWUnOyBpbXBvcnQgVnVlIGZyb20gJ3Z1ZS9kaXN0L3Z1ZS5lc20uanMnOyB3aW5kb3cuVnVlID0gVnVlO1xuaW1wb3J0ICdib290c3RyYXAnO1xuaW1wb3J0ICdqcXVlcnktY29uZmlybSc7XG5pbXBvcnQgJ3Byb21pc2UtcG9seWZpbGwvc3JjL3BvbHlmaWxsJztcblxuaW1wb3J0ICdmdWxsY2FsZW5kYXInO1xuaW1wb3J0ICdib290c3RyYXAtZ3JpZCc7XG5cbmltcG9ydCAnd2F5cG9pbnRzL2xpYi9qcXVlcnkud2F5cG9pbnRzLmpzJztcbi8vIGltcG9ydCAnd2F5cG9pbnRzJzsgaW1wb3J0IFdheXBvaW50IGZyb20gJ3dheXBvaW50cyc7IHdpbmRvdy5XYXlwb2ludCA9IFdheXBvaW50O1xuXG5pbXBvcnQgJ3R5cGVmYWNlLXJvYm90by1jb25kZW5zZWQnO1xuaW1wb3J0ICd0eXBlZmFjZS1yb2JvdG8nO1xuLy8gaW1wb3J0ICdtYXRlcmlhbC1kZXNpZ24taWNvbnMnO1xuaW1wb3J0ICdAZm9ydGF3ZXNvbWUvZm9udGF3ZXNvbWUnO1xuaW1wb3J0ICdAZm9ydGF3ZXNvbWUvZm9udGF3ZXNvbWUtZnJlZS1icmFuZHMnO1xuXG5cbi8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gTW9kdWxlcyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4vLyBpbXBvcnQgJy4uL3Njc3MvaW5kZXguc2Nzcyc7XG5cbmltcG9ydCAnLi9mZWVkYmFjayc7XG5pbXBvcnQgJy4vaGVhZGVyJztcbmltcG9ydCAnLi92dWUtZW52JztcblxuaW1wb3J0ICcuL2NvbW1vbic7XG4iLCJpbXBvcnQgVnVlIGZyb20gJ3Z1ZS9kaXN0L3Z1ZS5lc20uanMnXG5pbXBvcnQgQXBwIGZyb20gJy4vQXBwLnZ1ZSdcbmltcG9ydCByb3V0ZXIgZnJvbSAnLi9yb3V0ZXInO1xuaW1wb3J0IHN0b3JlIGZyb20gJy4vc3RvcmUvc3RvcmUnO1xuaW1wb3J0IFZ1ZU5hdGl2ZVNvY2sgZnJvbSAndnVlLW5hdGl2ZS13ZWJzb2NrZXQnO1xuXG5pbXBvcnQgJy4vcmVnaXN0ZXItc3cnXG5pbXBvcnQgJy4vYXNzZXRzL2pzL2luZGV4J1xuXG5WdWUuY29uZmlnLnByb2R1Y3Rpb25UaXAgPSBmYWxzZTtcblxuY29uc3QgZGF0YUVuZHBvaW50ID0gJ3dzOi8vJyArIHdpbmRvdy5sb2NhdGlvbi5ob3N0bmFtZSArICc6ODAwMC9lLWxvZ3MvJztcblZ1ZS51c2UoVnVlTmF0aXZlU29jaywgZGF0YUVuZHBvaW50LCB7XG4gICAgc3RvcmU6IHN0b3JlLFxuICAgIGZvcm1hdDogJ2pzb24nLFxuICAgIHJlY29ubmVjdGlvbjogdHJ1ZSxcbiAgICBjb25uZWN0TWFudWFsbHk6IHRydWUsXG4gICAgcGFzc1RvU3RvcmVIYW5kbGVyOiBmdW5jdGlvbiAoZXZlbnROYW1lLCBldmVudCkge1xuICAgICAgICBpZiAoIShldmVudE5hbWUgPT09ICdTT0NLRVRfb25tZXNzYWdlJykpIHsgcmV0dXJuIH1cbiAgICAgICAgbGV0IGRhdGEgPSBKU09OLnBhcnNlKGV2ZW50LmRhdGEpO1xuICAgICAgICB0aGlzLnN0b3JlLmNvbW1pdCgnam91cm5hbFN0YXRlL1NBVkVfQ0VMTF9WQUxVRScsIHtcbiAgICAgICAgICAgIHRhYmxlTmFtZTogZGF0YVsnY2VsbF9sb2NhdGlvbiddWyd0YWJsZV9uYW1lJ10sXG4gICAgICAgICAgICBmaWVsZE5hbWU6IGRhdGFbJ2NlbGxfbG9jYXRpb24nXVsnZmllbGRfbmFtZSddLFxuICAgICAgICAgICAgaW5kZXg6IGRhdGFbJ2NlbGxfbG9jYXRpb24nXVsnaW5kZXgnXSxcbiAgICAgICAgICAgIHZhbHVlOiBkYXRhWyd2YWx1ZSddXG4gICAgICAgIH0pXG4gICAgfVxufSk7XG5cbndpbmRvdy5tdiA9IG5ldyBWdWUoe1xuICAgIGVsOiAnI2FwcCcsXG4gICAgcm91dGVyLFxuICAgIHN0b3JlLFxuICAgIHJlbmRlcjogaCA9PiBoKEFwcCksXG4gICAgbW91bnRlZCAoKSB7XG4gICAgfVxufSk7XG4iLCJpbXBvcnQgYXhpb3MgZnJvbSAnYXhpb3MnO1xuaW1wb3J0IFZ1ZUNvb2tpZXMgZnJvbSAndnVlLWNvb2tpZXMnXG5cbmNvbnN0IGpvdXJuYWxTdGF0ZSA9IHtcbiAgICBuYW1lc3BhY2VkOiB0cnVlLFxuICAgIHN0YXRlOiB7XG4gICAgICAgIHBsYW50c0luZm86IFtdLFxuICAgICAgICBqb3VybmFsSW5mbzoge30sXG4gICAgICAgIGxvYWRlZDogZmFsc2UsXG4gICAgICAgIHNvY2tldDoge1xuICAgICAgICAgICAgaXNDb25uZWN0ZWQ6IGZhbHNlLFxuICAgICAgICAgICAgcmVjb25uZWN0RXJyb3I6IGZhbHNlLFxuICAgICAgICB9XG4gICAgfSxcbiAgICBnZXR0ZXJzOiB7XG4gICAgICAgIGxvYWRlZDogc3RhdGUgPT4gc3RhdGUubG9hZGVkLFxuICAgICAgICBqb3VybmFsSW5mbzogc3RhdGUgPT4gIHN0YXRlLmpvdXJuYWxJbmZvLFxuICAgICAgICB0YWJsZXM6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gT2JqZWN0LmtleXMoc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXMpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gW107XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHBsYW50czogc3RhdGUgPT4ge1xuICAgICAgICAgICAgcmV0dXJuIHN0YXRlLnBsYW50c0luZm9cbiAgICAgICAgfSxcbiAgICAgICAgcGxhbnROYW1lOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLnBsYW50Lm5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgcGxhbnRWZXJib3NlTmFtZTogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5wbGFudC5uYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGpvdXJuYWxOYW1lOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwubmFtZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBqb3VybmFsVmVyYm9zZU5hbWU6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC5uYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHRhYmxlVmVyYm9zZU5hbWU6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiB0YWJsZU5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgZmllbGRWZXJib3NlTmFtZTogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gZmllbGROYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHNoaWZ0T3JkZXI6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8ub3JkZXJcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIC0xO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBjZWxsVmFsdWU6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgZmllbGROYW1lLCByb3dJbmRleCkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShmaWVsZE5hbWUgaW4gZmllbGRzKSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZygnV0FSTklORyEgVHJ5aW5nIHRvIGdldCBjZWxsIHZhbHVlIG9mIHVuZXhpc3RlbnQgZmllbGQ6ICcgKyBmaWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGxldCBjZWxscyA9IGZpZWxkc1tmaWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChPYmplY3Qua2V5cyhjZWxscykubGVuZ3RoICE9PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChyb3dJbmRleCBpbiBjZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGNlbGxzW3Jvd0luZGV4XS52YWx1ZTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGNlbGwgdmFsdWUgd2l0aCB1bmV4aXN0ZW50IGluZGV4OiAnICsgZmllbGROYW1lICsgJyAnICsgcm93SW5kZXgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBjZWxsQ29tbWVudDogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUsIHJvd0luZGV4KSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKGZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGNlbGwgY29tbWVudCBvZiB1bmV4aXN0ZW50IGZpZWxkOiAnICsgZmllbGROYW1lKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBsZXQgY2VsbHMgPSBmaWVsZHNbZmllbGROYW1lXS5jZWxscztcbiAgICAgICAgICAgICAgICBpZiAoT2JqZWN0LmtleXMoY2VsbHMpLmxlbmd0aCAhPT0gMCkge1xuICAgICAgICAgICAgICAgICAgICBpZiAocm93SW5kZXggaW4gY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBjZWxsc1tyb3dJbmRleF0uY29tbWVudDtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGNlbGwgY29tbWVudCB3aXRoIHVuZXhpc3RlbnQgaW5kZXg6ICcgKyBmaWVsZE5hbWUgKyAnICcgKyByb3dJbmRleCk7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGZpZWxkQ2VsbHM6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgZmllbGROYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmIChmaWVsZE5hbWUgaW4gZmllbGRzKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkc1tmaWVsZE5hbWVdLmNlbGxzXG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2UgcmV0dXJuIFtdXG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiBbXVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBtYXhSb3dJbmRleDogKHN0YXRlKSA9PiAodGFibGVOYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IG1heCA9IC0xO1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBmb3IobGV0IGZpZWxkIGluIGZpZWxkcykge1xuICAgICAgICAgICAgICAgICAgICBmb3IgKGxldCBpbmRleCBpbiBmaWVsZHNbZmllbGRdLmNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpbmRleCA9IHBhcnNlSW50KGluZGV4KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIG1heCA9IG1heCA8IGluZGV4ID8gaW5kZXggOiBtYXg7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIG1heCsxO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gLTE7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHJvd0lzRW1wdHk6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgaW5kZXgpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHNcbiAgICAgICAgICAgICAgICBmb3IgKGxldCBmaWVsZCBpbiBmaWVsZHMpIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKCdjZWxscycgaW4gZmllbGRzW2ZpZWxkXSkge1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKGluZGV4IGluIGZpZWxkc1tmaWVsZF0uY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gZmFsc2VcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gdHJ1ZVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICB0YWJsZVRpdGxlOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUpID0+IHtcbiAgICAgICAgICAgIHJldHVybiAn0JfQsNCz0L7Qu9C+0LLQvtC6INGC0LDQsdC70LjRhtGLJ1xuICAgICAgICB9LFxuICAgICAgICBmaWVsZERlc2NyaXB0aW9uOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUsIGZpZWxkTmFtZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShmaWVsZE5hbWUgaW4gZmllbGRzKSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhcIldBUk5JTkchIFRyeWluZyB0byBnZXQgZmllbGQgZGVzY3RpcHRpb24gb2YgdW5leGlzdGVudCBmaWVsZDogXCIgKyBmaWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4ge307XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBmaWVsZHNbZmllbGROYW1lXS5maWVsZF9kZXNjcmlwdGlvbiB8fCAnJ1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnXG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9LFxuICAgIG11dGF0aW9uczoge1xuICAgICAgICBVUERBVEVfSk9VUk5BTF9JTkZPIChzdGF0ZSwgam91cm5hbEluZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLmpvdXJuYWxJbmZvID0gam91cm5hbEluZm87XG4gICAgICAgIH0sXG4gICAgICAgIFVQREFURV9QTEFOVFNfSU5GTyAoc3RhdGUsIHBsYW50c0luZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLnBsYW50c0luZm8gPSBwbGFudHNJbmZvO1xuICAgICAgICB9LFxuICAgICAgICBTRVRfTE9BREVEIChzdGF0ZSwgbG9hZGVkKSB7XG4gICAgICAgICAgICBzdGF0ZS5sb2FkZWQgPSBsb2FkZWQ7XG4gICAgICAgIH0sXG4gICAgICAgIFNBVkVfQ0VMTF9WQUxVRSAoc3RhdGUsIHBheWxvYWQpIHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbcGF5bG9hZC50YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShwYXlsb2FkLmZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gc2F2ZSB2YWx1ZSBvZiB1bmV4aXN0ZW50IGZpZWxkOiAnICsgcGF5bG9hZC5maWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZygnICBDcmVhdGluZyBmaWVsZCAnICsgcGF5bG9hZC5maWVsZE5hbWUgKyAnLi4uJyk7XG4gICAgICAgICAgICAgICAgICAgIGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV0gPSB7fTtcbiAgICAgICAgICAgICAgICAgICAgZmllbGRzW3BheWxvYWQuZmllbGROYW1lXVsnY2VsbHMnXSA9IHt9O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBsZXQgY2VsbHMgPSBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLnZhbHVlKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLmluZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAvLyB1cGRhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ3ZhbHVlJ10gPSBwYXlsb2FkLnZhbHVlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gY3JlYXRlIGNlbGxcbiAgICAgICAgICAgICAgICAgICAgICAgIFZ1ZS5zZXQoY2VsbHMsIHBheWxvYWQuaW5kZXgsIHt9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIFZ1ZS5zZXQoY2VsbHNbcGF5bG9hZC5pbmRleF0sICd2YWx1ZScsIHBheWxvYWQudmFsdWUpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICBWdWUuZGVsZXRlKGNlbGxzLCBwYXlsb2FkLmluZGV4KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIFNBVkVfQ0VMTF9DT01NRU5UIChzdGF0ZSwgcGF5bG9hZCkge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1twYXlsb2FkLnRhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKHBheWxvYWQuZmllbGROYW1lIGluIGZpZWxkcykpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBzYXZlIGNvbW1lbnQgb2YgdW5leGlzdGVudCBmaWVsZDogJyArIHBheWxvYWQuZmllbGROYW1lKTtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJyAgQ3JlYXRpbmcgZmllbGQgJyArIHBheWxvYWQuZmllbGROYW1lICsgJy4uLicpO1xuICAgICAgICAgICAgICAgICAgICBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdID0ge307XG4gICAgICAgICAgICAgICAgICAgIGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV1bJ2NlbGxzJ10gPSB7fTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgbGV0IGNlbGxzID0gZmllbGRzW3BheWxvYWQuZmllbGROYW1lXS5jZWxscztcbiAgICAgICAgICAgICAgICBpZiAocGF5bG9hZC5jb21tZW50KSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLmluZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAvLyB1cGRhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ2NvbW1lbnQnXSA9IHBheWxvYWQuY29tbWVudDtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIC8vIGNyZWF0ZSBjZWxsXG4gICAgICAgICAgICAgICAgICAgICAgICBWdWUuc2V0KGNlbGxzLCBwYXlsb2FkLmluZGV4LCB7fSk7XG4gICAgICAgICAgICAgICAgICAgICAgICBWdWUuc2V0KGNlbGxzW3BheWxvYWQuaW5kZXhdLCAnY29tbWVudCcsIHBheWxvYWQuY29tbWVudCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIFZ1ZS5kZWxldGUoY2VsbHMsIHBheWxvYWQuaW5kZXgpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgU0VUX1BBR0VfTU9ERSAoc3RhdGUsIG1vZGUpIHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBzdGF0ZS5qb3VybmFsSW5mby5tb2RlID0gbW9kZVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfT05PUEVOIChzdGF0ZSwgZXZlbnQpICB7XG4gICAgICAgICAgICBWdWUucHJvdG90eXBlLiRzb2NrZXQgPSBldmVudC5jdXJyZW50VGFyZ2V0XG4gICAgICAgICAgICBzdGF0ZS5zb2NrZXQuaXNDb25uZWN0ZWQgPSB0cnVlXG4gICAgICAgIH0sXG4gICAgICAgIFNPQ0tFVF9PTkNMT1NFIChzdGF0ZSwgZXZlbnQpICB7XG4gICAgICAgICAgICBzdGF0ZS5zb2NrZXQuaXNDb25uZWN0ZWQgPSBmYWxzZVxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfT05FUlJPUiAoc3RhdGUsIGV2ZW50KSAge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihzdGF0ZSwgZXZlbnQpXG4gICAgICAgIH0sXG4gICAgICAgIFNPQ0tFVF9PTk1FU1NBR0UgKHN0YXRlLCBtZXNzYWdlKSAge1xuXG4gICAgICAgIH0sXG4gICAgICAgIFNPQ0tFVF9SRUNPTk5FQ1Qoc3RhdGUsIGNvdW50KSB7XG4gICAgICAgICAgICBjb25zb2xlLmluZm8oc3RhdGUsIGNvdW50KVxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfUkVDT05ORUNUX0VSUk9SKHN0YXRlKSB7XG4gICAgICAgICAgICBzdGF0ZS5zb2NrZXQucmVjb25uZWN0RXJyb3IgPSB0cnVlO1xuICAgICAgICB9LFxuICAgIH0sXG4gICAgYWN0aW9uczoge1xuICAgICAgICBsb2FkSm91cm5hbDogZnVuY3Rpb24gKHsgY29tbWl0LCBzdGF0ZSwgZ2V0dGVycyB9LCBwYXlsb2FkKSB7XG4gICAgICAgICAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlcywgcmVqKSA9PiB7XG4gICAgICAgICAgICAgICAgYXhpb3NcbiAgICAgICAgICAgICAgICAgICAgLmdldCgnaHR0cDovL2xvY2FsaG9zdDo4MDAwL2FwaS9zaGlmdHMvJyArIHBheWxvYWQsIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHdpdGhDcmVkZW50aWFsczogdHJ1ZVxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICAudGhlbihyZXNwb25zZSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9KT1VSTkFMX0lORk8nLCByZXNwb25zZS5kYXRhKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbW1pdCgnU0VUX0xPQURFRCcsIHRydWUpO1xuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXMoKVxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICAuY2F0Y2goKGVycikgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgfSlcbiAgICAgICAgfSxcbiAgICAgICAgbG9hZFBsYW50czogZnVuY3Rpb24gKHsgY29tbWl0LCBzdGF0ZSwgZ2V0dGVycyB9KSB7XG4gICAgICAgICAgICBheGlvc1xuICAgICAgICAgICAgICAgIC5nZXQoJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hcGkvbWVudV9pbmZvLycpXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9QTEFOVFNfSU5GTycsIHJlc3BvbnNlLmRhdGEucGxhbnRzKTtcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICB9LFxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgam91cm5hbFN0YXRlIl0sInNvdXJjZVJvb3QiOiIifQ==