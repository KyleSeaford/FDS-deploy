// Initialize the current time to the current time on the server
$(document).ready(function(){
    setInterval(function(){
        const a =  window.location.origin + '/current_time';
        $.getJSON(a, function(data) {
            $('#current_time').text('Current Time: ' + data.current_time);
        })
    }, 1000); // update every second 

})
