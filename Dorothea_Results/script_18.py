
# ==========================================
# CHART 19: NOVEL - "Config Signature Parallel Coordinates"
# Each config as a line through all metrics
# ==========================================
from plotly.express import parallel_coordinates

merged2 = df_spectral.copy()
for cfg in configs:
    idx = merged2[merged2['config'] == cfg].index[0]
    cfg_data = df_class[df_class['config'] == cfg]
    
    merged2.loc[idx, 'best_hybrid_f1'] = cfg_data[cfg_data['method'].str.startswith('search_alpha')]['f1'].max()
    merged2.loc[idx, 'best_cosine_f1'] = cfg_data[cfg_data['method'].str.startswith('knn_cosine')]['f1'].max()
    merged2.loc[idx, 'best_umap_f1'] = cfg_data[cfg_data['method'].str.startswith('umap_2d')]['f1'].max()
    merged2.loc[idx, 'build_time'] = cfg_data.iloc[0]['build_time_s']

merged2['config_id'] = range(len(merged2))

dims = [
    dict(label='Lambda CV', values=merged2['lambda_cv']),
    dict(label='Spec Gap', values=merged2['spectral_gap']),
    dict(label='Fiedler', values=merged2['fiedler_value']),
    dict(label='Eff Rank', values=merged2['effective_rank']),
    dict(label="Cohen's d", values=merged2['cohens_d']),
    dict(label='Overlap', values=merged2['overlap']),
    dict(label='Hybrid F1', values=merged2['best_hybrid_f1']),
    dict(label='Cosine F1', values=merged2['best_cosine_f1']),
]

fig19 = go.Figure(data=go.Parcoords(
    line=dict(
        color=merged2['config_id'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Config ID"),
    ),
    dimensions=dims,
))

fig19.update_layout(
    title={"text": "Config Signatures: Spectral → Performance<br><span style='font-size: 18px; font-weight: normal;'>Each line = one config | Cosine F1 invariant, Hybrid varies</span>"},
)
fig19.write_image("chart19_parallel_coords.png")
with open("chart19_parallel_coords.png.meta.json", "w") as f:
    json.dump({"caption": "Parallel Coordinates: Config Signatures", "description": "Parallel coordinates plot tracing each config through spectral metrics to performance"}, f)

print("Chart 19 done")
