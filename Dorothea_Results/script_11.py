
# ==========================================
# CHART 12: NOVEL - "Lambda Entropy Landscape" 
# KDE of lambda distributions showing how the manifold L sees the data
# ==========================================
from scipy.stats import gaussian_kde

fig12 = make_subplots(rows=1, cols=2, 
    subplot_titles=("Lambda KDE by Config", "Lambda KDE by Class (Stacked)"))

# Panel 1: All configs overlaid
for cfg in configs:
    vals = df_lambda[df_lambda['config'] == cfg]['lambda'].values
    kde = gaussian_kde(vals, bw_method=0.1)
    x_range = np.linspace(0, 1, 300)
    fig12.add_trace(go.Scatter(
        x=x_range, y=kde(x_range),
        mode='lines', name=config_short[cfg],
        line=dict(color=config_colors[cfg], width=2.5),
        fill='tonexty' if cfg == configs[0] else None,
    ), row=1, col=1)

# Panel 2: Positive vs Negative (averaged across configs)
for cls, cls_name, color in [('positive', 'Positive', '#E74C3C'), ('negative', 'Negative', '#3498DB')]:
    all_vals = df_lambda[df_lambda['class'] == cls]['lambda'].values
    kde = gaussian_kde(all_vals, bw_method=0.1)
    x_range = np.linspace(0, 1, 300)
    fig12.add_trace(go.Scatter(
        x=x_range, y=kde(x_range),
        mode='lines', name=cls_name,
        line=dict(color=color, width=3),
        fill='tozeroy',
        opacity=0.5,
    ), row=1, col=2)

fig12.update_xaxes(title_text="Lambda (λ)", row=1, col=1)
fig12.update_yaxes(title_text="Density", row=1, col=1)
fig12.update_xaxes(title_text="Lambda (λ)", row=1, col=2)
fig12.update_yaxes(title_text="Density", row=1, col=2)
fig12.update_layout(
    title={"text": "Lambda Density Landscape<br><span style='font-size: 18px; font-weight: normal;'>Manifold L=Laplacian(Cᵀ) | Config shifts mean, classes remain inseparable</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5),
)
fig12.write_image("chart12_lambda_kde.png")
with open("chart12_lambda_kde.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda Density Landscape: Config & Class KDEs", "description": "KDE plots of lambda distributions showing config shifts and class inseparability"}, f)

print("Chart 12 done")
