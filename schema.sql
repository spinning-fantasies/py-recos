-- Schema for the 'locations' table
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

-- Schema for the 'activities' table
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    date DATE,
    time TIME,
    location_id INTEGER,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Sample data for initial display
INSERT INTO locations (name, latitude, longitude) VALUES
    ('Paris', 48.856614, 2.3522219),
    ('Morlaix', 48.577613, -3.828228),
    ('Montpellier', 43.610769, 3.876716);

INSERT INTO activities (name, description, date, time, location_id) VALUES
    ("Promenade au parc", "Profitez d'une agréable promenade en plein air", '2023-07-28', '15:00', 1),
    ("Visite du musée", "Découvrez l'histoire et l'art au musée", '2023-07-29', '10:30', 2),
    ("Dîner au restaurant", "Délicieux repas dans un cadre agréable", '2023-07-29', '19:00', 3);
