import React, { useState } from "react";
import { deletePatient } from "../api/api";
import "./PatientList.css";

function PatientList({ patients, onEdit, onDeleteSuccess, isLoading }) {
  const [deletingId, setDeletingId] = useState(null);

  const handleDelete = async (id, fullName) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete the record for "${fullName}"?`
    );
    if (!confirmed) return;

    setDeletingId(id);
    try {
      await deletePatient(id);
      onDeleteSuccess();
    } catch (err) {
      alert("Failed to delete patient. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) {
    return <p className="status-message">Loading patient records...</p>;
  }

  if (!patients || patients.length === 0) {
    return <p className="status-message">No patient records found. Add one above.</p>;
  }

  return (
    <div className="patient-list">
      <h2>Patient Records</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Full Name</th>
              <th>Date of Birth</th>
              <th>Email</th>
              <th>Glucose</th>
              <th>Haemoglobin</th>
              <th>Cholesterol</th>
              <th>Remarks (AI)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient) => (
              <tr key={patient.id}>
                <td>{patient.full_name}</td>
                <td>{patient.date_of_birth}</td>
                <td>{patient.email}</td>
                <td>{patient.glucose}</td>
                <td>{patient.haemoglobin}</td>
                <td>{patient.cholesterol}</td>
                <td className="remarks-cell">{patient.remarks || "—"}</td>
                <td className="actions-cell">
                  <button className="btn btn-small btn-edit" onClick={() => onEdit(patient)}>
                    Edit
                  </button>
                  <button
                    className="btn btn-small btn-delete"
                    onClick={() => handleDelete(patient.id, patient.full_name)}
                    disabled={deletingId === patient.id}
                  >
                    {deletingId === patient.id ? "Deleting..." : "Delete"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PatientList;