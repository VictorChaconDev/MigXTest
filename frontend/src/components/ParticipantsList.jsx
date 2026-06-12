import React, { useState, useEffect } from "react";
import { api } from "../api";

export default function ParticipantsList() {
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  // Modal form states
  const [modalOpen, setModalOpen] = useState(false);
  const [formError, setFormError] = useState("");
  const [editingId, setEditingId] = useState(null); // null = add, UUID = edit

  // Form Fields
  const [subjectId, setSubjectId] = useState("");
  const [studyGroup, setStudyGroup] = useState("treatment");
  const [enrollmentDate, setEnrollmentDate] = useState("");
  const [status, setStatus] = useState("active");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("F");

  const fetchParticipants = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.listParticipants();
      setParticipants(data);
    } catch (err) {
      setError(err.message || "Failed to load participants list.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParticipants();
  }, []);

  const openAddModal = () => {
    setEditingId(null);
    setSubjectId("");
    setStudyGroup("treatment");
    setEnrollmentDate(new Date().toISOString().split("T")[0]); // Default to today
    setStatus("active");
    setAge("");
    setGender("F");
    setFormError("");
    setModalOpen(true);
  };

  const openEditModal = (p) => {
    setEditingId(p.participant_id);
    setSubjectId(p.subject_id);
    setStudyGroup(p.study_group);
    setEnrollmentDate(p.enrollment_date);
    setStatus(p.status);
    setAge(p.age.toString());
    setGender(p.gender);
    setFormError("");
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to remove this participant?")) {
      return;
    }
    try {
      await api.deleteParticipant(id);
      setParticipants(participants.filter((p) => p.participant_id !== id));
    } catch (err) {
      alert(err.message || "Failed to delete participant.");
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!subjectId || !enrollmentDate || !age) {
      setFormError("Please fill in all required fields.");
      return;
    }

    const parsedAge = parseInt(age);
    if (isNaN(parsedAge) || parsedAge < 0 || parsedAge > 130) {
      setFormError("Please enter a valid age (0 - 130).");
      return;
    }

    const payload = {
      subject_id: subjectId,
      study_group: studyGroup,
      enrollment_date: enrollmentDate,
      status: status,
      age: parsedAge,
      gender: gender,
    };

    setFormError("");

    try {
      if (editingId) {
        // Edit record
        const updated = await api.updateParticipant(editingId, payload);
        setParticipants(
          participants.map((p) => (p.participant_id === editingId ? updated : p))
        );
      } else {
        // Create record
        const created = await api.createParticipant(payload);
        setParticipants([...participants, created]);
      }
      setModalOpen(false);
    } catch (err) {
      setFormError(err.message || "An error occurred while saving the record.");
    }
  };

  const filteredParticipants = participants.filter((p) =>
    p.subject_id.toLowerCase().includes(search.toLowerCase())
  );

  const getStatusBadgeClass = (statusVal) => {
    if (statusVal === "active") return "badge badge-active";
    if (statusVal === "completed") return "badge badge-completed";
    return "badge badge-withdrawn";
  };

  return (
    <div>
      <div className="controls-row">
        <div className="search-input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="🔍 Search by Subject ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" onClick={openAddModal} style={{ width: "auto" }}>
          ➕ Register Participant
        </button>
      </div>

      {loading ? (
        <div style={{ color: "var(--text-secondary)" }}>Retrieving participant records...</div>
      ) : error ? (
        <div>
          <div className="error-message">{error}</div>
          <button onClick={fetchParticipants} className="btn btn-secondary">
            Retry
          </button>
        </div>
      ) : filteredParticipants.length > 0 ? (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Subject ID</th>
                <th>Study Group</th>
                <th>Enrollment Date</th>
                <th>Status</th>
                <th>Age</th>
                <th>Gender</th>
                <th style={{ textAlign: "right" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredParticipants.map((p) => (
                <tr key={p.participant_id}>
                  <td style={{ fontWeight: "600", color: "var(--text-primary)" }}>{p.subject_id}</td>
                  <td style={{ textTransform: "capitalize" }}>{p.study_group}</td>
                  <td>{p.enrollment_date}</td>
                  <td>
                    <span className={getStatusBadgeClass(p.status)}>{p.status}</span>
                  </td>
                  <td>{p.age}</td>
                  <td>{p.gender}</td>
                  <td>
                    <div className="action-btns" style={{ justifyContent: "flex-end" }}>
                      <button className="btn-action" onClick={() => openEditModal(p)}>
                        Edit
                      </button>
                      <button
                        className="btn-action btn-action-delete"
                        onClick={() => handleDelete(p.participant_id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
          {search ? "No participants match your search criteria." : "No participants registered. Click 'Register Participant' to add one."}
        </div>
      )}

      {/* Modal Dialog Popup */}
      {modalOpen && (
        <div className="modal-overlay">
          <div className="modal-card">
            <div className="modal-header">
              <h3 className="modal-title">
                {editingId ? "Modify Participant Record" : "Register New Participant"}
              </h3>
              <button className="modal-close" onClick={() => setModalOpen(false)}>
                &times;
              </button>
            </div>

            <form onSubmit={handleFormSubmit}>
              <div className="modal-body">
                {formError && <div className="error-message">{formError}</div>}

                <div className="form-group">
                  <label className="form-label" htmlFor="subject_id">
                    Subject ID *
                  </label>
                  <input
                    type="text"
                    id="subject_id"
                    className="form-input"
                    value={subjectId}
                    onChange={(e) => setSubjectId(e.target.value)}
                    placeholder="e.g. SUB-005"
                    disabled={editingId !== null} // Lock subject_id on edit
                  />
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "16px",
                  }}
                >
                  <div className="form-group">
                    <label className="form-label" htmlFor="study_group">
                      Study Group
                    </label>
                    <select
                      id="study_group"
                      className="form-input"
                      value={studyGroup}
                      onChange={(e) => setStudyGroup(e.target.value)}
                    >
                      <option value="treatment">Treatment</option>
                      <option value="control">Control</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label" htmlFor="status">
                      Status
                    </label>
                    <select
                      id="status"
                      className="form-input"
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                    >
                      <option value="active">Active</option>
                      <option value="completed">Completed</option>
                      <option value="withdrawn">Withdrawn</option>
                    </select>
                  </div>
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "16px",
                  }}
                >
                  <div className="form-group">
                    <label className="form-label" htmlFor="age">
                      Age *
                    </label>
                    <input
                      type="number"
                      id="age"
                      className="form-input"
                      value={age}
                      onChange={(e) => setAge(e.target.value)}
                      placeholder="e.g. 45"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label" htmlFor="gender">
                      Gender
                    </label>
                    <select
                      id="gender"
                      className="form-input"
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                    >
                      <option value="F">Female</option>
                      <option value="M">Male</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label" htmlFor="enrollment_date">
                    Enrollment Date *
                  </label>
                  <input
                    type="date"
                    id="enrollment_date"
                    className="form-input"
                    value={enrollmentDate}
                    onChange={(e) => setEnrollmentDate(e.target.value)}
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setModalOpen(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" style={{ width: "auto" }}>
                  Save Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
