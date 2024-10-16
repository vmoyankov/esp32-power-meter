html = {
        "/" : b"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power Meter</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>

<h2>Data Table</h2>

<!-- Input box to set the update interval -->
<label for="updateInterval">Set update interval (in seconds): </label>
<input type="number" id="updateInterval" value="10" min="1">
<button onclick="updateInterval()">Set Interval</button>

<table id="dataTable">
    <thead>
        <tr>
            <th>Time</th>
            <th>Voltage (V)</th>
            <th>Current (A)</th>
            <th>Pf</th>
            <th>Power (W)</th>
	    <th>Energy (kWh)</th>
        </tr>
    </thead>
    <tbody>
        <!-- Data will be inserted here dynamically -->
    </tbody>
</table>

<script>
// Function to fetch data from the REST service
async function fetchData() {
    try {
        // Fetching data from the REST service (Replace with your actual REST API URL)
        const response = await fetch('/data');
        const data = await response.json();

        // Add the new data to the table
        updateTable(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to update the table with new data
function updateTable(data) {
    const table = document.getElementById("dataTable").getElementsByTagName("tbody")[0];

    // Create a new row
    const newRow = document.createElement("tr");

    // Insert cells and populate them with the data
    const cellTime = newRow.insertCell(0);
    const cellVoltage = newRow.insertCell(1);
    const cellCurrent = newRow.insertCell(2);
    const cellPf = newRow.insertCell(3);
    const cellPower = newRow.insertCell(4);
    const cellEnergy = newRow.insertCell(5);

    // Convert Unix timestamp (milliseconds) to local time
    const date = new Date(data.time * 1000); // Assuming time is in seconds, multiply by 1000 for milliseconds
    const localTime = date.toLocaleString(); // Convert to a readable local time

    cellTime.innerHTML = localTime;
    cellVoltage.innerHTML = data.u;
    cellCurrent.innerHTML = data.i;
    cellPf.innerHTML = data.pf;
    cellPower.innerHTML = data.p;
    cellEnergy.innerHTML = data.e / 1000;

    // Insert the new row at the top (as the first row after the header)
    table.insertBefore(newRow, table.firstChild);
}

// Function to update the interval based on user input
function updateInterval() {
    const intervalInput = document.getElementById("updateInterval").value;
    const intervalInSeconds = parseInt(intervalInput);

    if (!isNaN(intervalInSeconds) && intervalInSeconds >= 1) {

        // Clear the existing interval
        clearInterval(intervalID);

        // Set the new update time in milliseconds
        updateTime = intervalInSeconds * 1000;

        // Start the fetch loop with the new interval
        intervalID = setInterval(fetchData, updateTime);
        
        // Fetch data immediately after setting the new interval
        fetchData();
    } else {
        alert("Please enter a valid number greater than or equal to 1.");
    }
}

// Fetch and update the table initially
fetchData();

// Start the interval with the default time (10 seconds)
updateTime = 10000;
intervalID = setInterval(fetchData, updateTime);

</script>

</body>
</html>
""",
}

