
# ==========================================
# CHART 2: Balanced Accuracy Heatmap (Method x Config)
# ==========================================
methods_ordered = []
for m in df_class['method'].unique():
    methods_ordered.append(m)

# Create a pivot for balanced accuracy - best k per method family
method_families = {
    'Lambda k-NN': lambda x: x.str.startswith('knn_lambda'),
    'Cosine k-NN': lambda x: x.str.startswith('knn_cosine'),
    'UMAP 2D': lambda x: x.str.startswith('umap_2d'),
    'Hybrid α=0.4': lambda x: x == 'search_alpha0.4',
    'Hybrid α=0.6': lambda x: x == 'search_alpha0.6',
    'Hybrid α=0.8': lambda x: x == 'search_alpha0.8',
    'Hybrid α=0.9': lambda x: x == 'search_alpha0.9',
    'Hybrid α=1.0': lambda x: x == 'search_alpha1.0',
}

heat_data = []
for cfg in configs:
    cfg_data = df_class[df_class['config'] == cfg]
    row = {}
    for label, filt in method_families.items():
        subset = cfg_data[filt(cfg_data['method'])]
        if not subset.empty:
            row[label] = subset['balanced_accuracy'].max()
        else:
            row[label] = 0
    heat_data.append(row)

heat_df = pd.DataFrame(heat_data, index=[config_short[c] for c in configs])

fig2 = go.Figure(data=go.Heatmap(
    z=heat_df.values,
    x=heat_df.columns.tolist(),
    y=heat_df.index.tolist(),
    colorscale='RdYlGn',
    text=np.round(heat_df.values, 3).astype(str),
    texttemplate="%{text}",
    textfont={"size": 12},
    zmin=0.4, zmax=1.0,
    colorbar=dict(title="Bal Acc"),
))
fig2.update_layout(
    title={"text": "Balanced Accuracy Heatmap<br><span style='font-size: 18px; font-weight: normal;'>Method × Config | Green = high, Red = random chance (~0.5)</span>"},
)
fig2.update_xaxes(title_text="Method", tickangle=-30)
fig2.update_yaxes(title_text="Config")
fig2.write_image("chart2_balanced_acc_heatmap.png")
with open("chart2_balanced_acc_heatmap.png.meta.json", "w") as f:
    json.dump({"caption": "Balanced Accuracy Heatmap: Method × Config", "description": "Heatmap showing balanced accuracy for every method-config pair"}, f)

print("Chart 2 done")
