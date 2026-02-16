
# ==========================================
# CHART 14: NOVEL - "Spectral Metric Correlation Matrix"
# Correlate spectral metrics with classification outcomes
# ==========================================
# Build merged dataframe: spectral metrics → best F1/bal_acc per config
merged = df_spectral.copy()
for cfg in configs:
    idx = merged[merged['config'] == cfg].index[0]
    
    # Best lambda F1
    merged.loc[idx, 'lambda_best_f1'] = df_class[(df_class['config'] == cfg) & 
        (df_class['method'].str.startswith('knn_lambda'))]['f1'].max()
    
    # Best cosine F1
    merged.loc[idx, 'cosine_best_f1'] = df_class[(df_class['config'] == cfg) & 
        (df_class['method'].str.startswith('knn_cosine'))]['f1'].max()
    
    # Best hybrid F1
    merged.loc[idx, 'hybrid_best_f1'] = df_class[(df_class['config'] == cfg) & 
        (df_class['method'].str.startswith('search_alpha'))]['f1'].max()
    
    # Best hybrid balanced acc
    merged.loc[idx, 'hybrid_best_bal'] = df_class[(df_class['config'] == cfg) & 
        (df_class['method'].str.startswith('search_alpha'))]['balanced_accuracy'].max()
    
    # Best alpha
    best_row = df_class[(df_class['config'] == cfg) & (df_class['method'].str.startswith('search_alpha'))].sort_values('f1', ascending=False).iloc[0]
    merged.loc[idx, 'best_alpha'] = best_row['alpha']

corr_cols = ['lambda_mean', 'lambda_std', 'lambda_cv', 'spectral_gap', 'fiedler_value', 
             'effective_rank', 'participation_ratio', 'cohens_d', 'overlap',
             'hybrid_best_f1', 'hybrid_best_bal', 'best_alpha']
corr_matrix = merged[corr_cols].corr()

fig14 = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=[c.replace('_', ' ').title()[:15] for c in corr_cols],
    y=[c.replace('_', ' ').title()[:15] for c in corr_cols],
    colorscale='RdBu_r',
    zmin=-1, zmax=1,
    text=np.round(corr_matrix.values, 2).astype(str),
    texttemplate="%{text}",
    textfont={"size": 9},
))
fig14.update_layout(
    title={"text": "Spectral-Performance Correlation<br><span style='font-size: 18px; font-weight: normal;'>Which spectral metrics predict classification success?</span>"},
)
fig14.update_xaxes(tickangle=-45)
fig14.write_image("chart14_correlation_matrix.png")
with open("chart14_correlation_matrix.png.meta.json", "w") as f:
    json.dump({"caption": "Spectral-Performance Correlation Matrix", "description": "Heatmap of Pearson correlations between spectral metrics and classification outcomes"}, f)

print("Chart 14 done")
print("\n=== Key correlations with hybrid_best_f1 ===")
print(corr_matrix['hybrid_best_f1'].sort_values(ascending=False))
