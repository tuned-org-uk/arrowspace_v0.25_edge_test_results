
# ==========================================
# CHART 5: Lambda Distribution by Class (Violin + Overlay)
# ==========================================
fig5 = go.Figure()

for i, cfg in enumerate(configs):
    cfg_data = df_lambda[df_lambda['config'] == cfg]
    pos = cfg_data[cfg_data['class'] == 'positive']['lambda']
    neg = cfg_data[cfg_data['class'] == 'negative']['lambda']
    
    fig5.add_trace(go.Violin(
        x=[config_short[cfg]] * len(pos), y=pos,
        legendgroup=cfg, scalegroup=cfg,
        name=f"{config_short[cfg]} +", side='positive',
        line_color='#E74C3C', fillcolor='rgba(231,76,60,0.3)',
        showlegend=(i == 0),
    ))
    fig5.add_trace(go.Violin(
        x=[config_short[cfg]] * len(neg), y=neg,
        legendgroup=cfg + '_neg', scalegroup=cfg,
        name=f"{config_short[cfg]} −", side='negative',
        line_color='#3498DB', fillcolor='rgba(52,152,219,0.3)',
        showlegend=(i == 0),
    ))

fig5.update_layout(
    violinmode='overlay',
    title={"text": "Lambda Distribution by Class<br><span style='font-size: 18px; font-weight: normal;'>Red = Positive, Blue = Negative | Near-total overlap explains F1=0</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig5.update_xaxes(title_text="Config")
fig5.update_yaxes(title_text="Lambda (λ)")
fig5.write_image("chart5_lambda_violins.png")
with open("chart5_lambda_violins.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda Distributions: Positive vs Negative Class", "description": "Violin plots showing lambda distributions per class and config, revealing near-total overlap"}, f)

print("Chart 5 done")
