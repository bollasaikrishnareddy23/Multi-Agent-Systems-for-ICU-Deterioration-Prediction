-- 02_create_features_bigquery.sql
-- Purpose:
-- Create first-24-hour features for the 3-agent ICU deterioration project.
--
-- This version uses MIMIC-IV derived tables.
-- If `physionet-data.mimiciv_derived` is unavailable in your BigQuery project,
-- build the derived tables from the official MIMIC Code Repository first.
--
-- Replace `your_project.your_dataset` with your own project and dataset.

CREATE OR REPLACE TABLE `your_project.your_dataset.features_24h_3_agents` AS

WITH cohort AS (
    SELECT *
    FROM `your_project.your_dataset.cohort_icu_24h`
),

-- Vital signs from first 24 hours.
vitals AS (
    SELECT
        c.stay_id,

        MAX(v.heart_rate) AS heart_rate_max_24h,
        MIN(v.mbp) AS map_min_24h,
        MIN(v.sbp) AS sbp_min_24h,
        MAX(v.resp_rate) AS resp_rate_max_24h,
        MIN(v.spo2) AS spo2_min_24h,
        MAX(v.temperature) AS temperature_max_24h,
        MIN(v.temperature) AS temperature_min_24h

    FROM cohort c
    LEFT JOIN `physionet-data.mimiciv_derived.vitalsign` v
        ON c.stay_id = v.stay_id
       AND v.charttime >= c.intime
       AND v.charttime < DATETIME_ADD(c.intime, INTERVAL 24 HOUR)
    GROUP BY c.stay_id
),

-- Kidney labs from first 24 hours.
kidney_labs AS (
    SELECT
        c.stay_id,

        MAX(ch.creatinine) AS creatinine_max_24h,
        MAX(ch.bun) AS bun_max_24h,

        ARRAY_AGG(ch.creatinine IGNORE NULLS ORDER BY ch.charttime ASC LIMIT 1)[SAFE_OFFSET(0)]
            AS creatinine_first_24h,

        ARRAY_AGG(ch.creatinine IGNORE NULLS ORDER BY ch.charttime DESC LIMIT 1)[SAFE_OFFSET(0)]
            AS creatinine_last_24h

    FROM cohort c
    LEFT JOIN `physionet-data.mimiciv_derived.chemistry` ch
        ON c.subject_id = ch.subject_id
       AND c.hadm_id = ch.hadm_id
       AND ch.charttime >= c.intime
       AND ch.charttime < DATETIME_ADD(c.intime, INTERVAL 24 HOUR)
    GROUP BY c.stay_id
),

-- Urine output from first 24 hours.
urine AS (
    SELECT
        c.stay_id,
        SUM(uo.urineoutput) AS urine_output_24h
    FROM cohort c
    LEFT JOIN `physionet-data.mimiciv_derived.urine_output` uo
        ON c.stay_id = uo.stay_id
       AND uo.charttime >= c.intime
       AND uo.charttime < DATETIME_ADD(c.intime, INTERVAL 24 HOUR)
    GROUP BY c.stay_id
),

-- Ventilation from first 24 hours.
vent AS (
    SELECT
        c.stay_id,

        MAX(
            CASE
                WHEN LOWER(v.ventilation_status) LIKE '%invasive%' THEN 1
                ELSE 0
            END
        ) AS mechanical_ventilation_flag_24h,

        MAX(
            CASE
                WHEN v.ventilation_status IS NOT NULL THEN 1
                ELSE 0
            END
        ) AS oxygen_support_flag_24h

    FROM cohort c
    LEFT JOIN `physionet-data.mimiciv_derived.ventilation` v
        ON c.stay_id = v.stay_id
       AND v.starttime < DATETIME_ADD(c.intime, INTERVAL 24 HOUR)
       AND v.endtime >= c.intime
    GROUP BY c.stay_id
),

-- FiO2 and PEEP are often charted variables.
-- Depending on your derived setup, these may be available in respiratory/ventilator concepts.
-- Here we leave placeholders as NULL. You can fill them later using chartevents or respiratory derived tables.
vent_settings AS (
    SELECT
        c.stay_id,
        CAST(NULL AS FLOAT64) AS fio2_max_24h,
        CAST(NULL AS FLOAT64) AS peep_max_24h
    FROM cohort c
),

features AS (
    SELECT
        c.subject_id,
        c.hadm_id,
        c.stay_id,
        c.anchor_age,
        c.gender,
        c.race,
        c.hospital_expire_flag,

        k.creatinine_max_24h,
        k.creatinine_first_24h,
        k.creatinine_last_24h,
        (k.creatinine_last_24h - k.creatinine_first_24h) AS creatinine_trend_24h,
        k.bun_max_24h,

        u.urine_output_24h,

        -- Dialysis is a placeholder. Add dialysis/RRT concept table later if needed.
        0 AS dialysis_flag_24h,

        vi.heart_rate_max_24h,
        vi.map_min_24h,
        vi.sbp_min_24h,
        vi.resp_rate_max_24h,
        vi.spo2_min_24h,
        vi.temperature_max_24h,
        vi.temperature_min_24h,

        ve.mechanical_ventilation_flag_24h,
        ve.oxygen_support_flag_24h,
        vs.fio2_max_24h,
        vs.peep_max_24h

    FROM cohort c
    LEFT JOIN vitals vi
        ON c.stay_id = vi.stay_id
    LEFT JOIN kidney_labs k
        ON c.stay_id = k.stay_id
    LEFT JOIN urine u
        ON c.stay_id = u.stay_id
    LEFT JOIN vent ve
        ON c.stay_id = ve.stay_id
    LEFT JOIN vent_settings vs
        ON c.stay_id = vs.stay_id
)

SELECT *
FROM features;
