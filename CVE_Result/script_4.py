
# ==========================================
# CHART 7: Per-Query Score Curves (Small Multiples - 6x3 grid)
# ==========================================
n_queries = df_search['query_id'].nunique()
query_ids = sorted(df_search['query_id'].unique())

fig7 = make_subplots(rows=6, cols=3, 
    subplot_titles=[f"Q{qid}" for qid in query_ids],
    horizontal_spacing=0.05, vertical_spacing=0.04)

for i, qid in enumerate(query_ids):
    row = i // 3 + 1
    col = i % 3 + 1
    for method in ['Cosine', 'Hybrid', 'Taumode']:
        qdata = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == method)]
        fig7.add_trace(go.Scatter(
            x=qdata['rank'], y=qdata['score'],
            mode='lines+markers', name=tau_labels_short[method],
            line=dict(color=tau_colors[method], width=2),
            marker=dict(size=4), showlegend=(i == 0),
        ), row=row, col=col)

fig7.update_layout(
    title={"text": "Per-Query Score Curves (18 CVE Queries)<br><span style='font-size: 18px; font-weight: normal;'>Taumode (green) consistently above Cosine (blue) at every rank</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    height=1400,
)
fig7.write_image("cve_c7_per_query_curves.png")
with open("cve_c7_per_query_curves.png.meta.json", "w") as f:
    json.dump({"caption": "Per-Query Score Curves: All 18 Queries", "description": "Small multiples showing score decay for each query across Cosine, Hybrid, Taumode"}, f)

print("Chart 7 done")
