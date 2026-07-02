-- ============================================================
-- vaccination_db  |  Schema Definition
-- Matches the database already built in MySQL Workbench.
-- Run this only if you need to (re)create the DB from scratch.
-- ============================================================

CREATE DATABASE IF NOT EXISTS vaccination_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE vaccination_db;

-- ---------- Reference dimension ----------
CREATE TABLE IF NOT EXISTS countries (
    iso_3_code   VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(150) NOT NULL,
    who_region   VARCHAR(10)
);

-- ---------- Fact: vaccination coverage ----------
CREATE TABLE IF NOT EXISTS coverage_data (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    `group`             VARCHAR(50),
    code                VARCHAR(10),
    name                VARCHAR(150),
    year                SMALLINT,
    antigen             VARCHAR(30),
    antigen_description VARCHAR(150),
    coverage_category   VARCHAR(30),
    target_number       BIGINT,
    doses               BIGINT,
    coverage            DECIMAL(5,2),
    FOREIGN KEY (code) REFERENCES countries(iso_3_code),
    INDEX idx_cov_year (year),
    INDEX idx_cov_antigen (antigen)
);

-- ---------- Fact: disease incidence rate ----------
CREATE TABLE IF NOT EXISTS incidence_rate (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    `group`             VARCHAR(50),
    code                VARCHAR(10),
    name                VARCHAR(150),
    year                SMALLINT,
    disease             VARCHAR(30),
    disease_description VARCHAR(150),
    denominator         VARCHAR(100),
    incidence_rate      DECIMAL(10,2),
    FOREIGN KEY (code) REFERENCES countries(iso_3_code),
    INDEX idx_inc_year (year),
    INDEX idx_inc_disease (disease)
);

-- ---------- Fact: reported cases ----------
CREATE TABLE IF NOT EXISTS reported_cases (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    `group`             VARCHAR(50),
    code                VARCHAR(10),
    name                VARCHAR(150),
    year                SMALLINT,
    disease             VARCHAR(30),
    disease_description VARCHAR(150),
    cases               BIGINT,
    FOREIGN KEY (code) REFERENCES countries(iso_3_code),
    INDEX idx_rep_year (year),
    INDEX idx_rep_disease (disease)
);

-- ---------- Fact: vaccine introduction ----------
CREATE TABLE IF NOT EXISTS vaccine_introduction (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    iso_3_code   VARCHAR(10),
    country_name VARCHAR(150),
    who_region   VARCHAR(10),
    year         SMALLINT,
    description  VARCHAR(150),
    intro        VARCHAR(5),
    introduced   TINYINT(1),
    FOREIGN KEY (iso_3_code) REFERENCES countries(iso_3_code),
    INDEX idx_int_year (year)
);

-- ---------- Fact: vaccine schedule ----------
CREATE TABLE IF NOT EXISTS vaccine_schedule (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    iso_3_code            VARCHAR(10),
    country_name          VARCHAR(150),
    who_region            VARCHAR(10),
    year                  SMALLINT,
    vaccine_code          VARCHAR(30),
    vaccine_description   VARCHAR(150),
    schedule_rounds       DECIMAL(4,1),
    target_pop            VARCHAR(50),
    target_pop_description VARCHAR(150),
    geoarea               VARCHAR(100),
    age_administered       VARCHAR(100),
    FOREIGN KEY (iso_3_code) REFERENCES countries(iso_3_code),
    INDEX idx_sch_year (year)
);
