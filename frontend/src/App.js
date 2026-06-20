import React, { useState, useEffect, useCallback } from "react";
import PatientForm from "./components/PatientForm";
import PatientList from "./components/PatientList";
import { getAllPatients } from "./api/api";
import "./App.css";

function App() {
  const [patients, setPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [editingPatient, setEditingPatient] = useState(null);

  const fetchPatients = useCallback(async () => {
    setIsLoading(true);
    setLoadError("");
    try {
      const response = await getAllPatients();
      setPatients(response.data);
    } catch (err) {
      setLoadError(
        "Unable to load patient records. Please ensure the backend server is running on http://localhost:5000."
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPatients();
  }, [fetchPatients]);

  const handleSaveSuccess = () => {
    setEditingPatient(null);
    fetchPatients();
  };

  const handleEdit = (patient) => {
    setEditingPatient(patient);
  };

  const handleCancelEdit = () => {
    setEditingPatient(null);
  };

  const handleDeleteSuccess = () => {
    fetchPatients();
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Health Prediction Application</h1>
        <p>Manage patient records and view AI-generated health risk remarks.</p>
      </header>

      <main className="app-main">
        <PatientForm
          editingPatient={editingPatient}
          onSaveSuccess={handleSaveSuccess}
          onCancelEdit={handleCancelEdit}
        />

        {loadError && <p className="status-message error">{loadError}</p>}

        <PatientList
          patients={patients}
          onEdit={handleEdit}
          onDeleteSuccess={handleDeleteSuccess}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}

export default App;