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
    is_deleted INTEGER DEFAULT 0,  -- New column for soft deletion
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Sample data for initial display
INSERT INTO locations (name, latitude, longitude) VALUES
    ('Brest', 48.390394, -4.486076),
    ('Grenoble', 45.188529, 5.724524), 
    ('Lannion', 48.732084, -3.459144),
    ('Montpellier', 43.610769, 3.876716),
    ('Morlaix', 48.577613, -3.828228),
    ('Nantes', 47.218371, -1.553621),
    ('Paris', 48.856614, 2.3522219),
    ('Quimper', 47.997542, -4.097899),
    ('Rennes', 48.117266, -1.6777926);

INSERT INTO activities (name, description, date, time, location_id) VALUES
    ("boire un café à La Virgule ", "Profitez d'un cadre agréable et tranquille", '2023-07-28', '12:00', 4),
    ("goûter le kouignaman de chez Traon ", "Découvrez la pâtisserie la plus célèbre de Bretagne", '2023-07-29', '09:30', 4),
    ("prendre un Rooibos au SEW", "À partir de 17 du jeudi au dimanche", '2023-07-29', '17:00', 4);
