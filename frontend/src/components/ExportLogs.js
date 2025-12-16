import React, { useState } from "react";
import { exportLogs } from "../utils/api";

const ExportLogs = () => {
  const [format, setFormat] = useState("csv");
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");

  const handleExport = async () => {
    const response = await exportLogs(format, from, to);

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");

    link.href = url;
    link.setAttribute("download", `logs.${format}`);
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="export-container">
      <div className="export-card">
        <h3 className="export-title">Export Logs</h3>

        <div className="export-form">
          <div className="form-group">
            <label>From</label>
            <input type="date" onChange={(e) => setFrom(e.target.value)} />
          </div>

          <div className="form-group">
            <label>To</label>
            <input type="date" onChange={(e) => setTo(e.target.value)} />
          </div>

          <div className="form-group">
            <label>Format</label>
            <select onChange={(e) => setFormat(e.target.value)}>
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
              <option value="excel">Excel</option>
            </select>
          </div>

          <button className="btn btn-primary" onClick={handleExport}>
            Export
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExportLogs;
