from datetime import datetime, date
from extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    full_name = db.Column(db.String(150), nullable=False)

    date_of_birth = db.Column(db.Date, nullable=False)

    email = db.Column(db.String(150), nullable=False, unique=True)

    glucose = db.Column(db.Numeric(6, 2), nullable=False)

    haemoglobin = db.Column(db.Numeric(6, 2), nullable=False)

    cholesterol = db.Column(db.Numeric(6, 2), nullable=False)

    remarks = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        """
        Serialise the model instance into a JSON-friendly dict
        for API responses (Flask jsonify / React consumption).
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "date_of_birth": (
                self.date_of_birth.isoformat()
                if isinstance(self.date_of_birth, date)
                else self.date_of_birth
            ),
            "email": self.email,
            "glucose": float(self.glucose) if self.glucose is not None else None,
            "haemoglobin": (
                float(self.haemoglobin) if self.haemoglobin is not None else None
            ),
            "cholesterol": (
                float(self.cholesterol) if self.cholesterol is not None else None
            ),
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Patient id={self.id} full_name={self.full_name!r}>"