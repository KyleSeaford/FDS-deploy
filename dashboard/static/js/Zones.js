function CreateZoneContentDiv(i) {
    var zoneContentDiv = document.createElement("div");
    zoneContentDiv.id = "Zone_" + i;
    zoneContentDiv.className = "tabcontent";
    zoneContentDiv.innerHTML = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div id="unitInfo_${i}" class="unitInfo">
            
        </div>

        <div class="unit-container">
            <div class="unit-content">
                <button class="unitButton" onclick="configureUnits(${i})">Configure Units <i class="fa fa-gear" aria-hidden="true"></i></button>
                <table class="unit-table" id="unitTable_${i}">
                    <thead>
                        <tr>
                            <th>Unit <i class="fa fa-hashtag" aria-hidden="true"></i></th>
                            <th>Colour <i class="fa fa-paint-brush" aria-hidden="true"></i></th>
                        </tr>
                    </thead>
                    <tbody id="unitTableBody_${i}">
                        <!-- Unit rows will be added dynamically -->
                    </tbody>
                </table>
            </div>
        </div> 

        <div class="container">
            <div class="box">
                <canvas id="temperatureChart${i}"></canvas>
            </div>

            <div class="box">
                <canvas id="smokeChart${i}"></canvas>
            </div>

            <div class="box">
                <canvas id="rainChart${i}"></canvas>
            </div>
            
            <div class="box" id="">
                <h3>Camera Feed for Zone1</h3>
                <div class="img-wrapper">
                    <img id="camimg" src="" class="camera-img">
                </div>
            </div>
        </div>
        <style>
            .img-wrapper {
                overflow: hidden;
                width: 95%;
                height: 85%;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            
            .camera-img {
                transition: transform 0.6s ease;
            }
            
            .camera-img.exit {
                transform: translateX(-100%);
            }
            
            .camera-img.enter {
                transform: translateX(100%);
            }
            
            .camera-img.active {
                transform: translateX(0);
            }
            
            h3 {
                text-align: center;
                margin-bottom: 20px;
                color: gray;
                font-size: 0.7rem;
            }
        </style>
    `;
    return zoneContentDiv;
}


// Function to handle the settings button click
document.getElementById("settingsButton").addEventListener("click", function () {
    // Prompt the user to enter the number of zones
    var numberOfZones = prompt("How many zones are there?", "1");

    // Parse the number of zones as an integer
    numberOfZones = parseInt(numberOfZones);

    // Validate if the input is a number and greater than 0
    if (!isNaN(numberOfZones) && numberOfZones > 0 && numberOfZones <= 13) {
        // Save the number of zones
        setNumberOfZones(numberOfZones);

        // Remove existing zone buttons and content
        var tablinkContainer = document.querySelector(".tablink-container");
        tablinkContainer.innerHTML = '';

        var tabContentContainer = document.querySelector(".tabcontent-container");
        tabContentContainer.innerHTML = '';

        // Add zone buttons and corresponding content based on the input
        console.log("Adding zone buttons and content based on saved number of zones (top)", numberOfZones);
        for (var i = 1; i <= numberOfZones; i++) {
            // Create zone button
            var zoneButton = document.createElement("button");
            zoneButton.textContent = "Zone " + i;
            zoneButton.className = "tablink";
            zoneButton.setAttribute("onclick", "openPage('Zone_" + i + "', this, '#0d95b4')");
            if (i == 1)
                zoneButton.id = "defaultOpen"; // Added to set the first zone as the default open tab
            tablinkContainer.appendChild(zoneButton);

            // Create zone content div
            tabContentContainer.appendChild(CreateZoneContentDiv(i));

            // Populate unit table with descriptions
            populateUnitTableWithColorBoxes(i, getUnitColours(i));
        }

        // Get the element with id="defaultOpen" and click on it
        console.log("Triggering default open tab (top)");
        document.getElementById("defaultOpen").click();
        graphTemps();
    } else {
        alert("Please enter a valid number of zones: 1 to 13.");
    }
});

// Function to populate unit table with color boxes
function populateUnitTableWithColorBoxes(zoneNumber, descriptions) {
    var unitTableBody = document.getElementById(`unitTableBody_${zoneNumber}`);
    unitTableBody.innerHTML = ''; // Clear existing rows

    if (descriptions) {
        for (var j = 0; j < descriptions.length; j++) {
            var newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>Unit ${j + 1}</td>
                <td><div class="color-box" style="background-color: ${descriptions[j]};"></div></td>
            `;
            unitTableBody.appendChild(newRow);
        }
    }
}

// Function to handle configuring units
function configureUnits(zoneNumber) {
    // Prompt the user to enter the number of units for the specific zone
    var numberOfUnits = prompt(`Please enter the number of units for Zone ${zoneNumber}:`, getNumberOfUnits(zoneNumber) || "1");

    // Parse the number of units as an integer
    numberOfUnits = parseInt(numberOfUnits);

    // Validate if the input is a number and greater than or equal to 0
    if (!isNaN(numberOfUnits) && numberOfUnits >= 0 && numberOfUnits <= 5) {
        // Display the number of units in the zone content
        var unitInfoDiv = document.getElementById(`unitInfo_${zoneNumber}`);
        // unitInfoDiv.innerHTML = `<h1>Zone ${zoneNumber} | Number of Units: ${numberOfUnits}</h1>`; // Changed 'i' to 'zoneNumber'

        // If the new number of units is less than the existing number, truncate the array accordingly
        removeUnits(zoneNumber, numberOfUnits);

        // Predefined list of colors for the units (up to 5 units)
        var colors = ['#4169E1', '#50C878', '#DC143C', '#FFEF00', '#E6E6FA'];

        // Update unit table with descriptions
        var unitColourList = getUnitColours(zoneNumber);
        for (var unitNumber = unitColourList.length; unitNumber < numberOfUnits; unitNumber++) {
            // Assign color from the predefined list
            var color = colors[unitNumber % colors.length];
            unitColourList.push(color); 

            setUnitColor(zoneNumber, unitNumber, color);
            setUnitAddress(zoneNumber, unitNumber, `192.167.${zoneNumber}.${unitNumber}`);
        }

        // Save updated zone data to Storage
        setNumberOfUnits(zoneNumber, numberOfUnits);

        // Populate unit table with color boxes
        populateUnitTableWithColorBoxes(zoneNumber, unitColourList);

    } else {
        alert("Please enter a valid number of units: 0 to 5.");
    }
}

// Function to create zone buttons and content on page load
document.addEventListener('DOMContentLoaded', function () {
    // Check if numberOfZones is saved in Storage
    var savedNumberOfZones = getNumberOfZones();

    if (savedNumberOfZones !== null) {
        // Retrieve the number of zones from Storage
        var numberOfZones = parseInt(savedNumberOfZones);

        // Add zone buttons and corresponding content based on the saved number of zones
        var tablinkContainer = document.querySelector(".tablink-container");
        var tabContentContainer = document.querySelector(".tabcontent-container");

        console.log("Adding zone buttons and content based on saved number of zones (bottom)", numberOfZones);
        for (var i = 1; i <= numberOfZones; i++) {
            // Create zone button
            var zoneButton = document.createElement("button");
            zoneButton.textContent = "Zone " + i;
            zoneButton.className = "tablink";
            zoneButton.setAttribute("onclick", "openPage('Zone_" + i + "', this, '#0d95b4')");
            if (i == 1)
                zoneButton.id = "defaultOpen"; // Added to set the first zone as the default open tab
            tablinkContainer.appendChild(zoneButton);

            // Retrieve the number of units for this zone from Storage
            var numberOfUnits = parseInt(getNumberOfUnits(i)) || 0;

            // Create zone content div
            tabContentContainer.appendChild(CreateZoneContentDiv(i));

            // Populate unit table with color boxes
            var descriptions = getUnitColours(i);
            populateUnitTableWithColorBoxes(i, descriptions);

            // Save the number of units with default as 0
            setNumberOfUnits(i, numberOfUnits)
        }

        // Get the element with id="defaultOpen" and click on it
        console.log("Triggering default open tab (bottom)");
        document.getElementById("defaultOpen").click();

        // Trigger click event for the first zone button (Zone 1)
        var firstZoneButton = document.querySelector(".tablink");
        if (firstZoneButton) {
            openPage('Zone_1', firstZoneButton, '#0d95b4', true); // Adjusted to trigger click event
        }

    }
});
