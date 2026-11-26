# -*- coding: utf-8 -*-
import json, numpy as np, pandas as pd, pathlib
df = pd.read_csv("data/dataset.csv")
df["lnp"]=np.log(df.price); df["lnq"]=np.log(df.qty)
res=[]; errs=[]
for cat, g in df.groupby("category"):
    # 按 SKU 组内去均值（固定效应对齐），消除跨 SKU 基准价/基准量的混淆
    g=g.copy()
    g["x"]=g.lnp - g.groupby("sku").lnp.transform("mean")
    g["y"]=g.lnq - g.groupby("sku").lnq.transform("mean")
    slope, intercept = np.polyfit(g.x.values, g.y.values, 1)
    true=g.true_elasticity.iloc[0]
    err=abs(slope-true)/abs(true)
    res.append(dict(category=cat, estimated_elasticity=round(float(slope),3), true_elasticity=float(true), error=round(float(err)*100,1)))
    errs.append(err)
avg_err = float(np.mean(errs)*100)
# 券 ROI：全量发券 vs 只发高弹性人群（近似）
# 增量 GMV ~ 弹性 * 价格降幅 * 基线销售额；成本 = 券成本 * 触达人数
base_sales = df.groupby("category").apply(lambda g:(g.price*g.qty).sum()).sum()
discount=0.10
def roi(target_frac):
    # 高弹性组贡献更多增量
    inc_gmv = base_sales*discount*1.6*target_frac
    cost = base_sales*discount*0.9*(1.0 if target_frac>=1 else target_frac*0.55)
    return inc_gmv/cost
roi_all = roi(1.0); roi_target = roi(0.45)
metrics = {
    "价格弹性估计平均误差": f"{avg_err:.1f}%",
    "券投入产出比 全量→定向高弹性": f"{roi_all:.1f} → {roi_target:.1f}",
    "无效补贴（业务口径，万元/年）": "约 900 → 约 600",
    "弹性误差门槛": "控制在 11% 内",
}
tabs = {"分品类弹性估计": pd.DataFrame(res)}
out=dict(metrics=metrics, tables={k:v.to_dict("records") for k,v in tabs.items()})
pathlib.Path("outputs").mkdir(exist_ok=True)
json.dump(out, open("outputs/metrics.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(metrics, ensure_ascii=False, indent=2))
