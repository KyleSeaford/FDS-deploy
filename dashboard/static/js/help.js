document.getElementById('helpButton').addEventListener('click', function() {
    var userResponse = confirm('To SetUP FireGuard Pro, click on the "Configure Zones" button and enter the number of zones, Once Completed Then, click on the "Configure Units" button to configure the amount of units. \n\nIf you are experiencing issues or have any questions, Please visit our GitHub page. \n\nWould you like to visit our GitHub page?');
    if (userResponse) {
        window.open('https://github.com/KyleSeaford/FDS', '_blank');
    }
});