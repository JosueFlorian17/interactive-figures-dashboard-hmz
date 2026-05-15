import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

st.set_page_config(page_title="AudioMoth Biodiversity Dashboard", layout="wide")

# --- TRADUCCIONES Y PALETAS GLOBALES ---
CAT_TRANS = {
    "Antropogénico": "Anthropogenic", "Mamífero": "Mammal", 
    "Anfibio": "Amphibian", "Insecto": "Insect", "Ave": "Bird"
}
PERIOD_TRANS = {
    "Amanecer Crítico": "Dawn", "Anochecer Crítico": "Dusk"
}
COLORS_STACK = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"]

# --- CARGA DE DATOS ---
@st.cache_data
def load_all_data():
    # 1. Relevo 24h Estacional
    df_24h = pd.read_csv('data_24h_combined_seasons.csv')
    
    # 2. IPH Estacional (Nuevo archivo)
    with open(r'C:\Users\Florian\Documents\innovalab\graficas\ip-final-final.json', 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    df_iph = pd.DataFrame(data_json['rows'])
    
    df_iph['comunidad'] = df_iph['comunidad'].str.upper()
    df_iph['categoria'] = df_iph['categoria'].map(CAT_TRANS).fillna(df_iph['categoria'])
    df_iph['periodo_analisis'] = df_iph['periodo_analisis'].map(PERIOD_TRANS).fillna(df_iph['periodo_analisis'])
    
    # Filter only Vaciante and Creciente for all dataframes
    target_cycles = ["Vaciante", "Creciente"]
    df_24h = df_24h[df_24h['ciclo_hidrologico'].isin(target_cycles)]
    
    # Filter out 2022 data from IPH
    year_col = 'anio' if 'anio' in df_iph.columns else 'temporada_base'
    df_iph = df_iph[df_iph[year_col] != 2022]

    # Filter specific communities for IPH
    allowed_coms = ["SAN LUCAS", "PAUJIL", "VARILLAL", "12 DE ABRIL", "QUISTOCOCHA"]
    df_iph = df_iph[df_iph['comunidad'].isin(allowed_coms)]
    
    # 3. FTA (Logging)
    df_fta = pd.read_csv('output_fta/data_fta.csv')
    df_fta = df_fta[df_fta['ciclo_hidrologico'].isin(target_cycles)]
    
    # 4. Mapa de Riesgo (Burbujas)
    df_risk = pd.read_csv(r'C:\Users\Florian\Documents\innovalab\graficas\seasonal_risk_data.csv')
    
    return df_24h, df_iph, df_fta, df_risk

# Inicialización
try:
    df_24h, df_iph, df_fta, df_risk = load_all_data()
except FileNotFoundError as e:
    st.error(f"Missing file: {e.filename}. Please run the extraction scripts first.")
    st.stop()

st.title("AudioMoth Acoustic Monitoring Dashboard - Iquitos")

# --- SECCIÓN 1: RELEVO DIARIO (24H COMPOSITION) ---
st.header("1. Hourly Activity Composition (Seasonal)")
st.info("Analyze how acoustic composition changes by hour, year, and season.")

with st.expander("View Index Formulas: Activity Indices"):
    st.markdown("<div style='font-size: 1.1em;'>", unsafe_allow_html=True)
    st.markdown("""
    These indices evaluate the relative intensity of specific biological or anthropogenic sound classes over a 24-hour cycle.
    *   **BAI (Bird Activity Index):** $BAI = \\frac{n_{\\text{birds}}}{n_{\\text{total}}} \\times 100$
    *   **IAI (Insect Activity Index):** $IAI = \\frac{n_{\\text{mosquitoes}}}{n_{\\text{total}}} \\times 100$
    *   **AmAI (Amphibian Activity Index):** $AmAI = \\frac{n_{\\text{amphibians}}}{n_{\\text{total}}} \\times 100$
    *   **MAI (Mammal Activity Index):** $MAI = \\frac{n_{\\text{mammals}}}{n_{\\text{total}}} \\times 100$
    *   **AAI (Anthropogenic Activity Index):** $AAI = \\frac{n_{\\text{anthro}}}{n_{\\text{total}}} \\times 100$
    """)
    st.markdown("</div>", unsafe_allow_html=True)

col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    loc_24h = st.selectbox("Select Community:", df_24h['localidad'].unique(), key="loc_24h")
with col_a2:
    year_24h = st.selectbox("Select Year:", sorted(df_24h[df_24h['localidad'] == loc_24h]['anio'].unique()), key="year_24h")
with col_a3:
    available_cycles = df_24h[(df_24h['localidad'] == loc_24h) & (df_24h['anio'] == year_24h)]['ciclo_hidrologico'].unique().tolist()
    combined_filter = st.selectbox("Select Cycle:", sorted(available_cycles), key="combined_filter")

grid_full = st.checkbox("Show All Communities across Years (Grid View)", key="grid_full")

def plot_24h_stack(data, ax, title):
    f_24h_grouped = data.groupby(['hora_dia', 'primary_category'])['promedio_clips_hora'].mean().reset_index()
    pivot_24h = f_24h_grouped.pivot(index='hora_dia', columns='primary_category', values='promedio_clips_hora').fillna(0)
    cats_order = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"]
    cols = [c for c in cats_order if c in pivot_24h.columns]
    pivot_24h = pivot_24h[cols]
    ax.stackplot(pivot_24h.index, pivot_24h.T, labels=pivot_24h.columns, colors=COLORS_STACK)
    ax.set_title(title, fontweight='bold', fontsize=10)
    
    # Add peak percentage labels for each category
    for i, col in enumerate(pivot_24h.columns):
        peak_val = pivot_24h[col].max()
        peak_hour = pivot_24h[col].idxmax()
        ax.text(peak_hour, peak_val, f"{peak_val:.1f}", color='black', fontsize=8, fontweight='bold', ha='center', va='bottom')

    ax.set_xlim(0, 23); ax.set_xticks([0, 6, 12, 18, 23])

if grid_full:
    all_locs = sorted(df_24h['localidad'].unique())
    all_years = sorted(df_24h['anio'].unique())
    target_cycles = ["Vaciante", "Creciente"]
    
    for loc in all_locs:
        st.subheader(f"Community: {loc}")
        # Create a row for each hydrological cycle
        for cycle in target_cycles:
            st.write(f"**Cycle: {cycle}**")
            fig1, axes = plt.subplots(1, len(all_years), figsize=(18, 3.5), sharey=True)
            if len(all_years) == 1: axes = [axes]
            
            for i, y in enumerate(all_years):
                data_cell = df_24h[(df_24h['localidad'] == loc) & (df_24h['anio'] == y) & 
                                   (df_24h['ciclo_hidrologico'] == cycle)]
                if not data_cell.empty:
                    plot_24h_stack(data_cell, axes[i], f"{y}")
                else:
                    axes[i].set_title(f"{y} (No Data)")
            plt.tight_layout()
            st.pyplot(fig1)
else:
    f_24h = df_24h[(df_24h['localidad'] == loc_24h) & (df_24h['anio'] == year_24h) & (df_24h['ciclo_hidrologico'] == combined_filter)]
    if not f_24h.empty:
        fig1, ax1 = plt.subplots(figsize=(12, 4))
        plot_24h_stack(f_24h, ax1, f"{loc_24h} ({combined_filter} {year_24h})")
        ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Category")
        st.pyplot(fig1)

st.divider()

# --- SECCIÓN 2: IPH (PERIODOS CRÍTICOS ESTACIONAL) ---
st.header("2. Critical Periods Comparison (IP Seasonal)")
st.info("Comparison of relative acoustic occupation during Dawn/Dusk across seasons.")

with st.expander("View Index Formulas: Penetration Indices (PI)"):
    st.markdown("<div style='font-size: 1.1em;'>", unsafe_allow_html=True)
    st.markdown("""
    Penetration Indices quantify the acoustic footprint of specific sound domains during critical bioacoustic windows ($T_{\\text{crit}}$) such as Dawn or Dusk.
    $$\\text{PI} = \\frac{1}{|T_{\\text{crit}}|} \\sum P(\\text{group})_i$$
    *   **BPI (Bird Penetration Index):** Average bird sound presence index across critical times.
    *   **IPI (Insect Penetration Index):** Average insect sound presence index across critical times.
    *   **AmPI (Amphibian Penetration Index):** Average amphibian sound presence index across critical times.
    *   **MPI (Mammal Penetration Index):** Average mammal sound presence index across critical times.
    *   **HPI (Human Penetration Index):** Average human sound footprint across critical times.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

col_b1, col_b2 = st.columns(2)
with col_b1:
    year_col = 'anio' if 'anio' in df_iph.columns else 'temporada_base'
    year_iph = st.selectbox("Filter by Year:", sorted(df_iph[year_col].unique()), key="year_iph")
with col_b2:
    season_col = 'estacion' if 'estacion' in df_iph.columns else 'ciclo_hidrologico'
    available_iph_cycles = [c for c in df_iph[df_iph[year_col] == year_iph][season_col].unique() if c in ["Vaciante", "Creciente"]]
    season_iph = st.selectbox("Filter by Cycle:", available_iph_cycles, key="seas_iph")

grid_iph = st.checkbox("Grid View (All Years for selected Cycle)", key="grid_iph")
selected_coms = st.multiselect("Select Communities to compare:",
                               options=sorted(df_iph['comunidad'].unique()), 
                               default=sorted(df_iph['comunidad'].unique())[:4])

def plot_iph_bars(data, season_name, year_val):
    fig, (ax_dawn, ax_dusk) = plt.subplots(1, 2, figsize=(16, 5), sharey=True)
    for i, (period, ax) in enumerate(zip(['Dawn', 'Dusk'], [ax_dawn, ax_dusk])):
        data_p = data[data['periodo_analisis'] == period]
        if data_p.empty:
            ax.text(0.5, 0.5, f"No data for {period}", ha='center')
            continue
        sns.barplot(data=data_p, x='categoria', y='porcentaje_promedio', hue='comunidad', palette="viridis", ax=ax)
        for patch, (_, row) in zip([p for p in ax.patches if p.get_height() > 0], data_p.iterrows()):
            x_center = patch.get_x() + patch.get_width()/2
            ax.text(x_center, row['porcentaje_promedio'] + 1, f"[{row['porcentaje_min']}-{row['porcentaje_max']}]", ha='center', va='bottom', fontsize=8, rotation=90)
        ax.set_title(f"{period} ({season_name} {year_val})", fontsize=12, fontweight='bold')
        if i == 1: ax.legend(title="Community", bbox_to_anchor=(1.05, 1), loc='upper left')
        else: ax.get_legend().remove()
    return fig

if grid_iph:
    years_iph = sorted(df_iph[year_col].unique())
    for y in years_iph:
        data_y = df_iph[(df_iph['comunidad'].isin(selected_coms)) & (df_iph[year_col] == y) & (df_iph[season_col] == season_iph)]
        if not data_y.empty:
            st.pyplot(plot_iph_bars(data_y, season_iph, y))
else:
    f_iph = df_iph[(df_iph['comunidad'].isin(selected_coms)) & (df_iph[year_col] == year_iph) & (df_iph[season_col] == season_iph)]
    if not f_iph.empty:
        st.pyplot(plot_iph_bars(f_iph, season_iph, year_iph))
    else:
        st.warning("No IPH data for the selected combination.")

st.divider()

# --- SECCIÓN 3: FTA (HEATMAP DE TALA) ---
st.header("3. Acoustic Logging Frequency (ALF)")

with st.expander("View Index Formula: ALF"):
    st.markdown("<div style='font-size: 1.1em;'>", unsafe_allow_html=True)
    st.markdown("""
    **ALF (Acoustic Logging Frequency):** Represents the percentage of temporal presence of heavy machinery or chainsaw noises within a designated tracking delta window.
    $$ALF = \\frac{\\sum \\mathbb{1}_{\\text{chainsaws}}}{\\Delta T} \\times 100$$
    Where $\\mathbb{1}_{\\text{chainsaws}}$ is an indicator function tracking the explicit presence of environmental logging profiles within interval subdivisions.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    year_fta = st.selectbox("Select Year:", sorted(df_fta['anio'].unique(), reverse=True), key="year_fta")
with col_c2:
    cycle_fta = st.selectbox("Select Cycle:", df_fta[df_fta['anio'] == year_fta]['ciclo_hidrologico'].unique(), key="cycle_fta")
with col_c3:
    fta_coms = st.multiselect("Select communities:", 
                              options=sorted(df_fta['localidad'].unique()), 
                              default=sorted(df_fta['localidad'].unique())[:3], key="coms_fta")
grid_fta = st.checkbox("Grid View (All Years for selected Cycle)", key="grid_fta")

def plot_fta_heatmap(data, ax, title):
    pivot_fta = data.pivot(index='localidad', columns='hora_del_dia', values='pct_fta').fillna(0)
    sns.heatmap(pivot_fta, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': '% FTA'}, ax=ax)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Community")

if grid_fta:
    years_fta = sorted(df_fta['anio'].unique(), reverse=True)
    for y in years_fta:
        data_y = df_fta[(df_fta['localidad'].isin(fta_coms)) & (df_fta['anio'] == y) & (df_fta['ciclo_hidrologico'] == cycle_fta)]
        if not data_y.empty:
            fig3, ax3 = plt.subplots(figsize=(12, 4))
            plot_fta_heatmap(data_y, ax3, f"Logging Intensity - Year {y} ({cycle_fta})")
            st.pyplot(fig3)
        else:
            st.write(f"No data for Year {y}")
else:
    f_fta = df_fta[(df_fta['localidad'].isin(fta_coms)) & (df_fta['anio'] == year_fta) & (df_fta['ciclo_hidrologico'] == cycle_fta)]
    if not f_fta.empty:
        col_h, col_s = st.columns([4, 1])
        with col_h:
            fig3, ax3 = plt.subplots(figsize=(12, 5))
            plot_fta_heatmap(f_fta, ax3, f"Hourly Logging Intensity ({year_fta})")
            st.pyplot(fig3)
        with col_s:
            max_v = f_fta['pct_fta'].max()
            st.metric("Highest FTA Peak", f"{max_v:.2f}%")
            st.metric("Avg Logging Impact", f"{f_fta['pct_fta'].mean():.2f}%")
    else:
        st.warning("No FTA data found for the selected filters.")

st.divider()

# --- SECCIÓN 4: MAPA DE RIESGO ---
st.header("4. Epidemiological Risk Map")

with st.expander("View Index Formulas: Overlap & Vector Abundance"):
    st.markdown("<div style='font-size: 1.1em;'>", unsafe_allow_html=True)
    st.markdown("""
    *   **AIO (Anthropogenic-Insect Overlap):** Measures the synchronized temporal coincidence between vector insects and human activity markers across the site profiles.
        $$AIO = \\frac{\\sum \\left( \\mathbb{1}_{\\text{human}}(i) \\times \\mathbb{1}_{\\text{insect}}(i) \\right)}{n}$$
    *   **IAI (Insect Activity Index):** Measures total acoustic insect signal distribution footprint densities against baseline recording volumes.
        $$IAI = \\frac{n_{\\text{mosquitoes}}}{n_{\\text{total}}} \\times 100$$
    """)
    st.markdown("</div>", unsafe_allow_html=True)

col_d1, col_d2 = st.columns(2)
with col_d1:
    year_risk = st.selectbox("Select Year:", sorted(df_risk['Year'].unique(), reverse=True), key="year_risk")
with col_d2:
    season_risk = st.selectbox("Select Season:", df_risk[df_risk['Year'] == year_risk]['Season'].unique(), key="season_risk")

view_all_risk = st.checkbox("Show all years for selected Season (Grid view)")

def plot_risk_scatter(data, ax, title):
    ax.scatter(data['ISAHI_pct'], data['IAM_pct'], s=data['ISAHI_pct']*40, alpha=0.6, c=data['IAM_pct'], cmap='viridis', edgecolors="w", linewidth=1.5)
    for _, row in data.iterrows():
        ax.annotate(row['Locality'], (row['ISAHI_pct'], row['IAM_pct']), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=8)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('AIO %'); ax.set_ylabel('IAI %')
    ax.axhline(y=20, color='grey', linestyle='--', alpha=0.3); ax.axvline(x=25, color='grey', linestyle='--', alpha=0.3)
    ax.set_xlim(0, 100); ax.set_ylim(0, 60)
    ax.text(2, 52, 'HIGH VECTOR', color='#d62728', fontsize=7, fontweight='bold')
    ax.text(45, 52, 'HIGH RISK ZONE', color='#8c564b', fontsize=7, fontweight='bold')

if view_all_risk:
    years = sorted(df_risk['Year'].unique())
    fig4, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes_flat = axes.flatten()
    for i, year in enumerate(years):
        if i < 4:
            y_df = df_risk[(df_risk['Year'] == year) & (df_risk['Season'] == season_risk)]
            if not y_df.empty:
                plot_risk_scatter(y_df, axes_flat[i], f"Year {year} - {season_risk}")
            else:
                axes_flat[i].set_title(f"Year {year} (No Data)")
    # Hide unused subplot if any
    for j in range(len(years), 4):
        axes_flat[j].axis('off')
    plt.tight_layout()
    st.pyplot(fig4)
else:
    y_df = df_risk[(df_risk['Year'] == year_risk) & (df_risk['Season'] == season_risk)]

    total_clips = y_df['Total_Clips'].sum()
    st.metric(f"Total Effort in {year_risk} ({season_risk})", f"{total_clips:,} clips")

    col_m, col_t = st.columns([2, 1])
    with col_m:
        fig4, ax4 = plt.subplots(figsize=(10, 7))
        plot_risk_scatter(y_df, ax4, f"Risk Map {year_risk} - {season_risk}")
        st.pyplot(fig4)
    with col_t:
        st.subheader("Sampling Effort")
        st.dataframe(y_df[['Locality', 'Total_Clips']].sort_values(by='Total_Clips', ascending=False), hide_index=True)
        
        st.info("""
        **Legend Mapping:**
        - **X-Axis & Bubble Size:** Represents the **AIO %** (Anthro-Insect Overlap). Larger bubbles and rightward shifts indicate higher temporal synchronization between people and vectors.
        - **Y-Axis & Color Intensity:** Represents the **IAI %** (Insect Activity Index). Higher and brighter coordinates indicate maximum overall vector densities.
        """)

st.caption("Developed for InnovaLab UPCH - Acoustic Monitoring Project (Iquitos)")