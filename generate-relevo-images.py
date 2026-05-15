import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_community_plots(db_path):
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    
    # 1. Obtener lista de localidades únicas
    localidades_query = """
        SELECT DISTINCT localidad FROM clips 
        WHERE localidad IN ("12 DE ABRIL", "PAUJIL", "QUISTOCOCHA", "SAN LUCAS", "VARILLAL")
    """
    localidades = pd.read_sql_query(localidades_query, conn)['localidad'].tolist()
    
    # Crear carpeta para los resultados si no existe
    if not os.path.exists('output_plots'):
        os.makedirs('output_plots')

    # Diccionario de traducción para los gráficos
    translation = {
        "Antropogénico": "Anthropogenic",
        "Mamífero": "Mammal",
        "Anfibio": "Amphibian",
        "Insecto": "Insect",
        "Ave": "Bird"
    }
    
    # Orden de las capas (de abajo hacia arriba) y colores
    categories_order = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"]
    colors = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"]

    print(f"Starting plot generation for {len(localidades)} communities...")

    for loc in localidades:
        # 2. Query adaptada para iterar por localidad
        # Eliminamos el filtro fijo de '12 DE ABRIL' y usamos un placeholder
        query = f"""
        WITH dias_muestreados AS (
            SELECT localidad, COUNT(DISTINCT fecha) as total_dias
            FROM clips
            WHERE localidad = ?
            GROUP BY localidad
        )
        SELECT 
            c.localidad,
            CAST(strftime('%H', c.hora) AS INT) AS hora_dia,
            c.primary_category,
            ROUND(CAST(COUNT(*) AS FLOAT) / d.total_dias, 2) AS promedio_clips_hora
        FROM clips c
        JOIN dias_muestreados d ON c.localidad = d.localidad
        WHERE c.status != 'ruido_extremo'
          AND c.primary_category NOT IN ('Silencio', 'Ruido ambiental')
          AND c.localidad = ?
        GROUP BY 1, 2, 3
        ORDER BY hora_dia ASC;
        """
        
        df = pd.read_sql_query(query, conn, params=(loc, loc))
        
        if df.empty:
            print(f"Skipping {loc}: No data found.")
            continue

        # 3. Procesamiento de datos
        df['primary_category'] = df['primary_category'].map(translation)
        
        # Pivotar para el stackplot
        pivot_df = df.pivot(index='hora_dia', columns='primary_category', values='promedio_clips_hora').fillna(0)
        
        # Asegurar que todas las columnas existan para evitar errores si falta una categoría
        for cat in categories_order:
            if cat not in pivot_df.columns:
                pivot_df[cat] = 0
        
        pivot_df = pivot_df[categories_order]

        # 4. Generar el gráfico
        plt.figure(figsize=(12, 6))
        sns.set_theme(style="whitegrid", rc={"grid.alpha": 0.3})
        
        plt.stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns, colors=colors)
        
        plt.title(f'Average Activity 24h - Location: {loc}', fontsize=14, fontweight='bold')
        plt.xlabel('Hour of the day', fontsize=11)
        plt.ylabel('Average Detected Clips', fontsize=11)
        plt.xticks(range(0, 24))
        plt.xlim(0, 23)
        plt.legend(title='Category', loc='upper left', frameon=True, fontsize='small')
        
        # Guardar el archivo (limpiamos el nombre de la localidad por seguridad)
        clean_name = loc.replace(" ", "_").lower()
        plt.savefig(f'output_plots/plot_{clean_name}.png', dpi=300)
        plt.close() # Cerrar para liberar memoria
        
        print(f"Successfully generated: {loc}")

    conn.close()
    print("\nProcess finished. Check the 'output_plots' folder.")

# Ejecutar el script
if __name__ == "__main__":
    # Cambia 'sqlite.db' por el nombre real de tu archivo
    generate_community_plots(r'E:\audiomoth_2_discos.sqlite')