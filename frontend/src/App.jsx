import React, { useState, useEffect } from "react";
import Auth from "./components/Auth";
import MetricsDashboard from "./components/MetricsDashboard";
import ParticipantsList from "./components/ParticipantsList";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username"));
  const [activeTab, setActiveTab] = useState("metrics"); // 'metrics' or 'participants'

  const handleLoginSuccess = (newToken, user) => {
    setToken(newToken);
    setUsername(user);
    setActiveTab("metrics");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
    setUsername(null);
  };

  if (!token) {
    return <Auth onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app-container">
      {/* header bar */}
      <header className="app-header">
        <div className="header-brand"> MigX Clinical trial</div>
        <div className="header-user-info">
          <span className="user-tag"> {username}</span>
          <button className="btn btn-logout" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      </header>

      {/* Sidebar */}
      <div className="dashboard-layout">
        <aside className="dashboard-sidebar">
          <div
            className={`sidebar-tab ${activeTab === "metrics" ? "active" : ""}`}
            onClick={() => setActiveTab("metrics")}
          >
            <span>Metrics Dashboard</span>
          </div>

          <div
            className={`sidebar-tab ${
              activeTab === "participants" ? "active" : ""
            }`}
            onClick={() => setActiveTab("participants")}
          >
            <span>Participants List</span>
          </div>
        </aside>

        <main className="dashboard-content">
          {activeTab === "metrics" ? (
            <MetricsDashboard />
          ) : (
            <ParticipantsList />
          )}
        </main>
      </div>
    </div>
  );
}
