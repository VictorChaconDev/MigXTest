// frontend/src/api.js

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const getHeaders = () => {
  const token = localStorage.getItem("token");
  const headers = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
};

export const api = {

  register: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Registration failed");
    }
    return response.json();
  },

  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }
    return response.json();
  },


  listParticipants: async () => {
    const response = await fetch(`${API_BASE_URL}/participants/`, {
      method: "GET",
      headers: getHeaders(),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to retrieve participants");
    }
    return response.json();
  },

  createParticipant: async (participantData) => {
    const response = await fetch(`${API_BASE_URL}/participants/`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(participantData),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to create participant");
    }
    return response.json();
  },

  getParticipant: async (id) => {
    const response = await fetch(`${API_BASE_URL}/participants/${id}`, {
      method: "GET",
      headers: getHeaders(),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to retrieve participant");
    }
    return response.json();
  },

  updateParticipant: async (id, participantData) => {
    const response = await fetch(`${API_BASE_URL}/participants/${id}`, {
      method: "PUT",
      headers: getHeaders(),
      body: JSON.stringify(participantData),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to update participant");
    }
    return response.json();
  },

  deleteParticipant: async (id) => {
    const response = await fetch(`${API_BASE_URL}/participants/${id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to delete participant");
    }
    return true;
  },

  // Metrics
  getMetrics: async () => {
    const response = await fetch(`${API_BASE_URL}/participants/metrics`, {
      method: "GET",
      headers: getHeaders(),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to retrieve metrics");
    }
    return response.json();
  },
};
