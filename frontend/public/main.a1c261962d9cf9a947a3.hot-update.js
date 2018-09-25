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
        A: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNTksInVzZXJuYW1lIjoiaW5mcmFtaW5lIiwiZXhwIjoxNTM3ODA5OTQzLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.BOtmGRgf6GqyK92CT4VR-uvdX_4IGlW0UATmHtVY2MA'
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9zcmMvc3RvcmUvbW9kdWxlcy9qb3VybmFsU3RhdGUuanMiXSwibmFtZXMiOlsiam91cm5hbFN0YXRlIiwibmFtZXNwYWNlZCIsInN0YXRlIiwicGxhbnRzSW5mbyIsImpvdXJuYWxJbmZvIiwibG9hZGVkIiwiZ2V0dGVycyIsInRhYmxlcyIsIk9iamVjdCIsImtleXMiLCJqb3VybmFsIiwicGxhbnRzIiwicGxhbnROYW1lIiwicGxhbnQiLCJuYW1lIiwiam91cm5hbE5hbWUiLCJzaGlmdE9yZGVyIiwib3JkZXIiLCJjZWxsVmFsdWUiLCJ0YWJsZU5hbWUiLCJmaWVsZE5hbWUiLCJyb3dJbmRleCIsImZpZWxkcyIsImNvbnNvbGUiLCJsb2ciLCJjZWxscyIsImxlbmd0aCIsInZhbHVlIiwibWF4Um93SW5kZXgiLCJtYXgiLCJmaWVsZCIsImluZGV4IiwicGFyc2VJbnQiLCJ0YWJsZVRpdGxlIiwiZmllbGREZXNjcmlwdGlvbiIsImZpZWxkX2Rlc2NyaXB0aW9uIiwibXV0YXRpb25zIiwiVVBEQVRFX0pPVVJOQUxfSU5GTyIsIlVQREFURV9QTEFOVFNfSU5GTyIsIlNFVF9MT0FERUQiLCJTQVZFX0NFTExfVkFMVUUiLCJwYXlsb2FkIiwiYWN0aW9ucyIsImxvYWRKb3VybmFsIiwiY29tbWl0IiwiYXhpb3MiLCJnZXQiLCJBIiwidGhlbiIsInJlc3BvbnNlIiwiZGF0YSIsImxvYWRQbGFudHMiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUVBLElBQU1BLGVBQWU7QUFDakJDLGNBQVksSUFESztBQUVqQkMsU0FBTztBQUNIQyxnQkFBWSxFQURUO0FBRUhDLGlCQUFhLEVBRlY7QUFHSEMsWUFBUTtBQUhMLEdBRlU7QUFPakJDLFdBQVM7QUFDTEQsWUFBUTtBQUFBLGFBQVNILE1BQU1HLE1BQWY7QUFBQSxLQURIO0FBRUxFLFlBQVEsdUJBQVM7QUFDYixVQUFJTCxNQUFNRyxNQUFWLEVBQWtCO0FBQ2QsZUFB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QWYsRSIsImZpbGUiOiJtYWluLmExYzI2MTk2MmQ5Y2Y5YTk0N2EzLmhvdC11cGRhdGUuanMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgYXhpb3MgZnJvbSAnYXhpb3MnO1xuXG5jb25zdCBqb3VybmFsU3RhdGUgPSB7XG4gICAgbmFtZXNwYWNlZDogdHJ1ZSxcbiAgICBzdGF0ZToge1xuICAgICAgICBwbGFudHNJbmZvOiBbXSxcbiAgICAgICAgam91cm5hbEluZm86IHt9LFxuICAgICAgICBsb2FkZWQ6IGZhbHNlLFxuICAgIH0sXG4gICAgZ2V0dGVyczoge1xuICAgICAgICBsb2FkZWQ6IHN0YXRlID0+IHN0YXRlLmxvYWRlZCxcbiAgICAgICAgdGFibGVzOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIE9iamVjdC5rZXlzKHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIFtdO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBwbGFudHM6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIHJldHVybiBzdGF0ZS5wbGFudHNJbmZvXG4gICAgICAgIH0sXG4gICAgICAgIHBsYW50TmFtZTogc3RhdGUgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBzdGF0ZS5qb3VybmFsSW5mby5wbGFudC5uYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGpvdXJuYWxOYW1lOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwubmFtZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBzaGlmdE9yZGVyOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLm9yZGVyXG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAtMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgY2VsbFZhbHVlOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUsIGZpZWxkTmFtZSwgcm93SW5kZXgpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgaWYgKCEoZmllbGROYW1lIGluIGZpZWxkcykpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ1dBUk5JTkchIFRyeWluZyB0byBnZXQgY2VsbCB2YWx1ZSBvZiB1bmV4aXN0ZW50IGZpZWxkOiAnICsgZmllbGROYW1lKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBsZXQgY2VsbHMgPSBmaWVsZHNbZmllbGROYW1lXS5jZWxscztcbiAgICAgICAgICAgICAgICBpZiAoT2JqZWN0LmtleXMoY2VsbHMpLmxlbmd0aCAhPT0gMCkge1xuICAgICAgICAgICAgICAgICAgICBpZiAocm93SW5kZXggaW4gY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBjZWxsc1tyb3dJbmRleF0udmFsdWU7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIG1heFJvd0luZGV4OiAoc3RhdGUpID0+ICh0YWJsZU5hbWUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgbWF4ID0gLTE7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3RhYmxlTmFtZV0uZmllbGRzO1xuICAgICAgICAgICAgICAgIGZvcihsZXQgZmllbGQgaW4gZmllbGRzKSB7XG4gICAgICAgICAgICAgICAgICAgIGZvciAobGV0IGluZGV4IGluIGZpZWxkc1tmaWVsZF0uY2VsbHMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGluZGV4ID0gcGFyc2VJbnQoaW5kZXgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgbWF4ID0gbWF4IDwgaW5kZXggPyBpbmRleCA6IG1heDtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gbWF4KzE7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAtMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgdGFibGVUaXRsZTogKHN0YXRlKSA9PiAodGFibGVOYW1lKSA9PiB7XG4gICAgICAgICAgICByZXR1cm4gJ9CX0LDQs9C+0LvQvtCy0L7QuiDRgtCw0LHQu9C40YbRiydcbiAgICAgICAgfSxcbiAgICAgICAgZmllbGREZXNjcmlwdGlvbjogKHN0YXRlKSA9PiAodGFibGVOYW1lLCBmaWVsZE5hbWUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgaWYgKCEoZmllbGROYW1lIGluIGZpZWxkcykpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coXCJXQVJOSU5HISBUcnlpbmcgdG8gZ2V0IGZpZWxkIGRlc2N0aXB0aW9uIG9mIHVuZXhpc3RlbnQgZmllbGQ6IFwiICsgZmllbGROYW1lKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHt9O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gZmllbGRzW2ZpZWxkTmFtZV0uZmllbGRfZGVzY3JpcHRpb24gfHwgJydcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJ1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfSxcbiAgICBtdXRhdGlvbnM6IHtcbiAgICAgICAgVVBEQVRFX0pPVVJOQUxfSU5GTyAoc3RhdGUsIGpvdXJuYWxJbmZvKSB7XG4gICAgICAgICAgICBzdGF0ZS5qb3VybmFsSW5mbyA9IGpvdXJuYWxJbmZvO1xuICAgICAgICB9LFxuICAgICAgICBVUERBVEVfUExBTlRTX0lORk8gKHN0YXRlLCBwbGFudHNJbmZvKSB7XG4gICAgICAgICAgICBzdGF0ZS5wbGFudHNJbmZvID0gcGxhbnRzSW5mbztcbiAgICAgICAgfSxcbiAgICAgICAgU0VUX0xPQURFRCAoc3RhdGUsIGxvYWRlZCkge1xuICAgICAgICAgICAgc3RhdGUubG9hZGVkID0gbG9hZGVkO1xuICAgICAgICB9LFxuICAgICAgICBTQVZFX0NFTExfVkFMVUUgKHN0YXRlLCBwYXlsb2FkKSB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgbGV0IGZpZWxkcyA9IHN0YXRlLmpvdXJuYWxJbmZvLmpvdXJuYWwudGFibGVzW3BheWxvYWQudGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgaWYgKCEocGF5bG9hZC5maWVsZE5hbWUgaW4gZmllbGRzKSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZygnV0FSTklORyEgVHJ5aW5nIHRvIHNhdmUgdmFsdWUgb2YgdW5leGlzdGVudCBmaWVsZDogJyArIHBheWxvYWQuZmllbGROYW1lKTtcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coJyAgQ3JlYXRpbmcgZmllbGQgJyArIHBheWxvYWQuZmllbGROYW1lICsgJy4uLicpO1xuICAgICAgICAgICAgICAgICAgICBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdID0ge307XG4gICAgICAgICAgICAgICAgICAgIGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV1bJ2NlbGxzJ10gPSB7fTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgbGV0IGNlbGxzID0gZmllbGRzW3BheWxvYWQuZmllbGROYW1lXS5jZWxscztcbiAgICAgICAgICAgICAgICBpZiAocGF5bG9hZC5pbmRleCBpbiBjZWxscykge1xuICAgICAgICAgICAgICAgICAgICAvLyB1cGRhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICBjZWxsc1twYXlsb2FkLmluZGV4XVsndmFsdWUnXSA9IHBheWxvYWQudmFsdWU7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAvLyBjcmVhdGUgY2VsbFxuICAgICAgICAgICAgICAgICAgICBjZWxsc1twYXlsb2FkLmluZGV4XSA9IHt9O1xuICAgICAgICAgICAgICAgICAgICBjZWxsc1twYXlsb2FkLmluZGV4XVsndmFsdWUnXSA9IHBheWxvYWQudmFsdWU7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfSxcbiAgICBhY3Rpb25zOiB7XG4gICAgICAgIGxvYWRKb3VybmFsOiBmdW5jdGlvbiAoeyBjb21taXQsIHN0YXRlLCBnZXR0ZXJzIH0sIHBheWxvYWQpIHtcbiAgICAgICAgICAgIGF4aW9zXG4gICAgICAgICAgICAgICAgLmdldCgnaHR0cDovL2xvY2FsaG9zdDo4MDAwL2FwaS9zaGlmdHMvJyArIHBheWxvYWQsIHtBOiAnZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SjFjMlZ5WDJsa0lqb3hOVGtzSW5WelpYSnVZVzFsSWpvaWFXNW1jbUZ0YVc1bElpd2laWGh3SWpveE5UTTNPREE1T1RRekxDSmxiV0ZwYkNJNkltRmtiV2x1UUdGa2JXbHVMbU52YlNKOS5CT3RtR1JnZjZHcXlLOTJDVDRWUi11dmRYXzRJR2xXMFVBVG1IdFZZMk1BJ30pXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9KT1VSTkFMX0lORk8nLCByZXNwb25zZS5kYXRhKTtcbiAgICAgICAgICAgICAgICAgICAgY29tbWl0KCdTRVRfTE9BREVEJywgdHJ1ZSk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgfSxcbiAgICAgICAgbG9hZFBsYW50czogZnVuY3Rpb24gKHsgY29tbWl0LCBzdGF0ZSwgZ2V0dGVycyB9KSB7XG4gICAgICAgICAgICBheGlvc1xuICAgICAgICAgICAgICAgIC5nZXQoJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hcGkvbWVudV9pbmZvLycpXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1VQREFURV9QTEFOVFNfSU5GTycsIHJlc3BvbnNlLmRhdGEucGxhbnRzKTtcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICB9LFxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgam91cm5hbFN0YXRlIl0sInNvdXJjZVJvb3QiOiIifQ==