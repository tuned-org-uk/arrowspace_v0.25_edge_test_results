
# ==========================================
# CHART 6: Spectral Quality Radar Chart (per Config)
# ==========================================
# Normalize each metric to [0,1] for radar
radar_metrics = ['lambda_cv', 'spectral_gap', 'fiedler_value', 'effective_rank', 'participation_ratio', 'cohens_d']
radar_labels = ['Lambda CV', 'Spectral Gap', 'Fiedler', 'Eff Rank', 'Part. Ratio', "Cohen's d"]

radar_data = df_spectral[radar_metrics].copy()
for col in radar_metrics:
    mn, mx = radar_data[col].min(), radar_data[col].max()
    if mx > mn:
        radar_data[col] = (radar_data[col] - mn) / (mx - mn)
    else:
        radar_data[col] = 0.5

fig6 = go.Figure()
for i, cfg in enumerate(configs):
    vals = radar_data.iloc[i].values.tolist()
    vals.append(vals[0])  # close the polygon
    labels_closed = radar_labels + [radar_labels[0]]
    
    fig6.add_trace(go.Scatterpolar(
        r=vals, theta=labels_closed,
        fill='toself', name=config_short[cfg],
        line=dict(color=config_colors[cfg], width=2),
        opacity=0.6,
    ))

fig6.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1.1])),
    title={"text": "Spectral Quality Profiles<br><span style='font-size: 18px; font-weight: normal;'>Normalized metrics | Each config has distinct spectral signature</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5),
)
fig6.write_image("chart6_spectral_radar.png")
with open("chart6_spectral_radar.png.meta.json", "w") as f:
    json.dump({"caption": "Spectral Quality Radar: Config Fingerprints", "description": "Polar radar chart of normalized spectral quality metrics per config"}, f)

print("Chart 6 done")
