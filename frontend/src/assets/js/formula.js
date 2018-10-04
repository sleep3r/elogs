import formulaParser from 'hot-formula-parser'
import axios from 'axios'
var FormulaParser = require('hot-formula-parser').Parser;
var request = require('sync-request');

function isNumeric(num){
  return !isNaN(num)
}

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

console.log("Loading formula...")
var parser = new FormulaParser();
window.parser = parser
window.parser.setFunction('FUNC', function (params) {
    const journal = params[0];
    const table = params[1];
    const field = params[2];
    const index = params[3];
    const shift = params[4];

    var res = request("GET",
        "http://localhost:8000/api/cell/?journal={0}&table={1}&field={2}&shift={3}".format(
            journal, table, field, shift
        ))
    let json = JSON.parse(res.getBody())
    let result = null
    if (isNumeric(json.value)){
        result = Number(json.value)
    }
    else {
        result = window.parser.parse(json.value)
    }
    return result
})
