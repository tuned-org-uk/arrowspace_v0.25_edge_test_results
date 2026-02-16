
# ==========================================
# CHART 10: NOVEL - "Method Effectiveness Waterfall"
# Shows delta from majority-class baseline (accuracy=0.9062)
# ==========================================
majority_baseline_acc = 0.9062  # predicting all negative

fig10 = go.Figure()

# Collect best per method family per config
method_order = ['Lambda k-NN', 'UMAP 2D', 'Hybrid α=0.4', 'Hybrid α=0.6', 'Hybrid α=0.8', 'Hybrid α=0.9', 'Hybrid α=1.0', 'Cosine k-NN']

for cfg in configs:
    cfg_data = df_class[df_class['config'] == cfg]
    deltas = []
    for label, filt in method_families.items():
        if label not in method_order:
            continue
        subset = cfg_data[filt(cfg_data['method'])]
        best_bal = subset['balanced_accuracy'].max() if not subset.empty else 0.5
        delta = best_bal - 0.5  # Delta from random chance balanced acc
        deltas.append(delta)
    
    fig10.add_trace(go.Bar(
        x=method_order,
        y=deltas,
        name=config_short[cfg],
        marker_color=config_colors[cfg],
        opacity=0.85,
    ))

fig10.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Random (Bal Acc = 0.5)")

fig10.update_layout(
    barmode='group',
    title={"text": "Balanced Accuracy Lift Over Random<br><span style='font-size: 18px; font-weight: normal;'>ΔBalAcc from 0.5 baseline | Lambda/UMAP ≈ 0, Cosine ≈ +0.43</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig10.update_xaxes(title_text="Method", tickangle=-30)
fig10.update_yaxes(title_text="Δ Bal Accuracy")
fig10.update_traces(cliponaxis=False)
fig10.write_image("chart10_lift_waterfall.png")
with open("chart10_lift_waterfall.png.meta.json", "w") as f:
    json.dump({"caption": "Balanced Accuracy Lift Over Random Chance", "description": "Bar chart showing how much each method improves over random baseline"}, f)

print("Chart 10 done")
