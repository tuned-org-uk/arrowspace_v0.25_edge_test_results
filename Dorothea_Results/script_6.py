
# ==========================================
# CHART 7: UMAP Embeddings Colored by Class (5 configs in grid)
# ==========================================
fig7 = make_subplots(
    rows=2, cols=3,
    subplot_titles=[config_short[c] for c in configs] + [""],
    horizontal_spacing=0.06, vertical_spacing=0.12,
)

class_colors = {1: '#E74C3C', -1: '#3498DB'}
class_names = {1: 'Positive', -1: 'Negative'}

for i, cfg in enumerate(configs):
    row = i // 3 + 1
    col = i % 3 + 1
    udf = umap_dfs[cfg]
    
    for cls_val, cls_name in class_names.items():
        subset = udf[udf['label'] == cls_val]
        fig7.add_trace(go.Scatter(
            x=subset['umap1'], y=subset['umap2'],
            mode='markers',
            marker=dict(size=4, color=class_colors[cls_val], opacity=0.5),
            name=cls_name,
            showlegend=(i == 0),
        ), row=row, col=col)

fig7.update_layout(
    title={"text": "UMAP 2D Projections by Config<br><span style='font-size: 18px; font-weight: normal;'>Red = Positive, Blue = Negative | Classes overlap in all configs</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
for i in range(1, 7):
    fig7.update_xaxes(title_text="UMAP 1", row=(i-1)//3+1, col=(i-1)%3+1)
    fig7.update_yaxes(title_text="UMAP 2", row=(i-1)//3+1, col=(i-1)%3+1)
fig7.write_image("chart7_umap_grid.png")
with open("chart7_umap_grid.png.meta.json", "w") as f:
    json.dump({"caption": "UMAP 2D Projections: All 5 Configs", "description": "Grid of UMAP scatter plots colored by class label across all graph wiring configurations"}, f)

print("Chart 7 done")
