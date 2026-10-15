-- 01_create_cohort_bigquery.sql
-- Purpose:
-- Create adult first-ICU-stay cohort with at least 24 hours in ICU.
--
-- BigQuery output:
-- Replace `your_project.your_dataset.cohort_icu_24h` with your own destination table.

CREATE OR REPLACE TABLE `your_project.your_dataset.cohort_icu_24h` AS

WITH first_icu AS (
    SELECT
        icu.subject_id,
        icu.hadm_id,
        icu.stay_id,
        icu.intime,
        icu.outtime,
        DATETIME_DIFF(icu.outtime, icu.intime, HOUR) AS icu_los_hours,
        ROW_NUMBER() OVER (
            PARTITION BY icu.subject_id
            ORDER BY icu.intime
        ) AS rn
    FROM `physionet-data.mimiciv_v3_1_icu.icustays` icu
),

cohort AS (
    SELECT
        f.subject_id,
        f.hadm_id,
        f.stay_id,
        f.intime,
        f.outtime,
        f.icu_los_hours,
        p.anchor_age,
        p.gender,
        a.race,
        a.hospital_expire_flag
    FROM first_icu f
    JOIN `physionet-data.mimiciv_v3_1_hosp.patients` p
        ON f.subject_id = p.subject_id
    JOIN `physionet-data.mimiciv_v3_1_hosp.admissions` a
        ON f.hadm_id = a.hadm_id
    WHERE f.rn = 1
      AND p.anchor_age >= 18
      AND f.icu_los_hours >= 24
)

SELECT *
FROM cohort;
