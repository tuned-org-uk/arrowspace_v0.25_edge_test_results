
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import pandas as pd
import numpy as np

# Reload data
df_class = pd.read_csv('007_dorothea_classification_results.csv')
df_lambda = pd.read_csv('007_dorothea_lambda_distributions.csv')
df_spectral = pd.read_csv('007_dorothea_spectral_metrics.csv')

umap_files = {
    'gaussian_best': '007_dorothea_umap_embeddings_gaussian_best.csv',
    'tight_clusters': '007_dorothea_umap_embeddings_tight_clusters.csv',
    'high_compression': '007_dorothea_umap_embeddings_high_compression.csv',
    'dense_graph': '007_dorothea_umap_embeddings_dense_graph.csv',
    'sparse_graph': '007_dorothea_umap_embeddings_sparse_graph.csv',
}
umap_dfs = {k: pd.read_csv(v) for k, v in umap_files.items()}

configs = df_class['config'].unique().tolist()
config_colors = {
    'gaussian_best': '#1E90FF',
    'tight_clusters': '#FF6B35',
    'high_compression': '#2ECC71',
    'dense_graph': '#9B59B6',
    'sparse_graph': '#E74C3C',
}
config_short = {
    'gaussian_best': 'Gaussian',
    'tight_clusters': 'Tight',
    'high_compression': 'HiCompress',
    'dense_graph': 'Dense',
    'sparse_graph': 'Sparse',
}

# ==========================================
# CHART 1: Classification F1 Comparison (Grouped Bar)
# ==========================================
method_groups = {
    'Lambda k-NN': 'knn_lambda',
    'Cosine k-NN': 'knn_cosine',
    'UMAP 2D k-NN': 'umap_2d',
    'Hybrid α=0.4': 'search_alpha0.4',
    'Hybrid α=0.6': 'search_alpha0.6',
    'Hybrid α=0.8': 'search_alpha0.8',
    'Hybrid α=0.9': 'search_alpha0.9',
    'Hybrid α=1.0': 'search_alpha1.0',
}

fig1 = go.Figure()
for ci, cfg in enumerate(configs):
    cfg_data = df_class[df_class['config'] == cfg]
    best_f1s = []
    labels = []
    for label, prefix in method_groups.items():
        subset = cfg_data[cfg_data['method'].str.startswith(prefix) if not prefix.startswith('search') else cfg_data['method'] == prefix]
        if subset.empty:
            subset = cfg_data[cfg_data['method'] == prefix]
        best_f1 = subset['f1'].max() if not subset.empty else 0
        best_f1s.append(best_f1)
        labels.append(label)
    
    fig1.add_trace(go.Bar(
        name=config_short[cfg],
        x=labels,
        y=best_f1s,
        marker_color=config_colors[cfg],
        opacity=0.85,
    ))

fig1.update_layout(
    barmode='group',
    title={"text": "Best F1 by Method & Config<br><span style='font-size: 18px; font-weight: normal;'>Dorothea 100k features | Lambda fails, Cosine dominates</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig1.update_xaxes(title_text="Method", tickangle=-30)
fig1.update_yaxes(title_text="F1 Score", range=[0, 1])
fig1.update_traces(cliponaxis=False)
fig1.write_image("chart1_f1_comparison.png")
with open("chart1_f1_comparison.png.meta.json", "w") as f:
    json.dump({"caption": "F1 Score: All Methods vs Configs", "description": "Grouped bar chart of best F1 across Lambda, Cosine, UMAP, and Hybrid methods for each graph configuration"}, f)

print("Chart 1 done")
