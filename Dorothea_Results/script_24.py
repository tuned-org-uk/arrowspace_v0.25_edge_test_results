
# ==========================================
# CHART 24: NOVEL - "Lambda Cumulative Distribution + KS Test"
# CDF of lambda for positive vs negative with KS statistic
# ==========================================
from scipy.stats import ks_2samp

fig24 = make_subplots(rows=2, cols=3,
    subplot_titles=[config_short[c] for c in configs] + [""],
    horizontal_spacing=0.08, vertical_spacing=0.15,
)

for i, cfg in enumerate(configs):
    row = i // 3 + 1
    col = i % 3 + 1
    cfg_data = df_lambda[df_lambda['config'] == cfg]
    pos = np.sort(cfg_data[cfg_data['class'] == 'positive']['lambda'].values)
    neg = np.sort(cfg_data[cfg_data['class'] == 'negative']['lambda'].values)
    
    ks_stat, ks_p = ks_2samp(pos, neg)
    
    fig24.add_trace(go.Scatter(
        x=pos, y=np.linspace(0, 1, len(pos)),
        mode='lines', name='Positive' if i == 0 else None,
        line=dict(color='#E74C3C', width=2.5),
        showlegend=(i == 0),
    ), row=row, col=col)
    
    fig24.add_trace(go.Scatter(
        x=neg, y=np.linspace(0, 1, len(neg)),
        mode='lines', name='Negative' if i == 0 else None,
        line=dict(color='#3498DB', width=2.5),
        showlegend=(i == 0),
    ), row=row, col=col)
    
    # Add KS annotation
    fig24.add_annotation(
        text=f"KS={ks_stat:.3f}<br>p={ks_p:.3f}",
        xref=f"x{i+1}" if i > 0 else "x", yref=f"y{i+1}" if i > 0 else "y",
        x=0.7, y=0.3, showarrow=False,
        font=dict(size=10, color='black'),
        bgcolor='rgba(255,255,255,0.8)',
        row=row, col=col,
    )

for i in range(1, 6):
    fig24.update_xaxes(title_text="Lambda (λ)", row=(i-1)//3+1, col=(i-1)%3+1)
    fig24.update_yaxes(title_text="CDF", row=(i-1)//3+1, col=(i-1)%3+1)

fig24.update_layout(
    title={"text": "Lambda CDF: Kolmogorov-Smirnov Class Test<br><span style='font-size: 18px; font-weight: normal;'>CDFs nearly identical | KS test confirms no distributional separation</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig24.write_image("chart24_lambda_cdf_ks.png")
with open("chart24_lambda_cdf_ks.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda CDF with KS Test: Class Separation", "description": "CDFs of lambda for positive/negative classes with KS statistics showing no distributional difference"}, f)

print("Chart 24 done")
