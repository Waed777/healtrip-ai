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
            country TEXT NOT NULL,
            emergency_available INTEGER NOT NULL,
            specialties TEXT NOT NULL,
            demo_data INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            hospital_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            languages TEXT NOT NULL,
            demo_data INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
        );
        """
    )

    hospitals = [
        (
            1,
            "Riyadh Care Hospital",
            "Riyadh",
            "Saudi Arabia",
            1,
            "Cardiology, Emergency Medicine, Internal Medicine",
            1,
        ),
        (
            2,
            "Kingdom Medical Center",
            "Riyadh",
            "Saudi Arabia",
            1,
            "Cardiology, Neurology, Internal Medicine",
            1,
        ),
        (
            3,
            "Al Noor Medical Hospital",
            "Riyadh",
            "Saudi Arabia",
            0,
            "Cardiology, Orthopedics, Dermatology",
            1,
        ),
        (
            4,
            "North Riyadh Specialist Hospital",
            "Riyadh",
            "Saudi Arabia",
            1,
            "Cardiology, Internal Medicine, Pulmonology",
            1,
        ),
        (
            5,
            "Jeddah Medical Center",
            "Jeddah",
            "Saudi Arabia",
            1,
            "Cardiology, Pediatrics, Internal Medicine",
            1,
        ),
    ]

    doctors = [
        (
            1,
            "Dr. Ahmed Hassan",
            "Cardiology",
            1,
            "Riyadh",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
        (
            2,
            "Dr. Sara Khalid",
            "Cardiology",
            2,
            "Riyadh",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
        (
            3,
            "Dr. Omar Ali",
            "Internal Medicine",
            2,
            "Riyadh",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
        (
            4,
            "Dr. Lina Mohammed",
            "Cardiology",
            3,
            "Riyadh",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
        (
            5,
            "Dr. Faisal Nasser",
            "Pulmonology",
            4,
            "Riyadh",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
        (
            6,
            "Dr. Noor Abdullah",
            "Cardiology",
            5,
            "Jeddah",
            "Saudi Arabia",
            "Arabic, English",
            1,
        ),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO hospitals
        (
            id,
            name,
            city,
            country,
            emergency_available,
            specialties,
            demo_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        hospitals,
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO doctors
        (
            id,
            name,
            specialty,
            hospital_id,
            city,
            country,
            languages,
            demo_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        doctors,
    )

    connection.commit()
    connection.close()


def search_doctors(
    specialty=None,
    city=None,
):

    connection = get_connection()

    query = """
        SELECT
            doctors.id,
            doctors.name,
            doctors.specialty,
            doctors.city,
            doctors.country,
            doctors.languages,
            hospitals.name AS hospital
        FROM doctors
        JOIN hospitals
            ON doctors.hospital_id = hospitals.id
        WHERE 1 = 1
    """

    parameters = []

    if specialty:
        query += """
            AND LOWER(doctors.specialty)
            LIKE LOWER(?)
        """
        parameters.append(f"%{specialty}%")

    if city:
        query += """
            AND LOWER(doctors.city)
            LIKE LOWER(?)
        """
        parameters.append(f"%{city}%")

    query += """
        ORDER BY doctors.name
    """

    rows = connection.execute(
        query,
        parameters,
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def search_hospitals(
    city=None,
    specialty=None,
    emergency_only=False,
):

    connection = get_connection()

    query = """
        SELECT
            id,
            name,
            city,
            country,
            emergency_available,
            specialties
        FROM hospitals
        WHERE 1 = 1
    """

    parameters = []

    if city:
        query += """
            AND LOWER(city)
            LIKE LOWER(?)
        """
        parameters.append(f"%{city}%")

    if specialty:
        query += """
            AND LOWER(specialties)
            LIKE LOWER(?)
        """
        parameters.append(f"%{specialty}%")

    if emergency_only:
        query += """
            AND emergency_available = 1
        """

    query += """
        ORDER BY name
    """

    rows = connection.execute(
        query,
        parameters,
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_all_doctors():
    return search_doctors()


def get_all_hospitals():
    return search_hospitals()
