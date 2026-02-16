
# ==========================================
# CHART 8: NOVEL - "Ranking Agreement Network" 
# Which queries have identical rankings across methods?
# ==========================================
# Categorize queries by agreement type
agree_types = []
for _, row in df_metrics.iterrows():
    qid = row['query_id']
    sp_ch = row['spearman_cosine_hybrid']
    sp_ct = row['spearman_cosine_taumode']
    sp_ht = row['spearman_hybrid_taumode']
    
    if sp_ch == 1.0 and sp_ct == 1.0:
        agree_types.append('All Agree')
    elif sp_ht > 0.9:
        agree_types.append('Spectral Agree')
    elif sp_ch > 0.8:
        agree_types.append('Cosine-Hybrid')
    else:
        agree_types.append('All Diverge')

df_metrics['agreement'] = agree_types

# Count
agree_counts = pd.Series(agree_types).value_counts()
colors_agree = {'All Agree': '#2ECC71', 'Spectral Agree': '#F39C12', 'Cosine-Hybrid': '#3498DB', 'All Diverge': '#E74C3C'}

fig8 = go.Figure()
fig8.add_trace(go.Bar(
    x=agree_counts.index.tolist(),
    y=agree_counts.values,
    marker_color=[colors_agree.get(a, '#999') for a in agree_counts.index],
    text=[f"{v}/18" for v in agree_counts.values],
    textposition='outside',
))
fig8.update_layout(
    title={"text": "Ranking Agreement Across Methods<br><span style='font-size: 18px; font-weight: normal;'>7/18 queries rank identically | 6 queries show spectral divergence</span>"},
)
fig8.update_xaxes(title_text="Agreement Type")
fig8.update_yaxes(title_text="# Queries", range=[0, 12])
fig8.update_traces(cliponaxis=False)
fig8.write_image("cve_c8_agreement.png")
with open("cve_c8_agreement.png.meta.json", "w") as f:
    json.dump({"caption": "Ranking Agreement Types Across Methods", "description": "Bar chart categorizing queries by how much methods agree on ranking"}, f)

# ==========================================
# CHART 9: NOVEL - "Score Spread Landscape" per query
# Scatter: head_mean(Cosine) vs head_mean(Taumode) sized by T/H improvement
# ==========================================
fig9 = go.Figure()

cosine_tail = df_tail[df_tail['tau_method'] == 'Cosine (τ=1.0)'].sort_values('query_id').reset_index(drop=True)
taumode_tail = df_tail[df_tail['tau_method'] == 'Taumode (τ=0.0.6)'].sort_values('query_id').reset_index(drop=True)
hybrid_tail = df_tail[df_tail['tau_method'] == 'Hybrid (τ=0.75)'].sort_values('query_id').reset_index(drop=True)

# Improvement in T/H ratio from Cosine to Taumode
th_improvement = taumode_tail['tail_to_head_ratio'].values - cosine_tail['tail_to_head_ratio'].values

fig9.add_trace(go.Scatter(
    x=cosine_tail['head_mean'],
    y=taumode_tail['head_mean'],
    mode='markers+text',
    marker=dict(
        size=np.abs(th_improvement) * 3000 + 10,
        color=th_improvement,
        colorscale='RdYlGn',
        cmin=-0.02, cmax=0.02,
        showscale=True,
        colorbar=dict(title="ΔT/H"),
        line=dict(width=1, color='black'),
    ),
    text=[f"Q{q}" for q in cosine_tail['query_id']],
    textposition='top center',
    textfont=dict(size=9),
    showlegend=False,
))

# Diagonal reference line
fig9.add_trace(go.Scatter(
    x=[0.75, 0.92], y=[0.75, 0.92],
    mode='lines', line=dict(dash='dash', color='gray'),
    name='Equal', showlegend=True,
))

fig9.update_layout(
    title={"text": "Head Score: Cosine vs Taumode<br><span style='font-size: 18px; font-weight: normal;'>All points above diagonal → Taumode boosts ALL head scores | Color=ΔT/H</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig9.update_xaxes(title_text="Cosine Head μ")
fig9.update_yaxes(title_text="Taumode Head μ")
fig9.write_image("cve_c9_head_scatter.png")
with open("cve_c9_head_scatter.png.meta.json", "w") as f:
    json.dump({"caption": "Head Score: Cosine vs Taumode", "description": "Scatter showing Taumode consistently above diagonal for head scores, sized by T/H improvement"}, f)

print("Charts 8-9 done")
