$(document).ready(function(){
    graphTemps();
});

// Start all temperature graphs
function graphTemps() {
    for (let zoneNumber = 1; zoneNumber <= getNumberOfZones(); zoneNumber++){
        graphTemp(zoneNumber);
    }
}

// Start temperature graph
function graphTemp(zoneNumber) {
    console.log("Graphing temp for zone", zoneNumber);

    var temperatureData = [[],[],[],[],[]];
    var temperatureChart;
    var updateInterval = 2000; // Update every 2 seconds
    // Get the canvas element for the chart
    var ctx = document.getElementById(`temperatureChart${zoneNumber}`).getContext('2d');

    // Function to clear the canvas
    function clearCanvas() {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }

    // Function to initialize or update the chart
    function initOrUpdateChart() {
        if (temperatureChart) {
            clearCanvas();
            temperatureChart.destroy();
        }

        let datasets = [];
        for (let unitNumber =0; unitNumber < getNumberOfUnits(zoneNumber); unitNumber++){
            datasets.push({
                label: `Unit ${unitNumber + 1}`,
                data: temperatureData[unitNumber],
                fill: false,
                borderColor: getUnitColor(zoneNumber, unitNumber),
                tension: 0.1
            })
        }

        temperatureChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: datasets
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: `Temperature Data for zone${zoneNumber}`
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    }
                }
            }
        });
    }

    // Function to update the chart with new data
    function updateChart() {
        temperatureChart.data.labels = Array.from(Array(temperatureData[0].length).keys());
        temperatureChart.data.datasets[0].data = temperatureData[0];
        temperatureChart.update();
    }

    // Initialize the chart
    initOrUpdateChart();

    // Update the temperature data and display
    function fetchData() {
        console.log("Fetching temp data for zone", zoneNumber);
        if (temperatureData[0].length === 0) {
            // gets 10 readings from the unit
            console.log("Fetching 10 readings for zone", zoneNumber);
            const url = window.location.origin + '/zone1temp10data';
            $.getJSON(url, function(data) {
                console.log("data=", data);
                for (let i = 0; i < data.length; i++) {
                    let unitdata = data[i];
                    console.log("unitdata=",unitdata);

                    for (let j = 0; j < unitdata.temp.length; j++) {
                        let t = unitdata.temp[j][1];
                        console.log("j=",i,j,t);                        
                        temperatureData[i].push(t);                        
                    }
                }
                console.log("updatechart temperatureData=",temperatureData);
                updateChart();
            });
        }
        else{
            // gets 1 reading from the unit
            console.log("gets on reading from the pi single reading")
            console.log("Fetching 1 reading for zone", zoneNumber);
            const url = window.location.origin + '/zone1tempdata';
            $.getJSON(url, function(data) {
                console.log("single data=", data);
                for (let i = 0; i < data.length; i++) {
                    let unitdata = data[i];
                    console.log("single unitdata=",unitdata);
                    
                    $('#temp').text('Temperature: ' +unitdata.temp);
                    temperatureData[i].push(unitdata.temp);
                    if (temperatureData[i].length > 10) {
                        temperatureData[i].shift();
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
