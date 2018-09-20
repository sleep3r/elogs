import Parser from 'hot-formula-parser'

class Formula {
    // should be changed, when this cell used in another cell
    dependent_formulas = [];  // only neighbours: will be updated recursively
    // shouldbe set

    // on_formula_change find herself in dependensies

    static set_vars() {
        Parser.setFunction('$', function (params) {
            const journal = params[0];
            const table = params[1];
            const field = params[2];
            const index = params[3];
            const shift = params[4];

            return string.charAt(index);
        })
    }
}
