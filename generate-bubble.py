import sqlite3
import pandas as pd

def export_bubble_data(db_path):
    conn = sqlite3.connect(db_path)
    
    query_isahi = """
    WITH flags_por_clip AS (
        SELECT 
            UPPER(localidad) AS loc_clean,
            UniqueAudioKey,
            CAST(strftime('%Y', fecha) AS INT) AS anio,
            primary_category,
            yamnet_label_1, yamnet_label_2, clip_dbfs,
            CASE WHEN LOWER(primary_category) = 'antropogénico' THEN 1 ELSE 0 END AS es_humano,
            CASE WHEN LOWER(primary_category) = 'insecto' THEN 1 ELSE 0 END AS es_insecto,
            CASE WHEN LOWER(yamnet_label_1) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'motor', 'blender')
                   OR LOWER(yamnet_label_2) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'motor', 'blender')
            THEN 1 ELSE 0 END AS es_tala,
            CASE WHEN (primary_category = 'Insecto' OR yamnet_label_1 = 'Insect') AND clip_dbfs > -40 THEN 1 ELSE 0 END AS es_mosquito
        FROM clips
        WHERE status != 'ruido_extremo' 
          AND UPPER(localidad) IN ('12 DE ABRIL', 'PAUJIL', 'QUISTOCOCHA', 'SAN LUCAS', 'VARILLAL')
          AND CAST(strftime('%Y', fecha) AS INT) BETWEEN 2023 AND 2026
    ),
    superposicion AS (
        SELECT loc_clean, anio, UniqueAudioKey,
               CASE WHEN MAX(es_humano) = 1 AND MAX(es_insecto) = 1 THEN 1 ELSE 0 END AS coincidencia_hv
        FROM flags_por_clip GROUP BY 1, 2, 3
    ),
    stats_p AS (
        SELECT loc_clean, anio, CAST(SUM(coincidencia_hv) AS FLOAT) / COUNT(*) AS isahi_p
        FROM superposicion GROUP BY 1, 2
    )
    SELECT 
        f.anio AS Year,
        f.loc_clean AS Locality,
        ROUND(SUM(f.es_mosquito) * 100.0 / COUNT(*), 2) AS IAM_pct,
        ROUND(s.isahi_p * 100.0, 2) AS ISAHI_pct,
        ROUND(SUM(f.es_tala) * 100.0 / COUNT(*), 2) AS FTA_pct,
        COUNT(*) AS Total_Clips  -- <--- Esta columna es la que pediste
    FROM flags_por_clip f
    JOIN stats_p s ON f.loc_clean = s.loc_clean AND f.anio = s.anio
    GROUP BY 1, 2;
    """
    
    df_bubble = pd.read_sql_query(query_isahi, conn)
    df_bubble.to_csv('data_bubble.csv', index=False)
    conn.close()
    print("CSV 'data_bubble.csv' generado con éxito.")

if __name__ == "__main__":
    export_bubble_data(r'E:\audiomoth_2_discos - copia (2).sqlite')