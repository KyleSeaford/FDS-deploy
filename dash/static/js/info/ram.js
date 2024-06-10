// ram usage not used any more

$(document).ready(function () {
    $.getJSON('http://127.0.0.1:5000/ram_usage', function (data) {
        $('#ram-usage').text('RAM Usage: ' + data.ram_usage + '%');
    });
    setInterval(function () {
        $.getJSON('http://127.0.0.1:5000/ram_usage', function (data) {
            $('#ram-usage').text('RAM Usage: ' + data.ram_usage + '%');
        });
    }, 20000); // Update every 20 second
});
