-- ============================================================
-- vaccination_db  |  Analytical Views
-- These pre-aggregate metrics so Power BI / Streamlit stay fast.
-- ============================================================
USE vaccination_db;

-- Page 1: KPI cards + world map
CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    c.iso_3_code, c.country_name, c.who_region,
    AVG(cd.coverage) AS avg_coverage,
    COUNT(DISTINCT cd.antigen) AS total_antigens
FROM coverage_data cd
JOIN countries c ON c.iso_3_code = cd.code
GROUP BY c.iso_3_code, c.country_name, c.who_region;

-- Page 2: Coverage vs Incidence scatter
CREATE OR REPLACE VIEW vw_coverage_vs_incidence AS
SELECT
    c.country_name AS name, c.who_region,
    AVG(cd.coverage) AS avg_coverage_pct,
    AVG(ir.incidence_rate) AS avg_incidence_rate
FROM coverage_data cd
JOIN countries c  ON c.iso_3_code = cd.code
JOIN incidence_rate ir ON ir.code = cd.code
GROUP BY c.country_name, c.who_region;

-- Page 3 / 7: Country drill-down + raw coverage
CREATE OR REPLACE VIEW vw_coverage_summary AS
SELECT code AS name, antigen, year, AVG(coverage) AS avg_coverage
FROM coverage_data
GROUP BY code, antigen, year;

-- Page 4: Risk & Gaps (single-dose-round high priority vaccines)
CREATE OR REPLACE VIEW vw_high_risk_schedule AS
SELECT country_name, vaccine_description, who_region, schedule_rounds
FROM vaccine_schedule
WHERE schedule_rounds = 1;

-- Page 5 / 9: Disease case + incidence trends
CREATE OR REPLACE VIEW vw_cases_summary AS
SELECT year, disease, AVG(cases) AS avg_cases
FROM reported_cases
GROUP BY year, disease;

CREATE OR REPLACE VIEW vw_incidence_summary AS
SELECT c.who_region, ir.disease, AVG(ir.incidence_rate) AS avg_incidence_rate
FROM incidence_rate ir
JOIN countries c ON c.iso_3_code = ir.code
GROUP BY c.who_region, ir.disease;

-- Page 6 / 8: Introduction timeline + 2030 measles target
CREATE OR REPLACE VIEW vw_intro_timeline AS
SELECT year, who_region, COUNT(*) AS vaccines_introduced
FROM vaccine_introduction
WHERE introduced = 1
GROUP BY year, who_region;

CREATE OR REPLACE VIEW vw_measles_2030 AS
SELECT year, AVG(coverage) AS measles_coverage_pct,
       95 - AVG(coverage) AS gap_to_95pct_target
FROM coverage_data
WHERE antigen = 'MCV1'
GROUP BY year;
