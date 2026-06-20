-- MySQL 8.0 CE compatible schema
-- No CHECK(... CURDATE() ...) constraints used; future-DOB validation is enforced in Flask (validators.py)

CREATE DATABASE IF NOT EXISTS health_prediction_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE health_prediction_db;

CREATE TABLE IF NOT EXISTS patients (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    full_name       VARCHAR(150)   NOT NULL,
    date_of_birth   DATE           NOT NULL,
    email           VARCHAR(150)   NOT NULL,
    glucose         DECIMAL(6,2)   NOT NULL,
    haemoglobin     DECIMAL(6,2)   NOT NULL,
    cholesterol     DECIMAL(6,2)   NOT NULL,
    remarks         VARCHAR(255)   NULL,
    created_at      DATETIME       DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT uq_patients_email UNIQUE (email),
    CONSTRAINT chk_glucose_numeric CHECK (glucose >= 0),
    CONSTRAINT chk_haemoglobin_numeric CHECK (haemoglobin >= 0),
    CONSTRAINT chk_cholesterol_numeric CHECK (cholesterol >= 0)
) ENGINE=InnoDB;

CREATE INDEX idx_patients_full_name ON patients (full_name);