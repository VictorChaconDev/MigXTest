import React, { useState } from "react";
import { api } from "../api";

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("Please fill in all fields.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        const data = await api.login(username, password);
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", username);
        onLoginSuccess(data.access_token, username);
      } else {
        const data = await api.register(username, password);
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", username);
        onLoginSuccess(data.access_token, username);
      }
    } catch (err) {
      setError(err.message || "An error occurred during authentication.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1 className="auth-logo">MigX Trial</h1>
        <p className="auth-subtitle">
          {isLogin
            ? "Sign in to access researcher dashboard"
            : "Create an account to join the clinical study team"}
        </p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="username">
              Username
            </label>
            <input
              type="text"
              id="username"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              autoComplete="username"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ marginTop: "10px" }}
          >
            {loading ? "Processing..." : isLogin ? "Sign In" : "Register"}
          </button>
        </form>

        <div className="auth-switch">
          {isLogin ? "New to MigX?" : "Already have an account?"}
          <span
            className="auth-switch-link"
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
              setUsername("");
              setPassword("");
            }}
          >
            {isLogin ? "Create an account" : "Sign in here"}
          </span>
        </div>
      </div>
    </div>
  );
}
