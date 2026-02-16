
# ==========================================
# CHART 23: NOVEL - "Method Dominance Sankey"
# Flow from Config → Method Type → Performance Tier
# ==========================================

# Define performance tiers
def tier(f1):
    if f1 >= 0.8: return "High (F1≥0.8)"
    elif f1 >= 0.5: return "Medium (0.5-0.8)"
    else: return "Failed (F1<0.5)"

# Build flows
sources, targets, values, colors_sankey = [], [], [], []

# Nodes: 0-4 = configs, 5-8 = methods, 9-11 = tiers
config_nodes = {c: i for i, c in enumerate(configs)}
method_nodes = {'Lambda': 5, 'Cosine': 6, 'UMAP': 7, 'Hybrid': 8}
tier_nodes = {"High (F1≥0.8)": 9, "Medium (0.5-0.8)": 10, "Failed (F1<0.5)": 11}

node_labels = [config_short[c] for c in configs] + ['Lambda', 'Cosine', 'UMAP', 'Hybrid', 'High F1', 'Medium F1', 'Failed']
node_colors = [config_colors[c] for c in configs] + ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#27AE60', '#F1C40F', '#C0392B']

for cfg in configs:
    cfg_data = df_class[df_class['config'] == cfg]
    
    for prefix, method_name in [('knn_lambda', 'Lambda'), ('knn_cosine', 'Cosine'), ('umap_2d', 'UMAP'), ('search_alpha', 'Hybrid')]:
        subset = cfg_data[cfg_data['method'].str.startswith(prefix)]
        if subset.empty:
            continue
        best_f1 = subset['f1'].max()
        t = tier(best_f1)
        
        # Config → Method
        sources.append(config_nodes[cfg])
        targets.append(method_nodes[method_name])
        values.append(1)
        colors_sankey.append(config_colors[cfg])
        
        # Method → Tier
        sources.append(method_nodes[method_name])
        targets.append(tier_nodes[t])
        values.append(1)
        colors_sankey.append(node_colors[method_nodes[method_name]])

fig23 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=node_colors,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=[c.replace(')', ', 0.3)').replace('rgb', 'rgba') if 'rgb' in c else c + '55' for c in colors_sankey],
    ),
)])

fig23.update_layout(
    title={"text": "Method Dominance Sankey Flow<br><span style='font-size: 18px; font-weight: normal;'>Config → Method → Performance Tier | Only Cosine reaches 'High'</span>"},
)
fig23.write_image("chart23_sankey.png")
with open("chart23_sankey.png.meta.json", "w") as f:
    json.dump({"caption": "Method Dominance Sankey Flow", "description": "Sankey diagram showing flow from configs through methods to performance tiers"}, f)

print("Chart 23 done")
