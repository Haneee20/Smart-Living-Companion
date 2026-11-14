
console.log("Smart Living Companion MQTT dashboard started!");

async function updateSensors() {
    try {
        const response = await fetch("/api/sensors");
        const result = await response.json();

        const data = result.data;

        // Update temperature
        document.getElementById("temperature").innerText =
            data.temperature !== null
                ? data.temperature + " °C"
                : "-- °C";

        // Update humidity
        document.getElementById("humidity").innerText =
            data.humidity !== null
                ? data.humidity + " %"
                : "-- %";

        // Update motion
        document.getElementById("motion").innerText =
            data.motion ?? "Waiting...";

        console.log("MQTT connection:", result.connected);

    } catch (error) {
        console.log("Error fetching sensor data:", error);
    }
}

// LED buttons (temporary simulation)
document.getElementById("ledOn").addEventListener("click", function() {
    document.getElementById("ledStatus").innerText = "LED is ON";
});

document.getElementById("ledOff").addEventListener("click", function() {
    document.getElementById("ledStatus").innerText = "LED is OFF";
});

// Fetch readings every 2 seconds
updateSensors();
setInterval(updateSensors, 2000);
