# ECSMP 登记更正记录

> **表号说明**：本文件写作于 2026-11-04 插入 TABLE I 之前，文中 Table I–VII 为旧编号。对应新编号：旧 V→VI、旧 II→III、旧 VII→VIII、旧 III→IV、旧 IV→V、旧 VI→VII。

日期 2026-11-04　｜　触发材料：`human_coding/BLIND_RETURN.csv`（隔离目录内的 AI 复核）

## 1. 这批材料是什么，不是什么

`BLIND_RETURN.csv` 是一次**在隔离目录里从零重编**的结果：只拿到 codebook、空白模板和 6 份文档文本，没有首遍表、没有 census、没有综述正文。这一点与 22:00 那版 `HUMAN_RETURNED.csv` 不同——那一版自填 `saw_first_pass = yes`，只能算内部复核。

但它**仍然是 AI 编码**，`BLIND_RETURN_NOTES.md` §6 自己写明了。按 `EXECUTION_HANDOFF_20261104.md` P1-B，它**不能**用于正文的"独立第二编码者信度"声明。因此本轮：

- §II-C 与 §X 关于编码过程的措辞**一字未改**，仍写第二编码者未完成；
- 一致率数字不进入正文；
- 只处理它提出的**内容事实**，因为事实可以由原文独立复核。

## 2. 它提出的问题

ECSMP 首遍记 `released_target = self-report`、`additional_stream = none`；盲编记 `assigned` + `ratings`。

## 3. 独立复核（不看盲编的理由，直接读原文）

出处：`review/_pdftext/Gao2021_ECSMP_DataInBrief_retypeset_pdf.txt`（Data in Brief 2021，doi:10.1016/j.dib.2021.107660）。

- 六段影片与六种情绪的固定对应：

  > "these videos were used to induce neutral, fear, sad, happy, anger, and disgust, respectively. The videos' playback sequence was random for each participant."

  同一素材、同一映射，只随机播放顺序 → 刺激类别对每个被试相同，符合 codebook 对 `assigned` 的定义（"one category per stimulus, the same for every participant, and this is the corpus's main task"）。

- 主任务即识别：

  > "The database can not only be directly used for the research of emotion recognition on multi-modal physiological signals…"

- 评分流随库发布：

  > "the questionnaires scores containing … and current emotional self-assessment form (CESAF) were displayed in the scale.xlsx."

  逐段 CESAF（六情绪 1–7）随 Mendeley 包发布 → `additional_stream = ratings`。

- `stimuli_shared`：六段影片对全部 89 人相同，仅顺序随机 → `yes`（首遍记 `TBD`）。

## 4. 首遍为什么错

三条独立证据都指向同一结论：

1. **码本自身的规则被违反**：`additional_stream` 定义为"participant ratings are released on top of an assigned target"，而本行 census 的 note 原文就写着 "released as scale.xlsx"，却记了 `none`——同一行自相矛盾。
2. **同构语料处理不一致**：FACED 同样是"类别由片段设计给定 + 逐片段被试自评随库发布"，首遍记 `assigned` + `ratings`；ECSMP 记 `self-report` + `none`。
3. **码本的工作例恰好描述这种结构**："an immersive-sequence dataset where each clip carries an intended emotion category and participants also reported their own state → `assigned` + `ratings`"。

判断错误的技术原因可追：census 该行 note 只写了 CESAF，没写六段影片的固定映射，等于把"评分流"当成了"标签来源"。

## 5. 改动范围

`census/affect_eeg_census.csv`（ECSMP 行，3 个字段）

| 字段 | 原值 | 新值 |
|---|---|---|
| `released_target` | self-report | **assigned** |
| `additional_stream` | none | **ratings** |
| `stimuli_shared` | TBD | **yes** |
| `note` | 只写 CESAF | 补六段映射与"emotion recognition"定位 |

`manuscript/review_data_collection.md`（10 处，全部由上述三个字段推导）

| 位置 | 改动 |
|---|---|
| §II-E 标签来源句 | ECSMP 从"obtain participant reports"移到与 FACED 同组 |
| Table II ECSMP 行 | `self-report` → `assigned`；`TBD` → `yes` |
| §IV 登记总述 | self-report 十四→十三，assigned 十二→十三；共享 yes 二十二→二十三，TBD 三→二；评分流一→二 |
| §IV 总述末句 | Table V 范围 十一→十二 |
| §VII-A | assigned 组 十二→十三；FACED 与 ECSMP 并列；"other eleven"→"other twelve" |
| §VII-E 首句 | 十一→十二 |
| **Table V** 题注 | 十一→十二 |
| **Table V** 表体 | 新增 ECSMP 行：protocol yes；release description `explicitly describes CESAF scores (scale.xlsx)`；file check `not performed` |
| Table V 后段 | "Eight of these eleven"→"Nine of these twelve"；"Two also describe feedback files"→三类并列（SEED-V/VII 的 clip feedback、ECSMP 的 CESAF）；"other ten packages"→eleven |
| §X | "other ten packages"→"other eleven" |
| §IX 建议 | "ten packages not inspected"→eleven |

未动：五矩阵与 Table III/IV 的任何数值、区间、R²；四幅图（绘图脚本不读这三个字段，逐字节未变）；引用；中文稿。

## 6. 复验

```
verify_counts.py        17/17
audit_review_numbers.py 93/93
static_acceptance_p5.py PASS（69 引用键 / Table II 27 行 / 9 表 / 4 图 / CRLF 496 行 / 孤立 LF 0）
```

`verify_counts.py` 与 `audit_review_numbers.py` 的六条相关断言按新事实同步修改（13/13/23/2/5/12），不是把常数调到绿灯：每一条都能由 census 复算。

## 7. 尚未处置

- 一致率**不进正文**。5 个可比语料、6 个字段、n ≤ 5，且编码者非人类，任何 kappa 都不足以支撑方法节声明。
- SEED-IV 一行在盲包里无对应文档（`SOURCE_PACKET.md` 的链接正确，是取文档时下成了 arXiv 版 SEED 论文）。该行 TBD 与 `cannot judge` 保持不变。
- 真实人类第二编码仍未完成。`blind_packet.zip` 可继续使用，但需在 `SOURCE_PACKET.md` 旁注明"SEED-IV 用 TCYB 2018 那篇，不要用 arXiv 1601.02197"。
