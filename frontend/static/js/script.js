const logsTable = document.querySelector("#logs-table tbody");
const suspiciousList = document.querySelector("#suspicious-list");
const totalLogs = document.querySelector("#total-logs");
const searchInput = document.querySelector("#search");

let logsData = [];
let errorChart;

// Fetch logs from API
async function fetchLogs() {
  const res = await fetch("http://localhost:5000/logs");
  logsData = await res.json();
  totalLogs.textContent = logsData.length;
  renderLogs(logsData);
  updateChart(logsData);
}

// Fetch suspicious users
async function fetchSuspicious() {
  const res = await fetch("http://localhost:5000/suspicious");
  const data = await res.json();
  suspiciousList.innerHTML = "";
  data.suspicious_users.forEach(user => {
    suspiciousList.innerHTML += `<li>${user}</li>`;
  });
}

// Render logs in table with colors
function renderLogs(logs) {
  logsTable.innerHTML = "";
  logs.forEach(log => {
    let severity = "info";
    if (log.message.includes("failed") || log.message.includes("error")) severity = "error";
    else if (log.message.includes("warning")) severity = "warning";

    const row = `<tr class="${severity}">
      <td>${log.id}</td>
      <td>${log.message}</td>
      <td>${new Date(log.time).toLocaleString()}</td>
    </tr>`;
    logsTable.innerHTML += row;
  });
}

// Search filter
searchInput.addEventListener("input", () => {
  const term = searchInput.value.toLowerCase();
  const filtered = logsData.filter(log => log.message.toLowerCase().includes(term));
  renderLogs(filtered);
});

// Chart.js setup
function setupChart() {
  const ctx = document.getElementById("errorChart").getContext("2d");
  errorChart = new Chart(ctx, {
    type: "line",
    data: { labels: [], datasets: [{ label: "Errors", data: [], borderColor: "red", fill: false }] },
    options: { responsive: true, scales: { x: { title: { display: true, text: "Time" } }, y: { title: { display: true, text: "Count" } } } }
  });
}

// Update chart with latest errors
function updateChart(logs) {
  const errorLogs = logs.filter(log => log.message.includes("failed") || log.message.includes("error"));
  const counts = {};
  errorLogs.forEach(log => {
    const hour = new Date(log.time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    counts[hour] = (counts[hour] || 0) + 1;
  });

  errorChart.data.labels = Object.keys(counts);
  errorChart.data.datasets[0].data = Object.values(counts);
  errorChart.update();
}

// Refresh everything every 5 seconds
async function updateDashboard() {
  await fetchLogs();
  await fetchSuspicious();
}

setupChart();
updateDashboard();
setInterval(updateDashboard, 5000);