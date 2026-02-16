
# ==========================================
# CHART 12: NOVEL - "Score Distribution Violin" per method (all queries pooled)
# ==========================================
fig12 = go.Figure()
for method in ['Cosine', 'Hybrid', 'Taumode']:
    scores = df_search[df_search['tau_method'] == method]['score']
    fig12.add_trace(go.Violin(
        y=scores, name=tau_labels_short[method],
        box_visible=True, meanline_visible=True,
        line_color=tau_colors[method], fillcolor=tau_fill[method],
    ))

fig12.update_layout(
    title={"text": "Score Distribution: All Ranks Pooled<br><span style='font-size: 18px; font-weight: normal;'>270 scores per method | Taumode shifts entire distribution higher</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig12.update_yaxes(title_text="Score")
fig12.write_image("cve_c12_violin.png")
with open("cve_c12_violin.png.meta.json", "w") as f:
    json.dump({"caption": "Score Distribution Violin: All Ranks Pooled", "description": "Violin plots of all search scores per method"}, f)

# ==========================================
# CHART 13: NOVEL - "Tail Decay Rate" sorted by query difficulty
# ==========================================
# Sort queries by cosine head mean (proxy for difficulty)
cosine_head = cosine_tail.sort_values('head_mean').reset_index(drop=True)
difficulty_order = cosine_head['query_id'].values

fig13 = go.Figure()
for tm in tail_methods:
    tm_data = df_tail[df_tail['tau_method'] == tm]
    # Reorder by difficulty
    ordered = []
    for qid in difficulty_order:
        row = tm_data[tm_data['query_id'] == qid]
        if not row.empty:
            ordered.append(row.iloc[0])
    ordered_df = pd.DataFrame(ordered)
    
    color = tail_method_colors.get(tm, '#999')
    fig13.add_trace(go.Scatter(
        x=[f"Q{q}" for q in ordered_df['query_id']],
        y=ordered_df['tail_decay_rate'],
        mode='lines+markers',
        name=tm, line=dict(color=color, width=2.5), marker=dict(size=8),
    ))

fig13.update_layout(
    title={"text": "Tail Decay Rate (Sorted by Difficulty)<br><span style='font-size: 18px; font-weight: normal;'>Left = hardest queries | Lower = more gradual score falloff</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig13.update_xaxes(title_text="Query (easy→hard)")
fig13.update_yaxes(title_text="Decay Rate")
fig13.write_image("cve_c13_decay_rate.png")
with open("cve_c13_decay_rate.png.meta.json", "w") as f:
    json.dump({"caption": "Tail Decay Rate Sorted by Query Difficulty", "description": "Line chart of tail decay rate ordered by query difficulty"}, f)

# ==========================================
# CHART 14: NOVEL - "Spectral Boost Map" 
# Heatmap: (query x rank) showing Δscore = Taumode - Cosine
# ==========================================
boost_matrix = np.zeros((18, 15))
for qi, qid in enumerate(sorted(df_search['query_id'].unique())):
    cos_data = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Cosine')].sort_values('rank')
    tau_data = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Taumode')].sort_values('rank')
    
    for ri in range(min(15, len(cos_data), len(tau_data))):
        boost_matrix[qi, ri] = tau_data.iloc[ri]['score'] - cos_data.iloc[ri]['score']

fig14 = go.Figure(data=go.Heatmap(
    z=boost_matrix, x=[f"R{i+1}" for i in range(15)], y=[f"Q{i+1}" for i in range(18)],
    colorscale='RdYlGn', zmin=-0.02, zmax=0.08,
    text=np.round(boost_matrix, 3).astype(str), texttemplate="%{text}", textfont={"size": 8},
    colorbar=dict(title="Δ Score"),
))
fig14.update_layout(
    title={"text": "Spectral Boost Map: Taumode − Cosine<br><span style='font-size: 18px; font-weight: normal;'>Green = Taumode wins | Consistent positive lift across nearly all cells</span>"},
)
fig14.update_xaxes(title_text="Rank")
fig14.update_yaxes(title_text="Query")
fig14.write_image("cve_c14_boost_map.png")
with open("cve_c14_boost_map.png.meta.json", "w") as f:
    json.dump({"caption": "Spectral Boost Map: Taumode − Cosine", "description": "Heatmap of score difference at every query-rank cell"}, f)

print("Charts 12-14 done")
