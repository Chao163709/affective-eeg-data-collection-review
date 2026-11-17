# 27个语料未决项目（官方来源复核后）

日期：2026-11-13。仅使用指定官方原始资料、原作者论文/仓储或官方数据镜像；没有查询此前其他人的编码。

`cannot judge`不是“该语料客观无法判断”，只表示当前证据尚未支持确定编码。`TBD`表示计数未确认；`not inspected`表示对应发布说明尚未读到。

## 1. DEAP

- `released_target` = `cannot judge`：需发布的主标签/标签文件来源与任务定位；实验采集与主发布目标可能不同
- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `release_description` = `not inspected`：官方数据发布说明不可访问或模糊，不能确认评分文件名单
- **来源/版本/方法注意事项：** 官方发布主入口仍超时；此前原论文只能确认实验自评，未核对评分文件发布列表。
- 实际使用的来源：https://doi.org/10.1109/T-AFFC.2011.15

## 2. MAHNOB-HCI

- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- **来源/版本/方法注意事项：** 给定原入口无法访问；原作者发布手册可读，但未检查session.xml实例；原论文27人和手册提及招募30人需要区分口径。
- 实际使用的来源：https://mahnob-db.eu/hci-tagging/media/uploads/manual.pdf

## 3. SEED

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed.html

## 4. SEED-IV

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `protocol_records_self_report` = `not established`：资料缺乏足够采集程序说明。
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-iv.html

## 5. SEED-V

- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-v.html

## 6. SEED-VII

- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-vii.html

## 7. SEED-GER

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `n_stimuli` = `TBD`：官方页面20 clips和21 trials相互矛盾
- **来源/版本/方法注意事项：** 同一官方描述中20 clips与21 trials存在术语/计数冲突。
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-GER.html

## 8. SEED-FRA

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-FRA.html

## 9. SEED-MYA

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-MYA.html

## 10. SEED-SD

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `n_stimuli` = `TBD`：每次24段、三次，未证实跨会话视频集是否重复
- **来源/版本/方法注意事项：** 每次24个刺激、不同session之间是否为完全同一套材料暂未核实。
- 实际使用的来源：https://bcmi.sjtu.edu.cn/home/seed/seed-SD.html

## 11. DREAMER

- `released_target` = `cannot judge`：需发布的主标签/标签文件来源与任务定位；实验采集与主发布目标可能不同
- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `release_description` = `not inspected`：官方数据发布说明不可访问或模糊，不能确认评分文件名单
- `n_stimuli` = `TBD`：独立刺激数与条件数或跨场项目数未明确
- **来源/版本/方法注意事项：** 原给定DOI与数据集源不符；原作者Zenodo访问失败或受限，不能确定分发评分文件。
- 实际使用的来源：https://doi.org/10.1109/JBHI.2017.2688239

## 12. AMIGOS

- `released_target` = `cannot judge`：已读资料未确定公开主标签文件是否为同一评分单元的主要标签。
- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- `release_description` = `not inspected`：官方数据发布说明不可访问或模糊，不能确认评分文件名单
- **来源/版本/方法注意事项：** 原作者论文可读，但数据发布入口不可读；即使论文提及内外部评分，仍不能证明两种评分文件均随数据发布。
- 实际使用的来源：https://www.eecs.qmul.ac.uk/mmv/datasets/amigos/doc/Paper_TAC.pdf

## 14. MPED

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `protocol_records_self_report` = `not established`：资料缺乏足够采集程序说明。
- `n_subjects` = `TBD`：释放/分析样本数在已查原始页面未明确
- 实际使用的来源：https://github.com/Tengfei000/MPED

## 15. GAMEEMO

- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- **来源/版本/方法注意事项：** 作者仓储v1公开发布说明列出了SAM PDF；v5仍处于embargo，不能证明两版本下载包完全相同。
- 实际使用的来源：https://data.mendeley.com/datasets/b3pn4kwpmn/1

## 16. DENS

- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- `n_stimuli` = `TBD`：独立刺激数或跨session去重数无明确证据。
- **来源/版本/方法注意事项：** 作者/镜像README列出beh评分TSV，但未打开TSV；participant_details.xlsx的标注源性质未明确。
- 实际使用的来源：https://data.nemar.org/on003751/v1.0.0/README.md

## 17. IESD

- `released_target` = `cannot judge`：已读资料未确定公开主标签文件是否为同一评分单元的主要标签。
- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `ratings_per_stimulus` = `cannot judge`：现有原始资料未交代每个刺激对应的评分次数或按本codebook无法归类。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- `protocol_records_self_report` = `not established`：资料缺乏足够采集程序说明。
- `n_subjects` = `TBD`：发布/分析样本数缺少可用明确信息。
- **来源/版本/方法注意事项：** 给定MDPI文章与该语料无关；转用NEMAR README；声音引导和按键并不等于公开情绪评分。
- 实际使用的来源：https://data.nemar.org/on003004/v1.0.0/README.md

## 18. EmoEEG-MC

- `released_target` = `cannot judge`：已读资料未确定公开主标签文件是否为同一评分单元的主要标签。
- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- **来源/版本/方法注意事项：** 作者文档直接证明逐trial有10项主观评分，未实际打开每人的评分表；42指完整个体总trial数。
- 实际使用的来源：https://github.com/ncclab-sustech/EmoEEG-MC

## 19. EVA-MED

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `n_subjects` = `TBD`：释放/分析样本数在已查原始页面未明确
- `n_stimuli` = `TBD`：独立刺激数与条件数或跨场项目数未明确
- 实际使用的来源：https://pmc.ncbi.nlm.nih.gov/articles/PMC12705992/

## 20. EAV

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `protocol_records_self_report` = `not established`：资料缺乏足够采集程序说明。
- `release_description` = `cannot judge`：官方数据发布说明不可访问或模糊，不能确认评分文件名单
- `n_stimuli` = `TBD`：独立刺激数与条件数或跨场项目数未明确
- 实际使用的来源：https://www.nature.com/articles/s41597-024-03838-4

## 21. Voice-UI

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- 实际使用的来源：https://www.nature.com/articles/s41597-024-03887-9

## 22. Emognition

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://www.nature.com/articles/s41597-022-01262-0

## 23. K-EmoCon

- `ratings_per_stimulus` = `cannot judge`：每5秒评分在辩论后回看中完成；定义仅允许暴露期内定时评分归入time_resolved
- `n_stimuli` = `TBD`：独立刺激数与条件数或跨场项目数未明确
- **来源/版本/方法注意事项：** 原始数据的5秒自评属于会后回溯，codebook的time_resolved严格限于暴露期间，仍不能按该枚举填写。
- 实际使用的来源：https://pmc.ncbi.nlm.nih.gov/articles/PMC7479607/

## 24. ECSMP

- `released_target` = `cannot judge`：需发布的主标签/标签文件来源与任务定位；实验采集与主发布目标可能不同
- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `ratings_per_stimulus` = `cannot judge`：未确认每刺激评分数；或现有规则无法对应回溯式标签
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- `release_description` = `cannot judge`：官方数据发布说明不可访问或模糊，不能确认评分文件名单
- `n_stimuli` = `TBD`：独立刺激数与条件数或跨场项目数未明确
- 实际使用的来源：https://data.mendeley.com/datasets/vn5nknh3mn/3

## 25. LLaMAC

- `additional_stream` = `cannot judge`：未明确列出第二标注来源的公开文件；沉默不等于none
- `stimuli_shared` = `cannot judge`：没有明确证据证明所有被试收到相同或不同的刺激材料
- 实际使用的来源：https://pmc.ncbi.nlm.nih.gov/articles/PMC12678757/

## 26. Daly deposit

- `additional_stream` = `cannot judge`：尚未明确发布同一评分单元的另一来源标注文件；缺乏证据不等于不存在。
- `ratings_per_stimulus` = `cannot judge`：现有原始资料未交代每个刺激对应的评分次数或按本codebook无法归类。
- `stimuli_shared` = `cannot judge`：未找到全部参与者实际接触的材料是否完全相同的直接声明。
- **来源/版本/方法注意事项：** 原作者README明确分发自我报告的情绪响应，但没有具体评分文件名，不能宣称文件级检查。
- 实际使用的来源：https://data.nemar.org/on002721/v1.0.0/README.md

## 27. MET

- **来源/版本/方法注意事项：** 当前OpenNeuro镜像与早期NEMAR镜像版本内容不同；README对participants.tsv评分说明与实际表头不符；只检查ratings.tsv表头，未读取全量行。
- 实际使用的来源：https://github.com/OpenNeuroDatasets/ds008701

