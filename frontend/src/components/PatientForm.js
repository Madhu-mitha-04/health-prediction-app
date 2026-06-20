import React, { useState, useEffect } from "react";
import { createPatient, updatePatient } from "../api/api";
import "./PatientForm.css";

const EMAIL_REGEX = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

const initialFormState = {
  full_name: "",
  date_of_birth: "",
  email: "",
  glucose: "",
  haemoglobin: "",
  cholesterol: "",
};

function PatientForm({ editingPatient, onSaveSuccess, onCancelEdit }) {
  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form when switching into "edit" mode
  useEffect(() => {
    if (editingPatient) {
      setFormData({
        full_name: editingPatient.full_name || "",
        date_of_birth: editingPatient.date_of_birth || "",
        email: editingPatient.email || "",
        glucose: editingPatient.glucose ?? "",
        haemoglobin: editingPatient.haemoglobin ?? "",
        cholesterol: editingPatient.cholesterol ?? "",
      });
      setErrors({});
      setServerError("");
    } else {
      setFormData(initialFormState);
    }
  }, [editingPatient]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  /**
   * Client-side validation mirroring backend/validators.py rules:
   * - full_name required
   * - DOB required, cannot be a future date
   * - email valid format
   * - glucose / haemoglobin / cholesterol required, numeric, >= 0
   */
  const validate = () => {
    const newErrors = {};

    if (!formData.full_name.trim()) {
      newErrors.full_name = "Full name is required.";
    }

    if (!formData.date_of_birth) {
      newErrors.date_of_birth = "Date of birth is required.";
    } else {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const dob = new Date(formData.date_of_birth);
      if (dob > today) {
        newErrors.date_of_birth = "Date of birth cannot be a future date.";
      }
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required.";
    } else if (!EMAIL_REGEX.test(formData.email.trim())) {
      newErrors.email = "Invalid email address format.";
    }

    ["glucose", "haemoglobin", "cholesterol"].forEach((field) => {
      const value = formData[field];
      const label = field.charAt(0).toUpperCase() + field.slice(1);
      if (value === "" || value === null) {
        newErrors[field] = `${label} is required.`;
      } else if (isNaN(Number(value))) {
        newErrors[field] = `${label} must be a numeric value.`;
      } else if (Number(value) < 0) {
        newErrors[field] = `${label} cannot be negative.`;
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError("");

    if (!validate()) {
      return;
    }

    const payload = {
      full_name: formData.full_name.trim(),
      date_of_birth: formData.date_of_birth,
      email: formData.email.trim(),
      glucose: Number(formData.glucose),
      haemoglobin: Number(formData.haemoglobin),
      cholesterol: Number(formData.cholesterol),
    };

    setIsSubmitting(true);
    try {
      if (editingPatient) {
        await updatePatient(editingPatient.id, payload);
      } else {
        await createPatient(payload);
      }
      setFormData(initialFormState);
      setErrors({});
      onSaveSuccess();
    } catch (err) {
      if (err.response && err.response.data) {
        const data = err.response.data;
        if (data.errors) {
          setErrors(data.errors);
        } else if (data.error) {
          setServerError(data.error);
        }
      } else {
        setServerError("Unable to reach the server. Please ensure the backend is running.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setFormData(initialFormState);
    setErrors({});
    setServerError("");
    onCancelEdit();
  };

  return (
    <form className="patient-form" onSubmit={handleSubmit}>
      <h2>{editingPatient ? "Update Patient" : "Add New Patient"}</h2>

      {serverError && <div className="form-error-banner">{serverError}</div>}

      <div className="form-group">
        <label htmlFor="full_name">Full Name</label>
        <input
          type="text"
          id="full_name"
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
        />
        {errors.full_name && <span className="field-error">{errors.full_name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="date_of_birth">Date of Birth</label>
        <input
          type="date"
          id="date_of_birth"
          name="date_of_birth"
          value={formData.date_of_birth}
          onChange={handleChange}
          max={new Date().toISOString().split("T")[0]}
        />
        {errors.date_of_birth && (
          <span className="field-error">{errors.date_of_birth}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <span className="field-error">{errors.email}</span>}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="glucose">Glucose (mg/dL)</label>
          <input
            type="number"
            step="0.01"
            id="glucose"
            name="glucose"
            value={formData.glucose}
            onChange={handleChange}
          />
          {errors.glucose && <span className="field-error">{errors.glucose}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="haemoglobin">Haemoglobin (g/dL)</label>
          <input
            type="number"
            step="0.01"
            id="haemoglobin"
            name="haemoglobin"
            value={formData.haemoglobin}
            onChange={handleChange}
          />
          {errors.haemoglobin && (
            <span className="field-error">{errors.haemoglobin}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="cholesterol">Cholesterol (mg/dL)</label>
          <input
            type="number"
            step="0.01"
            id="cholesterol"
            name="cholesterol"
            value={formData.cholesterol}
            onChange={handleChange}
          />
          {errors.cholesterol && (
            <span className="field-error">{errors.cholesterol}</span>
          )}
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting
            ? "Saving..."
            : editingPatient
            ? "Update Patient"
            : "Add Patient"}
        </button>
        {editingPatient && (
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleCancel}
            disabled={isSubmitting}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default PatientForm;