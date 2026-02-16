
# ==========================================
# CHART 22: NOVEL - "UMAP Lambda Contour" 
# Lambda as a continuous field over UMAP space
# ==========================================
from scipy.interpolate import griddata

fig22 = make_subplots(rows=2, cols=3,
    subplot_titles=[config_short[c] for c in configs] + [""],
    horizontal_spacing=0.08, vertical_spacing=0.12,
)

for i, cfg in enumerate(configs):
    row = i // 3 + 1
    col = i % 3 + 1
    udf = umap_dfs[cfg].copy()
    cfg_lambda = df_lambda[df_lambda['config'] == cfg].reset_index(drop=True)
    udf['lambda_val'] = cfg_lambda['lambda'].values
    
    # Create grid
    xi = np.linspace(udf['umap1'].min(), udf['umap1'].max(), 50)
    yi = np.linspace(udf['umap2'].min(), udf['umap2'].max(), 50)
    xi, yi = np.meshgrid(xi, yi)
    
    # Interpolate lambda onto grid
    zi = griddata(
        (udf['umap1'].values, udf['umap2'].values),
        udf['lambda_val'].values,
        (xi, yi),
        method='cubic'
    )
    
    fig22.add_trace(go.Contour(
        x=np.linspace(udf['umap1'].min(), udf['umap1'].max(), 50),
        y=np.linspace(udf['umap2'].min(), udf['umap2'].max(), 50),
        z=zi,
        colorscale='Viridis',
        showscale=(i == 0),
        contours=dict(showlabels=False),
        ncontours=15,
        opacity=0.7,
        colorbar=dict(title="Lambda") if i == 0 else None,
    ), row=row, col=col)
    
    # Overlay positive class markers
    pos = udf[udf['label'] == 1]
    fig22.add_trace(go.Scatter(
        x=pos['umap1'], y=pos['umap2'],
        mode='markers',
        marker=dict(size=5, color='red', symbol='x', line=dict(width=1)),
        showlegend=(i == 0),
        name='Positive',
    ), row=row, col=col)

fig22.update_layout(
    title={"text": "Lambda Contour Fields Over UMAP Space<br><span style='font-size: 18px; font-weight: normal;'>× = Positive class | Lambda topology doesn't align with class regions</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig22.write_image("chart22_lambda_contour.png")
with open("chart22_lambda_contour.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda Contour Fields Over UMAP Space", "description": "Contour maps of lambda values interpolated onto UMAP embedding with positive class markers"}, f)

print("Chart 22 done")
