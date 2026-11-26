# -*- coding: utf-8 -*-
import numpy as np, pandas as pd
rng = np.random.default_rng(43)
cats = {"零食":-1.8, "生鲜":-2.4, "日用":-1.2, "美妆":-1.5}
rows=[]
for cat, true_e in cats.items():
    for sku in range(25):
        base_price = rng.uniform(10, 120); base_qty = rng.uniform(200, 1200)
        for week in range(12):
            price = base_price * rng.uniform(0.85, 1.15)
            qty = base_qty * (price/base_price)**true_e * rng.uniform(0.9,1.1)
            promo = int(rng.random()<0.25)
            rows.append(dict(sku=f"{cat}-{sku:02d}", category=cat, week=f"W{week+1:02d}",
                             price=round(price,2), qty=max(1,int(qty)), promo=promo, true_elasticity=true_e))
df=pd.DataFrame(rows); df.to_csv("data/dataset.csv", index=False)
print("wrote panel", df.shape)
