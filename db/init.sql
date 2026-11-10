-- Kharkiv Donor Center Database Initialization Script
-- Automatic schema setup and initial reference data

CREATE SCHEMA IF NOT EXISTS data_blood;
CREATE SCHEMA IF NOT EXISTS donor;
CREATE SCHEMA IF NOT EXISTS number_telephone;
CREATE SCHEMA IF NOT EXISTS admin;

-- 1. data_blood schema
CREATE TABLE IF NOT EXISTS data_blood.city (
    "ID" INT PRIMARY KEY,
    "city_name" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.region (
    "ID" INT PRIMARY KEY,
    "region_name" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.street (
    "ID" INT PRIMARY KEY,
    "street_name" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.area (
    "ID" INT PRIMARY KEY,
    "area_name" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.address (
    "ID" INT PRIMARY KEY,
    "region_ID" INT REFERENCES data_blood.region("ID"),
    "city_ID" INT REFERENCES data_blood.city("ID"),
    "area_ID" INT REFERENCES data_blood.area("ID"),
    "street_ID" INT REFERENCES data_blood.street("ID"),
    "house_number" INT NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.clinic (
    "ID" INT PRIMARY KEY,
    "clinic_name" VARCHAR(255) NOT NULL,
    "address_ID" INT REFERENCES data_blood.address("ID"),
    "working_hours" VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.blood_and_components (
    "ID" INT PRIMARY KEY,
    "blood_and_comp_name" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.status_appointment (
    "ID" INT PRIMARY KEY,
    "name_status" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS data_blood.clinic_has_blood_and_comp (
    "blood_and_comp_ID" INT REFERENCES data_blood.blood_and_components("ID"),
    "clinic_ID" INT REFERENCES data_blood.clinic("ID"),
    "kol" INT DEFAULT 0,
    PRIMARY KEY ("blood_and_comp_ID", "clinic_ID")
);

-- 2. donor schema
CREATE TABLE IF NOT EXISTS donor.gender (
    "ID" INT PRIMARY KEY,
    "gender_name" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS donor.language (
    "ID" INT PRIMARY KEY,
    "lang_name" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS donor.donor (
    "ID" INT PRIMARY KEY,
    "name_donor" VARCHAR(255),
    "surname_donor" VARCHAR(255),
    "date_of_birth" VARCHAR(50),
    "gender_ID" INT REFERENCES donor.gender("ID"),
    "email" VARCHAR(255),
    "telegram_ID" BIGINT UNIQUE,
    "password" VARCHAR(255),
    "language_ID" INT REFERENCES donor.language("ID")
);

-- 3. number_telephone schema
CREATE TABLE IF NOT EXISTS number_telephone.donor_number (
    "ID" INT PRIMARY KEY,
    "donor_ID" INT REFERENCES donor.donor("ID") ON DELETE CASCADE,
    "number" VARCHAR(50) NOT NULL
);

-- 4. data_blood appointments and reviews
CREATE TABLE IF NOT EXISTS data_blood.appointment (
    "ID" INT PRIMARY KEY,
    "clinic_ID" INT REFERENCES data_blood.clinic("ID"),
    "donor_number_ID" INT REFERENCES number_telephone.donor_number("ID") ON DELETE CASCADE,
    "status_ID" INT REFERENCES data_blood.status_appointment("ID"),
    "registration_date" VARCHAR(50),
    "appointment_date" VARCHAR(50),
    "analysis_file_path" VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS data_blood.reviews (
    "ID" INT PRIMARY KEY,
    "donor_ID" INT REFERENCES donor.donor("ID"),
    "clinic_ID" INT REFERENCES data_blood.clinic("ID"),
    "rating" INT NOT NULL,
    "comment" TEXT,
    "date_added" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. admin schema
CREATE TABLE IF NOT EXISTS admin.admin (
    "ID" INT PRIMARY KEY,
    "name_admin" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "clinic_ID" INT REFERENCES data_blood.clinic("ID")
);

CREATE TABLE IF NOT EXISTS admin.waiting_feed_back (
    "ID" SERIAL PRIMARY KEY,
    "status_ID" INT,
    "donor_number_ID" INT REFERENCES number_telephone.donor_number("ID"),
    "note" TEXT
);

-- Reference Data Seeds (matching config.py definitions)
INSERT INTO data_blood.city ("ID", "city_name") VALUES
    (1, 'Odessa'), (2, 'Kiyv'), (3, 'Lviv'), (4, 'Kharkiv')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.region ("ID", "region_name") VALUES
    (1, 'Odessa'), (2, 'Kyiv'), (3, 'Lviv'), (4, 'Kharkiv')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.street ("ID", "street_name") VALUES
    (1, 'Klochkivska'), (2, 'Pushkin''s')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.area ("ID", "area_name") VALUES
    (1, 'Shevchenkivskyi'), (2, 'Kyivіkyi')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID", "house_number") VALUES
    (1, 1, 1, 1, 1, 366),
    (2, 2, 2, 2, 2, 24)
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.clinic ("ID", "clinic_name", "address_ID", "working_hours") VALUES
    (1, 'Odesa Center #1', 1, '8:00:00'),
    (2, 'Kiyv Center #1'' mall', 2, '9:00:00')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.blood_and_components ("ID", "blood_and_comp_name") VALUES
    (1, 'AB+'), (2, 'AB-'), (3, 'A+'), (4, 'A-'),
    (5, 'B+'), (6, 'B-'), (7, 'O+'), (8, 'O-')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO data_blood.status_appointment ("ID", "name_status") VALUES
    (1, 'Success'), (2, 'Unsuccess'), (3, 'Waiting')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO donor.gender ("ID", "gender_name") VALUES
    (1, 'MALE'), (2, 'FEMALE'), (3, 'OTHER'), (4, 'NODATA')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO donor.language ("ID", "lang_name") VALUES
    (1, 'cn-CN'), (2, 'de-DE'), (3, 'en-EN'),
    (4, 'fr-FR'), (5, 'ru-RU'), (6, 'uk-UK')
ON CONFLICT ("ID") DO NOTHING;

INSERT INTO admin.admin ("ID", "name_admin", "password", "clinic_ID") VALUES
    (1, 'SuperAdminC1', 'qwerty', 1),
    (2, 'SuperAdminC2', 'qwerty', 2)
ON CONFLICT ("ID") DO NOTHING;
