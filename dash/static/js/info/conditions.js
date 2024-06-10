$(document).ready(function () {
    const a =  window.location.origin + '/conditions';
    $.getJSON(a, function (data) {
        $('#conditions').text('Current Conditions: ' + data.conditions);
    });
    setInterval(function () {
        $.getJSON(a, function (data) {
            $('#conditions').text('Current Conditions: ' + data.conditions);
        });
    }, 172800); // Update every 2.88 minutes, optimal amount of time to update due to api limit
});
