
# Color palette for tau methods
tau_colors = {'Cosine': '#3498DB', 'Hybrid': '#F39C12', 'Taumode': '#2ECC71'}
tau_labels_short = {'Cosine': 'Cosine (τ=1.0)', 'Hybrid': 'Hybrid (τ=0.72)', 'Taumode': 'Taumode (τ=0.42)'}

# Short query labels
qlabels = {qid: f"Q{qid}" for qid in df_metrics['query_id']}
qfull = dict(zip(df_metrics['query_id'], df_metrics['query_text']))

# ==========================================
# CHART 1: Score Distribution by Rank (All Queries Averaged)
# ==========================================
fig1 = go.Figure()

for method in ['Cosine', 'Hybrid', 'Taumode']:
    mdata = df_search[df_search['tau_method'] == method]
    avg_by_rank = mdata.groupby('rank')['score'].agg(['mean', 'std']).reset_index()
    
    fig1.add_trace(go.Scatter(
        x=avg_by_rank['rank'], y=avg_by_rank['mean'],
        mode='lines+markers',
        name=tau_labels_short[method],
        line=dict(color=tau_colors[method], width=3),
        marker=dict(size=8),
    ))
    # Error band
    fig1.add_trace(go.Scatter(
        x=list(avg_by_rank['rank']) + list(avg_by_rank['rank'][::-1]),
        y=list(avg_by_rank['mean'] + avg_by_rank['std']) + list((avg_by_rank['mean'] - avg_by_rank['std'])[::-1]),
        fill='toself',
        fillcolor=tau_colors[method].replace(')', ',0.15)').replace('#', 'rgba(') if '#' in tau_colors[method] else tau_colors[method],
        line=dict(width=0),
        showlegend=False,
    ))

# Fix fillcolor - use proper rgba
fig1.data[1].fillcolor = 'rgba(52,152,219,0.15)'
fig1.data[3].fillcolor = 'rgba(243,156,18,0.15)'
fig1.data[5].fillcolor = 'rgba(46,204,113,0.15)'

fig1.add_vline(x=3.5, line_dash="dash", line_color="red", annotation_text="Head|Tail")
fig1.update_layout(
    title={"text": "Average Score Decay by Rank<br><span style='font-size: 18px; font-weight: normal;'>18 CVE queries | Taumode maintains higher scores across all ranks</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig1.update_xaxes(title_text="Rank", dtick=1)
fig1.update_yaxes(title_text="Score")
fig1.write_image("cve_c1_score_decay.png")
with open("cve_c1_score_decay.png.meta.json", "w") as f:
    json.dump({"caption": "Average Score Decay by Rank (18 Queries)", "description": "Line chart showing average search scores with std bands across all ranks for Cosine, Hybrid, Taumode"}, f)

print("Chart 1 done")
