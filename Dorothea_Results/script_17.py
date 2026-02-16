
# ==========================================
# CHART 18: NOVEL - "Spectral Gap × Build Time × F1 Bubble"
# 3-variable visualization: what predicts success?
# ==========================================
fig18 = go.Figure()

for cfg in configs:
    sp = df_spectral[df_spectral['config'] == cfg].iloc[0]
    cfg_data = df_class[df_class['config'] == cfg]
    
    # Collect all methods for this config
    for prefix, label in [('knn_lambda', 'Lambda'), ('knn_cosine', 'Cosine'), ('search_alpha', 'Hybrid')]:
        subset = cfg_data[cfg_data['method'].str.startswith(prefix)]
        if subset.empty:
            continue
        best = subset.loc[subset['f1'].idxmax()]
        
        fig18.add_trace(go.Scatter(
            x=[sp['spectral_gap'] * 1000],  # Scale for readability
            y=[best['f1']],
            mode='markers',
            marker=dict(
                size=best['build_time_s'] / 3 + 5,
                color=config_colors[cfg],
                symbol='circle' if label == 'Lambda' else ('diamond' if label == 'Cosine' else 'square'),
                line=dict(width=1, color='black'),
                opacity=0.7,
            ),
            name=f"{config_short[cfg]} {label}",
            hovertext=f"{config_short[cfg]} {label}<br>F1={best['f1']:.3f}<br>Gap={sp['spectral_gap']:.4f}<br>Build={best['build_time_s']:.0f}s",
        ))

fig18.update_layout(
    title={"text": "Spectral Gap vs F1 (Sized by Build Time)<br><span style='font-size: 18px; font-weight: normal;'>●=Lambda, ◆=Cosine, ■=Hybrid | Gap doesn't predict F1 on Dorothea</span>"},
    legend=dict(font=dict(size=9)),
)
fig18.update_xaxes(title_text="Spectral Gap (×1000)")
fig18.update_yaxes(title_text="Best F1")
fig18.write_image("chart18_gap_f1_bubble.png")
with open("chart18_gap_f1_bubble.png.meta.json", "w") as f:
    json.dump({"caption": "Spectral Gap vs F1 Bubble Chart", "description": "Multi-variable bubble chart showing spectral gap, F1, and build time"}, f)

print("Chart 18 done")
