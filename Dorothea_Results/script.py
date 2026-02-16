
import pandas as pd
import numpy as np

# Load all data
df_class = pd.read_csv('007_dorothea_classification_results.csv')
df_lambda = pd.read_csv('007_dorothea_lambda_distributions.csv')
df_spectral = pd.read_csv('007_dorothea_spectral_metrics.csv')

# Load UMAP embeddings for all configs
umap_files = {
    'gaussian_best': '007_dorothea_umap_embeddings_gaussian_best.csv',
    'tight_clusters': '007_dorothea_umap_embeddings_tight_clusters.csv',
    'high_compression': '007_dorothea_umap_embeddings_high_compression.csv',
    'dense_graph': '007_dorothea_umap_embeddings_dense_graph.csv',
    'sparse_graph': '007_dorothea_umap_embeddings_sparse_graph.csv',
}

umap_dfs = {}
for k, v in umap_files.items():
    umap_dfs[k] = pd.read_csv(v)

print("=== Classification Results ===")
print(df_class.shape)
print(df_class.columns.tolist())
print(df_class.head(3))

print("\n=== Lambda Distributions ===")
print(df_lambda.shape)
print(df_lambda.columns.tolist())
print(df_lambda.head(3))

print("\n=== Spectral Metrics ===")
print(df_spectral.shape)
print(df_spectral.columns.tolist())
print(df_spectral)

print("\n=== UMAP sample ===")
print(umap_dfs['gaussian_best'].head(3))
print(umap_dfs['gaussian_best'].columns.tolist())
