// static/js/script.js

// Function to call Flask API and update the webpage with predictions
function getPredictions() {
  fetch("/predict") // This will hit the /predict endpoint of the Flask app
    .then((response) => response.json()) // Parse JSON response
    .then((data) => {
      // Update the UI with the predicted temperature
      document.getElementById("temp").innerText =
        data.predicted_temp.toFixed(2);

      // Optionally, you can use Plotly to create a graph (just as an example)
      var trace = {
        x: ["12 PM"], // Just an example, you can use real-time data
        y: [data.predicted_temp],
        mode: "lines+markers",
        type: "scatter",
        name: "Temperature",
      };

      var layout = {
        title: "Predicted Temperature over Time",
        xaxis: {
          title: "Time of Day",
        },
        yaxis: {
          title: "Temperature (°C)",
        },
      };

      Plotly.newPlot("graph-container", [trace], layout);
    })
    .catch((error) => console.error("Error fetching data:", error));
}
