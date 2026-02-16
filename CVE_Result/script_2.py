
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

df_search = pd.read_csv('cve_search_results.csv')
df_metrics = pd.read_csv('cve_comparison_metrics.csv')
df_summary = pd.read_csv('cve_summary.csv')
df_tail = pd.read_csv('cve_tail_metrics.csv')

tau_colors = {'Cosine': '#3498DB', 'Hybrid': '#F39C12', 'Taumode': '#2ECC71'}
tau_fill = {'Cosine': 'rgba(52,152,219,0.15)', 'Hybrid': 'rgba(243,156,18,0.15)', 'Taumode': 'rgba(46,204,113,0.15)'}
tau_labels_short = {'Cosine': 'Cosine (τ=1.0)', 'Hybrid': 'Hybrid (τ=0.72)', 'Taumode': 'Taumode (τ=0.42)'}
qfull = dict(zip(df_metrics['query_id'], df_metrics['query_text']))

# ==========================================
# CHART 1: Score Distribution by Rank (All Queries Averaged)
# ==========================================
fig1 = go.Figure()
for method in ['Cosine', 'Hybrid', 'Taumode']:
    mdata = df_search[df_search['tau_method'] == method]
    avg = mdata.groupby('rank')['score'].agg(['mean', 'std']).reset_index()
    
    fig1.add_trace(go.Scatter(
        x=avg['rank'], y=avg['mean'], mode='lines+markers',
        name=tau_labels_short[method], line=dict(color=tau_colors[method], width=3), marker=dict(size=8),
    ))
    fig1.add_trace(go.Scatter(
        x=list(avg['rank']) + list(avg['rank'][::-1]),
        y=list(avg['mean'] + avg['std']) + list((avg['mean'] - avg['std'])[::-1]),
        fill='toself', fillcolor=tau_fill[method], line=dict(width=0), showlegend=False,
    ))

fig1.add_vline(x=3.5, line_dash="dash", line_color="red", annotation_text="Head|Tail")
fig1.update_layout(
    title={"text": "Average Score Decay by Rank<br><span style='font-size: 18px; font-weight: normal;'>18 CVE queries | Taumode maintains higher scores across all ranks</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig1.update_xaxes(title_text="Rank", dtick=1)
fig1.update_yaxes(title_text="Score")
fig1.write_image("cve_c1_score_decay.png")
with open("cve_c1_score_decay.png.meta.json", "w") as f:
    json.dump({"caption": "Average Score Decay by Rank (18 Queries)", "description": "Line chart with std bands showing score decay for Cosine, Hybrid, Taumode"}, f)

# ==========================================
# CHART 2: Score Lift: Taumode & Hybrid vs Cosine per Rank
# ==========================================
fig2 = go.Figure()
cosine_avg = df_search[df_search['tau_method'] == 'Cosine'].groupby('rank')['score'].mean()
for method in ['Hybrid', 'Taumode']:
    m_avg = df_search[df_search['tau_method'] == method].groupby('rank')['score'].mean()
    lift = m_avg - cosine_avg
    fig2.add_trace(go.Bar(
        x=lift.index, y=lift.values, name=tau_labels_short[method],
        marker_color=tau_colors[method], opacity=0.85,
    ))

fig2.update_layout(
    title={"text": "Score Lift Over Cosine Baseline<br><span style='font-size: 18px; font-weight: normal;'>Positive = spectral method outperforms | Taumode lifts +0.04–0.07</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    barmode='group',
)
fig2.update_xaxes(title_text="Rank", dtick=1)
fig2.update_yaxes(title_text="Δ Score")
fig2.update_traces(cliponaxis=False)
fig2.write_image("cve_c2_score_lift.png")
with open("cve_c2_score_lift.png.meta.json", "w") as f:
    json.dump({"caption": "Score Lift Over Cosine by Rank", "description": "Bar chart showing score improvements from Hybrid and Taumode over Cosine at each rank"}, f)

# ==========================================
# CHART 3: NDCG@10 per Query (Grouped)
# ==========================================
fig3 = go.Figure()
qlabels = [f"Q{r['query_id']}" for _, r in df_metrics.iterrows()]
fig3.add_trace(go.Bar(x=qlabels, y=df_metrics['ndcg_hybrid_vs_cosine'], name='Hybrid vs Cos', marker_color='#F39C12'))
fig3.add_trace(go.Bar(x=qlabels, y=df_metrics['ndcg_taumode_vs_cosine'], name='Taumode vs Cos', marker_color='#2ECC71'))
fig3.add_trace(go.Bar(x=qlabels, y=df_metrics['ndcg_taumode_vs_hybrid'], name='Tau vs Hybrid', marker_color='#9B59B6'))

fig3.update_layout(
    barmode='group',
    title={"text": "NDCG@10 per Query<br><span style='font-size: 18px; font-weight: normal;'>Taumode vs Hybrid consistently >0.93 | Tau vs Cosine more variable</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig3.update_xaxes(title_text="Query")
fig3.update_yaxes(title_text="NDCG@10", range=[0, 1.1])
fig3.update_traces(cliponaxis=False)
fig3.write_image("cve_c3_ndcg.png")
with open("cve_c3_ndcg.png.meta.json", "w") as f:
    json.dump({"caption": "NDCG@10 per Query: Method Pairs", "description": "Grouped bars of NDCG for each method pair across 18 queries"}, f)

print("Charts 1-3 done")
