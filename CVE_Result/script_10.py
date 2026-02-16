
# ==========================================
# CHART 19: NOVEL - "Method Dominance Summary" 
# For each metric: which method wins on how many queries?
# ==========================================
wins = {'Metric': [], 'Cosine': [], 'Hybrid': [], 'Taumode': []}

# 1. Highest top-1 score
for qid in sorted(df_search['query_id'].unique()):
    pass  # Will count below

# Count wins for various metrics
metric_names = ['Top-1 Score', 'Tail T/H Ratio', 'Lowest Tail CV', 'Lowest Decay']
for metric_name in metric_names:
    cw, hw, tw = 0, 0, 0
    for qid in sorted(df_search['query_id'].unique()):
        if metric_name == 'Top-1 Score':
            cs = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Cosine') & (df_search['rank'] == 1)]['score'].values[0]
            hs = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Hybrid') & (df_search['rank'] == 1)]['score'].values[0]
            ts = df_search[(df_search['query_id'] == qid) & (df_search['tau_method'] == 'Taumode') & (df_search['rank'] == 1)]['score'].values[0]
            if cs >= max(hs, ts): cw += 1
            elif hs >= max(cs, ts): hw += 1
            else: tw += 1
        elif metric_name == 'Tail T/H Ratio':
            ct = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Cosine (τ=1.0)')]['tail_to_head_ratio'].values
            ht = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Hybrid (τ=0.75)')]['tail_to_head_ratio'].values
            tt = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Taumode (τ=0.0.6)')]['tail_to_head_ratio'].values
            if len(ct) and len(ht) and len(tt):
                if ct[0] >= max(ht[0], tt[0]): cw += 1
                elif ht[0] >= max(ct[0], tt[0]): hw += 1
                else: tw += 1
        elif metric_name == 'Lowest Tail CV':
            ct = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Cosine (τ=1.0)')]['tail_cv'].values
            ht = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Hybrid (τ=0.75)')]['tail_cv'].values
            tt = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Taumode (τ=0.0.6)')]['tail_cv'].values
            if len(ct) and len(ht) and len(tt):
                if ct[0] <= min(ht[0], tt[0]): cw += 1
                elif ht[0] <= min(ct[0], tt[0]): hw += 1
                else: tw += 1
        elif metric_name == 'Lowest Decay':
            ct = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Cosine (τ=1.0)')]['tail_decay_rate'].values
            ht = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Hybrid (τ=0.75)')]['tail_decay_rate'].values
            tt = df_tail[(df_tail['query_id'] == qid) & (df_tail['tau_method'] == 'Taumode (τ=0.0.6)')]['tail_decay_rate'].values
            if len(ct) and len(ht) and len(tt):
                if ct[0] <= min(ht[0], tt[0]): cw += 1
                elif ht[0] <= min(ct[0], tt[0]): hw += 1
                else: tw += 1
    
    wins['Metric'].append(metric_name)
    wins['Cosine'].append(cw)
    wins['Hybrid'].append(hw)
    wins['Taumode'].append(tw)

wins_df = pd.DataFrame(wins)

fig19 = go.Figure()
fig19.add_trace(go.Bar(x=wins_df['Metric'], y=wins_df['Cosine'], name='Cosine', marker_color='#3498DB'))
fig19.add_trace(go.Bar(x=wins_df['Metric'], y=wins_df['Hybrid'], name='Hybrid', marker_color='#F39C12'))
fig19.add_trace(go.Bar(x=wins_df['Metric'], y=wins_df['Taumode'], name='Taumode', marker_color='#2ECC71'))

fig19.update_layout(
    barmode='group',
    title={"text": "Method Wins per Metric (18 Queries)<br><span style='font-size: 18px; font-weight: normal;'>Taumode wins top-1 score on all 18 queries | Tail metrics split</span>"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
)
fig19.update_xaxes(title_text="Metric")
fig19.update_yaxes(title_text="# Wins", range=[0, 20])
fig19.update_traces(cliponaxis=False)
fig19.write_image("cve_c19_wins.png")
with open("cve_c19_wins.png.meta.json", "w") as f:
    json.dump({"caption": "Method Wins per Metric (18 Queries)", "description": "Grouped bar chart counting how many queries each method wins on each metric"}, f)

print("Chart 19 done")
print(wins_df)
