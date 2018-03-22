
leaching = {
    'shiftSelect': function(link) {
        shiftId = shift_select.options[shift_select.selectedIndex].value
        window.location.replace(link + "?shift=" + shiftId);
    }
};