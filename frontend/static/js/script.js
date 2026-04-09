async function fetchLogs() {
    try {
        const response = await fetch("http://localhost:5000/logs");
        const data = await response.json();
        const logList = document.getElementById("logs");
        logList.innerHTML = "";
        data.logs.forEach(log => {
            const li = document.createElement("li");
            li.textContent = `${log[0]} - ${log[1]}`;
            logList.appendChild(li);
        });
    } catch (err) {
        console.error("Error fetching logs:", err);
    }
}

setInterval(fetchLogs, 2000); // fetch every 2 seconds
window.onload = fetchLogs;