
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Load all CVE data
df_search = pd.read_csv('cve_search_results.csv')
df_metrics = pd.read_csv('cve_comparison_metrics.csv')
df_summary = pd.read_csv('cve_summary.csv')
df_tail = pd.read_csv('cve_tail_metrics.csv')

# Quick inspect
print("=== Search Results ===")
print(df_search.shape, df_search.columns.tolist())
print(f"Queries: {df_search['query_id'].nunique()}, Methods: {df_search['tau_method'].unique()}")
print(f"Ranks: {df_search['rank'].min()}-{df_search['rank'].max()}")

print("\n=== Comparison Metrics ===")
print(df_metrics.shape)
print(df_metrics.head(3))

print("\n=== Summary ===")
print(df_summary)

print("\n=== Tail Metrics ===")
print(df_tail.shape)
print(df_tail.columns.tolist())
print(df_tail.head(3))

# Query short names for readability
query_short = {}
for _, row in df_metrics.iterrows():
    qid = row['query_id']
    text = row['query_text']
    # Take first 30 chars
    query_short[qid] = f"Q{qid}: {text[:35]}..."
    
print("\n=== Query Short Names ===")
for k,v in query_short.items():
    print(v)
