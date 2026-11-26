# -*- coding: utf-8 -*-
import json, pathlib, sys
try:
    import json, pathlib, pandas as pd, numpy as np
    ROOT=pathlib.Path(__file__).resolve().parents[1]; m={}
    o=pd.read_csv(ROOT/"data/real/online_retail_orders_sample.csv")
    o=o[(o.Quantity>0)&(o.UnitPrice>0)]
    g=o.groupby("StockCode").agg(qty=("Quantity","sum"),avg_price=("UnitPrice","mean"),n=("Quantity","size"))
    g=g[(g.n>=20)&(g.avg_price>0)&(g.qty>0)]
    x=np.log(g.avg_price.values); y=np.log(g.qty.values)
    b,a=np.polyfit(x,y,1); yhat=a+b*x; ss=1-((y-yhat)**2).sum()/((y-y.mean())**2).sum()
    m["sku_count"]=int(len(g)); m["cross_section_elasticity"]=round(float(b),3); m["r2"]=round(float(ss),3)
    m["note"]="横截面(按商品均价与总销量)估计的品类需求弹性，非单品时序因果弹性"
    print(json.dumps(m,ensure_ascii=False,indent=2))
    _root=pathlib.Path(__file__).resolve().parents[1]
    (_root/'outputs').mkdir(exist_ok=True)
    (_root/'reports').mkdir(exist_ok=True)
    (_root/'outputs/real_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    NOTES='''# 真实公开数据集分析概览\n\n本仓库附带真实公开数据集（见 data/real/SOURCES.md），运行 `python src/real_data_analysis.py` 复现以下真实数据统计：\n\n```json\n'+json.dumps(m,ensure_ascii=False,indent=2)+'\n```\n\n> data/ 与 outputs/metrics.json 的主结果为脱敏/仿真案例，用于稳定演示方法；本文件使用公开真实数据集验证方法可运行。'''
    (_root/'reports/real-data-notes.md').write_text(NOTES,encoding='utf-8')
    print(json.dumps(m,ensure_ascii=False,indent=2))
except Exception as e:
    print('REAL_ANALYSIS_ERROR', type(e).__name__, e); sys.exit(1)
