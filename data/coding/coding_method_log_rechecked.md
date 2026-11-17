# EEG 情绪语料官方来源复核方法日志

- 复核日期：2026-11-13。编码方案：AECS v1.0.0（`codebook.md`），**枚举和判断规则无变更**。
- 输入仅采用本次上传的 `codebook.md`、`blind_coding_sheet.csv`、`evidence_pointers.csv`，及对所列语料可追踪的原作者论文、作者数据仓储、官方OpenNeuro/NEMAR镜像。
- 处理27个语料、原始14列；每语料9项编码证据，共243项。原始研究编码答案从未读取，未进行任何一致性计算。
- 本次指令（工作要点）：复核前一版未判定字段；只据原作者或官方数据发布资料确定；不得猜测；独立区分收集评分、论文提及、发布说明列文件及实际查看原文件；保留无法确定项目。
- **制作来源：计算机辅助文献与数据发布资料核查。** 不冒充真人编码。
- **文件级检查：** MET 的 OpenNeuro GitHub 发布文件页已直接查看 `ratings.tsv` 与 `participants.tsv` 的首行表头；尝试获取原始Raw链接时访问受限，因此没有读取全量记录。其余数据集只核实作者发布说明/表结构说明，均没有实际打开评分文件。
- **版本控制：** GAMEEMO 采用作者公开v1发布说明，v5仍受限；MET 采用OpenNeuro较新v1.0.4发布说明，较早NEMAR镜像的README缺失同样评分清单；不把不同版本混同。
- **访问失败：** DEAP、MAHNOB-HCI、AMIGOS所给发布入口无法读取；改查原作者纸本论文或作者手册；AMIGOS PDF截图请求超时（正文文字可以检索）；IESD给定MDPI链接内容错误；DREAMER原始入口不匹配/Zenodo未成功打开；GAMEEMO v5 embargo。
- **已观察资料矛盾：** MAHNOB原作者论文27人/手册30名招募者；MET当前OpenNeuro README声称participants.tsv含情绪标签，但实际该文件预览表头只有participant_id、age、sex；评分表在ratings.tsv。
- **规则判定：** `released_target`依据发布标注来源而不是刺激诱导类别；`additional_stream`要求同一cell的另一标注来源公开；`ratings_per_stimulus=time_resolved`严格要求暴露期间定时评分；`not inspected`不同于无文件。

## 本次实际修改的编码字段（不含notes、source_used和日志证据更新）

- MAHNOB-HCI / `released_target`: `cannot judge` → `self-report`。
- MAHNOB-HCI / `ratings_per_stimulus`: `cannot judge` → `multiple`。
- MAHNOB-HCI / `stimulus_unit`: `cannot judge` → `clip`。
- MAHNOB-HCI / `protocol_records_self_report`: `cannot judge` → `yes`。
- MAHNOB-HCI / `release_description`: `not inspected` → `explicitly describes`。
- MAHNOB-HCI / `n_subjects`: `TBD` → `27`。
- MAHNOB-HCI / `n_stimuli`: `TBD` → `20`。
- AMIGOS / `n_subjects`: `TBD` → `40`。
- AMIGOS / `n_stimuli`: `TBD` → `20`。
- AMIGOS / `stimulus_unit`: `cannot judge` → `clip`。
- AMIGOS / `ratings_per_stimulus`: `cannot judge` → `multiple`。
- AMIGOS / `protocol_records_self_report`: `cannot judge` → `yes`。
- GAMEEMO / `released_target`: `cannot judge` → `self-report`。
- GAMEEMO / `ratings_per_stimulus`: `cannot judge` → `multiple`。
- GAMEEMO / `stimulus_unit`: `cannot judge` → `game`。
- GAMEEMO / `protocol_records_self_report`: `cannot judge` → `yes`。
- GAMEEMO / `release_description`: `not inspected` → `explicitly describes`。
- GAMEEMO / `n_subjects`: `TBD` → `28`。
- GAMEEMO / `n_stimuli`: `TBD` → `4`。
- DENS / `released_target`: `cannot judge` → `self-report`。
- DENS / `release_description`: `does not mention` → `explicitly describes`。
- IESD / `n_stimuli`: `TBD` → `15`。
- EmoEEG-MC / `ratings_per_stimulus`: `cannot judge` → `multiple`。
- EmoEEG-MC / `protocol_records_self_report`: `not established` → `yes`。
- EmoEEG-MC / `n_stimuli`: `TBD` → `42`。
- EmoEEG-MC / `stimuli_shared`: `cannot judge` → `no`。
- Daly deposit / `released_target`: `cannot judge` → `self-report`。
- MET / `released_target`: `cannot judge` → `mixed`。
- MET / `additional_stream`: `cannot judge` → `ratings`。
- MET / `ratings_per_stimulus`: `cannot judge` → `multiple`。
- MET / `stimuli_shared`: `cannot judge` → `yes`。
- MET / `protocol_records_self_report`: `not established` → `yes`。
- MET / `release_description`: `does not mention` → `explicitly describes`。

## 仍需核实的类型

- `released_target`: 复核前无法判定11项，本次复核后仍有6项。
- `additional_stream`: 复核前无法判定23项，本次复核后仍有22项。
- `ratings_per_stimulus`: 复核前无法判定16项，本次复核后仍有11项。
- `stimulus_unit`: 复核前无法判定3项，本次复核后仍有0项。
- `stimuli_shared`: 复核前无法判定23项，本次复核后仍有21项。
- `protocol_records_self_report`: 复核前无法判定3项，本次复核后仍有0项。
- `release_description`: 复核前无法判定2项，本次复核后仍有2项。

证据精确路径、短证据、原入口与实际访问状态详见 `independent_ai_evidence_log_rechecked.csv`；仍无法确定的值、版本冲突及其原因详见 `unresolved_items_rechecked.md`。
