
# ==========================================
# CHART 21: NOVEL - "Information Bottleneck" diagram
# How much info survives each compression stage
# ==========================================

# Stages: Original → JL Projection → Clustering → Laplacian → Lambda
# Measure: dimension count and classification capability

stages = ['Original', 'JL Proj', 'Clustering', 'Laplacian', 'Lambda (λ)']
dims = [100000, 220, 50, 220, 1]  # from log output
f1_capability = [0.867, 0.867, 0.867, 0.867, 0.0]  # approx
# Note: cosine still works on original features regardless of lambda
# Lambda alone captures 0% of class-discriminative info

fig21 = make_subplots(rows=1, cols=2, 
    subplot_titles=("Dimensionality Through Pipeline", "Classification Signal Retained"))

# Left: Dimension reduction (log scale)
fig21.add_trace(go.Scatter(
    x=stages, y=dims,
    mode='lines+markers+text',
    line=dict(width=3, color='#3498DB'),
    marker=dict(size=12),
    text=[f"{d:,}" for d in dims],
    textposition='top center',
    name='Dimensions',
), row=1, col=1)

fig21.update_yaxes(type='log', title_text="Dimensions", row=1, col=1)

# Right: Signal retention
fig21.add_trace(go.Scatter(
    x=stages, y=f1_capability,
    mode='lines+markers',
    line=dict(width=3, color='#E74C3C'),
    marker=dict(size=12),
    name='F1 Capability',
    fill='tozeroy',
    fillcolor='rgba(231,76,60,0.1)',
), row=1, col=2)

fig21.update_yaxes(title_text="F1 Score", range=[0, 1], row=1, col=2)

fig21.update_layout(
    title={"text": "ArrowSpace Information Bottleneck<br><span style='font-size: 18px; font-weight: normal;'>100k→1D compression | Classification signal lost at λ stage</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5),
    showlegend=False,
)
fig21.write_image("chart21_info_bottleneck.png")
with open("chart21_info_bottleneck.png.meta.json", "w") as f:
    json.dump({"caption": "ArrowSpace Information Bottleneck", "description": "Pipeline visualization showing dimensionality reduction and signal loss through ArrowSpace stages"}, f)

print("Chart 21 done")
