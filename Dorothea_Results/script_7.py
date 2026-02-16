
# ==========================================
# CHART 8: NOVEL - Lambda-UMAP Fusion (Color by Lambda, shape by class)
# ==========================================
fig8 = make_subplots(
    rows=2, cols=3,
    subplot_titles=[config_short[c] for c in configs] + [""],
    horizontal_spacing=0.06, vertical_spacing=0.12,
)

for i, cfg in enumerate(configs):
    row = i // 3 + 1
    col = i % 3 + 1
    udf = umap_dfs[cfg].copy()
    
    # Merge lambda values
    cfg_lambda = df_lambda[df_lambda['config'] == cfg].reset_index(drop=True)
    # Match by sample_id
    udf = udf.merge(
        cfg_lambda.assign(sample_id=range(len(cfg_lambda))),
        on='sample_id', how='left', suffixes=('', '_lam')
    )
    
    # Positive class
    pos = udf[udf['label'] == 1]
    neg = udf[udf['label'] == -1]
    
    fig8.add_trace(go.Scatter(
        x=neg['umap1'], y=neg['umap2'],
        mode='markers',
        marker=dict(
            size=4, color=neg['lambda'], colorscale='Viridis',
            opacity=0.4, symbol='circle',
            showscale=(i == 0),
            colorbar=dict(title="Lambda", x=1.02) if i == 0 else None,
        ),
        name='Negative', showlegend=(i == 0),
    ), row=row, col=col)
    
    fig8.add_trace(go.Scatter(
        x=pos['umap1'], y=pos['umap2'],
        mode='markers',
        marker=dict(
            size=8, color=pos['lambda'], colorscale='Viridis',
            opacity=0.9, symbol='diamond',
            line=dict(width=1, color='red'),
        ),
        name='Positive', showlegend=(i == 0),
    ), row=row, col=col)

fig8.update_layout(
    title={"text": "Lambda on UMAP: Spectral Geography<br><span style='font-size: 18px; font-weight: normal;'>Color = λ value, ◆ = Positive | λ is spatially diffuse, not class-aligned</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig8.write_image("chart8_lambda_umap_fusion.png")
with open("chart8_lambda_umap_fusion.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda-UMAP Fusion: Spectral Geography", "description": "UMAP plots with lambda as color showing spectral values are spatially diffuse and not class-aligned"}, f)

print("Chart 8 done")
