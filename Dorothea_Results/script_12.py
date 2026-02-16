
# ==========================================
# CHART 13: NOVEL - "k-Sensitivity Curves" for cosine & lambda
# Show how k affects all metrics simultaneously
# ==========================================
fig13 = make_subplots(rows=1, cols=3,
    subplot_titles=("Lambda k-NN: k Effect", "Cosine k-NN: k Effect", "UMAP k-NN: k Effect"))

k_values = [1, 3, 5, 7, 11, 15]
metrics_to_plot = ['f1', 'balanced_accuracy', 'precision', 'recall']
metric_dashes = {'f1': 'solid', 'balanced_accuracy': 'dash', 'precision': 'dot', 'recall': 'dashdot'}
metric_labels = {'f1': 'F1', 'balanced_accuracy': 'Bal Acc', 'precision': 'Precision', 'recall': 'Recall'}

# Use gaussian_best as representative
cfg = 'gaussian_best'
cfg_data = df_class[df_class['config'] == cfg]

for col_idx, (prefix, title) in enumerate([('knn_lambda', 'Lambda'), ('knn_cosine', 'Cosine'), ('umap_2d', 'UMAP')]):
    subset = cfg_data[cfg_data['method'].str.startswith(prefix)].copy()
    subset['k_val'] = subset['method'].str.extract(r'_k(\d+)').astype(int)
    subset = subset.sort_values('k_val')
    
    for metric in metrics_to_plot:
        fig13.add_trace(go.Scatter(
            x=subset['k_val'], y=subset[metric],
            mode='lines+markers',
            name=metric_labels[metric],
            line=dict(dash=metric_dashes[metric], width=2),
            marker=dict(size=7),
            showlegend=(col_idx == 0),
        ), row=1, col=col_idx + 1)

for i in range(1, 4):
    fig13.update_xaxes(title_text="k", row=1, col=i)
    fig13.update_yaxes(title_text="Score", range=[-0.05, 1.05], row=1, col=i)

fig13.update_layout(
    title={"text": "k-Sensitivity: How Neighbors Affect Metrics<br><span style='font-size: 18px; font-weight: normal;'>Gaussian config | Lambda flat at 0, Cosine stable k≥3, UMAP noisy</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5),
)
fig13.write_image("chart13_k_sensitivity.png")
with open("chart13_k_sensitivity.png.meta.json", "w") as f:
    json.dump({"caption": "k-Sensitivity Curves: Lambda vs Cosine vs UMAP", "description": "Line charts showing how k parameter affects F1, balanced accuracy, precision, and recall for each method"}, f)

print("Chart 13 done")
