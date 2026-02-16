
# ==========================================
# CHART 15: NOVEL - "Search Time Budget Analysis"
# How much time does spectral search cost per marginal F1 gain?
# ==========================================
fig15 = go.Figure()

for cfg in configs:
    cfg_data = df_class[df_class['config'] == cfg]
    
    # Cosine baseline
    cosine_best = cfg_data[cfg_data['method'].str.startswith('knn_cosine')]
    cosine_f1 = cosine_best['f1'].max()
    cosine_time = cosine_best['query_time_s'].mean()
    
    # Alpha sweep
    alpha_data = cfg_data[cfg_data['method'].str.startswith('search_alpha')].sort_values('alpha')
    
    fig15.add_trace(go.Scatter(
        x=alpha_data['query_time_s'],
        y=alpha_data['f1'],
        mode='markers+lines+text',
        name=config_short[cfg],
        marker=dict(size=10, color=config_colors[cfg]),
        line=dict(color=config_colors[cfg], width=2),
        text=[f"α={a}" for a in alpha_data['alpha']],
        textposition='top center',
        textfont=dict(size=8),
    ))
    
    # Cosine baseline point
    fig15.add_trace(go.Scatter(
        x=[cosine_time], y=[cosine_f1],
        mode='markers',
        marker=dict(size=16, color=config_colors[cfg], symbol='star', line=dict(width=2, color='black')),
        name=f'{config_short[cfg]} Cosine ★',
        showlegend=False,
    ))

fig15.update_layout(
    title={"text": "Time vs F1: Is Spectral Search Worth It?<br><span style='font-size: 18px; font-weight: normal;'>★ = Cosine baseline | Hybrid takes 8x longer for ≤0 F1 gain</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig15.update_xaxes(title_text="Query Time (s)")
fig15.update_yaxes(title_text="F1 Score", range=[0.3, 1.0])
fig15.write_image("chart15_time_vs_f1.png")
with open("chart15_time_vs_f1.png.meta.json", "w") as f:
    json.dump({"caption": "Time-F1 Tradeoff: Search Cost Analysis", "description": "Scatter showing query time vs F1 for hybrid search versus cosine baseline"}, f)

print("Chart 15 done")
