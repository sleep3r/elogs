
leaching = {
    'shiftSelect': function() {
        shiftId = shift_select.options[shift_select.selectedIndex].value
        window.location.replace("/leaching/all/edit?shift=" + shiftId);
    }
};