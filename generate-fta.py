import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import math

def export_fta_data(db_path):
    conn = sqlite3.connect(db_path)
    
    localidades = ["12 DE ABRIL", "PAUJIL", "QUISTOCOCHA", "SAN LUCAS", "VARILLAL"]
    localidades_str = '("' + '", "'.join(localidades) + '")'

    query_fta = f"""
    WITH clips_base AS (
        SELECT 
            localidad,
            fecha,
            CAST(strftime('%Y', fecha) AS INT) AS anio,
            CAST(strftime('%H', hora) AS INT) AS hora_num,
            CASE 
                WHEN strftime('%m', fecha) BETWEEN '06' AND '10' THEN 'Vaciante'
                ELSE 'Creciente'
            END AS ciclo_hidrologico,
            CASE 
                WHEN LOWER(yamnet_label_1) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'electric toothbrush', 'motor', 'light engine (high frequency)', 'electric shaver, electric razor', 'blender')
                  OR LOWER(yamnet_label_2) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'electric toothbrush', 'motor', 'light engine (high frequency)', 'electric shaver, electric razor', 'blender')
                  OR LOWER(yamnet_label_3) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'electric toothbrush', 'motor', 'light engine (high frequency)', 'electric shaver, electric razor', 'blender')
                  OR LOWER(yamnet_label_4) IN ('chainsaw', 'saw', 'power tool', 'circular saw', 'mechanical fan', 'engine', 'idling', 'mechanisms', 'electric toothbrush', 'motor', 'light engine (high frequency)', 'electric shaver, electric razor', 'blender')
                THEN 1 ELSE 0 
            END AS es_tala
        FROM clips
        WHERE status != 'ruido_extremo'
          AND localidad IN {localidades_str}
    )
    SELECT 
        ciclo_hidrologico,
        anio,
        localidad,
        hora_num AS hora_del_dia,
        ROUND(CAST(SUM(es_tala) AS FLOAT) * 100 / COUNT(*), 4) AS pct_fta
    FROM clips_base
    GROUP BY 1, 2, 3, 4
    ORDER BY 1, 2, 3, 4;
    """
    
    df_fta = pd.read_sql_query(query_fta, conn)
    conn.close()

    if not os.path.exists('output_fta'):
        os.makedirs('output_fta')
    df_fta.to_csv('output_fta/data_fta.csv', index=False, encoding='utf-8-sig')

    # Generar Heatmap Grid por Ciclo
    for ciclo in df_fta['ciclo_hidrologico'].unique():
        df_ciclo = df_fta[df_fta['ciclo_hidrologico'] == ciclo]
        anios = sorted(df_ciclo['anio'].unique())
        
        n_cols = 3
        n_rows = math.ceil(len(anios) / n_cols)
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows), squeeze=False)
        axes_flat = axes.flatten()

        for i, anio in enumerate(anios):
            ax = axes_flat[i]
            df_year = df_ciclo[df_ciclo['anio'] == anio]
            pivot_fta = df_year.pivot(index='localidad', columns='hora_del_dia', values='pct_fta').fillna(0)
            
            sns.heatmap(pivot_fta, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, cbar_kws={'label': '% FTA'})
            ax.set_title(f"Year: {anio}", fontsize=12, fontweight='bold')
            ax.set_xlabel("Hour")
            ax.set_ylabel("Community")

        # Hide empty subplots
        for j in range(i + 1, len(axes_flat)):
            axes_flat[j].axis('off')
        
        fig.suptitle(f"Logging Activity (FTA) History - {ciclo}", fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'output_fta/grid_fta_{ciclo.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()

    print("CSV and Heatmaps generated in 'output_fta' folder.")

if __name__ == "__main__":
    export_fta_data(r'E:\audiomoth_2_discos - copia (2).sqlite')