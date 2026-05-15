import sqlite3
import pandas as pd

def export_data_seasonal_combined(db_path):
    conn = sqlite3.connect(db_path)
    
    localidades = ["12 DE ABRIL", "PAUJIL", "QUISTOCOCHA", "SAN LUCAS", "VARILLAL"]
    localidades_str = '("' + '", "'.join(localidades) + '")'
    
    translation = {
        "Antropogénico": "Anthropogenic", "Mamífero": "Mammal",
        "Anfibio": "Amphibian", "Insecto": "Insect", "Ave": "Bird"
    }

    # Query con Estaciones Astronómicas Y Ciclos Hidrológicos
    query = f"""
    WITH clips_categorizados AS (
        SELECT 
            localidad,
            fecha,
            hora,
            primary_category,
            CAST(strftime('%Y', fecha) AS INT) AS anio,
            -- Estaciones Astronómicas
            CASE 
                WHEN strftime('%m', fecha) IN ('12', '01', '02') THEN 'Summer'
                WHEN strftime('%m', fecha) IN ('03', '04', '05') THEN 'Autumn'
                WHEN strftime('%m', fecha) IN ('06', '07', '08') THEN 'Winter'
                WHEN strftime('%m', fecha) IN ('09', '10', '11') THEN 'Spring'
            END AS estacion,
            -- Ciclos Hidrológicos
            CASE 
                WHEN strftime('%m', fecha) BETWEEN '06' AND '10' THEN 'Vaciante'
                ELSE 'Creciente'
            END AS ciclo_hidrologico
        FROM clips
        WHERE status != 'ruido_extremo'
          AND primary_category NOT IN ('Silencio', 'Ruido ambiental')
          AND localidad IN {localidades_str}
    ),
    esfuerzo AS (
        -- El esfuerzo debe calcularse por la combinación de ambas categorías
        SELECT localidad, anio, estacion, ciclo_hidrologico, COUNT(DISTINCT fecha) as dias_muestreados
        FROM clips_categorizados
        GROUP BY 1, 2, 3, 4
    )
    SELECT 
        c.localidad, 
        c.anio, 
        c.estacion,
        c.ciclo_hidrologico,
        CAST(strftime('%H', c.hora) AS INT) AS hora_dia,
        c.primary_category,
        ROUND(CAST(COUNT(*) AS FLOAT) / e.dias_muestreados, 2) AS promedio_clips_hora
    FROM clips_categorizados c
    JOIN esfuerzo e ON 
        c.localidad = e.localidad AND 
        c.anio = e.anio AND 
        c.estacion = e.estacion AND
        c.ciclo_hidrologico = e.ciclo_hidrologico
    GROUP BY 1, 2, 3, 4, 5, 6
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Aplicar traducción y limpieza
    df['primary_category'] = df['primary_category'].map(translation)
    df = df.dropna(subset=['primary_category'])
    
    df.to_csv('data_24h_combined_seasons.csv', index=False)
    conn.close()
    print("CSV 'data_24h_combined_seasons.csv' generado con éxito.")

if __name__ == "__main__":
    export_data_seasonal_combined(r'E:\audiomoth_2_discos - copia (2).sqlite')