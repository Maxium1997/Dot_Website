import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [scanId, setScanId] = useState(null);
  const [progress, setProgress] = useState(null);
  const [alerts, setAlerts] = useState([]);

  // filter state
  const [riskFilter, setRiskFilter] = useState("All");

  // Risk summary counts
  const highCount = alerts.filter((a) => a.risk === "High").length;
  const mediumCount = alerts.filter((a) => a.risk === "Medium").length;
  const lowCount = alerts.filter((a) => a.risk === "Low").length;

  // filtered alerts
  const filteredAlerts =
    riskFilter === "All"
      ? alerts
      : alerts.filter((a) => a.risk === riskFilter);

  async function startScan() {
    setAlerts([]);
    setProgress(null);

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
        fetchAlerts();
      }
    }, 2000);
  }

  async function fetchAlerts() {
    const resp = await fetch("http://127.0.0.1:8000/api/scans/alerts/");
    const data = await resp.json();
    setAlerts(data.alerts);
  }

  // Card component
  function RiskCard({ label, count }) {
    const active = riskFilter === label;

    return (
      <button
        onClick={() => setRiskFilter(label)}
        className={`rounded-2xl p-6 shadow-sm border text-left transition
        ${
          active
            ? "border-black bg-black text-white"
            : "border-gray-200 bg-white hover:bg-gray-50"
        }`}
      >
        <p className="text-sm font-medium">{label}</p>
        <p className="text-3xl font-bold mt-2">{count}</p>
      </button>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-10">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <h1 className="text-3xl font-bold mb-6">
          Security Scanner Dashboard
        </h1>

        {/* Input */}
        <div className="flex gap-3 mb-6">
          <input
            className="flex-1 rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button
            onClick={startScan}
            className="rounded-xl bg-black text-white px-5 py-2 font-medium hover:bg-gray-800"
          >
            Start Scan
          </button>
        </div>

        {/* Scan status */}
        {scanId && (
          <p className="text-sm text-gray-600 mb-2">
            Scan ID: <b>{scanId}</b>
          </p>
        )}

        {progress !== null && (
          <p className="text-sm text-gray-600 mb-6">
            Progress: <b>{progress}%</b>
          </p>
        )}

        {/* Summary Cards */}
        {alerts.length > 0 && (
          <>
            <div className="grid grid-cols-4 gap-4 mb-8">
              <RiskCard label="All" count={alerts.length} />
              <RiskCard label="High" count={highCount} />
              <RiskCard label="Medium" count={mediumCount} />
              <RiskCard label="Low" count={lowCount} />
            </div>

            {/* Alerts Table */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="p-5 border-b">
                <h2 className="text-xl font-semibold">
                  Vulnerability Alerts ({riskFilter})
                </h2>
              </div>

              <table className="w-full text-sm">
                <thead className="bg-gray-100 text-gray-600">
                  <tr>
                    <th className="text-left px-5 py-3">Risk</th>
                    <th className="text-left px-5 py-3">Name</th>
                    <th className="text-left px-5 py-3">URL</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredAlerts.slice(0, 15).map((a, idx) => (
                    <tr
                      key={idx}
                      className="border-t hover:bg-gray-50"
                    >
                      <td className="px-5 py-3 font-medium">
                        {a.risk}
                      </td>
                      <td className="px-5 py-3">{a.name}</td>
                      <td className="px-5 py-3 truncate max-w-md">
                        <a
                          href={a.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 hover:underline"
                        >
                          {a.url}
                        </a>
                      </td>
                    </tr>
                  ))}

                  {filteredAlerts.length === 0 && (
                    <tr>
                      <td
                        colSpan="3"
                        className="text-center py-6 text-gray-400"
                      >
                        No alerts found for this risk level.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
