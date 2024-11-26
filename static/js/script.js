// Function to call Flask API and update the webpage with predictions
function getPredictions() {
  fetch("/predict") // This will hit the /predict endpoint of the Flask app
    .then((response) => response.json()) // Parse JSON response
    .then((data) => {
      // Update the UI with the predicted temperature
      document.getElementById("temp").innerText =
        data.predicted_temp.toFixed(2);
    })
    .catch((error) => console.error("Error fetching data:", error));
}

// Function to trigger model training
function trainModel() {
  fetch("/train_model") // This will hit the /train_model endpoint of the Flask app
    .then((response) => response.json())
    .then((data) => {
      // Display a success message on successful model training
      alert(data.message || "Model training failed");
    })
    .catch((error) => {
      alert("Error training model: " + error.message);
    });
}

// Function to refresh the data and update the graphs
function refreshData() {
  fetch("/get_data_for_graphs") // This will hit the /get_data_for_graphs endpoint
    .then((response) => response.json()) // Parse JSON response
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }

      // Update the graphs using Plotly
      updateGraph("temp-vs-hour", data.hour, data.temperature, "Hour", "Temperature (°C)");
      updateGraph("temp-vs-pressure", data.pressure, data.temperature, "Pressure (hPa)", "Temperature (°C)");
      updateGraph("temp-vs-altitude", data.altitude, data.temperature, "Altitude (m)", "Temperature (°C)");
      updateGraph("temp-vs-humidity", data.humidity, data.temperature, "Humidity (%)", "Temperature (°C)");
    })
    .catch((error) => console.error("Error fetching graph data:", error));
}

// Function to update a single graph
function updateGraph(elementId, xData, yData, xLabel, yLabel) {
  var trace = {
    x: xData,
    y: yData,
    mode: "lines+markers",
    type: "scatter",
    name: "Temperature",
  };

  var layout = {
    title: `Temperature vs ${xLabel}`,
    xaxis: { title: xLabel },
    yaxis: { title: yLabel },
  };

  Plotly.newPlot(elementId, [trace], layout);
}

// Call the refreshData function on page load to render the initial graphs
document.addEventListener("DOMContentLoaded", refreshData);
