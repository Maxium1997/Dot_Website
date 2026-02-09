import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [scanId, setScanId] = useState(null);
  const [progress, setProgress] = useState(null);
  const [alerts, setAlerts] = useState([]);

  async function startScan() {
    const resp = await fetch("http://127.0.0.1:8000/api/scans/start/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await resp.json();
    setScanId(data.scan_id);

    pollProgress(data.scan_id);
  }

  async function pollProgress(id) {
    const timer = setInterval(async () => {
      const resp = await fetch(
        `http://127.0.0.1:8000/api/scans/progress/${id}/`
      );
      const data = await resp.json();

      setProgress(data.progress);

      if (data.progress >= 100) {
        clearInterval(timer);
        fetchAlerts(); //掃描完成後抓漏洞
      }
    }, 2000);
  }

  async function fetchAlerts() {
    const resp = await fetch("http://127.0.0.1:8000/api/scans/alerts/");
    const data = await resp.json();
    setAlerts(data.alerts);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Security Scanner Dashboard</h1>

      <input
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={startScan} style={{ marginLeft: 10 }}>
        Start Scan
      </button>

      {scanId && (
        <p style={{ marginTop: 20 }}>
          Scan ID: <b>{scanId}</b>
        </p>
      )}

      {progress !== null && (
        <p>
          Progress: <b>{progress}%</b>
        </p>
      )}

      {/* 漏洞列表 */}
      {alerts.length > 0 && (
        <div style={{ marginTop: 30 }}>
          <h2>Vulnerability Alerts</h2>

          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Risk</th>
                <th>Name</th>
                <th>URL</th>
              </tr>
            </thead>
            <tbody>
              {alerts.slice(0, 10).map((a, idx) => (
                <tr key={idx}>
                  <td>{a.risk}</td>
                  <td>{a.name}</td>
                  <td style={{ maxWidth: 400 }}>
                    <a href={a.url} target="_blank">
                      {a.url}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
