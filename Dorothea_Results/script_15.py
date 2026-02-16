
# ==========================================
# CHART 16: NOVEL - "Lambda Quantile Classification" 
# Split items into lambda quantiles and show class composition
# ==========================================
fig16 = make_subplots(rows=2, cols=3,
    subplot_titles=[config_short[c] for c in configs] + [""],
    horizontal_spacing=0.08, vertical_spacing=0.15,
)

n_bins = 10
for i, cfg in enumerate(configs):
    row = i // 3 + 1
    col = i % 3 + 1
    cfg_data = df_lambda[df_lambda['config'] == cfg].copy()
    cfg_data['quantile'] = pd.qcut(cfg_data['lambda'], n_bins, labels=False, duplicates='drop')
    
    # Count positive and negative per quantile
    pivot = cfg_data.groupby(['quantile', 'class']).size().unstack(fill_value=0)
    if 'positive' not in pivot.columns:
        pivot['positive'] = 0
    if 'negative' not in pivot.columns:
        pivot['negative'] = 0
    
    # Positive rate per quantile
    total = pivot['positive'] + pivot['negative']
    pos_rate = pivot['positive'] / total
    
    fig16.add_trace(go.Bar(
        x=[f"Q{q}" for q in pivot.index],
        y=pos_rate.values,
        marker_color=config_colors[cfg],
        showlegend=False,
    ), row=row, col=col)
    
    # Add expected rate line
    fig16.add_hline(y=0.098, line_dash="dash", line_color="red", 
                    row=row, col=col, annotation_text="Base rate" if i==0 else None)

for i in range(1, 6):
    fig16.update_xaxes(title_text="λ Quantile", row=(i-1)//3+1, col=(i-1)%3+1)
    fig16.update_yaxes(title_text="Pos Rate", row=(i-1)//3+1, col=(i-1)%3+1, range=[0, 0.25])

fig16.update_layout(
    title={"text": "Positive Rate Across Lambda Quantiles<br><span style='font-size: 18px; font-weight: normal;'>Dashed = 9.8% base rate | No quantile enriches positives consistently</span>"},
)
fig16.write_image("chart16_lambda_quantile_class.png")
with open("chart16_lambda_quantile_class.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda Quantile Class Composition", "description": "Bar charts showing positive class rate per lambda decile across configs"}, f)

print("Chart 16 done")
