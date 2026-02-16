
# Fix color format for Sankey
def hex_to_rgba(hex_color, alpha=0.3):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

link_colors = [hex_to_rgba(c, 0.35) for c in colors_sankey]

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
        color=link_colors,
    ),
)])

fig23.update_layout(
    title={"text": "Method Dominance Sankey Flow<br><span style='font-size: 18px; font-weight: normal;'>Config → Method → Performance Tier | Only Cosine reaches 'High'</span>"},
)
fig23.write_image("chart23_sankey.png")
with open("chart23_sankey.png.meta.json", "w") as f:
    json.dump({"caption": "Method Dominance Sankey Flow", "description": "Sankey diagram showing flow from configs through methods to performance tiers"}, f)

print("Chart 23 done")
