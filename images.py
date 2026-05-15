import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de estilo y exportación
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
sns.set_theme(style="whitegrid")

# Crear carpeta de salida
OUTPUT_DIR = "high_res_exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- CONFIGURACIÓN GLOBAL ---
CAT_TRANS = {
    "Antropogénico": "Anthropogenic", "Mamífero": "Mammal", 
    "Anfibio": "Amphibian", "Insecto": "Insect", "Ave": "Bird"
}
PERIOD_TRANS = {
    "Amanecer Crítico": "Dawn", "Anochecer Crítico": "Dusk"
}
COLORS_STACK = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"]

def save_high_res(fig, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    fig.savefig(path, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close(fig)
    print(f"✅ Guardado: {path}")

# --- CARGA DE DATOS ---
df_24h = pd.read_csv('data_24h_combined_seasons.csv')
df_iph = pd.read_csv('ip categorico seasonal.csv')
df_fta = pd.read_csv('data_fta.csv')
df_risk = pd.read_csv('data_bubble.csv')

# Preprocesamiento IPH
df_iph['comunidad'] = df_iph['comunidad'].str.upper()
df_iph['categoria'] = df_iph['categoria'].map(CAT_TRANS).fillna(df_iph['categoria'])
df_iph['periodo_analisis'] = df_iph['periodo_analisis'].map(PERIOD_TRANS).fillna(df_iph['periodo_analisis'])

# --- 1. GENERACIÓN DE RELEVO 24H (Iterativo por localidad/año/estación) ---
print("Generando gráficos de Relevo 24h...")
for (loc, year), group in df_24h.groupby(['localidad', 'anio']):
    seasons = set(group['estacion'].unique().tolist() + group['ciclo_hidrologico'].unique().tolist())
    
    for season in seasons:
        f_24h = group[(group['estacion'] == season) | (group['ciclo_hidrologico'] == season)]
        if f_24h.empty: continue
        
        f_24h_grouped = f_24h.groupby(['hora_dia', 'primary_category'])['promedio_clips_hora'].mean().reset_index()
        pivot_24h = f_24h_grouped.pivot(index='hora_dia', columns='primary_category', values='promedio_clips_hora').fillna(0)
        
        cats_order = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"]
        pivot_24h = pivot_24h[[c for c in cats_order if c in pivot_24h.columns]]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.stackplot(pivot_24h.index, pivot_24h.T, labels=pivot_24h.columns, colors=COLORS_STACK)
        ax.set_title(f"Acoustic Composition: {loc} ({season} {year})", fontweight='bold')
        ax.set_xlim(0, 23); ax.set_xticks(range(24))
        ax.set_ylabel("Avg Clips per Hour")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Category")
        
        save_high_res(fig, f"24h_{loc}_{year}_{season}".replace(" ", "_"))

# --- 2. GENERACIÓN DE IPH (Periodos Críticos) ---
print("Generando comparativas IPH...")
for (year, season), data_s in df_iph.groupby(['anio', 'estacion']):
    fig, (ax_dawn, ax_dusk) = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
    
    for i, (period, ax) in enumerate(zip(['Dawn', 'Dusk'], [ax_dawn, ax_dusk])):
        data_p = data_s[data_s['periodo_analisis'] == period]
        if data_p.empty: continue

        sns.barplot(data=data_p, x='categoria', y='porcentaje_promedio', hue='comunidad', palette="viridis", ax=ax)
        
        # Anotaciones de Min-Max
        for patch, (_, row) in zip([p for p in ax.patches if p.get_height() > 0], data_p.iterrows()):
            x_center = patch.get_x() + patch.get_width()/2
            ax.text(x_center, row['porcentaje_promedio'] + 1, f"[{row['porcentaje_min']}-{row['porcentaje_max']}]", 
                    ha='center', va='bottom', fontsize=7, rotation=90)

        ax.set_title(f"{period} ({season} {year})", fontsize=14, fontweight='bold')
        ax.set_ylabel("% Occupation" if i==0 else "")
        if i == 1: ax.legend(title="Community", bbox_to_anchor=(1.05, 1))
        else: ax.get_legend().remove()

    save_high_res(fig, f"IPH_{year}_{season}".replace(" ", "_"))

# --- 3. GENERACIÓN DE FTA (Heatmap) ---
print("Generando Heatmap de Tala...")
pivot_fta = df_fta.pivot(index='localidad', columns='hora_del_dia', values='pct_fta').fillna(0)
fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot_fta, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': '% FTA'}, ax=ax)
ax.set_title("Hourly Logging Intensity Heatmap (All Localities)", fontweight='bold', fontsize=16)
save_high_res(fig, "FTA_Heatmap_Global")

# --- 4. MAPA DE RIESGO (Anual e Integral) ---
print("Generando Mapas de Riesgo...")

def plot_risk_scatter(data, ax, title):
    scatter = ax.scatter(data['ISAHI_pct'], data['IAM_pct'], s=data['ISAHI_pct']*50, alpha=0.6, 
                         c=data['IAM_pct'], cmap='viridis', edgecolors="black", linewidth=0.5)
    for _, row in data.iterrows():
        ax.annotate(row['Locality'], (row['ISAHI_pct'], row['IAM_pct']), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontweight='bold', fontsize=8)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('ISAHI %'); ax.set_ylabel('IAM %')
    ax.set_xlim(0, 75); ax.set_ylim(0, 55)
    ax.axhline(y=20, color='grey', linestyle='--', alpha=0.3)
    ax.axvline(x=25, color='grey', linestyle='--', alpha=0.3)
    return scatter

# Individual por año
for year, y_df in df_risk.groupby('Year'):
    fig, ax = plt.subplots(figsize=(11, 8))
    sc = plot_risk_scatter(y_df, ax, f"Epidemiological Risk Map - {year}")
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('IAM % (Mosquito Activity Intensity)', rotation=270, labelpad=15)
    save_high_res(fig, f"Risk_Map_{year}")

# Grid Completo
years = sorted(df_risk['Year'].unique())
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes_flat = axes.flatten()
sc_last = None
for i, year in enumerate(years):
    if i < 4:
        sc_last = plot_risk_scatter(df_risk[df_risk['Year'] == year], axes_flat[i], f"Year {year}")

fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
cbar = fig.colorbar(sc_last, cax=cbar_ax)
cbar.set_label('IAM % (Mosquito Activity Intensity)', rotation=270, labelpad=15)

plt.tight_layout()
save_high_res(fig, "Risk_Map_Grid_Comparison")

print("\n🚀 ¡Proceso finalizado! Todas las imágenes están en la carpeta:", OUTPUT_DIR)