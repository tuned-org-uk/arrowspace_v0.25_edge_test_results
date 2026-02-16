
# ==========================================
# CHART 4: Spearman/Kendall Correlation Heatmap
# ==========================================
corr_cols = ['spearman_cosine_hybrid', 'spearman_cosine_taumode', 'spearman_hybrid_taumode',
             'kendall_cosine_hybrid', 'kendall_cosine_taumode', 'kendall_hybrid_taumode']
col_labels = ['ρ Cos-Hyb', 'ρ Cos-Tau', 'ρ Hyb-Tau', 'τ Cos-Hyb', 'τ Cos-Tau', 'τ Hyb-Tau']

heat_z = df_metrics[corr_cols].values
qlabels = [f"Q{r['query_id']}" for _, r in df_metrics.iterrows()]

fig4 = go.Figure(data=go.Heatmap(
    z=heat_z, x=col_labels, y=qlabels,
    colorscale='RdYlGn', zmin=-1, zmax=1,
    text=np.round(heat_z, 2).astype(str), texttemplate="%{text}", textfont={"size": 9},
))
fig4.update_layout(
    title={"text": "Rank Correlation: Spearman & Kendall<br><span style='font-size: 18px; font-weight: normal;'>Green=agreement, Red=disagreement | Hybrid-Tau most consistent</span>"},
)
fig4.update_xaxes(title_text="Metric Pair")
fig4.update_yaxes(title_text="Query")
fig4.write_image("cve_c4_rank_corr.png")
with open("cve_c4_rank_corr.png.meta.json", "w") as f:
    json.dump({"caption": "Rank Correlation Heatmap (Spearman & Kendall)", "description": "Heatmap of pairwise ranking correlations across all 18 queries"}, f)

# ==========================================
# CHART 5: Tail Quality Metrics: T/H Ratio per Query
# ==========================================
fig5 = go.Figure()

tail_methods = df_tail['tau_method'].unique()
tail_method_colors = {
    'Cosine (τ=1.0)': '#3498DB', 
    'Hybrid (τ=0.75)': '#F39C12',
    'Taumode (τ=0.0.6)': '#2ECC71',
}

for tm in tail_methods:
    tm_data = df_tail[df_tail['tau_method'] == tm].sort_values('query_id')
    color = tail_method_colors.get(tm, '#999')
    fig5.add_trace(go.Scatter(
        x=[f"Q{q}" for q in tm_data['query_id']],
        y=tm_data['tail_to_head_ratio'],
        mode='lines+markers',
        name=tm, line=dict(color=color, width=2.5), marker=dict(size=8),
    ))

fig5.update_layout(
    title={"text": "Tail/Head Ratio per Query<br><span style='font-size: 18px; font-weight: normal;'>Higher = flatter decay → better RAG stability | Taumode wins most queries</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig5.update_xaxes(title_text="Query")
fig5.update_yaxes(title_text="T/H Ratio", range=[0.955, 1.001])
fig5.write_image("cve_c5_th_ratio.png")
with open("cve_c5_th_ratio.png.meta.json", "w") as f:
    json.dump({"caption": "Tail/Head Ratio per Query", "description": "Line chart of tail-to-head score ratio per query per method"}, f)

# ==========================================
# CHART 6: Tail CV (Stability) per Query
# ==========================================
fig6 = go.Figure()
for tm in tail_methods:
    tm_data = df_tail[df_tail['tau_method'] == tm].sort_values('query_id')
    color = tail_method_colors.get(tm, '#999')
    fig6.add_trace(go.Scatter(
        x=[f"Q{q}" for q in tm_data['query_id']],
        y=tm_data['tail_cv'],
        mode='lines+markers',
        name=tm, line=dict(color=color, width=2.5), marker=dict(size=8),
    ))

fig6.update_layout(
    title={"text": "Tail Coefficient of Variation<br><span style='font-size: 18px; font-weight: normal;'>Lower = more stable tail scores | Taumode most stable in 14/18 queries</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig6.update_xaxes(title_text="Query")
fig6.update_yaxes(title_text="Tail CV")
fig6.write_image("cve_c6_tail_cv.png")
with open("cve_c6_tail_cv.png.meta.json", "w") as f:
    json.dump({"caption": "Tail CV (Score Stability) per Query", "description": "Lower CV indicates more stable tail scores across ranks"}, f)

print("Charts 4-6 done")
