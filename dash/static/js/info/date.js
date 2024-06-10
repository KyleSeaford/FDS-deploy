// Initialize the current date to the current date on the server
$(document).ready(function(){
    setInterval(function(){        
        const a =  window.location.origin + '/current_date';
        $.getJSON(a, function(data) {
            $('#current_date').text('Current Date: ' + data.current_date);
        });
    }, 1000); // Update every second
});
