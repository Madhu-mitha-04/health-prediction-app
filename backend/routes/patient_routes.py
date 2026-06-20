from flask import Blueprint, request, jsonify
from extensions import db
from models import Patient
from validators import validate_patient_payload
from ml.test_model import predict_health_risk

patients_bp = Blueprint("patients", __name__, url_prefix="/api/patients")


@patients_bp.route("", methods=["POST"])
def create_patient():
    """
    POST /api/patients
    Creates a new patient record after validation, then auto-generates
    the remarks field via the ML model.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    is_valid, errors = validate_patient_payload(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    # Enforce email uniqueness with a clear message (DB also enforces this)
    existing = Patient.query.filter_by(email=data["email"].strip()).first()
    if existing:
        return jsonify({"errors": {"email": "A patient with this email already exists."}}), 409

    try:
        remarks = predict_health_risk(
            data["glucose"], data["haemoglobin"], data["cholesterol"]
        )
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500

    patient = Patient(
        full_name=data["full_name"].strip(),
        date_of_birth=data["date_of_birth"],
        email=data["email"].strip(),
        glucose=data["glucose"],
        haemoglobin=data["haemoglobin"],
        cholesterol=data["cholesterol"],
        remarks=remarks,
    )

    db.session.add(patient)
    db.session.commit()

    return jsonify(patient.to_dict()), 201


@patients_bp.route("", methods=["GET"])
def get_all_patients():
    """
    GET /api/patients
    Returns all patient records, most recently created first.
    """
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return jsonify([p.to_dict() for p in patients]), 200


@patients_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    """
    GET /api/patients/<id>
    Returns a single patient record by ID.
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": f"Patient with id {patient_id} not found."}), 404
    return jsonify(patient.to_dict()), 200


@patients_bp.route("/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """
    PUT /api/patients/<id>
    Updates an existing patient record after validation, then re-runs
    the ML prediction so remarks reflect the latest blood test values.
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": f"Patient with id {patient_id} not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    is_valid, errors = validate_patient_payload(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    # If email is changing, ensure it doesn't collide with another patient
    new_email = data["email"].strip()
    if new_email != patient.email:
        existing = Patient.query.filter_by(email=new_email).first()
        if existing:
            return jsonify({"errors": {"email": "A patient with this email already exists."}}), 409

    try:
        remarks = predict_health_risk(
            data["glucose"], data["haemoglobin"], data["cholesterol"]
        )
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500

    patient.full_name = data["full_name"].strip()
    patient.date_of_birth = data["date_of_birth"]
    patient.email = new_email
    patient.glucose = data["glucose"]
    patient.haemoglobin = data["haemoglobin"]
    patient.cholesterol = data["cholesterol"]
    patient.remarks = remarks

    db.session.commit()

    return jsonify(patient.to_dict()), 200


@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """
    DELETE /api/patients/<id>
    Deletes a patient record by ID.
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": f"Patient with id {patient_id} not found."}), 404

    db.session.delete(patient)
    db.session.commit()

    return jsonify({"message": f"Patient with id {patient_id} deleted successfully."}), 200