webpackHotUpdate("main",{

/***/ "./node_modules/babel-loader/lib/index.js?!./node_modules/vue-loader/lib/index.js?!./src/components/JournalPage.vue?vue&type=script&lang=js&":
/*!*************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib??ref--0-0!./node_modules/vue-loader/lib??vue-loader-options!./src/components/JournalPage.vue?vue&type=script&lang=js& ***!
  \*************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _TableCommon_vue__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./TableCommon.vue */ "./src/components/TableCommon.vue");
/* harmony import */ var _JournalPanel_vue__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./JournalPanel.vue */ "./src/components/JournalPanel.vue");
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
  name: "JournalPage",
  components: {
    'tablecommon': _TableCommon_vue__WEBPACK_IMPORTED_MODULE_0__["default"],
    'journal-panel': _JournalPanel_vue__WEBPACK_IMPORTED_MODULE_1__["default"]
  },
  updated: function updated() {// if (this.$route.params.shift_id) {
    //     this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
    // }
  },
  mounted: function mounted() {
    this.$connect();

    if (this.$route.params.shift_id) {
      this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id);
    }
  }
});

/***/ }),

/***/ "./node_modules/css-loader/index.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js?!./src/components/JournalPage.vue?vue&type=style&index=0&id=5964a534&scoped=true&lang=css&":
/*!**************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/css-loader!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib??vue-loader-options!./src/components/JournalPage.vue?vue&type=style&index=0&id=5964a534&scoped=true&lang=css& ***!
  \**************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(/*! ../../node_modules/css-loader/lib/css-base.js */ "./node_modules/css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", ""]);

// exports


/***/ }),

/***/ "./node_modules/vue-loader/lib/loaders/templateLoader.js?!./node_modules/vue-loader/lib/index.js?!./src/components/JournalPage.vue?vue&type=template&id=5964a534&scoped=true&":
/*!*****************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/JournalPage.vue?vue&type=template&id=5964a534&scoped=true& ***!
  \*****************************************************************************************************************************************************************************************************************/
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
    "main",
    { staticClass: "journal-page", attrs: { "data-mode": "?? page_mode ??" } },
    [
      _c("journal-panel"),
      _vm._v(" "),
      _c(
        "article",
        { staticClass: "journal-tables" },
        [
          _vm.$store.getters["journalState/loaded"]
            ? [
                _vm._v("\n<<<<<<< HEAD\n                "),
                _vm._l(_vm.$store.getters["journalState/tables"], function(
                  table
                ) {
                  return _c("tablecommon", {
                    key: table,
                    attrs: { name: table }
                  })
                }),
                _vm._v("\n=======\n                "),
                _vm._l(_vm.$store.getters["journalState/tables"], function(
                  table
                ) {
                  return _c("tablecommon", {
                    key:
                      _vm.$store.getters["journalState/journalName"] +
                      "_" +
                      table,
                    attrs: { name: table }
                  })
                }),
                _vm._v(
                  "\n>>>>>>> 304adfcf66a5b965c0bed68972eee2be53fb19fc\n            "
                )
              ]
            : [_c("span", [_vm._v("Нет данных")])]
        ],
        2
      )
    ],
    1
  )
}
var staticRenderFns = []
render._withStripped = true



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
    },
    isSynchronized: true
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
    isSynchronized: function isSynchronized(state) {
      return state.isSynchronized;
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
            // console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
            return '';
          }

          var cells = fields[fieldName].cells;

          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].value;
            } else {
              // console.log('WARNING! Trying to get cell value with unexistent index: ' + fieldName + ' ' + rowIndex);
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
            // console.log('WARNING! Trying to get cell comment of unexistent field: ' + fieldName);
            return '';
          }

          var cells = fields[fieldName].cells;

          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].comment;
            } else {
              // console.log('WARNING! Trying to get cell comment with unexistent index: ' + fieldName + ' ' + rowIndex);
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
    unsyncJournalCells: function unsyncJournalCells(state, getters) {
      return function () {
        var unsyncCells = [];
        getters.tables.map(function (table, index) {
          var currentTable = state.journalInfo.journal.tables[table];

          for (var field in currentTable.fields) {
            var currentCells = currentTable.fields[field].cells;

            for (var cell in currentCells) {
              if (currentCells[cell].notSynchronized) {
                unsyncCells.push(currentCells[cell]);
              }
            }
          }
        });
        return unsyncCells;
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
            // console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
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
    SET_SYNCHRONIZED: function SET_SYNCHRONIZED(state, isSynchronized) {
      state.isSynchronized = isSynchronized;
    },
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
          // console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
          // console.log('  Creating field ' + payload.fieldName + '...');
          fields[payload.fieldName] = {};
          fields[payload.fieldName]['cells'] = {};
        }

        var cells = fields[payload.fieldName].cells;

        if (payload.value) {
          if (payload.index in cells) {
            // update cell
            cells[payload.index]['value'] = payload.value;

            if (payload.notSynchronized) {
              cells[payload.index]['notSynchronized'] = payload.notSynchronized;
              cells[payload.index]['fieldName'] = payload.fieldName;
              cells[payload.index]['tableName'] = payload.tableName;
              cells[payload.index]['index'] = payload.index;
            }
          } else {
            // create cell
            Vue.set(cells, payload.index, {});
            Vue.set(cells[payload.index], 'value', payload.value);

            if (payload.notSynchronized) {
              Vue.set(cells[payload.index], 'notSynchronized', payload.notSynchronized);
            }
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
          // console.log('WARNING! Trying to save comment of unexistent field: ' + payload.fieldName);
          // console.log('  Creating field ' + payload.fieldName + '...');
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
          commit('UPDATE_JOURNAL_INFO', getters.isSynchronized ? response.data : JSON.parse(localStorage.getItem('vuex')).journalState.journalInfo);
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
    },
    sendUnsyncCell: function sendUnsyncCell(_ref3, payload) {
      var commit = _ref3.commit,
          state = _ref3.state,
          getters = _ref3.getters;
      window.mv.$socket.sendObj({
        'type': 'shift_data',
        'cell_location': {
          'group_id': getters.journalInfo.id,
          'table_name': payload.tableName,
          'field_name': payload.fieldName,
          'index': payload.index
        },
        'value': payload.value
      });
    }
  }
};
/* harmony default export */ __webpack_exports__["default"] = (journalState);

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vc3JjL2NvbXBvbmVudHMvSm91cm5hbFBhZ2UudnVlIiwid2VicGFjazovLy8uL3NyYy9jb21wb25lbnRzL0pvdXJuYWxQYWdlLnZ1ZT8wMDJmIiwid2VicGFjazovLy8uL3NyYy9jb21wb25lbnRzL0pvdXJuYWxQYWdlLnZ1ZT9lN2YyIiwid2VicGFjazovLy8uL3NyYy9zdG9yZS9tb2R1bGVzL2pvdXJuYWxTdGF0ZS5qcyJdLCJuYW1lcyI6WyJqb3VybmFsU3RhdGUiLCJuYW1lc3BhY2VkIiwic3RhdGUiLCJwbGFudHNJbmZvIiwiam91cm5hbEluZm8iLCJsb2FkZWQiLCJzb2NrZXQiLCJpc0Nvbm5lY3RlZCIsInJlY29ubmVjdEVycm9yIiwiaXNTeW5jaHJvbml6ZWQiLCJnZXR0ZXJzIiwidGFibGVzIiwiT2JqZWN0Iiwia2V5cyIsImpvdXJuYWwiLCJwbGFudHMiLCJwbGFudE5hbWUiLCJwbGFudCIsIm5hbWUiLCJwbGFudFZlcmJvc2VOYW1lIiwiam91cm5hbE5hbWUiLCJqb3VybmFsVmVyYm9zZU5hbWUiLCJ0YWJsZVZlcmJvc2VOYW1lIiwidGFibGVOYW1lIiwiZmllbGRWZXJib3NlTmFtZSIsImZpZWxkTmFtZSIsInNoaWZ0T3JkZXIiLCJvcmRlciIsImNlbGxWYWx1ZSIsInJvd0luZGV4IiwiZmllbGRzIiwiY2VsbHMiLCJsZW5ndGgiLCJ2YWx1ZSIsImNlbGxDb21tZW50IiwiY29tbWVudCIsImZpZWxkQ2VsbHMiLCJ1bnN5bmNKb3VybmFsQ2VsbHMiLCJ1bnN5bmNDZWxscyIsIm1hcCIsInRhYmxlIiwiaW5kZXgiLCJjdXJyZW50VGFibGUiLCJmaWVsZCIsImN1cnJlbnRDZWxscyIsImNlbGwiLCJub3RTeW5jaHJvbml6ZWQiLCJwdXNoIiwibWF4Um93SW5kZXgiLCJtYXgiLCJwYXJzZUludCIsInJvd0lzRW1wdHkiLCJ0YWJsZVRpdGxlIiwiZmllbGREZXNjcmlwdGlvbiIsImZpZWxkX2Rlc2NyaXB0aW9uIiwibXV0YXRpb25zIiwiU0VUX1NZTkNIUk9OSVpFRCIsIlVQREFURV9KT1VSTkFMX0lORk8iLCJVUERBVEVfUExBTlRTX0lORk8iLCJTRVRfTE9BREVEIiwiU0FWRV9DRUxMX1ZBTFVFIiwicGF5bG9hZCIsIlZ1ZSIsInNldCIsImRlbGV0ZSIsIlNBVkVfQ0VMTF9DT01NRU5UIiwiU0VUX1BBR0VfTU9ERSIsIm1vZGUiLCJTT0NLRVRfT05PUEVOIiwiZXZlbnQiLCJwcm90b3R5cGUiLCIkc29ja2V0IiwiY3VycmVudFRhcmdldCIsIlNPQ0tFVF9PTkNMT1NFIiwiU09DS0VUX09ORVJST1IiLCJjb25zb2xlIiwiZXJyb3IiLCJTT0NLRVRfT05NRVNTQUdFIiwibWVzc2FnZSIsIlNPQ0tFVF9SRUNPTk5FQ1QiLCJjb3VudCIsImluZm8iLCJTT0NLRVRfUkVDT05ORUNUX0VSUk9SIiwiYWN0aW9ucyIsImxvYWRKb3VybmFsIiwiY29tbWl0IiwiUHJvbWlzZSIsInJlcyIsInJlaiIsImF4aW9zIiwiZ2V0Iiwid2l0aENyZWRlbnRpYWxzIiwidGhlbiIsInJlc3BvbnNlIiwiZGF0YSIsIkpTT04iLCJwYXJzZSIsImxvY2FsU3RvcmFnZSIsImdldEl0ZW0iLCJjYXRjaCIsImVyciIsImxvZyIsImxvYWRQbGFudHMiLCJzZW5kVW5zeW5jQ2VsbCIsIndpbmRvdyIsIm12Iiwic2VuZE9iaiIsImlkIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBbUJBO0FBQ0E7QUFFQTtBQUNBLHFCQURBO0FBRUE7QUFDQSwyRUFEQTtBQUVBO0FBRkEsR0FGQTtBQU1BLFNBTkEscUJBTUEsQ0FDQTtBQUNBO0FBQ0E7QUFDQSxHQVZBO0FBV0EsU0FYQSxxQkFXQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBakJBLEc7Ozs7Ozs7Ozs7O0FDdEJBLDJCQUEyQixtQkFBTyxDQUFDLGdHQUErQztBQUNsRjs7O0FBR0E7QUFDQSxjQUFjLFFBQVM7O0FBRXZCOzs7Ozs7Ozs7Ozs7O0FDUEE7QUFBQTtBQUFB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T0FBVyxTQUFYQSxPQUFXO0FBQzlDK0Usa0RBQUtBLENBQ0FDLEdBREwsQ0FDUyxzQ0FEVCxFQUVLRSxJQUZMLENBRVUsb0JBQVk7QUFDZFAsZUFBTyxvQkFBUCxFQUE2QlEsU0FBU0MsSUFBVCxDQUFjL0UsTUFBM0M7QUFDSCxPQUpMO0FBS0gsS0F6Qkk7QUEwQkx3RixvQkFBZ0IsK0JBQXNDMUMsT0FBdEMsRUFBK0M7QUFBQSxVQUFuQ3dCLE1BQW1DLFNBQW5DQSxNQUFtQztBQUFBLFVBQTNCbkYsS0FBMkIsU0FBM0JBLEtBQTJCO0FBQUEsVUFBcEJRLE9BQW9CLFNBQXBCQSxPQUFvQjtBQUMzRDhGLGFBQU9DLEVBQVAsQ0FBVWxDLE9BQVYsQ0FBa0JtQyxPQUFsQixDQUEwQjtBQUN0QixnQkFBUSxZQURjO0FBRXRCLHlCQUFpQjtBQUNiLHNCQUFZaEcsUUFBUU4sV0FBUixDQUFvQnVHLEVBRG5CO0FBRWIsd0JBQWM5QyxRQUFRdEMsU0FGVDtBQUdiLHdCQUFjc0MsUUFBUXBDLFNBSFQ7QUFJYixtQkFBU29DLFFBQVFwQjtBQUpKLFNBRks7QUFRdEIsaUJBQVNvQixRQUFRNUI7QUFSSyxPQUExQjtBQVVIO0FBckNJO0FBalNRLENBQXJCO0FBMFVlakMsMkVBQWYsRSIsImZpbGUiOiJtYWluLjQyNzJjOTJkZThkZWFjNDU5ZGI0LmhvdC11cGRhdGUuanMiLCJzb3VyY2VzQ29udGVudCI6WyI8dGVtcGxhdGU+XG4gICAgPG1haW4gY2xhc3M9XCJqb3VybmFsLXBhZ2VcIiBkYXRhLW1vZGU9XCI/PyBwYWdlX21vZGUgPz9cIj5cbiAgICAgICAgPGpvdXJuYWwtcGFuZWw+PC9qb3VybmFsLXBhbmVsPlxuICAgICAgICA8YXJ0aWNsZSBjbGFzcz1cImpvdXJuYWwtdGFibGVzXCI+XG4gICAgICAgICAgICA8dGVtcGxhdGUgdi1pZj1cIiRzdG9yZS5nZXR0ZXJzWydqb3VybmFsU3RhdGUvbG9hZGVkJ11cIj5cbjw8PDw8PDwgSEVBRFxuICAgICAgICAgICAgICAgIDx0YWJsZWNvbW1vbiB2LWZvcj1cInRhYmxlIGluICRzdG9yZS5nZXR0ZXJzWydqb3VybmFsU3RhdGUvdGFibGVzJ11cIiA6bmFtZT1cInRhYmxlXCIgOmtleT1cInRhYmxlXCI+PC90YWJsZWNvbW1vbj5cbj09PT09PT1cbiAgICAgICAgICAgICAgICA8dGFibGVjb21tb24gdi1mb3I9XCJ0YWJsZSBpbiAkc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL3RhYmxlcyddXCIgOm5hbWU9XCJ0YWJsZVwiIDprZXk9XCIkc3RvcmUuZ2V0dGVyc1snam91cm5hbFN0YXRlL2pvdXJuYWxOYW1lJ10rJ18nK3RhYmxlXCI+PC90YWJsZWNvbW1vbj5cbj4+Pj4+Pj4gMzA0YWRmY2Y2NmE1Yjk2NWMwYmVkNjg5NzJlZWUyYmU1M2ZiMTlmY1xuICAgICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICAgIDx0ZW1wbGF0ZSB2LWVsc2UgPlxuICAgICAgICAgICAgICAgIDxzcGFuPtCd0LXRgiDQtNCw0L3QvdGL0YU8L3NwYW4+XG4gICAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICA8L2FydGljbGU+XG4gICAgPC9tYWluPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdD5cbmltcG9ydCBUYWJsZUNvbW1vbiBmcm9tICcuL1RhYmxlQ29tbW9uLnZ1ZSc7XG5pbXBvcnQgSm91cm5hbFBhbmVsIGZyb20gJy4vSm91cm5hbFBhbmVsLnZ1ZSc7XG5cbmV4cG9ydCBkZWZhdWx0IHtcbiAgICBuYW1lOiBcIkpvdXJuYWxQYWdlXCIsXG4gICAgY29tcG9uZW50czoge1xuICAgICAgICAndGFibGVjb21tb24nOiBUYWJsZUNvbW1vbixcbiAgICAgICAgJ2pvdXJuYWwtcGFuZWwnOiBKb3VybmFsUGFuZWxcbiAgICB9LFxuICAgIHVwZGF0ZWQgKCkge1xuICAgICAgICAvLyBpZiAodGhpcy4kcm91dGUucGFyYW1zLnNoaWZ0X2lkKSB7XG4gICAgICAgIC8vICAgICB0aGlzLiRzdG9yZS5kaXNwYXRjaCgnam91cm5hbFN0YXRlL2xvYWRKb3VybmFsJywgdGhpcy4kcm91dGUucGFyYW1zLnNoaWZ0X2lkKVxuICAgICAgICAvLyB9XG4gICAgfSxcbiAgICBtb3VudGVkICgpIHtcbiAgICAgICAgdGhpcy4kY29ubmVjdCgpO1xuXG4gICAgICAgIGlmICh0aGlzLiRyb3V0ZS5wYXJhbXMuc2hpZnRfaWQpIHtcbiAgICAgICAgICAgIHRoaXMuJHN0b3JlLmRpc3BhdGNoKCdqb3VybmFsU3RhdGUvbG9hZEpvdXJuYWwnLCB0aGlzLiRyb3V0ZS5wYXJhbXMuc2hpZnRfaWQpXG4gICAgICAgIH1cbiAgICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cblxuPC9zdHlsZT5cbiIsImV4cG9ydHMgPSBtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoXCIuLi8uLi9ub2RlX21vZHVsZXMvY3NzLWxvYWRlci9saWIvY3NzLWJhc2UuanNcIikoZmFsc2UpO1xuLy8gaW1wb3J0c1xuXG5cbi8vIG1vZHVsZVxuZXhwb3J0cy5wdXNoKFttb2R1bGUuaWQsIFwiXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXFxuXCIsIFwiXCJdKTtcblxuLy8gZXhwb3J0c1xuIiwidmFyIHJlbmRlciA9IGZ1bmN0aW9uKCkge1xuICB2YXIgX3ZtID0gdGhpc1xuICB2YXIgX2ggPSBfdm0uJGNyZWF0ZUVsZW1lbnRcbiAgdmFyIF9jID0gX3ZtLl9zZWxmLl9jIHx8IF9oXG4gIHJldHVybiBfYyhcbiAgICBcIm1haW5cIixcbiAgICB7IHN0YXRpY0NsYXNzOiBcImpvdXJuYWwtcGFnZVwiLCBhdHRyczogeyBcImRhdGEtbW9kZVwiOiBcIj8/IHBhZ2VfbW9kZSA/P1wiIH0gfSxcbiAgICBbXG4gICAgICBfYyhcImpvdXJuYWwtcGFuZWxcIiksXG4gICAgICBfdm0uX3YoXCIgXCIpLFxuICAgICAgX2MoXG4gICAgICAgIFwiYXJ0aWNsZVwiLFxuICAgICAgICB7IHN0YXRpY0NsYXNzOiBcImpvdXJuYWwtdGFibGVzXCIgfSxcbiAgICAgICAgW1xuICAgICAgICAgIF92bS4kc3RvcmUuZ2V0dGVyc1tcImpvdXJuYWxTdGF0ZS9sb2FkZWRcIl1cbiAgICAgICAgICAgID8gW1xuICAgICAgICAgICAgICAgIF92bS5fdihcIlxcbjw8PDw8PDwgSEVBRFxcbiAgICAgICAgICAgICAgICBcIiksXG4gICAgICAgICAgICAgICAgX3ZtLl9sKF92bS4kc3RvcmUuZ2V0dGVyc1tcImpvdXJuYWxTdGF0ZS90YWJsZXNcIl0sIGZ1bmN0aW9uKFxuICAgICAgICAgICAgICAgICAgdGFibGVcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgIHJldHVybiBfYyhcInRhYmxlY29tbW9uXCIsIHtcbiAgICAgICAgICAgICAgICAgICAga2V5OiB0YWJsZSxcbiAgICAgICAgICAgICAgICAgICAgYXR0cnM6IHsgbmFtZTogdGFibGUgfVxuICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICB9KSxcbiAgICAgICAgICAgICAgICBfdm0uX3YoXCJcXG49PT09PT09XFxuICAgICAgICAgICAgICAgIFwiKSxcbiAgICAgICAgICAgICAgICBfdm0uX2woX3ZtLiRzdG9yZS5nZXR0ZXJzW1wiam91cm5hbFN0YXRlL3RhYmxlc1wiXSwgZnVuY3Rpb24oXG4gICAgICAgICAgICAgICAgICB0YWJsZVxuICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgcmV0dXJuIF9jKFwidGFibGVjb21tb25cIiwge1xuICAgICAgICAgICAgICAgICAgICBrZXk6XG4gICAgICAgICAgICAgICAgICAgICAgX3ZtLiRzdG9yZS5nZXR0ZXJzW1wiam91cm5hbFN0YXRlL2pvdXJuYWxOYW1lXCJdICtcbiAgICAgICAgICAgICAgICAgICAgICBcIl9cIiArXG4gICAgICAgICAgICAgICAgICAgICAgdGFibGUsXG4gICAgICAgICAgICAgICAgICAgIGF0dHJzOiB7IG5hbWU6IHRhYmxlIH1cbiAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgfSksXG4gICAgICAgICAgICAgICAgX3ZtLl92KFxuICAgICAgICAgICAgICAgICAgXCJcXG4+Pj4+Pj4+IDMwNGFkZmNmNjZhNWI5NjVjMGJlZDY4OTcyZWVlMmJlNTNmYjE5ZmNcXG4gICAgICAgICAgICBcIlxuICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgOiBbX2MoXCJzcGFuXCIsIFtfdm0uX3YoXCLQndC10YIg0LTQsNC90L3Ri9GFXCIpXSldXG4gICAgICAgIF0sXG4gICAgICAgIDJcbiAgICAgIClcbiAgICBdLFxuICAgIDFcbiAgKVxufVxudmFyIHN0YXRpY1JlbmRlckZucyA9IFtdXG5yZW5kZXIuX3dpdGhTdHJpcHBlZCA9IHRydWVcblxuZXhwb3J0IHsgcmVuZGVyLCBzdGF0aWNSZW5kZXJGbnMgfSIsImltcG9ydCBheGlvcyBmcm9tICdheGlvcyc7XG5pbXBvcnQgVnVlQ29va2llcyBmcm9tICd2dWUtY29va2llcydcblxuY29uc3Qgam91cm5hbFN0YXRlID0ge1xuICAgIG5hbWVzcGFjZWQ6IHRydWUsXG4gICAgc3RhdGU6IHtcbiAgICAgICAgcGxhbnRzSW5mbzogW10sXG4gICAgICAgIGpvdXJuYWxJbmZvOiB7fSxcbiAgICAgICAgbG9hZGVkOiBmYWxzZSxcbiAgICAgICAgc29ja2V0OiB7XG4gICAgICAgICAgICBpc0Nvbm5lY3RlZDogZmFsc2UsXG4gICAgICAgICAgICByZWNvbm5lY3RFcnJvcjogZmFsc2UsXG4gICAgICAgIH0sXG4gICAgICAgIGlzU3luY2hyb25pemVkOiB0cnVlXG4gICAgfSxcbiAgICBnZXR0ZXJzOiB7XG4gICAgICAgIGxvYWRlZDogc3RhdGUgPT4gc3RhdGUubG9hZGVkLFxuICAgICAgICBqb3VybmFsSW5mbzogc3RhdGUgPT4gIHN0YXRlLmpvdXJuYWxJbmZvLFxuICAgICAgICB0YWJsZXM6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gT2JqZWN0LmtleXMoc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXMpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gW107XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGlzU3luY2hyb25pemVkOiBzdGF0ZSA9PiBzdGF0ZS5pc1N5bmNocm9uaXplZCxcbiAgICAgICAgcGxhbnRzOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICByZXR1cm4gc3RhdGUucGxhbnRzSW5mb1xuICAgICAgICB9LFxuICAgICAgICBwbGFudE5hbWU6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8ucGxhbnQubmFtZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBwbGFudFZlcmJvc2VOYW1lOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLnBsYW50Lm5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgam91cm5hbE5hbWU6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC5uYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGpvdXJuYWxWZXJib3NlTmFtZTogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLm5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgdGFibGVWZXJib3NlTmFtZTogKHN0YXRlKSA9PiAodGFibGVOYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHRhYmxlTmFtZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBmaWVsZFZlcmJvc2VOYW1lOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUsIGZpZWxkTmFtZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBmaWVsZE5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgc2hpZnRPcmRlcjogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5vcmRlclxuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gLTE7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGNlbGxWYWx1ZTogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUsIHJvd0luZGV4KSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKGZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGNlbGwgdmFsdWUgb2YgdW5leGlzdGVudCBmaWVsZDogJyArIGZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgbGV0IGNlbGxzID0gZmllbGRzW2ZpZWxkTmFtZV0uY2VsbHM7XG4gICAgICAgICAgICAgICAgaWYgKE9iamVjdC5rZXlzKGNlbGxzKS5sZW5ndGggIT09IDApIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHJvd0luZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gY2VsbHNbcm93SW5kZXhdLnZhbHVlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBnZXQgY2VsbCB2YWx1ZSB3aXRoIHVuZXhpc3RlbnQgaW5kZXg6ICcgKyBmaWVsZE5hbWUgKyAnICcgKyByb3dJbmRleCk7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGNlbGxDb21tZW50OiAoc3RhdGUpID0+ICh0YWJsZU5hbWUsIGZpZWxkTmFtZSwgcm93SW5kZXgpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgaWYgKCEoZmllbGROYW1lIGluIGZpZWxkcykpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBnZXQgY2VsbCBjb21tZW50IG9mIHVuZXhpc3RlbnQgZmllbGQ6ICcgKyBmaWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGxldCBjZWxscyA9IGZpZWxkc1tmaWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChPYmplY3Qua2V5cyhjZWxscykubGVuZ3RoICE9PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChyb3dJbmRleCBpbiBjZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGNlbGxzW3Jvd0luZGV4XS5jb21tZW50O1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBnZXQgY2VsbCBjb21tZW50IHdpdGggdW5leGlzdGVudCBpbmRleDogJyArIGZpZWxkTmFtZSArICcgJyArIHJvd0luZGV4KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgZmllbGRDZWxsczogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgaWYgKGZpZWxkTmFtZSBpbiBmaWVsZHMpIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzW2ZpZWxkTmFtZV0uY2VsbHNcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSByZXR1cm4gW11cbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIFtdXG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHVuc3luY0pvdXJuYWxDZWxsczogKHN0YXRlLCBnZXR0ZXJzKSA9PiAoKSA9PiB7XG4gICAgICAgICAgICBsZXQgdW5zeW5jQ2VsbHMgPSBbXVxuICAgICAgICAgICAgZ2V0dGVycy50YWJsZXMubWFwKCh0YWJsZSwgaW5kZXgpID0+IHtcbiAgICAgICAgICAgICAgICBsZXQgY3VycmVudFRhYmxlID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVdXG4gICAgICAgICAgICAgICAgZm9yIChsZXQgZmllbGQgaW4gY3VycmVudFRhYmxlLmZpZWxkcykge1xuICAgICAgICAgICAgICAgICAgICBsZXQgY3VycmVudENlbGxzID0gY3VycmVudFRhYmxlLmZpZWxkc1tmaWVsZF0uY2VsbHNcbiAgICAgICAgICAgICAgICAgICAgZm9yIChsZXQgY2VsbCBpbiBjdXJyZW50Q2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChjdXJyZW50Q2VsbHNbY2VsbF0ubm90U3luY2hyb25pemVkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdW5zeW5jQ2VsbHMucHVzaChjdXJyZW50Q2VsbHNbY2VsbF0pXG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KVxuICAgICAgICAgICAgcmV0dXJuIHVuc3luY0NlbGxzXG4gICAgICAgIH0sXG4gICAgICAgIG1heFJvd0luZGV4OiAoc3RhdGUpID0+ICh0YWJsZU5hbWUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgbWF4ID0gLTE7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGZvcihsZXQgZmllbGQgaW4gZmllbGRzKSB7XG4gICAgICAgICAgICAgICAgICAgIGZvciAobGV0IGluZGV4IGluIGZpZWxkc1tmaWVsZF0uY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGluZGV4ID0gcGFyc2VJbnQoaW5kZXgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgbWF4ID0gbWF4IDwgaW5kZXggPyBpbmRleCA6IG1heDtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gbWF4KzE7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAtMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgcm93SXNFbXB0eTogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBpbmRleCkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkc1xuICAgICAgICAgICAgICAgIGZvciAobGV0IGZpZWxkIGluIGZpZWxkcykge1xuICAgICAgICAgICAgICAgICAgICBpZiAoJ2NlbGxzJyBpbiBmaWVsZHNbZmllbGRdKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoaW5kZXggaW4gZmllbGRzW2ZpZWxkXS5jZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBmYWxzZVxuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiB0cnVlXG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHRhYmxlVGl0bGU6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSkgPT4ge1xuICAgICAgICAgICAgcmV0dXJuICfQl9Cw0LPQvtC70L7QstC+0Log0YLQsNCx0LvQuNGG0YsnXG4gICAgICAgIH0sXG4gICAgICAgIGZpZWxkRGVzY3JpcHRpb246IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgZmllbGROYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKGZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNvbnNvbGUubG9nKFwiV0FSTklORyEgVHJ5aW5nIHRvIGdldCBmaWVsZCBkZXNjdGlwdGlvbiBvZiB1bmV4aXN0ZW50IGZpZWxkOiBcIiArIGZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB7fTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIGZpZWxkc1tmaWVsZE5hbWVdLmZpZWxkX2Rlc2NyaXB0aW9uIHx8ICcnXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJydcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0sXG4gICAgbXV0YXRpb25zOiB7XG4gICAgICAgIFNFVF9TWU5DSFJPTklaRUQgKHN0YXRlLCBpc1N5bmNocm9uaXplZCkge1xuICAgICAgICAgICAgc3RhdGUuaXNTeW5jaHJvbml6ZWQgPSBpc1N5bmNocm9uaXplZFxuICAgICAgICB9LFxuICAgICAgICBVUERBVEVfSk9VUk5BTF9JTkZPIChzdGF0ZSwgam91cm5hbEluZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLmpvdXJuYWxJbmZvID0gam91cm5hbEluZm87XG4gICAgICAgIH0sXG4gICAgICAgIFVQREFURV9QTEFOVFNfSU5GTyAoc3RhdGUsIHBsYW50c0luZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLnBsYW50c0luZm8gPSBwbGFudHNJbmZvO1xuICAgICAgICB9LFxuICAgICAgICBTRVRfTE9BREVEIChzdGF0ZSwgbG9hZGVkKSB7XG4gICAgICAgICAgICBzdGF0ZS5sb2FkZWQgPSBsb2FkZWQ7XG4gICAgICAgIH0sXG4gICAgICAgIFNBVkVfQ0VMTF9WQUxVRSAoc3RhdGUsIHBheWxvYWQpIHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbcGF5bG9hZC50YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShwYXlsb2FkLmZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gc2F2ZSB2YWx1ZSBvZiB1bmV4aXN0ZW50IGZpZWxkOiAnICsgcGF5bG9hZC5maWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICAvLyBjb25zb2xlLmxvZygnICBDcmVhdGluZyBmaWVsZCAnICsgcGF5bG9hZC5maWVsZE5hbWUgKyAnLi4uJyk7XG4gICAgICAgICAgICAgICAgICAgIGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV0gPSB7fTtcbiAgICAgICAgICAgICAgICAgICAgZmllbGRzW3BheWxvYWQuZmllbGROYW1lXVsnY2VsbHMnXSA9IHt9O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBsZXQgY2VsbHMgPSBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLnZhbHVlKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLmluZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAvLyB1cGRhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ3ZhbHVlJ10gPSBwYXlsb2FkLnZhbHVlO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKHBheWxvYWQubm90U3luY2hyb25pemVkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ25vdFN5bmNocm9uaXplZCddID0gcGF5bG9hZC5ub3RTeW5jaHJvbml6ZWQ7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ2ZpZWxkTmFtZSddID0gcGF5bG9hZC5maWVsZE5hbWU7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ3RhYmxlTmFtZSddID0gcGF5bG9hZC50YWJsZU5hbWU7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ2luZGV4J10gPSBwYXlsb2FkLmluZGV4O1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gY3JlYXRlIGNlbGxcbiAgICAgICAgICAgICAgICAgICAgICAgIFZ1ZS5zZXQoY2VsbHMsIHBheWxvYWQuaW5kZXgsIHt9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIFZ1ZS5zZXQoY2VsbHNbcGF5bG9hZC5pbmRleF0sICd2YWx1ZScsIHBheWxvYWQudmFsdWUpO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKHBheWxvYWQubm90U3luY2hyb25pemVkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgVnVlLnNldChjZWxsc1twYXlsb2FkLmluZGV4XSwgJ25vdFN5bmNocm9uaXplZCcsIHBheWxvYWQubm90U3luY2hyb25pemVkKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgVnVlLmRlbGV0ZShjZWxscywgcGF5bG9hZC5pbmRleCk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBTQVZFX0NFTExfQ09NTUVOVCAoc3RhdGUsIHBheWxvYWQpIHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbcGF5bG9hZC50YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShwYXlsb2FkLmZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gc2F2ZSBjb21tZW50IG9mIHVuZXhpc3RlbnQgZmllbGQ6ICcgKyBwYXlsb2FkLmZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNvbnNvbGUubG9nKCcgIENyZWF0aW5nIGZpZWxkICcgKyBwYXlsb2FkLmZpZWxkTmFtZSArICcuLi4nKTtcbiAgICAgICAgICAgICAgICAgICAgZmllbGRzW3BheWxvYWQuZmllbGROYW1lXSA9IHt9O1xuICAgICAgICAgICAgICAgICAgICBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdWydjZWxscyddID0ge307XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGxldCBjZWxscyA9IGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV0uY2VsbHM7XG4gICAgICAgICAgICAgICAgaWYgKHBheWxvYWQuY29tbWVudCkge1xuICAgICAgICAgICAgICAgICAgICBpZiAocGF5bG9hZC5pbmRleCBpbiBjZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gdXBkYXRlIGNlbGxcbiAgICAgICAgICAgICAgICAgICAgICAgIGNlbGxzW3BheWxvYWQuaW5kZXhdWydjb21tZW50J10gPSBwYXlsb2FkLmNvbW1lbnQ7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAvLyBjcmVhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICAgICAgVnVlLnNldChjZWxscywgcGF5bG9hZC5pbmRleCwge30pO1xuICAgICAgICAgICAgICAgICAgICAgICAgVnVlLnNldChjZWxsc1twYXlsb2FkLmluZGV4XSwgJ2NvbW1lbnQnLCBwYXlsb2FkLmNvbW1lbnQpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICBWdWUuZGVsZXRlKGNlbGxzLCBwYXlsb2FkLmluZGV4KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIFNFVF9QQUdFX01PREUgKHN0YXRlLCBtb2RlKSB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgc3RhdGUuam91cm5hbEluZm8ubW9kZSA9IG1vZGVcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgU09DS0VUX09OT1BFTiAoc3RhdGUsIGV2ZW50KSAge1xuICAgICAgICAgICAgVnVlLnByb3RvdHlwZS4kc29ja2V0ID0gZXZlbnQuY3VycmVudFRhcmdldFxuICAgICAgICAgICAgc3RhdGUuc29ja2V0LmlzQ29ubmVjdGVkID0gdHJ1ZVxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfT05DTE9TRSAoc3RhdGUsIGV2ZW50KSAge1xuICAgICAgICAgICAgc3RhdGUuc29ja2V0LmlzQ29ubmVjdGVkID0gZmFsc2VcbiAgICAgICAgfSxcbiAgICAgICAgU09DS0VUX09ORVJST1IgKHN0YXRlLCBldmVudCkgIHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3Ioc3RhdGUsIGV2ZW50KVxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfT05NRVNTQUdFIChzdGF0ZSwgbWVzc2FnZSkgIHtcblxuICAgICAgICB9LFxuICAgICAgICBTT0NLRVRfUkVDT05ORUNUKHN0YXRlLCBjb3VudCkge1xuICAgICAgICAgICAgY29uc29sZS5pbmZvKHN0YXRlLCBjb3VudClcbiAgICAgICAgfSxcbiAgICAgICAgU09DS0VUX1JFQ09OTkVDVF9FUlJPUihzdGF0ZSkge1xuICAgICAgICAgICAgc3RhdGUuc29ja2V0LnJlY29ubmVjdEVycm9yID0gdHJ1ZTtcbiAgICAgICAgfSxcbiAgICB9LFxuICAgIGFjdGlvbnM6IHtcbiAgICAgICAgbG9hZEpvdXJuYWw6IGZ1bmN0aW9uICh7IGNvbW1pdCwgc3RhdGUsIGdldHRlcnMgfSwgcGF5bG9hZCkge1xuICAgICAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXMsIHJlaikgPT4ge1xuICAgICAgICAgICAgICAgIGF4aW9zXG4gICAgICAgICAgICAgICAgICAgIC5nZXQoJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hcGkvc2hpZnRzLycgKyBwYXlsb2FkLCB7XG4gICAgICAgICAgICAgICAgICAgICAgICB3aXRoQ3JlZGVudGlhbHM6IHRydWVcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29tbWl0KCdVUERBVEVfSk9VUk5BTF9JTkZPJywgZ2V0dGVycy5pc1N5bmNocm9uaXplZCA/IHJlc3BvbnNlLmRhdGEgOiBKU09OLnBhcnNlKGxvY2FsU3RvcmFnZS5nZXRJdGVtKCd2dWV4JykpLmpvdXJuYWxTdGF0ZS5qb3VybmFsSW5mbyk7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1NFVF9MT0FERUQnLCB0cnVlKTtcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzKClcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgLmNhdGNoKChlcnIpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGVycilcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgIH0pXG4gICAgICAgIH0sXG4gICAgICAgIGxvYWRQbGFudHM6IGZ1bmN0aW9uICh7IGNvbW1pdCwgc3RhdGUsIGdldHRlcnMgfSkge1xuICAgICAgICAgICAgYXhpb3NcbiAgICAgICAgICAgICAgICAuZ2V0KCdodHRwOi8vbG9jYWxob3N0OjgwMDAvYXBpL21lbnVfaW5mby8nKVxuICAgICAgICAgICAgICAgIC50aGVuKHJlc3BvbnNlID0+IHtcbiAgICAgICAgICAgICAgICAgICAgY29tbWl0KCdVUERBVEVfUExBTlRTX0lORk8nLCByZXNwb25zZS5kYXRhLnBsYW50cyk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgfSxcbiAgICAgICAgc2VuZFVuc3luY0NlbGw6IGZ1bmN0aW9uICh7IGNvbW1pdCwgc3RhdGUsIGdldHRlcnMgfSwgcGF5bG9hZCkge1xuICAgICAgICAgICAgd2luZG93Lm12LiRzb2NrZXQuc2VuZE9iaih7XG4gICAgICAgICAgICAgICAgJ3R5cGUnOiAnc2hpZnRfZGF0YScsXG4gICAgICAgICAgICAgICAgJ2NlbGxfbG9jYXRpb24nOiB7XG4gICAgICAgICAgICAgICAgICAgICdncm91cF9pZCc6IGdldHRlcnMuam91cm5hbEluZm8uaWQsXG4gICAgICAgICAgICAgICAgICAgICd0YWJsZV9uYW1lJzogcGF5bG9hZC50YWJsZU5hbWUsXG4gICAgICAgICAgICAgICAgICAgICdmaWVsZF9uYW1lJzogcGF5bG9hZC5maWVsZE5hbWUsXG4gICAgICAgICAgICAgICAgICAgICdpbmRleCc6IHBheWxvYWQuaW5kZXhcbiAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICd2YWx1ZSc6IHBheWxvYWQudmFsdWVcbiAgICAgICAgICAgIH0pXG4gICAgICAgIH0sXG4gICAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBqb3VybmFsU3RhdGVcbiJdLCJzb3VyY2VSb290IjoiIn0=