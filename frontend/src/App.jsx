import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [scanId, setScanId] = useState(null);
  const [progress, setProgress] = useState(null);

  async function startScan() {
    const resp = await fetch("http://127.0.0.1:8000/api/scans/start/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await resp.json();
    setScanId(data.scan_id);

    // 開始輪詢進度
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
      }
    }, 2000);
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
    </div>
  );
}

export default App;
