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
        Authorization: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNTksInVzZXJuYW1lIjoiaW5mcmFtaW5lIiwiZXhwIjoxNTM3ODA5OTQzLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.BOtmGRgf6GqyK92CT4VR-uvdX_4IGlW0UATmHtVY2MA'
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9zcmMvc3RvcmUvbW9kdWxlcy9qb3VybmFsU3RhdGUuanMiXSwibmFtZXMiOlsiam91cm5hbFN0YXRlIiwibmFtZXNwYWNlZCIsInN0YXRlIiwicGxhbnRzSW5mbyIsImpvdXJuYWxJbmZvIiwibG9hZGVkIiwiZ2V0dGVycyIsInRhYmxlcyIsIk9iamVjdCIsImtleXMiLCJqb3VybmFsIiwicGxhbnRzIiwicGxhbnROYW1lIiwicGxhbnQiLCJuYW1lIiwiam91cm5hbE5hbWUiLCJzaGlmdE9yZGVyIiwib3JkZXIiLCJjZWxsVmFsdWUiLCJ0YWJsZU5hbWUiLCJmaWVsZE5hbWUiLCJyb3dJbmRleCIsImZpZWxkcyIsImNvbnNvbGUiLCJsb2ciLCJjZWxscyIsImxlbmd0aCIsInZhbHVlIiwibWF4Um93SW5kZXgiLCJtYXgiLCJmaWVsZCIsImluZGV4IiwicGFyc2VJbnQiLCJ0YWJsZVRpdGxlIiwiZmllbGREZXNjcmlwdGlvbiIsImZpZWxkX2Rlc2NyaXB0aW9uIiwibXV0YXRpb25zIiwiVVBEQVRFX0pPVVJOQUxfSU5GTyIsIlVQREFURV9QTEFOVFNfSU5GTyIsIlNFVF9MT0FERUQiLCJTQVZFX0NFTExfVkFMVUUiLCJwYXlsb2FkIiwiYWN0aW9ucyIsImxvYWRKb3VybmFsIiwiY29tbWl0IiwiYXhpb3MiLCJnZXQiLCJBdXRob3JpemF0aW9uIiwidGhlbiIsInJlc3BvbnNlIiwiZGF0YSIsImxvYWRQbGFudHMiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUVBLElBQU1BLGVBQWU7QUFDakJDLGNBQVksSUFESztBQUVqQkMsU0FBTztBQUNIQyxnQkFBWSxFQURUO0FBRUhDLGlCQUFhLEVBRlY7QUFHSEMsWUFBUTtBQUhMLEdBRlU7QUFPakJDLFdBQVM7QUFDTEQsWUFBUTtBQUFBLGFBQVNILE1BQU1HLE1BQWY7QUFBQSxLQURIO0FBRUxFLFlBQVEsdUJBQVM7QUFDYixVQUFJTCxNQUFNRyxNQUFWLEVB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QXJCO0FBNkllWCwyRUFBZixFIiwiZmlsZSI6Im1haW4uNjA5ZjUwMGQ4OGYyMTJlODQ2ZTguaG90LXVwZGF0ZS5qcyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBheGlvcyBmcm9tICdheGlvcyc7XG5cbmNvbnN0IGpvdXJuYWxTdGF0ZSA9IHtcbiAgICBuYW1lc3BhY2VkOiB0cnVlLFxuICAgIHN0YXRlOiB7XG4gICAgICAgIHBsYW50c0luZm86IFtdLFxuICAgICAgICBqb3VybmFsSW5mbzoge30sXG4gICAgICAgIGxvYWRlZDogZmFsc2UsXG4gICAgfSxcbiAgICBnZXR0ZXJzOiB7XG4gICAgICAgIGxvYWRlZDogc3RhdGUgPT4gc3RhdGUubG9hZGVkLFxuICAgICAgICB0YWJsZXM6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gT2JqZWN0LmtleXMoc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXMpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gW107XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHBsYW50czogc3RhdGUgPT4ge1xuICAgICAgICAgICAgcmV0dXJuIHN0YXRlLnBsYW50c0luZm9cbiAgICAgICAgfSxcbiAgICAgICAgcGxhbnROYW1lOiBzdGF0ZSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUubG9hZGVkKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHN0YXRlLmpvdXJuYWxJbmZvLnBsYW50Lm5hbWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgam91cm5hbE5hbWU6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC5uYW1lO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHNoaWZ0T3JkZXI6IHN0YXRlID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gc3RhdGUuam91cm5hbEluZm8ub3JkZXJcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIC0xO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBjZWxsVmFsdWU6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSwgZmllbGROYW1lLCByb3dJbmRleCkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShmaWVsZE5hbWUgaW4gZmllbGRzKSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZygnV0FSTklORyEgVHJ5aW5nIHRvIGdldCBjZWxsIHZhbHVlIG9mIHVuZXhpc3RlbnQgZmllbGQ6ICcgKyBmaWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGxldCBjZWxscyA9IGZpZWxkc1tmaWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChPYmplY3Qua2V5cyhjZWxscykubGVuZ3RoICE9PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChyb3dJbmRleCBpbiBjZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGNlbGxzW3Jvd0luZGV4XS52YWx1ZTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuICcnO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgbWF4Um93SW5kZXg6IChzdGF0ZSkgPT4gKHRhYmxlTmFtZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBtYXggPSAtMTtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbdGFibGVOYW1lXS5maWVsZHM7XG4gICAgICAgICAgICAgICAgZm9yKGxldCBmaWVsZCBpbiBmaWVsZHMpIHtcbiAgICAgICAgICAgICAgICAgICAgZm9yIChsZXQgaW5kZXggaW4gZmllbGRzW2ZpZWxkXS5jZWxscykge1xuICAgICAgICAgICAgICAgICAgICAgICAgaW5kZXggPSBwYXJzZUludChpbmRleCk7XG4gICAgICAgICAgICAgICAgICAgICAgICBtYXggPSBtYXggPCBpbmRleCA/IGluZGV4IDogbWF4O1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBtYXgrMTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIC0xO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICB0YWJsZVRpdGxlOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUpID0+IHtcbiAgICAgICAgICAgIHJldHVybiAn0JfQsNCz0L7Qu9C+0LLQvtC6INGC0LDQsdC70LjRhtGLJ1xuICAgICAgICB9LFxuICAgICAgICBmaWVsZERlc2NyaXB0aW9uOiAoc3RhdGUpID0+ICh0YWJsZU5hbWUsIGZpZWxkTmFtZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLmxvYWRlZCkge1xuICAgICAgICAgICAgICAgIGxldCBmaWVsZHMgPSBzdGF0ZS5qb3VybmFsSW5mby5qb3VybmFsLnRhYmxlc1t0YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShmaWVsZE5hbWUgaW4gZmllbGRzKSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhcIldBUk5JTkchIFRyeWluZyB0byBnZXQgZmllbGQgZGVzY3RpcHRpb24gb2YgdW5leGlzdGVudCBmaWVsZDogXCIgKyBmaWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4ge307XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBmaWVsZHNbZmllbGROYW1lXS5maWVsZF9kZXNjcmlwdGlvbiB8fCAnJ1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICcnXG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9LFxuICAgIG11dGF0aW9uczoge1xuICAgICAgICBVUERBVEVfSk9VUk5BTF9JTkZPIChzdGF0ZSwgam91cm5hbEluZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLmpvdXJuYWxJbmZvID0gam91cm5hbEluZm87XG4gICAgICAgIH0sXG4gICAgICAgIFVQREFURV9QTEFOVFNfSU5GTyAoc3RhdGUsIHBsYW50c0luZm8pIHtcbiAgICAgICAgICAgIHN0YXRlLnBsYW50c0luZm8gPSBwbGFudHNJbmZvO1xuICAgICAgICB9LFxuICAgICAgICBTRVRfTE9BREVEIChzdGF0ZSwgbG9hZGVkKSB7XG4gICAgICAgICAgICBzdGF0ZS5sb2FkZWQgPSBsb2FkZWQ7XG4gICAgICAgIH0sXG4gICAgICAgIFNBVkVfQ0VMTF9WQUxVRSAoc3RhdGUsIHBheWxvYWQpIHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5sb2FkZWQpIHtcbiAgICAgICAgICAgICAgICBsZXQgZmllbGRzID0gc3RhdGUuam91cm5hbEluZm8uam91cm5hbC50YWJsZXNbcGF5bG9hZC50YWJsZU5hbWVdLmZpZWxkcztcbiAgICAgICAgICAgICAgICBpZiAoIShwYXlsb2FkLmZpZWxkTmFtZSBpbiBmaWVsZHMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdXQVJOSU5HISBUcnlpbmcgdG8gc2F2ZSB2YWx1ZSBvZiB1bmV4aXN0ZW50IGZpZWxkOiAnICsgcGF5bG9hZC5maWVsZE5hbWUpO1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZygnICBDcmVhdGluZyBmaWVsZCAnICsgcGF5bG9hZC5maWVsZE5hbWUgKyAnLi4uJyk7XG4gICAgICAgICAgICAgICAgICAgIGZpZWxkc1twYXlsb2FkLmZpZWxkTmFtZV0gPSB7fTtcbiAgICAgICAgICAgICAgICAgICAgZmllbGRzW3BheWxvYWQuZmllbGROYW1lXVsnY2VsbHMnXSA9IHt9O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBsZXQgY2VsbHMgPSBmaWVsZHNbcGF5bG9hZC5maWVsZE5hbWVdLmNlbGxzO1xuICAgICAgICAgICAgICAgIGlmIChwYXlsb2FkLmluZGV4IGluIGNlbGxzKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIHVwZGF0ZSBjZWxsXG4gICAgICAgICAgICAgICAgICAgIGNlbGxzW3BheWxvYWQuaW5kZXhdWyd2YWx1ZSddID0gcGF5bG9hZC52YWx1ZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGNyZWF0ZSBjZWxsXG4gICAgICAgICAgICAgICAgICAgIGNlbGxzW3BheWxvYWQuaW5kZXhdID0ge307XG4gICAgICAgICAgICAgICAgICAgIGNlbGxzW3BheWxvYWQuaW5kZXhdWyd2YWx1ZSddID0gcGF5bG9hZC52YWx1ZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9LFxuICAgIGFjdGlvbnM6IHtcbiAgICAgICAgbG9hZEpvdXJuYWw6IGZ1bmN0aW9uICh7IGNvbW1pdCwgc3RhdGUsIGdldHRlcnMgfSwgcGF5bG9hZCkge1xuICAgICAgICAgICAgYXhpb3NcbiAgICAgICAgICAgICAgICAuZ2V0KCdodHRwOi8vbG9jYWxob3N0OjgwMDAvYXBpL3NoaWZ0cy8nICsgcGF5bG9hZCwge0F1dGhvcml6YXRpb246ICdleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpJVXpJMU5pSjkuZXlKMWMyVnlYMmxrSWpveE5Ua3NJblZ6WlhKdVlXMWxJam9pYVc1bWNtRnRhVzVsSWl3aVpYaHdJam94TlRNM09EQTVPVFF6TENKbGJXRnBiQ0k2SW1Ga2JXbHVRR0ZrYldsdUxtTnZiU0o5LkJPdG1HUmdmNkdxeUs5MkNUNFZSLXV2ZFhfNElHbFcwVUFUbUh0VlkyTUEnfSlcbiAgICAgICAgICAgICAgICAudGhlbihyZXNwb25zZSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGNvbW1pdCgnVVBEQVRFX0pPVVJOQUxfSU5GTycsIHJlc3BvbnNlLmRhdGEpO1xuICAgICAgICAgICAgICAgICAgICBjb21taXQoJ1NFVF9MT0FERUQnLCB0cnVlKTtcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICB9LFxuICAgICAgICBsb2FkUGxhbnRzOiBmdW5jdGlvbiAoeyBjb21taXQsIHN0YXRlLCBnZXR0ZXJzIH0pIHtcbiAgICAgICAgICAgIGF4aW9zXG4gICAgICAgICAgICAgICAgLmdldCgnaHR0cDovL2xvY2FsaG9zdDo4MDAwL2FwaS9tZW51X2luZm8vJylcbiAgICAgICAgICAgICAgICAudGhlbihyZXNwb25zZSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGNvbW1pdCgnVVBEQVRFX1BMQU5UU19JTkZPJywgcmVzcG9uc2UuZGF0YS5wbGFudHMpO1xuICAgICAgICAgICAgICAgIH0pXG4gICAgICAgIH0sXG4gICAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBqb3VybmFsU3RhdGUiXSwic291cmNlUm9vdCI6IiJ9