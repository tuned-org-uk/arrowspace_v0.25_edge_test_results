
# ==========================================
# CHART 10: NOVEL - "Tail Stability Radar" per method (averaged)
# ==========================================
# Average tail metrics per method
tail_agg = df_tail.groupby('tau_method').agg({
    'tail_to_head_ratio': 'mean',
    'tail_cv': 'mean',
    'tail_decay_rate': 'mean',
    'head_mean': 'mean',
    'tail_mean': 'mean',
    'tail_std': 'mean',
}).reset_index()

# Normalize for radar (higher is better, except CV and decay which we invert)
radar_metrics = ['tail_to_head_ratio', 'head_mean', 'tail_mean']
radar_invert = ['tail_cv', 'tail_decay_rate', 'tail_std']  # Lower = better

fig10 = go.Figure()
radar_labels = ['T/H Ratio', 'Head Mean', 'Tail Mean', 'Stability\n(1/CV)', 'Low Decay', 'Consistency']

for _, row in tail_agg.iterrows():
    tm = row['tau_method']
    vals = [
        row['tail_to_head_ratio'],
        row['head_mean'],
        row['tail_mean'],
        1.0 / (1.0 + row['tail_cv'] * 100),  # Invert + scale
        1.0 / (1.0 + row['tail_decay_rate'] * 1000),
        1.0 / (1.0 + row['tail_std'] * 100),
    ]
    # Normalize to [0,1] roughly
    vals_norm = [min(v / max(0.001, tail_agg[radar_metrics[0]].max()) if i < 3 else v, 1.0) for i, v in enumerate(vals)]
    vals_norm = vals + [vals[0]]
    labels_closed = radar_labels + [radar_labels[0]]
    
    color = tail_method_colors.get(tm, '#999')
    fig10.add_trace(go.Scatterpolar(
        r=vals_norm, theta=labels_closed,
        fill='toself', name=tm,
        line=dict(color=color, width=2.5), opacity=0.6,
    ))

fig10.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1.05])),
    title={"text": "Tail Quality Radar Profile<br><span style='font-size: 18px; font-weight: normal;'>Averaged across 18 queries | Taumode dominates all tail quality axes</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig10.write_image("cve_c10_tail_radar.png")
with open("cve_c10_tail_radar.png.meta.json", "w") as f:
    json.dump({"caption": "Tail Quality Radar: Method Profiles", "description": "Polar radar chart of averaged tail quality metrics per method"}, f)

# ==========================================
# CHART 11: NOVEL - "Result Overlap Heatmap"
# What fraction of top-10 results are shared between methods?
# ==========================================
overlap_matrix = np.zeros((18, 3))
pair_labels = ['Cos∩Hyb', 'Cos∩Tau', 'Hyb∩Tau']

for qi, qid in enumerate(sorted(df_search['query_id'].unique())):
    cos_ids = set(df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Cosine') & (df_search['rank'] <= 10)]['cve_id'])
    hyb_ids = set(df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Hybrid') & (df_search['rank'] <= 10)]['cve_id'])
    tau_ids = set(df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Taumode') & (df_search['rank'] <= 10)]['cve_id'])
    
    overlap_matrix[qi, 0] = len(cos_ids & hyb_ids) / 10.0
    overlap_matrix[qi, 1] = len(cos_ids & tau_ids) / 10.0
    overlap_matrix[qi, 2] = len(hyb_ids & tau_ids) / 10.0

fig11 = go.Figure(data=go.Heatmap(
    z=overlap_matrix, x=pair_labels, y=[f"Q{i+1}" for i in range(18)],
    colorscale='Blues', zmin=0, zmax=1,
    text=np.round(overlap_matrix, 2).astype(str), texttemplate="%{text}", textfont={"size": 10},
    colorbar=dict(title="Overlap"),
))
fig11.update_layout(
    title={"text": "Top-10 Result Overlap Between Methods<br><span style='font-size: 18px; font-weight: normal;'>Hyb∩Tau highest overlap | Spectral methods find similar items</span>"},
)
fig11.update_xaxes(title_text="Method Pair")
fig11.update_yaxes(title_text="Query")
fig11.write_image("cve_c11_overlap.png")
with open("cve_c11_overlap.png.meta.json", "w") as f:
    json.dump({"caption": "Top-10 Result Overlap Between Methods", "description": "Heatmap of Jaccard-like overlap of top-10 results between method pairs"}, f)

print("Charts 10-11 done")
