$(document).ready(function () {
    const a =  window.location.origin + '/windspeed';
    $.getJSON(a, function (data) {
        $('#windspeed').text('Windspeed: ' + data.windspeed);
    });
    setInterval(function () {
        $.getJSON(a, function (data) {
            $('#windspeed').text('Windspeed: ' + data.windspeed);
        });
    }, 172800); // Update every 2.88 minutes, optimal amount of time to update due to api limit
});
