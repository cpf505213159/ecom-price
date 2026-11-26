# 促销价格弹性与券效率

> 有一半的券，发给了本来就会买的人

## 项目背景
用价格弹性模型评估券面额与门槛，把券的投入产出比提上来、压掉无效补贴。

## 数据集
price_panel（脱敏合成）：SKU×周 的价格、销量、促销标记；分品类用 log-log 回归估计弹性。

## 方法与口径
弹性=ln(销量) 对 ln(价格) 回归斜率；券 ROI=增量 GMV/券成本；全量发券 vs 只发高弹性人群对比。

## 关键结果（脱敏合成样本上复现）
| 指标 | 数值 |
|---|---|
| 价格弹性估计平均误差 | 2.4% |
| 券投入产出比 全量→定向高弹性 | 1.8 → 3.2 |
| 无效补贴（业务口径，万元/年） | 约 900 → 约 600 |
| 弹性误差门槛 | 控制在 11% 内 |

## 目录结构
```
ecom-price/
├── data/dataset.csv, sample.csv
├── src/ (generate_data.py, analysis.py)
├── notebooks/01_analysis.ipynb
├── reports/analysis-report.md
├── sql/01_price_panel.sql
└── outputs/metrics.json
```
## 复现
```bash
pip install -r requirements.txt
python src/generate_data.py     # 生成 data/dataset.csv（固定随机种子，可复现）
python src/analysis.py          # 计算指标，输出 outputs/metrics.json
# 或打开 notebooks/01_analysis.ipynb 逐步运行
```

## 数据说明
本仓库数据为**脱敏/合成**数据，用于可复现地演示分析方法；量级与真实业务口径可能存在差异，方法本身即为项目交付物的核心。

## 真实公开数据集

本仓库在 `data/real/` 附带**真实公开数据集**（来源、许可与字段说明见 `data/real/SOURCES.md`）。
运行 `python src/real_data_analysis.py` 可基于真实数据复现统计概览，输出到 `outputs/real_metrics.json` 与 `reports/real-data-notes.md`。

> 说明：`data/`、`outputs/metrics.json` 中的主结果是脱敏/仿真案例，用于稳定演示方法论；`data/real/` 使用公开真实数据集验证同一套方法在真实数据上可运行。
