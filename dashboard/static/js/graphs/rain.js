$(document).ready(function () {
    graphRains();
});

// Start all rain graphs
function graphRains() {
    for (let zoneNumber = 1; zoneNumber <= getNumberOfZones(); zoneNumber++) {
        graphRain(zoneNumber);
    }
}

// Start rain graph
function graphRain(zoneNumber) {
    console.log("Graphing rain for zone", zoneNumber);

    var rainData = [[],[],[],[],[]];
    var rainChart;
    var updateInterval = 2300; // Update every 2 seconds
    // Get the canvas element for the chart
    var ctx = document.getElementById(`rainChart${zoneNumber}`).getContext('2d');

    // Function to clear the canvas
    function clearCanvas() {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }

    // Function to initialize or update the chart
    function initOrUpdateChart() {
        if (rainChart) {
            clearCanvas();
            rainChart.destroy();
        }

        let datasets = [];
        for (let unitNumber = 0; unitNumber < getNumberOfUnits(zoneNumber); unitNumber++) {
            datasets.push({
                label: `Unit ${unitNumber + 1}`,
                data: rainData[unitNumber],
                fill: false,
                borderColor: getUnitColor(zoneNumber, unitNumber),
                tension: 0.1
            })
        }

        rainChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: datasets
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: `Rain Data for zone${zoneNumber}`
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Rain Percentage (%)'
                        }
                    }
                }
            }
        });
    }

    // Function to update the chart with new data
    function updateChart() {
        rainChart.data.labels = Array.from(Array(rainData[0].length).keys());
        rainChart.data.datasets[0].data = rainData[0];
        rainChart.update();
    }

    // Initialize the chart
    initOrUpdateChart();

    // update the rain data and display 
    function fetchData() {
        console.log("Fetching rain data for zone", zoneNumber);
        if (rainData[0].length === 0) {
            // gets 10 readings from the unit
            console.log("Fetching rain data for zone", zoneNumber);
            const url = window.location.origin + `/zone1rain10data`;
            $.get(url, function (data) {
                console.log("data=", data);
                for (let i = 0; i < data.length; i++) {
                    let unitdata = data[i];
                    console.log("unitdata=", unitdata);

                    for (let j = 0; j < unitdata.rain.length; j++) {
                        let r = unitdata.rain[j][1];
                        console.log("j=", i, j, r);
                        rainData[i].push(r);
                    }
                }
                console.log("updatechart rainData=", rainData);
                updateChart();
            });
        }
        else {
            // get 1 reading from the unit
            console.log("gets one reading from the pi single reading")
            console.log("Fetching 1 reading for zone", zoneNumber);
            const url = window.location.origin + `/zone1raindata`;
            $.get(url, function (data) {
                console.log("data=", data);
                for (let i = 0; i < data.length; i++){
                    let unitdata = data[i];
                    console.log("single unitdata=", unitdata);

                    $('#rain').text('Rain: ' + unitdata.rain);
                    rainData[i].push(unitdata.rain);
                    if (rainData[i].length > 10){
                        rainData[i].shift();
                    }
                }
                updateChart();
            });
        }
    }

    // Fetch data initially and then regular intervals
    fetchData();
    setInterval(fetchData, updateInterval);
}
