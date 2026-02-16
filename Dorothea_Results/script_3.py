
# ==========================================
# CHART 3: Alpha Sweep - F1 vs Alpha for all configs (Search Analysis)
# ==========================================
fig3 = go.Figure()

for cfg in configs:
    cfg_data = df_class[(df_class['config'] == cfg) & (df_class['method'].str.startswith('search_alpha'))]
    cfg_data = cfg_data.sort_values('alpha')
    
    # Add cosine baseline as dashed line
    cosine_best = df_class[(df_class['config'] == cfg) & (df_class['method'].str.startswith('knn_cosine'))]['f1'].max()
    
    fig3.add_trace(go.Scatter(
        x=cfg_data['alpha'],
        y=cfg_data['f1'],
        mode='lines+markers',
        name=config_short[cfg],
        line=dict(color=config_colors[cfg], width=3),
        marker=dict(size=10),
    ))

# Add cosine baseline (same for all configs)
cosine_baseline = df_class[df_class['method'].str.startswith('knn_cosine')]['f1'].max()
fig3.add_hline(y=cosine_baseline, line_dash="dash", line_color="gray", 
               annotation_text=f"Cosine baseline F1={cosine_baseline:.3f}")

fig3.update_layout(
    title={"text": "Hybrid Search: F1 vs Alpha<br><span style='font-size: 18px; font-weight: normal;'>α=1.0 pure cosine, α=0.0 pure spectral | Spectral hurts F1</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig3.update_xaxes(title_text="Alpha (α)", dtick=0.1)
fig3.update_yaxes(title_text="F1 Score", range=[0.3, 1.0])
fig3.write_image("chart3_alpha_sweep_f1.png")
with open("chart3_alpha_sweep_f1.png.meta.json", "w") as f:
    json.dump({"caption": "Hybrid Search F1 vs Alpha Parameter", "description": "Line chart of F1 score across alpha sweep for each graph configuration, with cosine baseline"}, f)

# ==========================================
# CHART 4: Alpha Sweep - Balanced Accuracy & Precision/Recall tradeoff
# ==========================================
fig4 = make_subplots(rows=1, cols=2, subplot_titles=("Balanced Accuracy vs α", "Precision vs Recall by α"))

for cfg in configs:
    cfg_data = df_class[(df_class['config'] == cfg) & (df_class['method'].str.startswith('search_alpha'))].sort_values('alpha')
    
    fig4.add_trace(go.Scatter(
        x=cfg_data['alpha'], y=cfg_data['balanced_accuracy'],
        mode='lines+markers', name=config_short[cfg],
        line=dict(color=config_colors[cfg], width=2),
        marker=dict(size=8), showlegend=True,
    ), row=1, col=1)
    
    fig4.add_trace(go.Scatter(
        x=cfg_data['precision'], y=cfg_data['recall'],
        mode='lines+markers+text', name=config_short[cfg],
        line=dict(color=config_colors[cfg], width=2),
        marker=dict(size=8),
        text=[f"α={a}" for a in cfg_data['alpha']],
        textposition='top center', textfont=dict(size=8),
        showlegend=False,
    ), row=1, col=2)

fig4.update_xaxes(title_text="Alpha (α)", row=1, col=1)
fig4.update_yaxes(title_text="Balanced Acc", row=1, col=1)
fig4.update_xaxes(title_text="Precision", row=1, col=2)
fig4.update_yaxes(title_text="Recall", row=1, col=2)
fig4.update_layout(
    title={"text": "Search Tradeoffs Across Alpha<br><span style='font-size: 18px; font-weight: normal;'>Higher α → more cosine | Precision-Recall reveals spectral tension</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5),
)
fig4.write_image("chart4_alpha_tradeoffs.png")
with open("chart4_alpha_tradeoffs.png.meta.json", "w") as f:
    json.dump({"caption": "Hybrid Search: Balanced Accuracy & PR Tradeoff", "description": "Dual panel showing balanced accuracy vs alpha and precision-recall curves colored by alpha"}, f)

print("Charts 3 & 4 done")
