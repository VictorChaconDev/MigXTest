import React, { useState, useEffect } from "react";
import { api } from "../api";

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchMetrics = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getMetrics();
      setMetrics(data);
    } catch (err) {
      setError(err.message || "Failed to load metrics dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  if (loading) {
    return <div style={{ color: "var(--text-secondary)" }}>Loading trial metrics...</div>;
  }

  if (error) {
    return (
      <div>
        <div className="error-message">{error}</div>
        <button onClick={fetchMetrics} className="btn btn-secondary">
          Retry
        </button>
      </div>
    );
  }

  const { total_participants, study_groups, statuses, genders, average_age } = metrics;

  // Percentage calculations
  const calculatePercent = (value) => {
    if (total_participants === 0) return 0;
    return Math.round((value / total_participants) * 100);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
        <h2 style={{ fontSize: "1.75rem", fontWeight: "700" }}>Trial Metrics Dashboard</h2>
        <button onClick={fetchMetrics} className="btn btn-secondary" style={{ padding: "8px 16px", fontSize: "0.85rem" }}>
           Refresh Metrics
        </button>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <span className="metric-label">Total Participants</span>
          <span className="metric-value">{total_participants}</span>
          <span className="metric-footer">Registered in active database</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Average Subject Age</span>
          <span className="metric-value">{average_age} yrs</span>
          <span className="metric-footer">Target demographic variance</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Active Ratio</span>
          <span className="metric-value">{calculatePercent(statuses.active)}%</span>
          <span className="metric-footer">
            {statuses.active} of {total_participants} currently active
          </span>
        </div>
      </div>

      {total_participants > 0 ? (
        <div className="charts-grid">
          <div className="chart-card">
            <h3 className="chart-title">Study Group Assignments</h3>
            <div className="metrics-progress-list">
              <div className="progress-item">
                <div className="progress-label-row">
                  <span>Treatment Group</span>
                  <span>
                    {study_groups.treatment} ({calculatePercent(study_groups.treatment)}%)
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${calculatePercent(study_groups.treatment)}%`,
                      backgroundColor: "var(--accent-color)",
                    }}
                  />
                </div>
              </div>

              <div className="progress-item">
                <div className="progress-label-row">
                  <span>Control Group</span>
                  <span>
                    {study_groups.control} ({calculatePercent(study_groups.control)}%)
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${calculatePercent(study_groups.control)}%`,
                      backgroundColor: "var(--accent-success)",
                    }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Participant Status Statuses</h3>
            <div className="metrics-progress-list">
              <div className="progress-item">
                <div className="progress-label-row">
                  <span>Active</span>
                  <span>
                    {statuses.active} ({calculatePercent(statuses.active)}%)
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${calculatePercent(statuses.active)}%`,
                      backgroundColor: "var(--accent-color)",
                    }}
                  />
                </div>
              </div>

              <div className="progress-item">
                <div className="progress-label-row">
                  <span>Completed</span>
                  <span>
                    {statuses.completed} ({calculatePercent(statuses.completed)}%)
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${calculatePercent(statuses.completed)}%`,
                      backgroundColor: "var(--accent-success)",
                    }}
                  />
                </div>
              </div>

              <div className="progress-item">
                <div className="progress-label-row">
                  <span>Withdrawn</span>
                  <span>
                    {statuses.withdrawn} ({calculatePercent(statuses.withdrawn)}%)
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${calculatePercent(statuses.withdrawn)}%`,
                      backgroundColor: "var(--accent-danger)",
                    }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="chart-card" style={{ gridColumn: "1 / -1" }}>
            <h3 className="chart-title">Gender Distribution Breakdown</h3>
            <div
              style={{
                display: "flex",
                justifyContent: "space-around",
                alignItems: "center",
                flexWrap: "wrap",
                gap: "20px",
                padding: "20px 0",
              }}
            >
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "#818cf8" }}>{genders.F}</div>
                <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: "500" }}>Female</div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{calculatePercent(genders.F)}%</div>
              </div>

              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "#34d399" }}>{genders.M}</div>
                <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: "500" }}>Male</div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{calculatePercent(genders.M)}%</div>
              </div>

              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "var(--accent-warning)" }}>{genders.Other}</div>
                <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: "500" }}>Other</div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{calculatePercent(genders.Other)}%</div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div
          style={{
            textAlign: "center",
            padding: "40px",
            backgroundColor: "var(--bg-secondary)",
            borderRadius: "var(--border-radius-md)",
            border: "1px solid var(--border-color)",
            color: "var(--text-muted)",
          }}
        >
          No participant records found to generate metrics charts.
        </div>
      )}
    </div>
  );
}
