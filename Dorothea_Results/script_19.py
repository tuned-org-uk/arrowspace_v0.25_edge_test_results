
# ==========================================
# CHART 20: NOVEL - "Lambda Rank-Order Stability"
# If we sort items by lambda, how stable is the ordering across configs?
# ==========================================

# Get lambda values for each config, compute rank
lambda_ranks = {}
for cfg in configs:
    vals = df_lambda[df_lambda['config'] == cfg].sort_values('lambda').reset_index(drop=True)
    vals['rank'] = range(len(vals))
    lambda_ranks[cfg] = vals

# Compare rankings between pairs of configs using Spearman
from scipy.stats import spearmanr

# Build item-level lambda matrix
lambda_matrix = pd.DataFrame()
for cfg in configs:
    cfg_data = df_lambda[df_lambda['config'] == cfg].reset_index(drop=True)
    lambda_matrix[cfg] = cfg_data['lambda'].values

# Pairwise Spearman
n_cfg = len(configs)
spearman_matrix = np.zeros((n_cfg, n_cfg))
for i in range(n_cfg):
    for j in range(n_cfg):
        rho, _ = spearmanr(lambda_matrix[configs[i]], lambda_matrix[configs[j]])
        spearman_matrix[i, j] = rho

fig20 = go.Figure(data=go.Heatmap(
    z=spearman_matrix,
    x=[config_short[c] for c in configs],
    y=[config_short[c] for c in configs],
    colorscale='Blues',
    zmin=0, zmax=1,
    text=np.round(spearman_matrix, 3).astype(str),
    texttemplate="%{text}",
    textfont={"size": 14},
))
fig20.update_layout(
    title={"text": "Lambda Rank-Order Stability Across Configs<br><span style='font-size: 18px; font-weight: normal;'>Spearman ρ | High correlation = lambda ordering is config-invariant</span>"},
)
fig20.update_xaxes(title_text="Config")
fig20.update_yaxes(title_text="Config")
fig20.write_image("chart20_rank_stability.png")
with open("chart20_rank_stability.png.meta.json", "w") as f:
    json.dump({"caption": "Lambda Rank Stability Across Configs", "description": "Heatmap of pairwise Spearman correlations of lambda rankings between configs"}, f)

print("Chart 20 done")
print("\nSpearman matrix:")
print(pd.DataFrame(spearman_matrix, 
    index=[config_short[c] for c in configs],
    columns=[config_short[c] for c in configs]).round(3))
