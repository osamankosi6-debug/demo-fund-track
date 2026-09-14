
import yfinance as yf, pandas as pd
assets = ["TLT","GLD","DBC","UUP","SPY","BIL","QQQ"]
px = yf.download(assets, start="2007-01-01", auto_adjust=True, progress=False)['Close']
ret = px.pct_change().fillna(0)
m_end = px.resample('ME').last().index
defense = pd.Series(0.0, index=px.index)
for i,d in enumerate(m_end[:-1]):
    try:
        scores = {a: px[a].pct_change(126).loc[d] for a in ["TLT","GLD","DBC","UUP"]}
        ranked = sorted(scores, key=scores.get, reverse=True)
        final = {ranked[0]:0.4, ranked[1]:0.3, ranked[2]:0.2, ranked[3]:0.1}
        nxt = m_end[i+1]
        mask = (ret.index >= d) & (ret.index < nxt)
        for s,w in final.items():
            defense.loc[mask] += w*ret.loc[mask,s]
    except: pass
defense_net = defense - 0.013/252
net_5_proxy = 0.6*ret["QQQ"] + 0.4*ret["SPY"]
net_comb = 0.85*net_5_proxy + 0.15*defense_net
net_fees = net_comb - 0.0010*2.3/252 - 0.02/252
eq = 100000*(1+net_fees).cumprod()
eq.to_csv("track_record.csv")
print(f"NAV ${eq.iloc[-1]:,.0f} done")
