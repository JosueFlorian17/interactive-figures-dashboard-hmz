import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

def export_and_plot_all_periods(db_path):
    conn = sqlite3.connect(db_path)
    
    localidades = ["12 DE ABRIL", "PAUJIL", "QUISTOCOCHA", "SAN LUCAS", "VARILLAL"]
    localidades_str = '("' + '", "'.join(localidades) + '")'
    
    translation = {
        "Antropogénico": "Anthropogenic", "Mamífero": "Mammal",
        "Anfibio": "Amphibian", "Insecto": "Insect", "Ave": "Bird"
    }
    cycle_trans = {"Creciente": "Rainy Season", "Vaciante": "Dry Season"}
    colors = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"]
    cats_order = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"]

    if not os.path.exists('output_relevo'):
        os.makedirs('output_relevo')

    # 1. SQL con lógica de Temporada Unificada (Creciente Nov-May / Vaciante Jun-Oct)
    query = f"""
    WITH clips_base AS (
        SELECT 
            localidad, fecha, hora, primary_category,
            CAST(strftime('%Y', fecha) AS INT) AS anio,
            CAST(strftime('%m', fecha) AS INT) AS mes,
            CASE 
                WHEN strftime('%m', fecha) BETWEEN '06' AND '10' THEN 'Vaciante'
                ELSE 'Creciente'
            END AS ciclo_hidrologico
        FROM clips
        WHERE status != 'ruido_extremo'
          AND primary_category NOT IN ('Silencio', 'Ruido ambiental')
          AND localidad IN {localidades_str}
    ),
    clips_temporada AS (
        SELECT *,
               -- Si es Creciente en meses 01-05, pertenece a la temporada iniciada el año anterior
               CASE 
                   WHEN ciclo_hidrologico = 'Creciente' AND mes <= 5 THEN anio - 1
                   ELSE anio 
               END AS temporada_base
        FROM clips_base
    ),
    esfuerzo AS (
        SELECT localidad, ciclo_hidrologico, temporada_base, COUNT(DISTINCT fecha) as dias_muestreados
        FROM clips_temporada
        GROUP BY 1, 2, 3
    )
    SELECT 
        c.localidad, c.ciclo_hidrologico, c.temporada_base,
        CAST(strftime('%H', c.hora) AS INT) AS hora_dia,
        c.primary_category,
        ROUND(CAST(COUNT(*) AS FLOAT) / e.dias_muestreados, 2) AS promedio_clips_hora
    FROM clips_temporada c
    JOIN esfuerzo e ON c.localidad = e.localidad 
                    AND c.ciclo_hidrologico = e.ciclo_hidrologico 
                    AND c.temporada_base = e.temporada_base
    GROUP BY 1, 2, 3, 4, 5
    """
    
    df = pd.read_sql_query(query, conn)
    df['primary_category'] = df['primary_category'].map(translation)
    df = df.dropna(subset=['primary_category'])
    
    # Save the processed data to a CSV
    df.to_csv('output_relevo/relevo_data.csv', index=False, encoding='utf-8-sig')
    conn.close()

    # 2. Generación de imágenes por comunidad y ciclo hidrológico
    for loc in df['localidad'].unique():
        for ciclo in df['ciclo_hidrologico'].unique():
            data_sub = df[(df['localidad'] == loc) & (df['ciclo_hidrologico'] == ciclo)].copy()
            if data_sub.empty: continue

            # Crear etiquetas únicas para cada periodo
            data_sub['label'] = data_sub.apply(
                lambda x: f"{cycle_trans[x['ciclo_hidrologico']]} {x['temporada_base']}" if x['ciclo_hidrologico'] == 'Vaciante'
                else f"{cycle_trans[x['ciclo_hidrologico']]} {x['temporada_base']}-{str(x['temporada_base']+1)[2:]}", axis=1
            )
            
            periodos = sorted(data_sub['label'].unique())
            n_periods = len(periodos)
            n_cols = 3
            n_rows = math.ceil(n_periods / n_cols)
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 4 * n_rows), squeeze=False)
            axes_flat = axes.flatten()
            
            for i, p_label in enumerate(periodos):
                ax = axes_flat[i]
                df_p = data_sub[data_sub['label'] == p_label]
                pivot = df_p.pivot(index='hora_dia', columns='primary_category', values='promedio_clips_hora').fillna(0)
                pivot = pivot[[c for c in cats_order if c in pivot.columns]]

                # Calculate percentages for labels
                row_sums = pivot.sum(axis=1)
                pivot_perc = pivot.div(row_sums, axis=0) * 100
                
                ax.stackplot(pivot.index, pivot.T, labels=pivot.columns, colors=colors[:len(pivot.columns)], alpha=0.8)

                # Add labels to the peaks of each category
                for col in pivot.columns:
                    peak_hour = pivot[col].idxmax()
                    peak_perc = pivot_perc.loc[peak_hour, col]
                    if pivot[col].max() > 0:
                        ax.text(peak_hour, pivot.loc[peak_hour, col], f'{peak_perc:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

                ax.set_title(p_label, fontsize=10, loc='left', fontweight='bold')
                ax.set_xlim(0, 23); ax.set_xticks([0, 6, 12, 18, 23])
                ax.set_xlabel("Hour of Day")
                ax.set_ylabel("Avg Clips")
                ax.grid(axis='x', linestyle='--', alpha=0.3)

            for j in range(i + 1, len(axes_flat)):
                axes_flat[j].axis('off')

            fig.suptitle(f"{cycle_trans[ciclo]} History: {loc}", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            filename = f"relevo_{loc.replace(' ', '_').lower()}_{ciclo.lower()}.png"
            plt.savefig(f"output_relevo/{filename}", dpi=300, bbox_inches='tight')
            plt.close()

    print("Process finished. Images saved in 'output_relevo' folder.")

if __name__ == "__main__":
    export_and_plot_all_periods(r'E:\audiomoth_2_discos - copia (2).sqlite')