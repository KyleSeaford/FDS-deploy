$(document).ready(function(){
    const a =  window.location.origin + '/location';
    $.getJSON(a, function(data) {
        $('#current_location').text('Current Location: ' + data.location);
    });
});
