import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getAllPatients = () => apiClient.get("/patients");

export const getPatientById = (id) => apiClient.get(`/patients/${id}`);

export const createPatient = (patientData) =>
  apiClient.post("/patients", patientData);

export const updatePatient = (id, patientData) =>
  apiClient.put(`/patients/${id}`, patientData);

export const deletePatient = (id) => apiClient.delete(`/patients/${id}`);

export default apiClient;