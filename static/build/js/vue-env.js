
Vue.filter("formatNumber", function (value) {
    return numeral(value).format("00.00");
});

Vue.filter('formatDate', function(value) {
    if (value) {
        return moment(String(value)).format('DD.MM.YYYY hh:mm')
    }
})

Vue.filter('formatHour', function(value) {
    if (value) {
        return moment(String(value)).format('hh')
    }
})
