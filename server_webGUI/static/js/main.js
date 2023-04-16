function uploadCSV() {
    const input = document.getElementById('csvFileInput');
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      const csv = e.target.result;
      const lines = csv.split('\n');
      const urls = lines.map(line => line.trim());
      sendUrlsToServer(urls);
    };
    reader.readAsText(file);
  }
  
  function sendUrlsToServer(urls) {
    const socket = new WebSocket('ws://localhost:5000/upload');
    socket.onopen = function() {
      urls.forEach(url => {
        socket.send(url);
      });
    };
    socket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      const url = data.url;
      const status = data.status;
      const row = document.createElement('tr');
      const urlCell = document.createElement('td');
      const statusCell = document.createElement('td');
      urlCell.textContent = url;
      statusCell.textContent = status;
      row.appendChild(urlCell);
      row.appendChild(statusCell);
      document.getElementById('urlTable').appendChild(row);
    };
    socket.onclose = function() {
      console.log('Socket closed');
    };
  }
  