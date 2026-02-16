
# ==========================================
# CHART 11: NOVEL - "Spectral Compression Efficiency"
# Dimensionality reduction ratio: 100k → lambda (scalar) vs UMAP (2D)
# Showing information preserved as measured by classification performance
# ==========================================

fig11 = go.Figure()

# Data: method, dims_out, best_f1, build_time
methods_dim = [
    ('Original 100k\n(Cosine k-NN)', 100000, 0.8667, 45.5),
    ('ArrowSpace λ\n(1D scalar)', 1, df_class[df_class['method'].str.startswith('knn_lambda')]['f1'].max(), 45.3),
    ('UMAP\n(2D)', 2, df_class[df_class['method'].str.startswith('umap_2d')]['f1'].max(), 92.1),
    ('Hybrid α=0.9\n(100k + 1D)', 100001, 
     df_class[(df_class['method'] == 'search_alpha0.9')]['f1'].max(), 391.0),
]

names = [m[0] for m in methods_dim]
f1s = [m[2] for m in methods_dim]
build_times = [m[3] for m in methods_dim]
dims = [m[1] for m in methods_dim]

# Log scale for dimensions
fig11.add_trace(go.Bar(
    x=names, y=f1s,
    marker_color=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12'],
    text=[f"F1={f:.3f}<br>{d} dims<br>{t:.0f}s" for f, d, t in zip(f1s, dims, build_times)],
    textposition='inside',
    textfont=dict(size=11),
))

fig11.update_layout(
    title={"text": "Compression vs Classification Quality<br><span style='font-size: 18px; font-weight: normal;'>100k→1D via λ loses all signal | 100k→2D via UMAP also fails</span>"},
)
fig11.update_xaxes(title_text="Method")
fig11.update_yaxes(title_text="F1 Score", range=[0, 1])
fig11.update_traces(cliponaxis=False)
fig11.write_image("chart11_compression_efficiency.png")
with open("chart11_compression_efficiency.png.meta.json", "w") as f:
    json.dump({"caption": "Compression Ratio vs Classification Quality", "description": "Bar chart comparing F1 across dimensionality reduction methods with build times"}, f)

print("Chart 11 done")
