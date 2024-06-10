$(document).ready(function(){
    graphSmokes();
});

// Start all smoke graphs
function graphSmokes() {
    for (let zoneNumber = 1; zoneNumber <= getNumberOfZones(); zoneNumber++){
        graphSmoke(zoneNumber);
    }
}

// Start smoke graph
function graphSmoke(zoneNumber) {
    console.log("Graphing smoke for zone", zoneNumber);

    var smokeData = [[],[],[],[],[]];
    var smokeChart;
    var updateInterval = 2100; // Update every 2 seconds
    // Get the canvas element for the chart
    var ctx = document.getElementById(`smokeChart${zoneNumber}`).getContext('2d');

    // Function to clear the canvas
    function clearCanvas() {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }

    // Function to initialize or update the chart
    function initOrUpdateChart() {
        if (smokeChart) {
            clearCanvas();
            smokeChart.destroy();
        }

        let datasets = [];
        for (let unitNumber =0; unitNumber < getNumberOfUnits(zoneNumber); unitNumber++){
            datasets.push({
                label: `Unit ${unitNumber + 1}`,
                data: smokeData[unitNumber],
                fill: false,
                borderColor: getUnitColor(zoneNumber, unitNumber),
                tension: 0.1
            })
        }

        smokeChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: datasets
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: `Smoke Data for zone${zoneNumber}`
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Smoke Percentage (%)'
                        }
                    }
                }
            }
        });
    }

    // Function to update the chart with new data
    function updateChart() {
        smokeChart.data.labels = Array.from(Array(smokeData[0].length).keys());
        smokeChart.data.datasets[0].data = smokeData[0];
        smokeChart.update();
    }

    // Initialize the chart
    initOrUpdateChart();

    // Update the temperature data and display
    function fetchData(){
        console.log("Fetching smoke data for zone", zoneNumber);
        if (smokeData[0].length === 0) {
            // gets 10 readings from the unit
            console.log("Fetching 10 readings for zone", zoneNumber);
            const url = window.location.origin + '/zone1smoke10data';
            $.get(url, function(data){
                console.log("data=", data);
                for (let i = 0; i < data.length; i++){
                    let unitdata = data[i];
                    console.log("unitdata=", unitdata);

                    for (let j = 0; j < unitdata.smoke.length; j++){
                        let s = unitdata.smoke[j][1];
                        console.log("j=", i, j, s);
                        smokeData[i].push(s);
                    }
                }
                console.log("updatechart smokeData=", smokeData);
                updateChart();
            });
        }
        else {
            // gets 1 reading from the unit
            console.log("gets one reading from the pi single reading")
            console.log("Fetching 1 reading for zone", zoneNumber);
            const url = window.location.origin + '/zone1smokedata';
            $.get(url, function(data){
                console.log("data=", data);
                for (let i = 0; i < data.length; i++){
                    let unitdata = data[i];
                    console.log("single unitdata=", unitdata);

                    $('#smoke').text('Smoke: ' + unitdata.smoke);
                    smokeData[i].push(unitdata.smoke);
                    if (smokeData[i].length > 10){
                        smokeData[i].shift();
                    }
                }
                updateChart();
            });
        }
    }

    // Fetch data initially and then at regular intervals
    fetchData();
    setInterval(fetchData, updateInterval);
}
