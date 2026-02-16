
# ==========================================
# CHART 17: NOVEL - "Multi-Query Stability Heatmap"
# For each method: std of score at each rank across queries
# Lower = more consistent across diverse query types
# ==========================================
stability_data = {}
for method in ['Cosine', 'Hybrid', 'Taumode']:
    mdata = df_search[df_search['tau_method'] == method]
    # Pivot: rows=queries, cols=ranks
    pivot = mdata.pivot_table(index='query_id', columns='rank', values='score')
    # Std across queries at each rank
    stability_data[method] = pivot.std(axis=0).values

fig17 = go.Figure()
for method in ['Cosine', 'Hybrid', 'Taumode']:
    fig17.add_trace(go.Scatter(
        x=list(range(1, 16)),
        y=stability_data[method],
        mode='lines+markers',
        name=tau_labels_short[method],
        line=dict(color=tau_colors[method], width=3),
        marker=dict(size=8),
    ))

fig17.update_layout(
    title={"text": "Cross-Query Score Variability<br><span style='font-size: 18px; font-weight: normal;'>Std of scores across 18 queries | Taumode reduces variability at tail</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig17.update_xaxes(title_text="Rank", dtick=1)
fig17.update_yaxes(title_text="Score Std")
fig17.write_image("cve_c17_stability.png")
with open("cve_c17_stability.png.meta.json", "w") as f:
    json.dump({"caption": "Cross-Query Score Variability by Rank", "description": "Std of scores across 18 queries at each rank position"}, f)

# ==========================================
# CHART 18: NOVEL - "Score Compression" 
# Range (max-min) at each rank across methods
# ==========================================
fig18 = go.Figure()
for method in ['Cosine', 'Hybrid', 'Taumode']:
    mdata = df_search[df_search['tau_method'] == method]
    pivot = mdata.pivot_table(index='query_id', columns='rank', values='score')
    score_range = pivot.max(axis=0) - pivot.min(axis=0)
    
    fig18.add_trace(go.Bar(
        x=list(range(1, 16)), y=score_range.values,
        name=tau_labels_short[method], marker_color=tau_colors[method], opacity=0.8,
    ))

fig18.update_layout(
    barmode='group',
    title={"text": "Score Range Across Queries<br><span style='font-size: 18px; font-weight: normal;'>Spectral methods compress score range → more uniform retrieval</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig18.update_xaxes(title_text="Rank", dtick=1)
fig18.update_yaxes(title_text="Score Range")
fig18.update_traces(cliponaxis=False)
fig18.write_image("cve_c18_range.png")
with open("cve_c18_range.png.meta.json", "w") as f:
    json.dump({"caption": "Score Range Across Queries by Rank", "description": "Bar chart of score range at each rank showing spectral compression effect"}, f)

print("Charts 17-18 done")
