import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "healtrip.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            emergency_available INTEGER NOT NULL,
            specialties TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            hospital_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            languages TEXT NOT NULL,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
        );
        """
    )

    hospitals = [
        (
            1,
            "Riyadh Care Hospital",
            "Riyadh",
            1,
            "Cardiology, Emergency Medicine, Internal Medicine",
        ),
        (
            2,
            "Kingdom Medical Center",
            "Riyadh",
            1,
            "Cardiology, Neurology, Internal Medicine",
        ),
        (
            3,
            "Al Noor Medical Hospital",
            "Riyadh",
            0,
            "Cardiology, Orthopedics, Dermatology",
        ),
        (
            4,
            "North Riyadh Specialist Hospital",
            "Riyadh",
            1,
            "Cardiology, Internal Medicine, Pulmonology",
        ),
    ]

    doctors = [
        (
            1,
            "Dr. Ahmed Hassan",
            "Cardiology",
            1,
            "Riyadh",
            "Arabic, English",
        ),
        (
            2,
            "Dr. Sara Khalid",
            "Cardiology",
            2,
            "Riyadh",
            "Arabic, English",
        ),
        (
            3,
            "Dr. Omar Ali",
            "Internal Medicine",
            2,
            "Riyadh",
            "Arabic, English",
        ),
        (
            4,
            "Dr. Lina Mohammed",
            "Cardiology",
            3,
            "Riyadh",
            "Arabic, English",
        ),
        (
            5,
            "Dr. Faisal Nasser",
            "Pulmonology",
            4,
            "Riyadh",
            "Arabic, English",
        ),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO hospitals
        (id, name, city, emergency_available, specialties)
        VALUES (?, ?, ?, ?, ?)
        """,
        hospitals,
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO doctors
        (id, name, specialty, hospital_id, city, languages)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        doctors,
    )

    connection.commit()
    connection.close()


def search_doctors(specialty=None, city="Riyadh"):
    connection = get_connection()

    query = """
        SELECT
            doctors.name,
            doctors.specialty,
            doctors.city,
            doctors.languages,
            hospitals.name AS hospital
        FROM doctors
        JOIN hospitals
            ON doctors.hospital_id = hospitals.id
        WHERE 1 = 1
    """

    parameters = []

    if specialty:
        query += " AND LOWER(doctors.specialty) LIKE LOWER(?)"
        parameters.append(f"%{specialty}%")

    if city:
        query += " AND LOWER(doctors.city) = LOWER(?)"
        parameters.append(city)

    query += " ORDER BY doctors.name"

    rows = connection.execute(query, parameters).fetchall()
    connection.close()

    return [dict(row) for row in rows]


def search_hospitals(city="Riyadh", specialty=None, emergency_only=False):
    connection = get_connection()

    query = """
        SELECT
            id,
            name,
            city,
            emergency_available,
            specialties
        FROM hospitals
        WHERE 1 = 1
    """

    parameters = []

    if city:
        query += " AND LOWER(city) = LOWER(?)"
        parameters.append(city)

    if specialty:
        query += " AND LOWER(specialties) LIKE LOWER(?)"
        parameters.append(f"%{specialty}%")

    if emergency_only:
        query += " AND emergency_available = 1"

    query += " ORDER BY name"

    rows = connection.execute(query, parameters).fetchall()
    connection.close()

    return [dict(row) for row in rows]
