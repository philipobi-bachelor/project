-- compute runtime percentage of event caused by fitGFRaveVertex and removeHitsAndRefit

-- create two CTEs (temporary result tables) for processing
WITH
    /*  
    - (inner) join fitGFRaveVertex, vertexFit and fitAndStore tables together
    - group by event_id and sum fitGFRaveVertex duration of group
    */
    t1 AS (
        SELECT
            fas.event AS event_id,
            SUM(fit_gf.duration) AS sum_fit_gf
        FROM
            fitGFRaveVertex AS fit_gf
            JOIN vertexFit AS vf ON vf.id = fit_gf.vertexFit
            JOIN fitAndStore AS fas ON fas.id = vf.fitAndStore
        GROUP BY
            event_id
    ),
    /*
    - (inner) join removeHitsAndRefit and fitAndStore together
    - group by event_id and sum removeHitsAndRefit duration of group
    */
    t2 AS (
        SELECT
            fas.event AS event_id,
            SUM(rmh.duration) AS sum_rmh
        FROM
            removeHitsAndRefit AS rmh
            JOIN fitAndStore AS fas ON fas.id = rmh.fitAndStore
        GROUP BY
            fas.event
    )
/*
- left join event and CTEs for fitGFRaveVertex and removeHitsAndRefit durations
- compute percentage of total event duration calls to the functions took
*/
SELECT
    event.id,
    event.duration,
    COALESCE(t1.sum_fit_gf, 0) / event.duration * 100 AS fit_gf_percentage,
    COALESCE(t2.sum_rmh, 0) / event.duration * 100 AS rmh_percentage
FROM
    event
    LEFT JOIN t1 ON t1.event_id = event.id
    LEFT JOIN t2 ON t2.event_id = event.id
ORDER BY
    event.id;

/* Averages:
fit_gf_percentage   rmh_percentage
62.8540435566334   5.754463973079
*/

