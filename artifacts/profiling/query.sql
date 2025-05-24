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
            SUM(fit_gf.t) AS sum_fit_gf
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
            SUM(rmh.t) AS sum_rmh
        FROM
            removeHitsAndRefit AS rmh
            JOIN fitAndStore AS fas ON fas.id = rmh.fitAndStore
        GROUP BY
            event_id
    )
/*
- left join event and CTEs for fitGFRaveVertex and removeHitsAndRefit durations
- compute percentage of total event duration calls to the functions took
*/
SELECT
    event.id,
    event.t,
    COALESCE(t1.sum_fit_gf, 0) / event.t * 100 AS fit_gf_percentage,
    COALESCE(t2.sum_rmh, 0) / event.t * 100 AS rmh_percentage
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

-- 
WITH 
    fitAndStore AS (
        SELECT 
            fas.event,
            SUM(fas.t)
        FROM fitAndStore as fas
        GROUP BY fas.event
    )
,   vertexFit AS (
        SELECT 
            vf.fitAndStore,
            SUM(vf.t)
        FROM vertexFit as vf
        GROUP BY vf.fitAndStore
    )
,   fitGFRaveVertex AS (
        SELECT 
            fgv.vertexFit,
            SUM(fgv.t)
        FROM fitGFRaveVertex as fgv
        GROUP BY fgv.vertexFit
    )
, 
    
,   t0 AS (
        SELECT 
            e.id AS event_id,
            e.t AS t_event,
            IFNULL(fas.t, 0) AS t_fitAndStore,
            IFNULL(vf.t, 0) AS t_vertexFit,
            IFNULL(frv.t, 0) AS t_fitGFRaveVertex,
            IFNULL(rmh.t, 0) AS t_removeHitsAndRefit
        FROM event AS e
        LEFT JOIN fitAndStore AS fas ON fas.event = e.id
        LEFT JOIN vertexFit AS vf ON vf.fitAndStore = fas.id
        LEFT JOIN fitGFRaveVertex AS frv ON frv.vertexFit = vf.id
        LEFT JOIN removeHitsAndRefit AS rmh ON rmh.fitAndStore = fas.id
        ORDER BY e.id
    )
,   t1 AS (
        SELECT 
            event_id,
            t_event,
            SUM(t_fitAndStore) AS t_fitAndStore,
            SUM(t_vertexFit) AS t_vertexFit,
            SUM(t_fitGFRaveVertex) AS t_fitGFRaveVertex,
            SUM(t_removeHitsAndRefit) AS t_removeHitsAndRefit
        FROM t0
        GROUP BY event_id
    )
SELECT * FROM t1;