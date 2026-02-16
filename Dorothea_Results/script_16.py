
# ==========================================
# CHART 17: NOVEL - "Manifold Invariant: Effective Rank vs Participation Ratio"
# Shows how close each config is to full-rank (no compression)
# ==========================================
fig17 = go.Figure()

# Theoretical max: N items = 800
n_items = 800

for cfg in configs:
    sp = df_spectral[df_spectral['config'] == cfg].iloc[0]
    fig17.add_trace(go.Scatter(
        x=[sp['effective_rank']],
        y=[sp['participation_ratio']],
        mode='markers+text',
        marker=dict(
            size=30,
            color=config_colors[cfg],
            line=dict(width=2, color='white'),
        ),
        text=[config_short[cfg]],
        textposition='top center',
        name=config_short[cfg],
    ))

# Add diagonal (perfect correlation line)
fig17.add_trace(go.Scatter(
    x=[650, 760], y=[650, 760],
    mode='lines', line=dict(dash='dash', color='gray'),
    name='EffRank=PartRatio', showlegend=True,
))

# Add N=800 reference
fig17.add_vline(x=800, line_dash="dot", line_color="red", annotation_text="N=800")
fig17.add_hline(y=800, line_dash="dot", line_color="red")

fig17.update_layout(
    title={"text": "Effective Rank vs Participation Ratio<br><span style='font-size: 18px; font-weight: normal;'>Both near N=800 → near full-rank, minimal spectral compression</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig17.update_xaxes(title_text="Effective Rank", range=[700, 810])
fig17.update_yaxes(title_text="Part. Ratio", range=[640, 810])
fig17.write_image("chart17_rank_vs_participation.png")
with open("chart17_rank_vs_participation.png.meta.json", "w") as f:
    json.dump({"caption": "Effective Rank vs Participation Ratio", "description": "Scatter showing both metrics near N=800, indicating minimal spectral compression"}, f)

print("Chart 17 done")
