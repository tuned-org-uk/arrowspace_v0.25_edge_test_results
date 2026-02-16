
# ==========================================
# FINAL SUMMARY CHART 25: "The Verdict" - Comprehensive comparison strip
# ==========================================

# Method | Best F1 | Best BalAcc | Avg Build | Class sep possible? | Search value?
summary_data = {
    'Method': ['Lambda k-NN', 'UMAP 2D', 'Hybrid α=0.4', 'Hybrid α=0.6', 'Hybrid α=0.8', 'Hybrid α=0.9', 'Hybrid α=1.0', 'Cosine k-NN'],
    'Best F1': [0, 0.24, 0.593, 0.774, 0.741, 0.857, 0.839, 0.867],
    'Best BalAcc': [0.511, 0.576, 0.753, 0.886, 0.845, 0.923, 0.923, 0.926],
    'Spectral %': [100, 0, 60, 40, 20, 10, 0, 0],
}

# Compute actual bests from data
for i, (prefix, alpha_val) in enumerate([
    ('knn_lambda', None), ('umap_2d', None),
    ('search_alpha0.4', 0.4), ('search_alpha0.6', 0.6),
    ('search_alpha0.8', 0.8), ('search_alpha0.9', 0.9),
    ('search_alpha1.0', 1.0), ('knn_cosine', None)
]):
    if alpha_val is not None:
        subset = df_class[df_class['method'] == prefix]
    else:
        subset = df_class[df_class['method'].str.startswith(prefix)]
    
    if not subset.empty:
        summary_data['Best F1'][i] = subset['f1'].max()
        summary_data['Best BalAcc'][i] = subset['balanced_accuracy'].max()

sdf = pd.DataFrame(summary_data)

fig25 = make_subplots(rows=1, cols=2,
    subplot_titles=("F1 Score by Method", "Balanced Accuracy by Method"))

colors_bar = ['#E74C3C', '#2ECC71', '#F39C12', '#F39C12', '#F39C12', '#F39C12', '#F39C12', '#3498DB']

fig25.add_trace(go.Bar(
    y=sdf['Method'], x=sdf['Best F1'],
    orientation='h',
    marker_color=colors_bar,
    text=[f"{v:.3f}" for v in sdf['Best F1']],
    textposition='outside',
    showlegend=False,
), row=1, col=1)

fig25.add_trace(go.Bar(
    y=sdf['Method'], x=sdf['Best BalAcc'],
    orientation='h',
    marker_color=colors_bar,
    text=[f"{v:.3f}" for v in sdf['Best BalAcc']],
    textposition='outside',
    showlegend=False,
), row=1, col=2)

fig25.update_xaxes(title_text="F1 Score", range=[0, 1.1], row=1, col=1)
fig25.update_xaxes(title_text="Bal Accuracy", range=[0, 1.1], row=1, col=2)

fig25.update_layout(
    title={"text": "The Verdict: Method Performance Ranking<br><span style='font-size: 18px; font-weight: normal;'>Red=Lambda, Green=UMAP, Orange=Hybrid, Blue=Cosine | Best across all configs</span>"},
)
fig25.update_traces(cliponaxis=False)
fig25.write_image("chart25_verdict.png")
with open("chart25_verdict.png.meta.json", "w") as f:
    json.dump({"caption": "The Verdict: Full Method Ranking", "description": "Horizontal bar chart ranking all methods by best F1 and balanced accuracy across all configs"}, f)

print("Chart 25 done")
print("\nAll 25 charts generated successfully!")
