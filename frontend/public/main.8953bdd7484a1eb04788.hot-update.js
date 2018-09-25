webpackHotUpdate("main",{

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
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! axios */ "./node_modules/axios/index.js");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_3__);




var journalState = {
  namespaced: true,
  state: {
    plantsInfo: [],
    journalInfo: {},
    loaded: false
  },
  getters: {
    loaded: function loaded(state) {
      return state.loaded;
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
    journalName: function journalName(state) {
      if (state.loaded) {
        return state.journalInfo.journal.name;
      } else {
        return '';
      }
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
            }
          } else {
            return '';
          }
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

        if (payload.index in cells) {
          // update cell
          cells[payload.index]['value'] = payload.value;
        } else {
          // create cell
          cells[payload.index] = {};
          cells[payload.index]['value'] = payload.value;
        }
      }
    }
  },
  actions: {
    loadJournal: function loadJournal(_ref, payload) {
      var commit = _ref.commit,
          state = _ref.state,
          getters = _ref.getters;
      axios__WEBPACK_IMPORTED_MODULE_3___default.a.get('http://localhost:8000/api/shifts/' + payload, {
        headers: {
          Authorization: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNTksInVzZXJuYW1lIjoiaW5mcmFtaW5lIiwiZXhwIjoxNTM3ODA5OTQzLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.BOtmGRgf6GqyK92CT4VR-uvdX_4IGlW0UATmHtVY2MA'
        }
      }).then(function (response) {
        commit('UPDATE_JOURNAL_INFO', response.data);
        commit('SET_LOADED', true);
      });
    },
    loadPlants: function loadPlants(_ref2) {
      var commit = _ref2.commit,
          state = _ref2.state,
          getters = _ref2.getters;
      axios__WEBPACK_IMPORTED_MODULE_3___default.a.get('http://localhost:8000/api/menu_info/').then(function (response) {
        commit('UPDATE_PLANTS_INFO', response.data.plants);
      });
    }
  }
};
/* harmony default export */ __webpack_exports__["default"] = (journalState);

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9zcmMvc3RvcmUvbW9kdWxlcy9qb3VybmFsU3RhdGUuanMiXSwibmFtZXMiOlsiam91cm5hbFN0YXRlIiwibmFtZXNwYWNlZCIsInN0YXRlIiwicGxhbnRzSW5mbyIsImpvdXJuYWxJbmZvIiwibG9hZGVkIiwiZ2V0dGVycyIsInRhYmxlcyIsIk9iamVjdCIsImtleXMiLCJqb3VybmFsIiwicGxhbnRzIiwicGxhbnROYW1lIiwicGxhbnQiLCJuYW1lIiwiam91cm5hbE5hbWUiLCJzaGlmdE9yZGVyIiwib3JkZXIiLCJjZWxsVmFsdWUiLCJ0YWJsZU5hbWUiLCJmaWVsZE5hbWUiLCJyb3dJbmRleCIsImZpZWxkcyIsImNvbnNvbGUiLCJsb2ciLCJjZWxscyIsImxlbmd0aCIsInZhbHVlIiwibWF4Um93SW5kZXgiLCJtYXgiLCJmaWVsZCIsImluZGV4IiwicGFyc2VJbnQiLCJ0YWJsZVRpdGxlIiwiZmllbGREZXNjcmlwdGlvbiIsImZpZWxkX2Rlc2NyaXB0aW9uIiwibXV0YXRpb25zIiwiVVBEQVRFX0pPVVJOQUxfSU5GTyIsIlVQREFURV9QTEFOVFNfSU5GTyIsIlNFVF9MT0FERUQiLCJTQVZFX0NFTExfVkFMVUUiLCJwYXlsb2FkIiwiYWN0aW9ucyIsImxvYWRKb3VybmFsIiwiY29tbWl0IiwiYXhpb3MiLCJnZXQiLCJoZWFkZXJzIiwiQXV0aG9yaXphdGlvbiIsInRoZW4iLCJyZXNwb25zZSIsImRhdGEiLCJsb2FkUGxhbnRzIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7QUFFQSxJQUFNQSxlQUFlO0FBQ2pCQyxjQUFZLElBREs7QUFFakJDLFNBQU87QUFDSEMsZ0JBQVksRUFEVDtBQUVIQyxpQkFBYSxFQUZWO0FBR0hDLFlBQVE7QUFITCxHQUZVO0FBT2pCQyxXQUFTO0FBQ0xELFlBQVE7QUFBQSxhQUFTSCxNQUFNRyxNQUFmO0FBQUEsS0FESDtBQUVMRSxZQUFRLHVCQUFTO0FBQ2IsVUFBSUwsTUFBTUcsTUFBVixFQUFrQjtBQUNkLGVBQU9HLE9BQU9DLElBQVAsQ0FBWVAsTUFBTUUsV0FBTixDQUFrQk0sT0FBbEIsQ0FBMEJILE1BQXRDLENBQVA7QUFDSCxPQUZELE1BRU87QUFDSCxlQUFPLEVBQVA7QUFDSDtBQUNKLEtBUkk7QUFTTEksWUFBUSx1QkFBUztBQUNiLGFBQU9ULE1BQU1DLFVBQWI7QUFDSCxLQVhJO0FBWUxTLGVBQVcsMEJBQVM7QUFDaEIsVUFBSVYsTUFBTUcsTUFBVixFQUFrQjtBQUNkLGVBQU9ILE1BQU1FLFdBQU4sQ0FBa0JTLEtBQWxCLENBQXdCQyxJQUEvQjtBQUNILE9BRkQsTUFFTztBQUNILGVBQU8sRUFBUDtBQUNIO0FBQ0osS0FsQkk7QUFtQkxDLGlCQUFhLDRCQUFTO0FBQ2xCLFVBQUliLE1BQU1HLE1BQVYsRUFBa0I7QUFDZCxlQUFPSCxNQUFNRSxXQUFOLENBQWtCTSxPQUFsQixDQUEwQkksSUFBakM7QUFDSCxPQUZELE1BRU87QUFDSCxlQUFPLEVBQVA7QUFDSDtBQUNKLEtBekJJO0FBMEJMRSxnQkFBWSwyQkFBUztBQUNqQixVQUFJZCxNQUFNRyxNQUFWLEVBQWtCO0FBQ2QsZUFBT0gsTUFBTUUsV0FBTixDQUFrQmEsS0FBekI7QUFDSCxPQUZELE1BRU87QUFDSCxlQUFPLENBQUMsQ0FBUjtBQUNIO0FBQ0osS0FoQ0k7QUFpQ0xDLGVBQVcsbUJBQUNoQixLQUFEO0FBQUEsYUFBVyxVQUFDaUIsU0FBRCxFQUFZQyxTQUFaLEVBQXVCQyxRQUF2QixFQUFvQztBQUN0RCxZQUFJbkIsTUFBTUcsTUFBVixFQUFrQjtBQUNkLGNBQUlpQixTQUFTcEIsTUFBTUUsV0FBTixDQUFrQk0sT0FBbEIsQ0FBMEJILE1BQTFCLENBQWlDWSxTQUFqQyxFQUE0Q0csTUFBekQ7O0FBQ0EsY0FBSSxFQUFFRixhQUFhRSxNQUFmLENBQUosRUFBNEI7QUFDeEJDLG9CQUFRQyxHQUFSLENBQVksNERBQTRESixTQUF4RTtBQUNBLG1CQUFPLEVBQVA7QUFDSDs7QUFDRCxjQUFJSyxRQUFRSCxPQUFPRixTQUFQLEVBQWtCSyxLQUE5Qjs7QUFDQSxjQUFJakIsT0FBT0MsSUFBUCxDQUFZZ0IsS0FBWixFQUFtQkMsTUFBbkIsS0FBOEIsQ0FBbEMsRUFBcUM7QUFDakMsZ0JBQUlMLFlBQVlJLEtBQWhCLEVBQXVCO0FBQ25CLHFCQUFPQSxNQUFNSixRQUFOLEVBQWdCTSxLQUF2QjtBQUNIO0FBQ0osV0FKRCxNQUtLO0FBQ0QsbUJBQU8sRUFBUDtBQUNIO0FBQ0o7QUFDSixPQWpCVTtBQUFBLEtBakNOO0FBbURMQyxpQkFBYSxxQkFBQzFCLEtBQUQ7QUFBQSxhQUFXLFVBQUNpQixTQUFELEVBQWU7QUFDbkMsWUFBSWpCLE1BQU1HLE1BQVYsRUFBa0I7QUFDZCxjQUFJd0IsTUFBTSxDQUFDLENBQVg7QUFDQSxjQUFJUCxTQUFTcEIsTUFBTUUsV0FBTixDQUFrQk0sT0FBbEIsQ0FBMEJILE1BQTFCLENBQWlDWSxTQUFqQyxFQUE0Q0csTUFBekQ7O0FBQ0EsZUFBSSxJQUFJUSxLQUFSLElBQWlCUixNQUFqQixFQUF5QjtBQUNyQixpQkFBSyxJQUFJUyxLQUFULElBQWtCVCxPQUFPUSxLQUFQLEVBQWNMLEtBQWhDLEVBQXVDO0FBQ25DTSxzQkFBUUMsU0FBU0QsS0FBVCxDQUFSO0FBQ0FGLG9CQUFNQSxNQUFNRSxLQUFOLEdBQWNBLEtBQWQsR0FBc0JGLEdBQTVCO0FBQ0g7QUFDSjs7QUFDRCxpQkFBT0EsTUFBSSxDQUFYO0FBQ0gsU0FWRCxNQVVPO0FBQ0gsaUJBQU8sQ0FBQyxDQUFSO0FBQ0g7QUFDSixPQWRZO0FBQUEsS0FuRFI7QUFrRUxJLGdCQUFZLG9CQUFDL0IsS0FBRDtBQUFBLGFBQVcsVUFBQ2lCLFNBQUQsRUFBZTtBQUNsQyxlQUFPLG1CQUFQO0FBQ0gsT0FGVztBQUFBLEtBbEVQO0FBcUVMZSxzQkFBa0IsMEJBQUNoQyxLQUFEO0FBQUEsYUFBVyxVQUFDaUIsU0FBRCxFQUFZQyxTQUFaLEVBQTBCO0FBQ25ELFlBQUlsQixNQUFNRyxNQUFWLEVBQWtCO0FBQ2QsY0FBSWlCLFNBQVNwQixNQUFNRSxXQUFOLENBQWtCTSxPQUFsQixDQUEwQkgsTUFBMUIsQ0FBaUNZLFNBQWpDLEVBQTRDRyxNQUF6RDs7QUFDQSxjQUFJLEVBQUVGLGFBQWFFLE1BQWYsQ0FBSixFQUE0QjtBQUN4QkMsb0JBQVFDLEdBQVIsQ0FBWSxtRUFBbUVKLFNBQS9FO0FBQ0EsbUJBQU8sRUFBUDtBQUNIOztBQUNELGlCQUFPRSxPQUFPRixTQUFQLEVBQWtCZSxpQkFBbEIsSUFBdUMsRUFBOUM7QUFDSCxTQVBELE1BUUs7QUFDRCxpQkFBTyxFQUFQO0FBQ0g7QUFDSixPQVppQjtBQUFBO0FBckViLEdBUFE7QUEwRmpCQyxhQUFXO0FBQ1BDLHVCQURPLCtCQUNjbkMsS0FEZCxFQUNxQkUsV0FEckIsRUFDa0M7QUFDckNGLFlBQU1FLFdBQU4sR0FBb0JBLFdBQXBCO0FBQ0gsS0FITTtBQUlQa0Msc0JBSk8sOEJBSWFwQyxLQUpiLEVBSW9CQyxVQUpwQixFQUlnQztBQUNuQ0QsWUFBTUMsVUFBTixHQUFtQkEsVUFBbkI7QUFDSCxLQU5NO0FBT1BvQyxjQVBPLHNCQU9LckMsS0FQTCxFQU9ZRyxNQVBaLEVBT29CO0FBQ3ZCSCxZQUFNRyxNQUFOLEdBQWVBLE1BQWY7QUFDSCxLQVRNO0FBVVBtQyxtQkFWTywyQkFVVXRDLEtBVlYsRUFVaUJ1QyxPQVZqQixFQVUwQjtBQUM3QixVQUFJdkMsTUFBTUcsTUFBVixFQUFrQjtBQUNkLFlBQUlpQixTQUFTcEIsTUFBTUUsV0FBTixDQUFrQk0sT0FBbEIsQ0FBMEJILE1BQTFCLENBQWlDa0MsUUFBUXRCLFNBQXpDLEVBQW9ERyxNQUFqRTs7QUFDQSxZQUFJLEVBQUVtQixRQUFRckIsU0FBUixJQUFxQkUsTUFBdkIsQ0FBSixFQUFvQztBQUNoQ0Msa0JBQVFDLEdBQVIsQ0FBWSx3REFBd0RpQixRQUFRckIsU0FBNUU7QUFDQUcsa0JBQVFDLEdBQVIsQ0FBWSxzQkFBc0JpQixRQUFRckIsU0FBOUIsR0FBMEMsS0FBdEQ7QUFDQUUsaUJBQU9tQixRQUFRckIsU0FBZixJQUE0QixFQUE1QjtBQUNBRSxpQkFBT21CLFFBQVFyQixTQUFmLEVBQTBCLE9BQTFCLElBQXFDLEVBQXJDO0FBQ0g7O0FBQ0QsWUFBSUssUUFBUUgsT0FBT21CLFFBQVFyQixTQUFmLEVBQTBCSyxLQUF0Qzs7QUFDQSxZQUFJZ0IsUUFBUVYsS0FBUixJQUFpQk4sS0FBckIsRUFBNEI7QUFDeEI7QUFDQUEsZ0JBQU1nQixRQUFRVixLQUFkLEVBQXFCLE9BQXJCLElBQWdDVSxRQUFRZCxLQUF4QztBQUNILFNBSEQsTUFJSztBQUNEO0FBQ0FGLGdCQUFNZ0IsUUFBUVYsS0FBZCxJQUF1QixFQUF2QjtBQUNBTixnQkFBTWdCLFFBQVFWLEtBQWQsRUFBcUIsT0FBckIsSUFBZ0NVLFFBQVFkLEtBQXhDO0FBQ0g7QUFDSjtBQUNKO0FBOUJNLEdBMUZNO0FBMEhqQmUsV0FBUztBQUNMQyxpQkFBYSwyQkFBc0NGLE9BQXRDLEVBQStDO0FBQUEsVUFBbkNHLE1BQW1DLFFBQW5DQSxNQUFtQztBQUFBLFVBQTNCMUMsS0FBMkIsUUFBM0JBLEtBQTJCO0FBQUEsVUFBcEJJLE9BQW9CLFFBQXBCQSxPQUFvQjtBQUN4RHVDLGtEQUFLQSxDQUNBQyxHQURMLENBQ1Msc0NBQXNDTCxPQUQvQyxFQUN3RDtBQUFDTSxpQkFBUztBQUN0REMseUJBQWU7QUFEdUM7QUFBVixPQUR4RCxFQUtLQyxJQUxMLENBS1Usb0JBQVk7QUFDZEwsZUFBTyxxQkFBUCxFQUE4Qk0sU0FBU0MsSUFBdkM7QUFDQVAsZUFBTyxZQUFQLEVBQXFCLElBQXJCO0FBQ0gsT0FSTDtBQVNILEtBWEk7QUFZTFEsZ0JBQVksMkJBQXNDO0FBQUEsVUFBMUJSLE1BQTBCLFNBQTFCQSxNQUEwQjtBQUFBLFVBQWxCMUMsS0FBa0IsU0FBbEJBLEtBQWtCO0FBQUEsVUFBWEksT0FBVyxTQUFYQSxPQUFXO0FBQzlDdUMsa0RBQUtBLENBQ0FDLEdBREwsQ0FDUyxzQ0FEVCxFQUVLRyxJQUZMLENBRVUsb0JBQVk7QUFDZEwsZUFBTyxvQkFBUCxFQUE2Qk0sU0FBU0MsSUFBVCxDQUFjeEMsTUFBM0M7QUFDSCxPQUpMO0FBS0g7QUFsQkk7QUExSFEsQ0FBckI7QUFnSmVYLDJFQUFmLEUiLCJmaWxlIjoibWFpbi44OTUzYmRkNzQ4NGExZWIwNDc4OC5ob3QtdXBkYXRlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IGF4aW9zIGZyb20gJ2F4aW9zJztcblxuY29uc3Qgam91cm5hbFN0YXRlID0ge1xuICAgIG5hbWVzcGFjZWQ6IHRydWUsXG4gICAgc3RhdGU6IHtcbiAgICAgICAgcGxhbnRzSW5mbzogW10sXG4gICAgICAgIGpvdXJuYWxJbmZvOiB7fSxcbiAgICAgICAgbG9hZGVkOiBmYWxzZSxcbiAgICB9LFxuICAgIGdldHRlcnM6IHtcbiAgICAgICAgbG9hZGVkOiBzdGF0ZSA9PiBzdGF0ZS5sb2FkZWQsXG4gICAgICAgIHRhYmxlczogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBPYmplY3Qua2V5cyhzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlcyk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiBbXTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgcGxhbnRzOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICByZXR1cm4gc3RhdGUucGxhbnRzSW5mb1xuICAgICAgICB9LFxuICAgICAgICBwbGFudE5hbWU6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8ucGxhbnQubmFtZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBqb3VybmFsTmFtZTogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLm5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgc2hpZnRPcmRlcjogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5vcmRlclxuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gLTE7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGNlbGxWYWx1ZTogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUsIHJvd0luZGV4KSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKGZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGNlbGwgdmFsdWUgb2YgdW5leGlzdGVudCBmaWVsZDogJyArIGZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgbGV0IGNlbGxzID0gZmllbGRzW2ZpZWxkTmFtZV0uY2VsbHM7XG4gICAgICAgICAgICAgICAgaWYgKE9iamVjdC5rZXlzKGNlbGxzKS5sZW5ndGggIT09IDApIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHJvd0luZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gY2VsbHNbcm93SW5kZXhdLnZhbHVlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBtYXhSb3dJbmRleDogKHN0YXRlKSA9PiAodGFibGVOYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IG1heCA9IC0xO1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBmb3IobGV0IGZpZWxkIGluIGZpZWxkcykge1xuICAgICAgICAgICAgICAgICAgICBmb3IgKGxldCBpbmRleCBpbiBmaWVsZHNbZmllbGRdLmNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpbmRleCA9IHBhcnNlSW50KGluZGV4KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIG1heCA9IG1heCA8IGluZGV4ID8gaW5kZXggOiBtYXg7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIG1heCsxO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gLTE7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHRhYmxlVGl0bGU6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSkgPT4ge1xuICAgICAgICAgICAgcmV0dXJuICfQl9Cw0LPQvtC70L7QstC+0Log0YLQsNCx0LvQuNGG0YsnXG4gICAgICAgIH0sXG4gICAgICAgIGZpZWxkRGVzY3JpcHRpb246IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgZmllbGROYW1lKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKGZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKFwiV0FSTklORyEgVHJ5aW5nIHRvIGdldCBmaWVsZCBkZXNjdGlwdGlvbiBvZiB1bmV4aXN0ZW50IGZpZWxkOiBcIiArIGZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB7fTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIGZpZWxkc1tmaWVsZE5hbWVdLmZpZWxkX2Rlc2NyaXB0aW9uIHx8ICcnXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJydcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0sXG4gICAgbXV0YXRpb25zOiB7XG4gICAgICAgIFVQREFURV9KT1VSTkFMX0lORk8gKHN0YXRlLCBqb3VybmFsSW5mbykge1xuICAgICAgICAgICAgc3RhdGUuam91cm5hbEluZm8gPSBqb3VybmFsSW5mbztcbiAgICAgICAgfSxcbiAgICAgICAgVVBEQVRFX1BMQU5UU19JTkZPIChzdGF0ZSwgcGxhbnRzSW5mbykge1xuICAgICAgICAgICAgc3RhdGUucGxhbnRzSW5mbyA9IHBsYW50c0luZm87XG4gICAgICAgIH0sXG4gICAgICAgIFNFVF9MT0FERUQgKHN0YXRlLCBsb2FkZWQpIHtcbiAgICAgICAgICAgIHN0YXRlLmxvYWRlZCA9IGxvYWRlZDtcbiAgICAgICAgfSxcbiAgICAgICAgU0FWRV9DRUxMX1ZBTFVFIChzdGF0ZSwgcGF5bG9hZCkge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1twYXlsb2FkLnRhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGlmICghKHBheWxvYWQuZmllbGROYW1lIGluIGZpZWxkcykpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBzYXZlIHZhbHVlIG9mIHVuZXhpc3RlbnQgZmllbGQ6ICcgKyBwYXlsb2FkLmZpZWxkTmFtZSk7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCcgIENyZWF0aW5nIGZpZWxkICcgKyBwYXlsb2FkLmZpZWxkTmFtZSArICcuLi4nKTtcbiAgICAgICAgICAgICAgICAgICAgZmllbGRzW3BheWxvYWQuZmllbGROYW1lXSA9IHt9O1xuICAgICAgICAgICAgICAgICAgICBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdWydjZWxscyddID0ge307XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGxldCBjZWxscyA9IGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV0uY2VsbHM7XG4gICAgICAgICAgICAgICAgaWYgKHBheWxvYWQuaW5kZXggaW4gY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gdXBkYXRlIGNlbGxcbiAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ3ZhbHVlJ10gPSBwYXlsb2FkLnZhbHVlO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gY3JlYXRlIGNlbGxcbiAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF0gPSB7fTtcbiAgICAgICAgICAgICAgICAgICAgY2VsbHNbcGF5bG9hZC5pbmRleF1bJ3ZhbHVlJ10gPSBwYXlsb2FkLnZhbHVlO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0sXG4gICAgYWN0aW9uczoge1xuICAgICAgICBsb2FkSm91cm5hbDogZnVuY3Rpb24gKHsgY29tbWl0LCBzdGF0ZSwgZ2V0dGVycyB9LCBwYXlsb2FkKSB7XG4gICAgICAgICAgICBheGlvc1xuICAgICAgICAgICAgICAgIC5nZXQoJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hcGkvc2hpZnRzLycgKyBwYXlsb2FkLCB7aGVhZGVyczoge1xuICAgICAgICAgICAgICAgICAgICAgICAgQXV0aG9yaXphdGlvbjogJ2V5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlKOS5leUoxYzJWeVgybGtJam94TlRrc0luVnpaWEp1WVcxbElqb2lhVzVtY21GdGFXNWxJaXdpWlhod0lqb3hOVE0zT0RBNU9UUXpMQ0psYldGcGJDSTZJbUZrYldsdVFHRmtiV2x1TG1OdmJTSjkuQk90bUdSZ2Y2R3F5SzkyQ1Q0VlItdXZkWF80SUdsVzBVQVRtSHRWWTJNQSd9XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9KT1VSTkFMX0lORk8nLCByZXNwb25zZS5kYXRhKTtcbiAgICAgICAgICAgICAgICAgICAgY29tbWl0KCdTRVRfTE9BREVEJywgdHJ1ZSk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgfSxcbiAgICAgICAgbG9hZFBsYW50czogZnVuY3Rpb24gKHsgY29tbWl0LCBzdGF0ZSwgZ2V0dGVycyB9KSB7XG4gICAgICAgICAgICBheGlvc1xuICAgICAgICAgICAgICAgIC5nZXQoJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hcGkvbWVudV9pbmZvLycpXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9QTEFOVFNfSU5GTycsIHJlc3BvbnNlLmRhdGEucGxhbnRzKTtcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICB9LFxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgam91cm5hbFN0YXRlIl0sInNvdXJjZVJvb3QiOiIifQ==