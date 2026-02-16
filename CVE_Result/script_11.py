
# ==========================================
# CHART 20: NOVEL - "Score Landscape Contour" 
# 2D: Query ID x Rank, Z = score; one per method
# ==========================================
fig20 = make_subplots(rows=1, cols=3, subplot_titles=['Cosine (τ=1.0)', 'Hybrid (τ=0.72)', 'Taumode (τ=0.42)'],
                      horizontal_spacing=0.06)

for mi, method in enumerate(['Cosine', 'Hybrid', 'Taumode']):
    mdata = df_search[df_search['tau_method'] == method]
    pivot = mdata.pivot_table(index='query_id', columns='rank', values='score')
    
    fig20.add_trace(go.Heatmap(
        z=pivot.values,
        x=[f"R{c}" for c in pivot.columns],
        y=[f"Q{r}" for r in pivot.index],
        colorscale='Viridis',
        zmin=0.72, zmax=0.95,
        showscale=(mi == 2),
        colorbar=dict(title="Score") if mi == 2 else None,
    ), row=1, col=mi + 1)

fig20.update_layout(
    title={"text": "Score Landscape: Query × Rank<br><span style='font-size: 18px; font-weight: normal;'>Taumode surface is brighter throughout → global score elevation</span>"},
)
fig20.write_image("cve_c20_landscape.png")
with open("cve_c20_landscape.png.meta.json", "w") as f:
    json.dump({"caption": "Score Landscape: Query × Rank Heatmaps", "description": "Side-by-side heatmaps showing score values across all query-rank combinations for each method"}, f)

# ==========================================
# CHART 21: NOVEL - "Parallel Coordinates: Query Signatures"
# Each query as a line through: Cosine_top1, Tau_top1, NDCG, Spearman, T/H_cosine, T/H_tau
# ==========================================
qb_df = pd.DataFrame(query_benefit)
qb_df = qb_df.merge(df_metrics[['query_id', 'ndcg_taumode_vs_cosine', 'spearman_cosine_taumode']], 
                     left_on='qid', right_on='query_id')
qb_df['th_cosine'] = cosine_tail.set_index('query_id').loc[qb_df['qid']]['tail_to_head_ratio'].values
qb_df['th_taumode'] = taumode_tail.set_index('query_id').loc[qb_df['qid']]['tail_to_head_ratio'].values

dims = [
    dict(label='Cos Head', values=qb_df['cos_head']),
    dict(label='Score Lift', values=qb_df['score_lift']),
    dict(label='NDCG T/C', values=qb_df['ndcg_tau_cos']),
    dict(label='ρ Cos-Tau', values=qb_df['spearman_cosine_taumode']),
    dict(label='T/H Cos', values=qb_df['th_cosine']),
    dict(label='T/H Tau', values=qb_df['th_taumode']),
]

fig21 = go.Figure(data=go.Parcoords(
    line=dict(
        color=qb_df['score_lift'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Lift"),
    ),
    dimensions=dims,
))
fig21.update_layout(
    title={"text": "Query Signatures: Parallel Coordinates<br><span style='font-size: 18px; font-weight: normal;'>Each line = one query | Higher lift correlates with higher T/H improvement</span>"},
)
fig21.write_image("cve_c21_parcoords.png")
with open("cve_c21_parcoords.png.meta.json", "w") as f:
    json.dump({"caption": "Query Signatures: Parallel Coordinates", "description": "Parallel coordinates plot tracing each query through head score, lift, NDCG, spearman, and tail metrics"}, f)

print("Charts 20-21 done")
