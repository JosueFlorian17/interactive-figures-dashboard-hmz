import pandas as pd
import json
import base64
import os

def generate_html_dashboard():
    # --- DATA LOADING (Using paths from app.py) ---
    # 1. Relevo 24h
    df_24h = pd.read_csv('data_24h_combined_seasons.csv')
    
    # 2. IPH
    with open(r'C:\Users\Florian\Documents\innovalab\graficas\ip-final-final.json', 'r', encoding='utf-8') as f:
        df_iph = pd.DataFrame(json.load(f)['rows'])
    
    # 3. FTA
    df_fta = pd.read_csv('output_fta/data_fta.csv')
    
    # 4. Risk
    df_risk = pd.read_csv(r'C:\Users\Florian\Documents\innovalab\graficas\seasonal_risk_data.csv')

    # Convert dataframes to JSON for embedding in HTML
    data_json = {
        "df_24h": df_24h.to_dict(orient='records'),
        "df_iph": df_iph.to_dict(orient='records'),
        "df_fta": df_fta.to_dict(orient='records'),
        "df_risk": df_risk.to_dict(orient='records')
    }

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AudioMoth Biodiversity Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #0e1117; color: #fafafa; font-family: sans-serif; }}
        .card {{ background-color: #262730; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem; }}
        select, input {{ background-color: #0e1117; border: 1px solid #464855; color: white; padding: 5px; border-radius: 4px; }}
        .info-box {{ background-color: rgba(28, 131, 225, 0.1); border-left: 5px solid #1c83e1; padding: 1rem; margin: 1rem 0; }}
    </style>
</head>
<body class="p-8">
    <h1 class="text-4xl font-bold mb-4">AudioMoth Acoustic Monitoring Dashboard - Iquitos</h1>
    
    <!-- SECTION 1: 24H -->
    <div class="card">
        <h2 class="text-2xl font-bold mb-2">1. Hourly Activity Composition (Seasonal)</h2>
        <div class="info-box">Analyze how acoustic composition changes by hour, year, and season.</div>
        <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
                <label>Community:</label><br>
                <select id="sel_loc_24h" onchange="update24h()"></select>
            </div>
            <div>
                <label>Year:</label><br>
                <select id="sel_year_24h" onchange="update24h()"></select>
            </div>
            <div>
                <label>Cycle:</label><br>
                <select id="sel_cycle_24h" onchange="update24h()"></select>
            </div>
        </div>
        <div id="plot_24h" style="height: 400px;"></div>
    </div>

    <!-- SECTION 2: IPH -->
    <div class="card">
        <h2 class="text-2xl font-bold mb-2">2. Critical Periods Comparison (IP Seasonal)</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label>Year:</label><br>
                <select id="sel_year_iph" onchange="updateIPH()"></select>
            </div>
            <div>
                <label>Cycle:</label><br>
                <select id="sel_cycle_iph" onchange="updateIPH()"></select>
            </div>
        </div>
        <div id="plot_iph" style="height: 500px;"></div>
    </div>

    <!-- SECTION 3: FTA -->
    <div class="card">
        <h2 class="text-2xl font-bold mb-2">3. Acoustic Logging Frequency (ALF)</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label>Year:</label><br>
                <select id="sel_year_fta" onchange="updateFTA()"></select>
            </div>
            <div>
                <label>Cycle:</label><br>
                <select id="sel_cycle_fta" onchange="updateFTA()"></select>
            </div>
        </div>
        <div id="plot_fta" style="height: 400px;"></div>
    </div>

    <!-- SECTION 4: RISK -->
    <div class="card">
        <h2 class="text-2xl font-bold mb-2">4. Epidemiological Risk Map</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label>Year:</label><br>
                <select id="sel_year_risk" onchange="updateRisk()"></select>
            </div>
            <div>
                <label>Season:</label><br>
                <select id="sel_season_risk" onchange="updateRisk()"></select>
            </div>
        </div>
        <div id="plot_risk" style="height: 600px;"></div>
    </div>

    <script>
        const data = {json.dumps(data_json)};
        const COLORS = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"];
        const CATS = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"];

        function init() {{
            // Populate selects
            const locs = [...new Set(data.df_24h.map(d => d.localidad))].sort();
            const years = [...new Set(data.df_24h.map(d => d.anio))].sort();
            const cycles = ["Vaciante", "Creciente"];

            fillSelect("sel_loc_24h", locs);
            fillSelect("sel_year_24h", years);
            fillSelect("sel_cycle_24h", cycles);
            
            fillSelect("sel_year_iph", [...new Set(data.df_iph.map(d => d.anio || d.temporada_base))].sort());
            fillSelect("sel_cycle_iph", cycles);

            fillSelect("sel_year_fta", [...new Set(data.df_fta.map(d => d.anio))].sort().reverse());
            fillSelect("sel_cycle_fta", cycles);

            fillSelect("sel_year_risk", [...new Set(data.df_risk.map(d => d.Year))].sort().reverse());
            fillSelect("sel_season_risk", [...new Set(data.df_risk.map(d => d.Season))]);

            update24h();
            updateIPH();
            updateFTA();
            updateRisk();
        }}

        function fillSelect(id, items) {{
            const el = document.getElementById(id);
            items.forEach(item => {{
                const opt = document.createElement("option");
                opt.value = item; opt.text = item;
                el.add(opt);
            }});
        }}

        function update24h() {{
            const loc = document.getElementById("sel_loc_24h").value;
            const year = parseInt(document.getElementById("sel_year_24h").value);
            const cycle = document.getElementById("sel_cycle_24h").value;

            const filtered = data.df_24h.filter(d => d.localidad === loc && d.anio === year && d.ciclo_hidrologico === cycle);
            
            let traces = [];
            CATS.forEach((cat, i) => {{
                const catData = filtered.filter(d => d.primary_category === cat || d.primary_category === cat.toLowerCase());
                traces.push({{
                    x: catData.map(d => d.hora_dia),
                    y: catData.map(d => d.promedio_clips_hora),
                    name: cat,
                    type: 'scatter',
                    stackgroup: 'one',
                    fillcolor: COLORS[i],
                    line: {{color: COLORS[i]}}
                }});
            }});

            Plotly.newPlot('plot_24h', traces, {{
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{color: '#fff'}}, margin: {{t:30, b:40, l:40, r:20}},
                xaxis: {{title: 'Hour of Day', range: [0, 23]}},
                yaxis: {{title: 'Avg Clips'}}
            }});
        }}

        function updateIPH() {{
            const year = parseInt(document.getElementById("sel_year_iph").value);
            const cycle = document.getElementById("sel_cycle_iph").value;
            
            const filtered = data.df_iph.filter(d => (d.anio === year || d.temporada_base === year) && (d.estacion === cycle || d.ciclo_hidrologico === cycle));
            const coms = [...new Set(filtered.map(d => d.comunidad))];
            
            let traces = [];
            coms.forEach(com => {{
                const comData = filtered.filter(d => d.comunidad === com && d.periodo_analisis === "Dawn");
                traces.push({{
                    x: comData.map(d => d.categoria),
                    y: comData.map(d => d.porcentaje_promedio),
                    name: com,
                    type: 'bar'
                }});
            }});

            Plotly.newPlot('plot_iph', traces, {{
                barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{color: '#fff'}}, title: 'Dawn Activity Comparison'
            }});
        }}

        function updateFTA() {{
            const year = parseInt(document.getElementById("sel_year_fta").value);
            const cycle = document.getElementById("sel_cycle_fta").value;
            const filtered = data.df_fta.filter(d => d.anio === year && d.ciclo_hidrologico === cycle);
            
            const locs = [...new Set(filtered.map(d => d.localidad))];
            const hours = [...new Set(filtered.map(d => d.hora_del_dia))].sort((a,b)=>a-b);
            
            let z = locs.map(l => hours.map(h => {{
                const match = filtered.find(f => f.localidad === l && f.hora_del_dia === h);
                return match ? match.pct_fta : 0;
            }}));

            Plotly.newPlot('plot_fta', [{{
                z: z, x: hours, y: locs, type: 'heatmap', colorscale: 'YlOrRd'
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{color: '#fff'}}, margin: {{t:30, b:40, l:100, r:20}}
            }});
        }}

        function updateRisk() {{
            const year = parseInt(document.getElementById("sel_year_risk").value);
            const season = document.getElementById("sel_season_risk").value;
            const filtered = data.df_risk.filter(d => d.Year === year && d.Season === season);

            Plotly.newPlot('plot_risk', [{{
                x: filtered.map(d => d.ISAHI_pct),
                y: filtered.map(d => d.IAM_pct),
                mode: 'markers+text',
                text: filtered.map(d => d.Locality),
                textposition: 'top center',
                marker: {{
                    size: filtered.map(d => d.ISAHI_pct * 2),
                    color: filtered.map(d => d.IAM_pct),
                    colorscale: 'Viridis',
                    showscale: true
                }}
            }}], {{
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                font: {{color: '#fff'}},
                xaxis: {{title: 'AIO % (Interaction)', range: [0, 100]}},
                yaxis: {{title: 'IAI % (Mosquito Activity)', range: [0, 60]}},
                shapes: [
                    {{type: 'line', x0: 25, x1: 25, y0: 0, y1: 60, line: {{color: 'grey', dash: 'dash'}}, opacity: 0.3}},
                    {{type: 'line', x0: 0, x1: 100, y0: 20, y1: 20, line: {{color: 'grey', dash: 'dash'}}, opacity: 0.3}}
                ]
            }});
        }}

        window.onload = init;
    </script>
</body>
</html>
    """
    
    with open("biodiversity_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Standalone HTML dashboard generated: biodiversity_dashboard.html")

if __name__ == "__main__":
    generate_html_dashboard()
