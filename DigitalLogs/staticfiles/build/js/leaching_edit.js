
leaching = {
    'shiftSelect': function(link) {
         shiftId = shift_select.options[shift_select.selectedIndex].value
         let newLink = link + "?shift=" + shiftId
         console.log(newLink)
         window.location.replace(newLink);
    },
};

