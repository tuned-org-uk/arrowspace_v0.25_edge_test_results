
# ==========================================
# CHART 9: NOVEL - "Spectral Diagnostic Dashboard" 
# Scatter: Cohen's d vs Best Hybrid F1, sized by Fiedler, colored by overlap
# ==========================================
fig9 = go.Figure()

for cfg in configs:
    sp = df_spectral[df_spectral['config'] == cfg].iloc[0]
    # Best hybrid F1 for this config
    hybrid_data = df_class[(df_class['config'] == cfg) & (df_class['method'].str.startswith('search_alpha'))]
    best_hybrid_f1 = hybrid_data['f1'].max()
    best_alpha = hybrid_data.loc[hybrid_data['f1'].idxmax(), 'alpha']
    
    fig9.add_trace(go.Scatter(
        x=[sp['cohens_d']],
        y=[best_hybrid_f1],
        mode='markers+text',
        marker=dict(
            size=sp['fiedler_value'] * 400 + 15,
            color=sp['overlap'],
            colorscale='RdYlGn_r',
            cmin=0.35, cmax=0.6,
            showscale=True,
            colorbar=dict(title="Overlap"),
            line=dict(width=2, color=config_colors[cfg]),
        ),
        text=[f"{config_short[cfg]}<br>α={best_alpha}"],
        textposition='top center',
        name=config_short[cfg],
        showlegend=False,
    ))

fig9.update_layout(
    title={"text": "Spectral Diagnostic: Can λ Predict F1?<br><span style='font-size: 18px; font-weight: normal;'>Cohen's d vs F1 | Size=Fiedler, Color=Overlap | Weak d → Weak F1</span>"},
)
fig9.update_xaxes(title_text="Cohen's d", range=[0.03, 0.1])
fig9.update_yaxes(title_text="Best Hybrid F1", range=[0.4, 1.0])
fig9.write_image("chart9_spectral_diagnostic.png")
with open("chart9_spectral_diagnostic.png.meta.json", "w") as f:
    json.dump({"caption": "Spectral Diagnostic: Cohen's d vs Best F1", "description": "Bubble chart showing relationship between spectral class separation and classification performance"}, f)

print("Chart 9 done")
