import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

def plot_risk_scatter(data, ax, title):
    """
    Generates a bubble chart where:
    X-axis: ISAHI % (Human-Insect Intersection)
    Y-axis: IAM % (Mosquito Activity)
    Bubble size: ISAHI %
    """
    # Bubble size is based on ISAHI_pct
    scatter = ax.scatter(data['ISAHI_pct'], data['IAM_pct'], s=data['ISAHI_pct']*60, 
                         alpha=0.6, c=data['IAM_pct'], cmap='viridis', edgecolors="w", linewidth=1.2)
    
    for _, row in data.iterrows():
        ax.annotate(row['Locality'], (row['ISAHI_pct'], row['IAM_pct']), textcoords="offset points", 
                    xytext=(0, 12), ha='center', fontweight='bold', fontsize=7)
    
    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.set_xlabel('ISAHI % (Interaction)', fontsize=9)
    ax.set_ylabel('IAM % (Mosquito Activity)', fontsize=9)
    
    # Risk thresholds
    ax.axhline(y=20, color='grey', linestyle='--', alpha=0.3)
    ax.axvline(x=25, color='grey', linestyle='--', alpha=0.3)
    
    # Limits and quadrant labels
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 60)
    ax.text(2, 57, 'HIGH VECTOR', color='#d62728', fontsize=7, fontweight='bold')
    ax.text(50, 57, 'HIGH RISK ZONE', color='#8c564b', fontsize=7, fontweight='bold')

def export_seasonal_risk_data(db_path):
    conn = sqlite3.connect(db_path)
    
    # SQL Query incorporating the Hydrological Cycle (Vaciante/Creciente)
    query_isahi = """
    WITH flags_per_clip AS (
        SELECT 
            UPPER(localidad) AS loc_clean,
            UniqueAudioKey,
            CAST(strftime('%Y', fecha) AS INT) AS anio,
            CASE 
                WHEN strftime('%m', fecha) BETWEEN '06' AND '10' THEN 'Low Water (Vaciante)'
                ELSE 'High Water (Creciente)'
            END AS hydro_cycle,
            primary_category,
            yamnet_label_1, yamnet_label_2, clip_dbfs,
            CASE WHEN LOWER(primary_category) = 'antropogénico' THEN 1 ELSE 0 END AS is_human,
            CASE WHEN LOWER(primary_category) = 'insecto' THEN 1 ELSE 0 END AS is_insect,
            CASE WHEN (primary_category = 'Insecto' OR yamnet_label_1 = 'Insect') AND clip_dbfs > -40 THEN 1 ELSE 0 END AS is_mosquito
        FROM clips
        WHERE status != 'ruido_extremo' 
          AND UPPER(localidad) IN ('12 DE ABRIL', 'PAUJIL', 'QUISTOCOCHA', 'SAN LUCAS', 'VARILLAL')
          AND CAST(strftime('%Y', fecha) AS INT) BETWEEN 2023 AND 2026
    ),
    overlap_calc AS (
        SELECT loc_clean, anio, hydro_cycle, UniqueAudioKey,
               CASE WHEN MAX(is_human) = 1 AND MAX(is_insect) = 1 THEN 1 ELSE 0 END AS isahi_event
        FROM flags_per_clip GROUP BY 1, 2, 3, 4
    ),
    isahi_stats AS (
        SELECT 
            loc_clean, anio, hydro_cycle,
            AVG(isahi_event) * 100.0 AS isahi_avg,
            -- Standard deviation of a Bernoulli distribution: sqrt(p * (1-p))
            SQRT(AVG(isahi_event) * (1 - AVG(isahi_event))) * 100.0 AS isahi_sd
        FROM overlap_calc
        GROUP BY 1, 2, 3
    )
    SELECT 
        f.anio AS Year,
        f.hydro_cycle AS Season,
        f.loc_clean AS Locality,
        ROUND(SUM(f.is_mosquito) * 100.0 / COUNT(*), 2) AS IAM_pct,
        ROUND(AVG(f.is_mosquito) * 100.0, 2) AS IAM_avg,
        ROUND(SQRT(AVG(f.is_mosquito) * (1 - AVG(f.is_mosquito))) * 100.0, 2) AS IAM_sd,
        ROUND(MIN(f.is_mosquito) * 100.0, 2) AS IAM_min,
        ROUND(MAX(f.is_mosquito) * 100.0, 2) AS IAM_max,
        ROUND(s.isahi_avg, 2) AS ISAHI_pct,
        ROUND(s.isahi_sd, 2) AS ISAHI_sd,
        COUNT(*) AS Total_Clips
    FROM flags_per_clip f
    JOIN isahi_stats s ON f.loc_clean = s.loc_clean AND f.anio = s.anio AND f.hydro_cycle = s.hydro_cycle
    GROUP BY 1, 2, 3;
    """
    
    print("Executing query and processing data...")
    df_risk = pd.read_sql_query(query_isahi, conn)
    df_risk.to_csv('seasonal_risk_data.csv', index=False)
    conn.close()

    # --- PLOT GENERATION ---
    output_dir = 'seasonal_risk_maps'
    os.makedirs(output_dir, exist_ok=True)
    
    seasons = df_risk['Season'].unique()
    
    for season in seasons:
        df_season = df_risk[df_risk['Season'] == season]
        years = sorted(df_season['Year'].unique())
        
        # Determine grid size
        n_years = len(years)
        n_cols = 2
        n_rows = math.ceil(n_years / n_cols)
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 6 * n_rows), squeeze=False)
        axes_flat = axes.flatten()
        
        for i, year in enumerate(years):
            y_df = df_season[df_season['Year'] == year]
            plot_risk_scatter(y_df, axes_flat[i], f"Risk Map: {year} ({season})")
            
        # Remove empty subplots
        for j in range(i + 1, len(axes_flat)):
            fig.delaxes(axes_flat[j])
            
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        season_filename = season.lower().replace(' ', '_').replace('(', '').replace(')', '')
        output_path = os.path.join(output_dir, f'risk_grid_{season_filename}.png')
        
        plt.suptitle(f"Ecological Risk Assessment - {season.upper()}", fontsize=16, fontweight='bold')
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Generated grid for {season}: {output_path}")

    print("\nProcess finished. Data saved to 'seasonal_risk_data.csv'.")

if __name__ == "__main__":
    # Ensure the path to your database is correct
    DB_PATH = r'E:\audiomoth_2_discos - copia (2).sqlite'
    if os.path.exists(DB_PATH):
        export_seasonal_risk_data(DB_PATH)
    else:
        print(f"Error: Database not found at {DB_PATH}")