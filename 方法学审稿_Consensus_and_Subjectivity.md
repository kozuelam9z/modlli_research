# 方法学聚焦审稿：Consensus and Subjectivity of Skin Tone Annotation for ML Fairness

> academic-research-skills `academic-paper-reviewer` methodology-focus 模式（合同 reviewer/reviewer_methodology_focus/v2，panel_size = 2）。2026-10-08 运行。
> 这是模拟审稿：论文已发表于 NeurIPS 2023 Datasets & Benchmarks，下面的决定不代表论文真实状态，`calibration_status: NOT_CALIBRATED`。
> 检查记录：合约验证 OK；两位审稿人 Phase 1 / Phase 2 conformance 均 PASS；panel synthesis 复算 PASS（exit 0）。
> 统计复算记录（Arithmetic Receipts）通过的是格式检查，不等于算术正确；正确与否需人工核对。

---

# 第一部分：编辑决定包（综合者）


## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

当前运行边界：本包不得依据候选档案或文字命名的档案升级。在封闭的档案工件与重放验证器把目标字段绑定到实际完成面板的 `execution_topology_sha256` 之前，`PROFILE_MEASURED` 不可用。两个席位在出具时同样为 `NOT_CALIBRATED`。

**运行边界说明**

- 模式：`reviewer_methodology_focus`，合同 `reviewer/reviewer_methodology_focus/v2`，panel_size = 2（期刊契合审稿人 EIC + 方法学审稿人 R1）。
- 评审标准绑定：本次为未绑定运行。据调度方说明，两个席位的 Phase 1 均披露了 `criteria_binding_unavailable`。本包不作任何期刊或会议契合度判断。
- 跨模型核查：未配置（`ARS_CROSS_MODEL` 未设置），Step 4b 跳过，本信不含跨模型检查点记录。
- 面板执行来源（Review Panel Provenance）块只适用于 `reviewer_full`，本模式不出具。

---

## Part 1: Editorial Decision Letter

> 说明：本稿已发表于 NeurIPS 2023 Datasets & Benchmarks track（据稿件首页），本信是应读者要求所做的模拟方法学审稿结论，不代表该论文的真实审稿状态。

尊敬的作者：

感谢您提交关于 MST-E 数据集及肤色标注主观性研究的稿件（本次为模拟审稿，不对应任何真实期刊）。稿件经 2 个角色分离的审稿席位审阅：期刊契合审稿人（Journal-Fit Reviewer，EIC，负责 D2 写作与结构）和审稿人 1（方法学，R1，负责 D1 方法严谨性）。methodology-focus 模式不包含 R2（领域）、R3（跨学科视角）和魔鬼代言人席位。本信不对两个席位的独立性作任何二元声明。

### Decision: Major Revision

#### 机械审计（Mechanical audit）

dimension_verdicts: [D1=block, D2=warn]

fired_conditions: [F2, F4]

da_critical_adjudications: []

editorial_decision=major_revision

**Step 1：按角色限定的评分矩阵**（无资格席位的 not_assessed 不计入分子和分母）

| 维度 | 有资格角色 | EIC | R1 | 审计判定 |
|---|---|---|---|---|
| D1 methodology_rigor（mandatory） | methodology | not_assessed（无资格，不计入） | block，block_class: repairable（未声明 fatal） | block |
| D2 writing_and_structure（normal） | eic | warn | not_assessed（无资格，不计入） | warn |

**Step 2：逐条评估失败条件**（所有表达式均在封闭词汇表内）

| 条件 | severity | 跨席位量词 | 表达式 | 是否触发 |
|---|---|---|---|---|
| F1 | 95 | any | D1 has a fatal block | 否：R1 的 block_class 为 repairable |
| F2 | 90 | any | D1 scores 'block' | 是 |
| F3 | 70 | any | D1 scores 'warn' | 否：该式要求恰为 warn，D1 为 block |
| F4 | 40 | any | D2 scores 'warn' or worse | 是 |
| F0 | 10 | all | every dimension scores 'pass' | 否 |

**Step 3：优先级。** 已触发条件中 severity 最高的是 F2（90），其动作为 major_revision。没有 DA CRITICAL 编号需要裁决。

**Schema 6 criterion_judgements**（`judgement_scale: sprint_contract`，原值照录，不换算为 EXCEEDS/MEETS 等量表）：EIC 的 D1 为 not_assessed，D2 为 warn；R1 的 D1 为 block（repairable），D2 为 not_assessed。

### Consensus Analysis

面板只有 2 个席位，分母恒为 2。两个席位都提出的子主张记为「EIC 与 R1 双席位印证」（corroborated by EIC and R1）；只有一个席位提出的记为单席位发现。5 席位面板的 CONSENSUS-4/CONSENSUS-3 标签在本模式下不适用。子主张编号 SC-n 见 Part 2 的 Sub-Claim(s) 列。

#### Points of Agreement（EIC 与 R1 双席位印证）

- **优点（双席位印证）：** 公开 MST-E 图像及逐条众包标注（EIC S3、R1 S1）；附录 E 完整列出逐图像检验，包括不显著结果（EIC S4、R1 S4）；以预研究说明为何选择摄影师而非皮肤科医生作为专家（EIC S5、R1 S6）。
- **SC-1、SC-2：** 众包标注者的 MST 培训从未描述，且未说明培训材料是否使用了 MST-E 图像，存在训练与评估重叠的风险（EIC W1、R1 W8，均为 Major）。
- **SC-3、SC-4：** 「学会对光照不变」超出证据。研究没有未经培训的对照或培训前后比较；困难光照下一致性更低、离散度更大（EIC W2、R1 W7，均为 Major）。
- **SC-6、SC-7：** 复本数建议没有声明目标信度阈值；Spearman-Brown 外推不能刻画「每地区 1/2 人」的结构，其平行测量前提也与地区差异结论相矛盾（EIC W4、R1 W6，均为 Major）。
- **SC-9、SC-10：** 地区差异只有一次总体 MANOVA 支撑，没有方向、幅度、事后比较和效应量；正文把结果解读成「标注预测地区」，方向写反（EIC W5、R1 W4，均为 Major）。
- **SC-11：** 把地区差异归因于「不同心智模型」或「文化语境」超出了证据。EIC 的依据是该构念未定义，且与「shared mental model」的表述相互矛盾；R1 的依据是地区与供应商团队、培训交付、薪酬、语言、设备等因素混杂（EIC W5、R1 W5，均为 Major）。两者依据不同，补救方案相容。
- **SC-14：** 专家研究中 88.9%/83.4% 的分母和汇总方式未说明，83.4% 无法由所述分母得到（EIC W7、R1 W14，均为 Minor；R1 附 AR3 mismatch）。
- **SC-18：** Open Images 扩展部分的结论超出了实际测量的内容：没有参照标注，只测了信度和地区分布（EIC W11、R1 W12，均为 Minor）。
- **SC-19：** Open Images 分析的统计设定（χ² 检验方法与自由度、V2 的统计量名称等）未报告（EIC W12、R1 W12，均为 Minor）。
- **SC-22：** 被跳过的标注、「difficult」标记及缺失数据的处理方式未报告（EIC W15、R1 W17，均为 Minor）。

#### 单席位发现（不带共识标签，按其所依据的证据锚点评估）

- 仅 EIC 提出：SC-5、SC-8、SC-12（Major）；SC-13、SC-15、SC-16、SC-20、SC-21、SC-24（Minor）。
- 仅 R1 提出：SC-25 至 SC-31（Major）；SC-32 至 SC-39（Minor）。其中 SC-25（参照标准信度未知）在 EIC 卡片中被明确交由方法学席位判断，记为沉默，不记为异议。
- 表面形式一致性检查：EIC W17（Confidence 2，仅依据参考文献标题）、EIC W8 与 R1 W2（依据图表目测读数）都按其实质保留，不因措辞或自报信心而升降。

#### Points of Disagreement

两个席位之间没有「问题是否存在」或「修改方向」上的分歧，只有 2 处严重度分歧，记为 [SPLIT]：

- **[SPLIT] SC-17 参照标注者的身份、锚定流程与单一参照问题**：EIC W10 评为 Minor，范围限定在披露与表述，卡片原文写明「这一安排是否构成方法学问题由方法学席位判断」；R1 W1 评为 Major，认为参照标准信度未知、受作者预标注锚定、且与研究者不独立。分歧类型：严重度。
  - **Editor's Resolution**：按方法学席位的判断处理，列为 must_fix（路线图 R9）。理由：参照标准的设计属于方法学问题，按「专业优先」原则应由 R1 判断，且 EIC 自己已将方法学严重度交给方法学席位。EIC 提出的披露要求（在摘要和 §3 写明作者身份与锚定流程、在局限性中讨论单一参照）并入验收标准。两个席位的严重度原值并列保留，不重新评级。
- **[SPLIT] SC-23 困难图像集的筛选标准与光照难度定义**：EIC W16 将其作为独立的报告缺口，评为 Minor；R1 W7 将其列为「学会对光照不变」超出证据的三条理由之一，该条整体评为 Major。分歧类型：严重度。
  - **Editor's Resolution**：列为 must_fix（路线图 R10）。理由：两个席位都把这一缺口与光照稳健性结论挂钩（EIC W16 写明「光照稳健性的结论依赖黄金集与困难集之间的对比」），而该结论本身已是双席位印证的 Major（路线图 R2）；刺激难度能否客观界定属于 R1 的专业范围。EIC 要求补充 lighting 字段全部取值的定义，一并纳入。

**不构成异议的情形**：EIC 正文称「核心发现在证据章节中可以找到依据」，但同时声明「统计推断是否正确由方法学席位负责」，因此不视为对 R1 统计类发现的反驳。EIC S4 赞许逐图像检验列示透明，R1 W10 质疑这些检验的推断方式，前者针对透明度，后者针对推断，两者相容。

### Decision Rationale

本决定由 v3.6.2 合同的机械规则得出。D1（methodology_rigor）只有方法学席位有资格评分，R1 评为 block，block_class 为 repairable，未声明 fatal；D2（writing_and_structure）只有 EIC 有资格评分，EIC 评为 warn。据此 F2（severity 90）和 F4（severity 40）触发，F1、F3、F0 未触发。按优先级取 F2，结论为 Major Revision。F4 单独只对应 Minor Revision，此处被 F2 覆盖。

综合协议的定性阅读与机械结论一致。两个席位分别从方法和表述角度，独立指向同一组核心问题：众包培训未披露且可能与评估集重叠；「学会对光照不变」超出证据；复本数建议缺少判定阈值，也无法由 Spearman-Brown 推出；地区差异只有一次设定不清的总体检验，却被归因于心智模型或文化。此外，R1 有 6 项单席位 Major（参照标准信度、±1 容差掩盖方向性偏差、ICC 没有置信区间、MANOVA 设定无法确定、信度不等于准确性、缺少等价检验），EIC 有 3 项（多元标注池带来对齐的因果表述、复本数建议在各节不一致、许可条款相互矛盾）。

两个席位都判断上述问题可以通过用现有数据重新分析或补充报告来修复。R1 明确写明「未见无法挽救的设计缺陷」，EIC 也认为核心发现在证据章节中有依据。因此决定不是 Reject，但修改需要重新分析，并应在修改后再次审阅。各条发现的自报 Confidence 只作为不确定性披露，没有参与任何计数、裁决或义务分级。

### Blocking Issues (0–3, immutable source order)

选取依据：R1 在 D1 评分理由中点名三项核心结论（可靠且与专家对齐、存在区域差异、对光照不变），每项各取来源顺序中第一个双席位印证的 must_fix 条目。其余 must_fix 条目同样须在录用前处理，本表只是阅读入口。注意：Transport ref 中的 R1–R16 是路线图编号，与审稿席位 R1（方法学审稿人）无关。

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---|---|---|---|---|
| R1 | 众包培训未描述，可能与 MST-E 评估图像重叠，「可靠」与「与专家对齐」可能被高估 | EIC W1 + R1 W8 | EIC: `absence: §6 众包标注流程 — expected 众包标注者所受 MST 培训的内容、时长、所用示例以及培训材料是否包含 MST-E 图像; checked §4, §6, §7, §8, 附录 C, 附录 D, 附录 K`；R1: `absence: §6 and §7 — expected the crowd annotators' MST training procedure and materials, including whether MST-E images were used in training; checked §4, §6, §7, Appendix C, Appendix D, Appendix K, Appendix L` | Part 2 R1 |
| R2 | 「学会对光照不变」缺少对照，且与困难光照下一致性下降的结果相矛盾 | EIC W2 + R1 W7 | EIC: `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"`；R1: `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"` | Part 2 R2 |
| R6 | 地区差异只有一次方向写反的总体 MANOVA，没有方向、幅度和事后比较 | EIC W5 + R1 W4 | EIC: `text: Abstract "annotators from different geographic regions rely on different mental models of MST categories resulting in annotations that systematically vary across regions"`；R1: `text: §6 Regional Differences in Annotation "the subject annotations were a significantly high predictor of the region of the annotators"` | Part 2 R6 |

### Required Item Details（must_fix，按来源顺序）

#### R1 — 众包培训披露与训练-评估重叠
- **Acceptance criteria**: §6（或正文明确指向的附录）给出培训内容、时长、示例来源与合格标准，并明确说明培训材料与 MST-E 评估图像或受试者是否重叠；若有重叠，另行报告未用于培训的受试者上的结果。

#### R2 — 光照「学会不变」表述
- **Acceptance criteria**: §7 与 §8 结论 (b)(e) 不再出现无对照支撑的「learn」，「invariant」改为与 §6 结果一致的表述（共识距离相近，单个标注者一致性在困难光照下下降），或补充相应的对照证据。

#### R3 — 多元标注池与对齐的比较
- **Acceptance criteria**: §6 给出各地区池与全局池的 1 分内比例和平均中位距离对比表，结论 (c) 与 §7 的表述与该表结果一致。

#### R4 — 复本数建议的阈值与结构依据
- **Acceptance criteria**: §6 写明判断「suffices/beneficial」所用的目标信度阈值及其依据，并分别交代「总复本数」与「每地区覆盖」两项建议各自的证据来源。

#### R5 — 复本数建议在各节的一致性
- **Acceptance criteria**: §6、§7 建议清单与局限性一节中关于 10 名标注者适用条件的表述一致。

#### R6 — 地区差异的方向、幅度与 MANOVA 表述
- **Acceptance criteria**: §6 正文报告各地区按 MST 区段相对全局中位数的偏离方向与幅度、事后比较与效应量，更正 MANOVA 结果的表述方向，并说明 V2 是何统计量。

#### R7 — 地区差异的成因归因
- **Acceptance criteria**: 摘要与 §6–§8 的成因表述改为关联性或描述性措辞，「mental model」已定义或不再使用，局限性一节列出地区与供应商团队、培训交付、薪酬、语言熟练度、显示设备的混杂。

#### R8 — 数据集许可与用途条款
- **Acceptance criteria**: §3、附录 C、附录 I 与数据集网站上的许可及允许/禁止用途清单一致，且所用许可本身与用途限制不冲突。

#### R9 — 参照标注者身份、锚定流程与结论措辞（[SPLIT] 已裁决）
- **Acceptance criteria**: 摘要与 §3/§4 写明 Dr. Monk 的作者身份和「作者先标、Dr. Monk 审定」的流程，局限性讨论单一参照标注的影响，「准确」「与专家对齐」改为「与量表创建者的标注一致」。

#### R10 — 困难图像集的筛选与光照界定（[SPLIT] 已裁决）
- **Acceptance criteria**: §3 写明困难图像的筛选者、筛选标准、光照难度的界定方式以及各受试者难度是否可比，数据卡给出 lighting 字段全部取值的定义。

#### R11 — 参照标准的信度
- **Acceptance criteria**: 正文报告作者预标注与最终参照标签的一致率，并讨论参照标准信度未知这一限制；R1 W1 原文将第二位独立专家盲评列为「如有可能」，未做时须在正文说明。

#### R12 — ±1 容差掩盖的方向性偏差
- **Acceptance criteria**: §6 报告按 MST 等级的带符号误差及其区间、完全一致率、二次加权 kappa 或有序 Krippendorff's α、阈值敏感性分析（完全一致与 ±2），并论证 ±1 阈值在 10 点量表上的适用性。

#### R13 — ICC 的不确定性
- **Acceptance criteria**: 每个 ICC 均附 95% 置信区间，「ICC 显著」一类针对零值的表述改为与预设信度基准比较。

#### R14 — MANOVA 设定
- **Acceptance criteria**: §6 写明观测单位、N 与依赖结构，或改报有序混合效应模型下的地区效应、地区 × MST 等级交互的估计及区间，以及经多重比较校正的两两对比。

#### R15 — 复本数与准确性的经验估计
- **Acceptance criteria**: §6 报告按 k 子抽样（按地区构成分层）得到的中位数与参照标签一致率和偏差随 k 的变化，「每张图像 10 人」的建议与之对应。

#### R16 — 光照不变的等价检验
- **Acceptance criteria**: §6 报告按受试者配对的两种光照下带符号误差与绝对误差的差值及区间，并给出预设界值的 TOST 等价检验结果。

---

## Part 2: Revision Roadmap

> Sub-Claim(s) 列给出每个条目对应的 SC 编号。Severity、Evidence Anchor、Confidence 逐字转录自来源卡片的对应发现，双席位条目两者并列。
>
> 机器可读的 `revision-roadmap/1.0` 核心没有在本文件中生成：本次运行没有绑定区块清单，`proposed_targets[]` 无从填写；封闭的 consequence 代码表也不在本次读取范围内。下表是人读版本，Bounded consequence 一栏以文字写出影响对象，不含概率或录用预测。作者分流（author triage）由之后的作者侧 sidecar 单独收集，本文件不给出工作顺序。

### Required Revisions (Must Fix)

> **Ordinal contract (#576/#670):** `R<n>` 按不可变的路线图来源顺序编号，只计 `obligation_class == must_fix` 的条目；作者自选的显示顺序和分流不参与编号。

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | 在 §6 完整描述众包 MST 培训（内容、时长、示例来源、合格标准），说明培训材料是否使用 MST-E 图像或受试者；如有重叠，单独报告未用于培训的受试者上的结果 | SC-1, SC-2 | EIC W1: Major；R1 W8: Major | EIC W1: `absence: §6 众包标注流程 — expected 众包标注者所受 MST 培训的内容、时长、所用示例以及培训材料是否包含 MST-E 图像; checked §4, §6, §7, §8, 附录 C, 附录 D, 附录 K`；R1 W8: `absence: §6 and §7 — expected the crowd annotators' MST training procedure and materials, including whether MST-E images were used in training; checked §4, §6, §7, Appendix C, Appendix D, Appendix K, Appendix L` | EIC W1: 4 — 逐节核对了正文和全部附录中关于标注者准备工作的描述；R1 W8: 3 — 标注任务设计与训练-测试分离 | EIC W1 + R1 W8（双席位印证） | must_fix | section: §6 众包标注流程（若有重叠，另需 re_analysis） | 摘要、§7、结论 (a)(b)(e) 中的「经培训」限定语仍不可核查、不可复现，也无法排除训练与评估重叠 |
| R2 | 删除或补证「learn」；把「对光照不变」改写为证据支持的表述（共识距离相近，单个标注者一致性在困难光照下下降） | SC-3, SC-4 | EIC W2: Major；R1 W7: Major | EIC W2: `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"`；R1 W7: `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"` | EIC W2: 4 — 对照了 §6 文字与图 3、图 5 的渲染图；R1 W7: 4 — 等价性检验与刺激抽样设计 | EIC W2 + R1 W7（双席位印证） | must_fix | sentence: §7、§8 结论 (b)(e) | 核心结论之一（光照不变）仍超出 §6 证据 |
| R3 | 在 §6 增加各地区池与全局池的 1 分内比例和平均中位距离对比表；若全局池不明显优于单一地区池，改写结论 (c) 与 §7，把推荐多元标注池的依据放在地区间差异上 | SC-5 | EIC W3: Major | `text: §8 "when collecting annotations from a diverse geographical pool, annotators are able to provide annotations that match the original intention behind the MST scale"` | 4 — 核对了 §6、§7、§8 的文字与附录 F 的图 8 | EIC W3（单席位） | must_fix | re_analysis: §6 Distance from Intended Annotations（现有数据） | 「多样性带来对齐」的因果表述无法由证据章节核查 |
| R4 | 写明判断「suffices/beneficial」的目标信度阈值及依据；分开说明「总复本数」与「地区覆盖」两项建议各自的证据来源，并交代 Spearman-Brown 的平行测量前提如何与地区差异结论调和 | SC-6, SC-7 | EIC W4: Major；R1 W6: Major | EIC W4: `text: §6 "one rater per region likely suffices (5 total annotators). For more challenging images, two annotators per region is beneficial."`；R1 W6: `text: §6 Replications "one rater per region likely suffices (5 total annotators)"` | EIC W4: 4 — 依据图 5 渲染图的目测读数与 §6、§7 文字对照得出，读数为近似值；R1 W6: 4 — Spearman-Brown 与 k 评分者信度 | EIC W4 + R1 W6（双席位印证） | must_fix | section: §6 Replications | 实践建议「每地区 1/2 人」无法由图 5 推出 |
| R5 | 统一 §6、§7 建议清单与局限性一节中 10 名标注者的适用范围（仅低质量图像 / 每张图像 / 图像质量未知时） | SC-8 | EIC W4: Major | `text: §6 "one rater per region likely suffices (5 total annotators). For more challenging images, two annotators per region is beneficial."` | 4 — 依据图 5 渲染图的目测读数与 §6、§7 文字对照得出，读数为近似值 | EIC W4（单席位） | must_fix | sentence: §6、§7、局限性 | 读者从三处得到三种不同的复本数建议 |
| R6 | 报告各地区按 MST 区段相对全局中位数的偏离方向与幅度、事后比较与效应量；更正把 MANOVA 写成「标注预测地区」的方向错误；说明 Open Images 部分 V2 是何统计量 | SC-9, SC-10 | EIC W5: Major；R1 W4: Major | EIC W5: `text: Abstract "annotators from different geographic regions rely on different mental models of MST categories resulting in annotations that systematically vary across regions"`；R1 W4: `text: §6 Regional Differences in Annotation "the subject annotations were a significantly high predictor of the region of the annotators"` | EIC W5: 3 — 结构与表述层面的判断有把握，统计检验是否适用不在本席位的范围内；R1 W4: 4 — 多元方差分析与混合效应模型设定 | EIC W5 + R1 W4（双席位印证） | must_fix | re_analysis: §6 Regional Differences in Annotation | 头条发现「系统性地区差异」只有一个方向写反的总体检验支撑 |
| R7 | 把「不同心智模型/文化语境导致差异」改为关联性、描述性表述；定义或弃用「mental model」，消除与「shared mental model」的矛盾；在局限性列出地区与供应商团队、培训交付、薪酬、语言熟练度、显示设备的混杂 | SC-11 | EIC W5: Major；R1 W5: Major | EIC W5: `text: Abstract "annotators from different geographic regions rely on different mental models of MST categories resulting in annotations that systematically vary across regions"`；R1 W5: `text: §8 Conclusion "We show that cultural contexts across geographical regions influence MST annotations."` | EIC W5: 3 — 结构与表述层面的判断有把握，统计检验是否适用不在本席位的范围内；R1 W5: 3 — 观察性分组比较中的混杂与因果推断 | EIC W5 + R1 W5（双席位印证） | must_fix | sentence: 摘要、§6、§7、§8；section: 局限性 | 因果解释超出非随机分组比较所能支撑的范围 |
| R8 | 统一数据集许可与允许/禁止用途：只采用一个许可（或分别说明图像与标注的许可），并在 §3、附录 C、附录 I 和数据集网站使用一致的用途清单 | SC-12 | EIC W6: Major | `text: §3 "The images cannot be used to train machine learning models. The images and annotations are licensed under CC BY."` | 4 — 逐字对照了 §3、§7、附录 C 与附录 I；对 CC BY 条款含义的判断基于该许可的通行理解 | EIC W6（单席位） | must_fix | other: 许可文本 + §3、附录 C、附录 I、数据集网站 | 使用者无法确定数据集（核心贡献之一）的合法用途 |
| R9 | 在摘要与 §3/§4 写明参照标注者 Dr. Monk 的作者身份及「作者先标、Dr. Monk 审定」的流程；在局限性讨论单一参照标注的影响；「准确/与专家对齐」改为「与量表创建者的标注一致」 | SC-17 | EIC W10: Minor；R1 W1: Major（[SPLIT]，见 Part 1 裁决） | EIC W10: `text: §3 "Images were first annotated by an author and sent to Dr. Monk for final golden annotations."`；R1 W1: `text: §3 "Images were first annotated by an author and sent to Dr. Monk for final golden annotations."` | EIC W10: 3 — 本条只涉及披露与表述，这一安排是否构成方法学问题由方法学席位判断；R1 W1: 4 — 心理测量与参照标准效度方法学 | EIC W10 + R1 W1（[SPLIT]，已裁决） | must_fix | sentence: 摘要、§3/§4、局限性 | 所有「对齐」结论的参照来源及其独立性对读者不透明 |
| R10 | 说明困难图像集由谁、按什么标准挑选，光照难度如何界定，各受试者难度是否可比；给出数据卡 lighting 字段全部取值的定义 | SC-23 | EIC W16: Minor；R1 W7: Major（[SPLIT]，见 Part 1 裁决） | EIC W16: `absence: §3 Challenging Images set — expected 困难图像的筛选者与筛选标准以及光照条件的界定方式; checked §3, §4, §5, 附录 B, 附录 C`；R1 W7: `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"` | EIC W16: 4 — 检索了列出的全部章节；R1 W7: 4 — 等价性检验与刺激抽样设计 | EIC W16 + R1 W7（[SPLIT]，已裁决） | must_fix | section: §3 Challenging Images；附录 C 数据卡 | 光照稳健性对比所依赖的刺激定义不可核查 |
| R11 | 报告作者预标注与最终参照标签的一致率，说明参照标准信度未知这一限制；如有可能，请第二位独立 MST 专家对 19 名受试者盲评并报告加权 kappa | SC-25 | R1 W1: Major | `text: §3 "Images were first annotated by an author and sent to Dr. Monk for final golden annotations."` | 4 — 心理测量与参照标准效度方法学 | R1 W1（单席位；EIC 明确把方法学判断交给方法学席位） | must_fix | re_analysis: §3/§4（现有记录）；可选 new_data: 第二位专家盲评 | 「与专家对齐」的估计缺少参照端误差 |
| R12 | 按 MST 等级报告带符号误差及区间、完全一致率，以及与参照标签的二次加权 kappa 或有序 Krippendorff's α；做阈值敏感性分析（完全一致与 ±2）；论证借自 6 点 FST 的 ±1 阈值；讨论量表两端压缩对公平性分析的影响 | SC-26, SC-27 | R1 W2: Major | `figure: Figure 8(a) Global Annotation Confusion Matrix — row Intended MST 10: 50 at column 8, 36 at column 9, 2 at column 10; row 5: 50 at column 4` | 4 — 有序评分一致性分析；数值按图中行百分比近似读取 | R1 W2（单席位） | must_fix | re_analysis: §6 Distance from Intended Annotations | 「94.7% 在 ±1 内」可能掩盖量表两端的系统性压缩 |
| R13 | 为每个 ICC 报告 95% 置信区间（F 分布法或 bootstrap）；删除针对 ICC = 0 的「显著」表述，改为与预设信度基准比较；把 ICC 的解释限定在所选刺激集上 | SC-28 | R1 W3: Major | `absence: §5 and §6 Inter-Rater Reliability — expected 95% confidence intervals for every ICC estimate; checked §5, §6, Figure 3(a), Figure 3(b) and caption, Figure 5, Appendices E-F` | 4 — 评分者信度估计与区间方法 | R1 W3（单席位） | must_fix | re_analysis: §5、§6、图 3、图 5 | 「可靠」结论没有不确定性度量，美国专家在两种光照间的差异无法判断 |
| R14 | 写明 MANOVA 的观测单位、N 与非独立结构，或改用累积 logit 混合效应模型（地区为固定效应，标注者与图像为随机效应），报告地区效应、地区 × MST 等级交互及区间，以及经多重比较校正的两两对比 | SC-29 | R1 W4: Major | `text: §6 Regional Differences in Annotation "the subject annotations were a significantly high predictor of the region of the annotators"` | 4 — 多元方差分析与混合效应模型设定 | R1 W4（单席位；AR9 not_computable） | must_fix | re_analysis: §6 Regional Differences in Annotation | 地区差异推断所依赖的模型设定无法核查 |
| R15 | 利用每张图像 25 次重复，按 k 分层抽样，直接估计中位数与参照标签的一致率和偏差如何随 k 变化，替代或补充 Spearman-Brown 外推，并据此支撑「每张图像 10 人」的建议 | SC-30 | R1 W6: Major | `text: §6 Replications "one rater per region likely suffices (5 total annotators)"` | 4 — Spearman-Brown 与 k 评分者信度 | R1 W6（单席位） | must_fix | re_analysis: §6 Replications、§7 | 复本数建议只基于信度，没有检验准确性 |
| R16 | 按受试者配对比较两种光照下的带符号误差与绝对误差，报告差值及区间，并用预设界值的 TOST 做等价检验；可利用数据卡逐图像的 lighting 字段扩展到全部 1515 张图像 | SC-31 | R1 W7: Major | `text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"` | 4 — 等价性检验与刺激抽样设计 | R1 W7（单席位） | must_fix | re_analysis: §6 | 「不变」只由两个相等的均值支撑 |

### Suggested Revisions (Should Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | 在正文直接写明专家研究实际分析的图像数（脚注 4 排除 1 名受试者后为 18），并与图 7 一致 | SC-13 | EIC W7: Minor | `text: §5 "Experts were asked to annotate a total of 50 images, 19 from the MST-E Golden Images or Challenging Image sets"` | 4 — 对照了 §5 正文、脚注 4 与附录 E 的图 7 | EIC W7（单席位） | should_fix | sentence: §5 | 样本数在正文与图 7 之间不一致 |
| S2 | 报告 88.9%、83.4% 的分子、分母、是否合并两种条件以及取整规则 | SC-14 | EIC W7: Minor；R1 W14: Minor | EIC W7: `text: §5 "Experts were asked to annotate a total of 50 images, 19 from the MST-E Golden Images or Challenging Image sets"`；R1 W14: `text: §5 Distance from Intended Annotations "88.9% in India and 83.4% in the United States"` | EIC W7: 4 — 对照了 §5 正文、脚注 4 与附录 E 的图 7；R1 W14: 3 — 粒度检验，依赖由设计推得的分母与取整约定 | EIC W7 + R1 W14（双席位印证；R1 Arithmetic Receipt AR3: mismatch） | should_fix | sentence: §5 | 83.4% 无法由所述分母复现 |
| S3 | 分别描述 Subject 14 两张图像（图 4a/4b）的标注分布，并注明参照标注 | SC-15 | EIC W8: Minor | `figure: Figure 4(b) — US panel counts fall at MST4, MST5 and MST6, none at MST7` | 3 — 基于渲染图的目测读数 | EIC W8（单席位） | should_fix | sentence: §5 | §5 文字与图 4(b) 不符 |
| S4 | 逐栏核对数据卡：更正「Data Subject(s)」栏的模板残留，在人类属性来源栏反映两步标注流程 | SC-16 | EIC W9: Minor | `text: Appendix C "Data about image search queries"` | 4 — 逐栏对照了数据卡与 §3 的数据集描述 | EIC W9（单席位） | should_fix | other: 附录 C 数据卡 | 数据集文档的主要载体描述有误 |
| S5 | 把 Open Images 部分的结论限定为「信度与地区差异两项性质得到重现」，删去「likely translate」「perform similarly」等超出测量的表述 | SC-18 | EIC W11: Minor；R1 W12: Minor | EIC W11: `text: §6 "this shows that recommendations based on annotator behaviors observed in our controlled studies likely translate to real-world scenarios"`；R1 W12: `text: §6 Extension to In-the-Wild Annotations "has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset"` | EIC W11: 4 — 对照了 §6 的 Open Images 段落、§7 与局限性一节；R1 W12: 4 — 信度系数比较与等价推断 | EIC W11 + R1 W12（双席位印证） | should_fix | sentence: §6、§7、局限性 | 对齐度和复本数建议被表述为已在真实场景得到验证 |
| S6 | 报告 Open Images 分析的设定：每张人脸的复本数与地区分配、ICC 形式、比较 ICC 的 χ² 检验方法与自由度、V2 的统计量名称 | SC-19 | EIC W12: Minor；R1 W12: Minor | EIC W12: `absence: §6 Extension to In-the-Wild Annotations — expected 每张人脸的标注复本数与地区分配、所用 ICC 形式、得出 χ2 = 0.26 与 V2 = 0.0766 的检验名称; checked §4, §6, §7, 附录 C, 附录 D, 附录 J`；R1 W12: `text: §6 Extension to In-the-Wild Annotations "has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset"` | EIC W12: 4 — 检索了列出的全部章节；R1 W12: 4 — 信度系数比较与等价推断 | EIC W12 + R1 W12（双席位印证；R1 正文引用 AR8、AR11 not_computable） | should_fix | section: §6 Extension to In-the-Wild Annotations | χ2 = 0.26、p = 0.99、V2 = 0.0766 无法核查 |
| S7 | 在引言末尾加入贡献清单，在 §7 逐一回答研究问题 (a)(b)(c)，区分问题 (b) 的「质量」与结果中的「差异」 | SC-20 | EIC W13: Minor | `text: §1 "Does annotator location, a proxy for cultural context and lived experience, matter and have any effect on annotation quality?"` | 4 — 对照了 §1 的研究问题与 §6、§7、§8 的结论 | EIC W13（单席位） | should_fix | section: §1 引言末尾、§7 | 研究问题 (b) 与结果不对应 |
| S8 | 在 §6「Distance from Intended Annotations」一段引用附录 F 图 8 | SC-21 | EIC W14: Minor | `absence: §6 Distance from Intended Annotations — expected 指向附录 F 图 8 逐地区混淆矩阵的引用; checked §4, §5, §6, §7, §8` | 4 — 检索了正文中全部附录引用 | EIC W14（单席位） | should_fix | sentence: §6 | 唯一的逐地区对齐证据对读者不可见 |
| S9 | 在 §6 报告被跳过的标注数量及其在两种光照间的分布、「difficult」标记的分布，以及中位数与 ICC 如何处理缺失 | SC-22 | EIC W15: Minor；R1 W17: Minor | EIC W15: `text: Appendix C "Some images were too hard to annotate"`；R1 W17: `absence: §6 Inter-Rater Reliability — expected the number of distinct annotators per region, per-annotator workload, skipped-annotation counts and any quality-control exclusions; checked §6, Appendix C, Appendix D, Appendix K` | EIC W15: 3 — 缺失数据对困难集结果的影响大小，需由方法学席位评估；R1 W17: 4 — 标注研究的样本与缺失数据报告 | EIC W15 + R1 W17（双席位印证） | should_fix | section: §6 | 无法判断困难集结果是否受缺失影响 |
| S10 | 核对 §2 中 [33, 48, 50] 是否支撑「专家与众包标注相近」，以及 Casual Conversations 在 §2（[38]）与附录 A.3（[51]）中的归属 | SC-24 | EIC W17: Minor | `text: §2 "studies find that expert and crowdsource annotators tend toward fairly similar annotations on the FST [33, 48, 50]"` | 2 — 仅依据参考文献列表中的标题判断，未查阅原文 | EIC W17（单席位） | should_fix | sentence: §2、附录 A.3 | 一处标为「Critically for this work」的背景依据可能引用有误 |
| S11 | 写明专家部分 ICC 是一致性型还是绝对一致型（ICC(C,1)/ICC(A,1)）以及「Per Subject」ICC 的目标单位；补充二次加权 kappa 或有序 Krippendorff's α 作为稳健性检验 | SC-32 | R1 W9: Minor | `text: §5 Inter-Rater Reliability "we use a two-way random, single score ICC where the subject and annotator are viewed as random effect"` | 4 — ICC 模型选择（McGraw & Wong） | R1 W9（单席位） | should_fix | re_analysis: §5 Inter-Rater Reliability | 专家 ICC 的含义无法确定 |
| S12 | 写明 36 次逐图像检验的期望假阳性数，报告效应量（如 rank-biserial 相关），说明 p 值计算方法；单独说明 Subject 14 在两种条件下均显著 | SC-33 | R1 W10: Minor | `table: Appendix E Figure 7(a) and 7(b) — 36 uncorrected per-image tests, three with p below .05 (S13 Golden 0.026888, S14 Golden 0.018119, S14 Challenging 0.048632)` | 4 — 多重比较与小样本非参数检验 | R1 W10（单席位；正文引用 AR10 not_computable） | should_fix | re_analysis: §5、附录 E | 「三张图像显著」可能被读成超出偶然水平 |
| S13 | 在局限性写明专家研究中光照条件与评定顺序完全混同 | SC-34 | R1 W11: Minor | `text: §5 "Participants first annotated the Golden Images set and distractor images."` | 4 — 实验设计中的顺序效应 | R1 W11（单席位） | consider（R1 W11 认为专家研究属探索性，影响有限） | sentence: 局限性 | 图 3(a) 中美国专家 ICC 的下降可能被误归因于光照 |
| S14 | 不把「无显著差异」解读为「相似」（相似需要等价检验）；在约 8.7 万张人脸的样本量下，以效应量为主解释地区分布差异 | SC-35 | R1 W12: Minor | `text: §6 Extension to In-the-Wild Annotations "has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset"` | 4 — 信度系数比较与等价推断 | R1 W12（单席位） | should_fix | sentence: §6 Extension to In-the-Wild Annotations | 不显著的结果被当作相似性证据 |
| S15 | 更正图 8 图注（中位数还是个体标注），在每一行标出 n，并说明 Global 池的定义 | SC-36 | R1 W13: Minor | `figure: Figure 8(a) Global Annotation Confusion Matrix — row Intended MST 7 (single subject) shows 2 at column 5 and 2 at column 9, against the caption's median wording` | 3 — 由单元格粒度推断，取决于未报告的分母 | R1 W13（单席位；正文引用 AR7 not_computable） | should_fix | other: 附录 F 图 8 图注与行标注 | 图 8 以及基于它的偏差估计无法核对 |
| S16 | 报告 0.84 的分子、分母与取整规则，并说明「average median distance」取绝对值还是带符号差 | SC-37 | R1 W15: Minor | `text: §5 Distance from Intended Annotations "0.78 in India and 0.84 in the United States"` | 3 — 粒度检验，依赖由设计推得的分母与取整约定 | R1 W15（单席位；Arithmetic Receipt AR5: mismatch） | should_fix | sentence: §5 | 0.84 无法由所述分母复现 |
| S17 | 发布分析代码、摄影专家标注与 Open Images MST 标注，或说明不能发布的原因；注明统计软件及版本 | SC-38 | R1 W16: Minor | `absence: Appendix C data card and Appendix J — expected release of the photographer annotations, the Open Images skin tone annotations and the analysis code, with the statistical software named; checked §4-§6, Appendix C, Appendix E, Appendix H, Appendix I, Appendix J, Appendix L` | 4 — 可复现性审查 | R1 W16（单席位） | should_fix | other: 代码与标注发布 + 附录 J | ICC、MANOVA、χ² 结果无法复现 |
| S18 | 补充一张表：各地区不同标注者的人数、每人标注量、质量控制排除情况 | SC-39 | R1 W17: Minor | `absence: §6 Inter-Rater Reliability — expected the number of distinct annotators per region, per-annotator workload, skipped-annotation counts and any quality-control exclusions; checked §6, Appendix C, Appendix D, Appendix K` | 4 — 标注研究的样本与缺失数据报告 | R1 W17（单席位） | should_fix | section: §6 | 无法评估单向 ICC 的依赖结构和地区比较 |

### Source-Traceability Checklist

> 按来源顺序排列，不代表工作顺序。作者分流之后作为完整的 sidecar 单独收集。

- [ ] R1 — obligation `must_fix`: 众包培训披露与训练-评估重叠（EIC W1 + R1 W8）
- [ ] R2 — obligation `must_fix`: 光照「学会不变」表述（EIC W2 + R1 W7）
- [ ] R3 — obligation `must_fix`: 多元池与单一地区池的对齐比较（EIC W3）
- [ ] R4 — obligation `must_fix`: 复本数建议的阈值与结构依据（EIC W4 + R1 W6）
- [ ] R5 — obligation `must_fix`: 复本数建议在各节一致（EIC W4）
- [ ] R6 — obligation `must_fix`: 地区差异的方向、幅度与 MANOVA 表述（EIC W5 + R1 W4）
- [ ] R7 — obligation `must_fix`: 地区差异的成因归因（EIC W5 + R1 W5）
- [ ] R8 — obligation `must_fix`: 数据集许可与用途条款（EIC W6）
- [ ] S1 — obligation `should_fix`: 专家研究实际图像数（EIC W7）
- [ ] S2 — obligation `should_fix`: 88.9%/83.4% 的分母与汇总方式（EIC W7 + R1 W14）
- [ ] S3 — obligation `should_fix`: 图 4 描述（EIC W8）
- [ ] S4 — obligation `should_fix`: 数据卡错误（EIC W9）
- [ ] R9 — obligation `must_fix`: 参照标注者身份、锚定流程与结论措辞（EIC W10 + R1 W1，[SPLIT] 已裁决）
- [ ] S5 — obligation `should_fix`: Open Images 结论范围（EIC W11 + R1 W12）
- [ ] S6 — obligation `should_fix`: Open Images 统计设定（EIC W12 + R1 W12）
- [ ] S7 — obligation `should_fix`: 研究问题与贡献清单（EIC W13）
- [ ] S8 — obligation `should_fix`: 引用附录 F（EIC W14）
- [ ] S9 — obligation `should_fix`: 跳过标注与缺失处理（EIC W15 + R1 W17）
- [ ] R10 — obligation `must_fix`: 困难图像集筛选与光照界定（EIC W16 + R1 W7，[SPLIT] 已裁决）
- [ ] S10 — obligation `should_fix`: §2 引用核对（EIC W17）
- [ ] R11 — obligation `must_fix`: 参照标准信度（R1 W1）
- [ ] R12 — obligation `must_fix`: ±1 容差掩盖的方向性偏差（R1 W2）
- [ ] R13 — obligation `must_fix`: ICC 置信区间（R1 W3）
- [ ] R14 — obligation `must_fix`: MANOVA 设定或改用混合效应模型（R1 W4）
- [ ] R15 — obligation `must_fix`: 复本数与准确性的经验子抽样（R1 W6）
- [ ] R16 — obligation `must_fix`: 光照不变的等价检验（R1 W7）
- [ ] S11 — obligation `should_fix`: ICC 形式与有序补充指标（R1 W9）
- [ ] S12 — obligation `should_fix`: 逐图像检验的多重比较（R1 W10）
- [ ] S13 — obligation `consider`: 专家研究的顺序混同（R1 W11）
- [ ] S14 — obligation `should_fix`: 不显著不等于相似（R1 W12）
- [ ] S15 — obligation `should_fix`: 图 8 图注与分母（R1 W13）
- [ ] S16 — obligation `should_fix`: 0.84 的分母（R1 W15）
- [ ] S17 — obligation `should_fix`: 代码、标注与软件（R1 W16）
- [ ] S18 — obligation `should_fix`: 标注者样本与质量控制（R1 W17）

### Response Letter Template

请按 `templates/revision_response_template.md` 的格式逐条回应 R1–R16 与 S1–S18。如不采纳某项，须在回应信中写明理由；该条目会保持可见、记为未解决，不会被静默删除。

---

## Part 3: Reviewer Report Summary (Appendix)

本模式的面板只有以下两个席位。R2（领域）、R3（跨学科视角）和魔鬼代言人不属于 methodology-focus 模式，因此没有相应摘要，也没有 DA CRITICAL 条目。

| 项目 | Journal-Fit Reviewer（EIC） | Reviewer 1（方法学，R1） |
|---|---|---|
| 维度评分 | D1 not_assessed（非本席位维度）；D2 评为 warn | D1 评为 block，block_class: repairable；D2 not_assessed（非本席位维度） |
| 自报 Confidence | 无报告级数值；逐条 2–4 | 无报告级数值；逐条 3–4 |
| 优点 | S1–S7 | S1–S7 |
| 缺陷 | W1–W17（Major 6 项，Minor 11 项） | W1–W17（Major 8 项，Minor 9 项） |
| 问题（Questions） | 0 | 0 |
| 其他 | 不作期刊契合度判断；统计推断交由方法学席位 | 统计报告充分性总体 DOES_NOT_MEET；Arithmetic Receipts AR1–AR11：3 项 consistent（AR1、AR2、AR4），2 项 mismatch（AR3、AR5），6 项 not_computable（AR6–AR11） |

### Journal-Fit Review Report Summary
- Recommendation: 卡片未给出整体推荐，D2 评为 warn | Confidence: 无报告级数值，逐条 2–4
- Key Point: 稿件主干可以追溯，问题都可修复；但讨论与结论中有四处表述强于 §6 的证据，核查所需的若干方法细节缺失，数据集许可条款在三处相互矛盾。

### Reviewer 1 (Methodology) Summary
- Recommendation: 卡片未给出整体推荐，D1 评为 block（repairable） | Confidence: 无报告级数值，逐条 3–4
- Key Point: 三项核心推断（可靠且与专家对齐、存在区域差异、对光照不变）及复本数建议所依赖的分析，要么设定不清，要么缺少不确定性报告，要么超出了设计所能支撑的范围；这些问题都可以用现有数据修复。

## Attachment: Acronym Check (advisory, #849)

### 縮寫檢查（僅供參考，不必回覆）
範圍：正文（部分）
此檔沒有：英文摘要、中文摘要。
未檢查：
- 正文第 309 行：IRR（括號前各字的字首拼不出這個縮寫）
- 正文第 370 行：MANOVA（括號前各字的字首拼不出這個縮寫）
- 正文第 564 行：ICASSP（括號前各字的字首拼不出這個縮寫）

| 範圍 | 行 | 問題 | 縮寫 | 次數 |
|---|---|---|---|---|
| 正文 | 3 | 未定義 | ML | 6 |
| 正文 | 31 | 未定義 | AI | 9 |
| 正文 | 62 | 未定義 | MST1 | 4 |
| 正文 | 62 | 未定義 | MST10 | 3 |
| 正文 | 62 | 未定義 | MST2 | 7 |
| 正文 | 62 | 未定義 | MST3 | 6 |
| 正文 | 62 | 未定義 | MST4 | 5 |
| 正文 | 62 | 未定義 | MST5 | 7 |
| 正文 | 62 | 未定義 | MST6 | 5 |
| 正文 | 62 | 未定義 | MST7 | 4 |
| 正文 | 62 | 未定義 | MST8 | 5 |
| 正文 | 62 | 未定義 | MST9 | 5 |
| 正文 | 63 | 重複定義 | MST | 119 |
| 正文 | 106 | 未定義 | LGBTQ | 3 |
| 正文 | 157 | 定義晚於首次使用 | ITA | 10 |
| 正文 | 158 | 未定義 | RGB | 5 |
| 正文 | 184 | 重複定義 | MST | 119 |
| 正文 | 185 | 重複定義 | MST | 119 |
| 正文 | 194 | 未定義 | TONL3 | 1 |
| 正文 | 213 | 未定義 | TONL | 11 |
| 正文 | 219 | 未定義 | CO | 6 |
| 正文 | 220 | 未定義 | ALL | 2 |
| 正文 | 220 | 未定義 | RIGHTS | 2 |
| 正文 | 222 | 未定義 | BY | 1 |
| 正文 | 222 | 未定義 | CC | 1 |
| 正文 | 311 | 重複定義 | ICC | 14 |
| 正文 | 423 | 未定義 | MSTE | 1 |
| 正文 | 424 | 未定義 | OI | 1 |
| 正文 | 451 | 未定義 | UI | 1 |
| 正文 | 524 | 未定義 | TA | 1 |
| 正文 | 530 | 未定義 | AAAI | 5 |
| 正文 | 530 | 未定義 | ACM | 12 |
| 正文 | 543 | 未定義 | PMLR | 1 |
| 正文 | 554 | 未定義 | AJ | 1 |
| 正文 | 563 | 未定義 | IEEE | 11 |
| 正文 | 574 | 未定義 | FJBJoD | 1 |
| 正文 | 579 | 未定義 | FAccT | 2 |
| 正文 | 579 | 未定義 | NY | 1 |
| 正文 | 588 | 未定義 | JAMA | 1 |
| 正文 | 593 | 未定義 | ECCV | 2 |
| 正文 | 601 | 未定義 | CUTIS | 1 |
| 正文 | 601 | 未定義 | NEW | 1 |
| 正文 | 602 | 未定義 | YORK | 1 |
| 正文 | 612 | 未定義 | CVF | 4 |
| 正文 | 647 | 未定義 | CF | 1 |
| 正文 | 656 | 未定義 | KS | 1 |
| 正文 | 663 | 未定義 | GA | 1 |
| 正文 | 663 | 未定義 | JC | 1 |
| 正文 | 663 | 未定義 | JL | 1 |
| 正文 | 699 | 未定義 | JB | 1 |
| 正文 | 699 | 未定義 | SC | 1 |
| 正文 | 718 | 未定義 | KIPS | 1 |
| 正文 | 718 | 未定義 | PERROT | 1 |
| 正文 | 718 | 未定義 | TRAN | 1 |
| 正文 | 781 | 未定義 | CIE | 1 |
| 正文 | 796 | 重複定義 | FST | 20 |
| 正文 | 838 | 重複定義 | MST | 119 |
| 正文 | 867 | 未定義 | MSCOCO | 1 |
| 正文 | 925 | 未定義 | LLC | 1 |
| 正文 | 934 | 未定義 | GB | 1 |
| 正文 | 967 | 未定義 | PXL | 5 |


---

# 附录 A：方法学审稿人（R1）审稿卡（Phase 2）

contract_role: methodology
## Dimension Scores

### D1: methodology_rigor
score: block
trigger: "存在动摇核心结论、但可以通过重新分析或补充报告修复的方法缺陷"
block_class: repairable

W1 至 W8 的多项 Major 缺陷合在一起动摇了三项核心结论（可靠且与专家对齐、存在区域差异、对光照不变）以及重复数建议，但都可以用现有数据重新分析或补充报告来修复，未见无法挽救的设计缺陷，因此判为可修复的 block。

### D2: writing_and_structure
score: not_assessed

## Review Body

本文的设计有几处难得的优点：每名受试者的图像在短时间内集中拍摄，众包部分每张图像有 5 个地区 × 5 次重复，并公开了 MST-E 图像和逐条众包标注。问题在于，文章的三项核心推断和实践建议所依赖的分析，要么设定不清，要么缺少不确定性报告，要么超出了设计所能支撑的范围。具体来说：准确性的参照只有一位评分者，而且他也是作者之一；±1 容差掩盖了量表两端的系统性压缩；ICC 没有置信区间；MANOVA 的观测单位无法确定；Spearman-Brown 外推的前提与区域效应结论相互矛盾；"学会对光照不变"缺少等价性检验和培训对照；众包培训内容没有披露。以上问题都可以用现有数据修复。

统计报告充分性判断（依据 APA 7 与统计报告标准第 1–4 节）：总体为 DOES_NOT_MEET。效应量方面，MANOVA 只报告了 Pillai's trace，逐图像 Mann-Whitney 检验没有效应量，地区分布检验的 V² 统计量没有命名，属于 PARTLY_MEETS。置信区间方面，所有 ICC、±1 命中率和平均中位数距离都没有区间，属于 DOES_NOT_MEET。多重比较方面，36 次逐图像检验未做校正，属于 DOES_NOT_MEET，作者已将其标为提示性结果，减轻了影响。检验程序方面，比较 ICC 的 χ² 检验方法与自由度、MANOVA 的设定都未说明，属于 DOES_NOT_MEET。缺失数据（跳过的标注）与统计软件均未报告，属于 DOES_NOT_MEET。可重算的数值见文末 Arithmetic Receipts：两个美国专家数值在设计所隐含的分母下不可达，其余大多因缺少输入而无法重算。

### S1: 公开 MST-E 及逐条众包标注
**Evidence Anchor**: dataset: MST-E crowdsourced annotations csv (Appendix C data card) — per-annotation fields subject, image, region, annotation

数据卡给出了逐图像元数据（姿势、光照、口罩、受试者 MST）和逐条众包标注（受试者、图像、地区、标注值），地区差异与光照分析因此可以被独立复现和扩展。下文多条修改建议都依赖这份已公开的数据。

### S2: 按非交叉标注设计选择单向随机 ICC
**Evidence Anchor**: text: §6 Inter-Rater Reliability "As the group of annotators was not consistent from image to image, we use a one-way random, single score ICC"

众包部分每张图像的标注者并不固定，作者据此采用单向随机模型，没有误用双向模型，说明对 McGraw & Wong 的模型选择逻辑理解正确。

### S3: 拍摄时间受控，真实肤色在不同光照下保持恒定
**Evidence Anchor**: text: §3 "All images and videos of a subject were collected within a short timespan of 4 hours"

同一受试者的全部图像在 4 小时内拍摄，排除了季节或晒黑造成的真实肤色变化。用同一个受试者级标签比较不同光照下的标注，因此有站得住的恒定目标。

### S4: 逐图像检验结果完整报告
**Evidence Anchor**: table: Appendix E Figure 7(b) Challenging Images — all 18 per-image U and p values reported, including non-significant rows such as S18 p = 1.000000

附录 E 列出了全部逐图像检验，包括大量不显著的结果，没有选择性报告。

### S5: 多地区、多重复的密集标注设计
**Evidence Anchor**: text: §6 "Each task was replicated 5 times in each region resulting in 25 annotations per image."

5 个地区、每区 5 次重复，远多于常见的 3 次重复，使地区层面的比较和关于重复数的经验分析成为可能。

### S6: 构念界定和专家选择的理由透明
**Evidence Anchor**: text: §5 "dermatologists interviewed in the pilot study were more likely to attempt to assess skin tone beneath clothing"

作者通过预研究明确要测的是社会感知意义上的肤色，而不是医学评估，并据此选择摄影师作为专家。构念与评分者类型的对应关系交代得清楚。

### S7: 用混入相似图像的方式减轻记忆效应
**Evidence Anchor**: text: §6 "the images were mixed into a much larger set of similar images to prevent face recall among annotators"

同一受试者有大量图像，把它们混入相似图像池可以减少标注者凭记忆作答，这是对重复刺激的合理控制。

### W1: 准确性的参照标准只来自一位非独立的评分者
**Severity**: Major
**Evidence Anchor**: text: §3 "Images were first annotated by an author and sent to Dr. Monk for final golden annotations."
**Confidence**: 4 — 心理测量与参照标准效度方法学

"准确性"以 Dr. Monk 一人给出的受试者级标签为参照（数据卡注明共 19 个唯一的专家标注，每名受试者一个值），而且这些标签是一位作者先标注、再交由 Dr. Monk 审定的。这里有三个问题。第一，参照标准本身的信度未知：没有第二位专家，没有重测，也没有报告作者预标注与最终标签的一致程度，因此"与专家对齐"的估计里缺少参照端的误差。第二，作者的预标注可能对最终标签产生锚定。第三，Dr. Monk 是本文作者之一，参照标准与研究者并不独立。论文同时把肤色感知定位为主观、受文化影响的判断，在这种情况下把单一评分者的标签称为"oracle"，需要更谨慎的论证。建议：报告作者预标注与最终标签的一致率；如有可能，请第二位独立的 MST 专家对 19 名受试者盲评，并报告二者的加权 kappa；正文把结论表述为"与量表创建者的标注一致"，不要写成一般意义上的"准确"。

### W2: ±1 容差与平均距离掩盖了随 MST 等级变化的方向性偏差
**Severity**: Major
**Evidence Anchor**: figure: Figure 8(a) Global Annotation Confusion Matrix — row Intended MST 10: 50 at column 8, 36 at column 9, 2 at column 10; row 5: 50 at column 4
**Confidence**: 4 — 有序评分一致性分析；数值按图中行百分比近似读取

两个准确性指标（中位数落在 ±1 内的比例、平均中位数距离）都不区分方向。审稿人按 Figure 8(a) Global 的行百分比粗略计算（另见 W13 关于该图分母的问题），各行的带符号平均偏差约为：MST1–3 约 +0.8（标得更深），MST5 约 −1.2，MST10 约 −1.8（标得更浅）。MST10 行只有约 38% 落在 ±1 内，标为 10 的只有 2%。按受试者数加权的完全一致率约为 30%。这是典型的向量表中段压缩，而它对公平性研究的影响恰恰集中在量表两端，例如最深肤色会被系统性地归入 8–9。中位数共识进一步压低了离散度，所以"94.7% 的受试者在 ±1 内"与上述偏差可以同时成立。此外，±1 阈值借自 6 点的 FST 研究，用在 10 点量表上相对宽松，论文没有论证两者的等价性。建议：按 MST 等级报告带符号误差及其区间、完全一致率，以及与参照标签的二次加权 kappa 或有序 Krippendorff's α；对阈值做敏感性分析（完全一致与 ±2）；在讨论中说明两端压缩对下游公平性分析的影响。

### W3: ICC 只有点估计，没有任何不确定性报告
**Severity**: Major
**Evidence Anchor**: absence: §5 and §6 Inter-Rater Reliability — expected 95% confidence intervals for every ICC estimate; checked §5, §6, Figure 3(a), Figure 3(b) and caption, Figure 5, Appendices E-F
**Confidence**: 4 — 评分者信度估计与区间方法

所有 ICC 都只给了点估计（Figure 3 的条形图没有误差线），而所报告的显著性检验针对的是 ICC = 0 这一零假设，对"可靠"这一结论几乎不提供信息。目标数很少：专家每种条件 18 张图像，众包 Golden 与 Challenging 各 19 张，区间必然很宽。按单向模型、n = 18、k = 5 粗略估算，美国专家 Challenging 的 ICC 约 0.68，对应 95% 区间约为 [0.50, 0.84]；Golden 约 0.84，区间约为 [0.72, 0.93]。也就是说，美国专家在两种光照之间的差异既无法排除，也无法确认，而正文对 Figure 3(a) 中这一可见的下降没有讨论。19 名受试者是按覆盖整条量表挑选的，受试者间方差被有意放大，ICC 的解释应限定在这类刺激集上。建议：为每个 ICC 报告 95% 置信区间（F 分布法，或按图像/受试者做 bootstrap）；删除"ICC 显著"一类针对零值的表述，改为与预先设定的信度基准比较。

### W4: MANOVA 的设定无法确定，不足以支撑区域差异的推断
**Severity**: Major
**Evidence Anchor**: text: §6 Regional Differences in Annotation "the subject annotations were a significantly high predictor of the region of the annotators"
**Confidence**: 4 — 多元方差分析与混合效应模型设定

正文称以地区为自变量、"各受试者的 MST 标注"为因变量做了 MANOVA。但在众包设计中，每张图像的 5 名标注者是从地区标注池中随机抽取的，标注者并没有交叉评完所有受试者，因此无法为同一观测单位构造跨受试者的因变量向量。观测单位是什么（标注者、重复槽位还是图像），N 是多少，各受试者图像数不等如何处理，论文都没有说明。同一标注者对多张图像的评分并不独立，这一结构也被忽略了。结果只报告了 Pillai's trace = 1.97 和 p < 0.05，没有近似 F、自由度、效应量或事后比较，看不出是哪些地区、哪些 MST 等级、朝哪个方向不同（AR9 因缺少输入无法重算）。另外，"subject annotations were a significantly high predictor of the region"把 MANOVA 当成判别分析来解读，方向也颠倒了。建议：改用累积 logit（有序）混合效应模型，地区作为固定效应，标注者与图像（嵌套于受试者）作为随机效应；报告地区效应及地区 × MST 等级交互的估计与置信区间；在控制多重比较的前提下报告地区两两对比；用 MST 点数表示的地区间平均差异作为效应量。

### W5: 区域差异被解释为文化因果，但地区与标注条件混杂
**Severity**: Major
**Evidence Anchor**: text: §8 Conclusion "We show that cultural contexts across geographical regions influence MST annotations."
**Confidence**: 3 — 观察性分组比较中的混杂与因果推断

地区不是随机分配的。它与标注供应商团队、培训的交付方式、薪酬（附录 K 中约每小时 6 至 19 美元）、英语任务的熟练程度、显示设备等因素一起变化。文中把差异归因于"regional cultural contexts"和不同的"mental models"（§6、§7、§8），这是从非随机分组比较中得出的因果解释。即便 W4 的检验修复后显示存在稳定的地区差异，也不能据此推断文化是原因。建议：把结论改写为关联性表述；在局限部分列出上述混杂来源；如有记录，说明各地区标注者的培训流程、设备与质量控制是否一致；在 W4 的混合模型中检验差异是否集中在特定 MST 区段，这比"心理模型不同"更直接可检验。

### W6: Spearman-Brown 外推不足以支撑"每区 1 人或 2 人"的建议
**Severity**: Major
**Evidence Anchor**: text: §6 Replications "one rater per region likely suffices (5 total annotators)"
**Confidence**: 4 — Spearman-Brown 与 k 评分者信度

有三个问题。第一，Spearman-Brown 假定评分者可以互换（平行测量），而论文同时报告地区之间存在系统差异。跨地区合并 k 名评分者时，复合分数的信度取决于地区构成，公式的前提与区域效应结论相互矛盾。第二，建议没有预先设定的信度目标：Figure 5 中三条曲线在 k = 5 时都已约为 0.98，k = 10 时只再增加很少，看不出"困难图像每区 2 人"是依据什么标准得出的。第三，信度不等于准确性。实践者关心的是 k 名标注者的中位数离参照标签有多远，而作者手中每张图像有 25 次重复，完全可以按 k 抽样（分层到地区构成）直接估计中位数与参照标签的一致率和偏差如何随 k 变化。建议用这种经验子抽样替代或补充公式外推，并事先说明目标阈值；讨论部分"每张图像 10 人"的建议也应以此为依据。

### W7: "学会对光照不变"超出了设计所能支撑的范围
**Severity**: Major
**Evidence Anchor**: text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"
**Confidence**: 4 — 等价性检验与刺激抽样设计

支持这一结论的证据是 Golden 与 Challenging 的平均中位数距离都为 0.78，以及 Challenging 条件下 ICC 稍低但仍显著。问题有三。第一，没有等价性检验，也没有预设的等价界值，两个均值相等不等于不变；Figure 8(b) Global 显示 Challenging 条件下离散度更大，例如 MST1 行的完全一致率约为 19%，而 Golden 为 38%。第二，每名受试者只有一张由作者挑选的 Challenging 图像（共 19 张），光照难度没有客观定义。第三，"learn"意味着培训效应，但研究没有未经培训的对照组，也没有培训前后的比较。建议：按受试者配对比较两种条件下的带符号误差与绝对误差，给出差值及其区间，并用预先设定界值的 TOST 等价检验；利用数据卡中逐图像的 lighting 字段，把分析扩展到全部 1515 张图像；删去"learn"的说法，或补充对照数据。

### W8: 众包培训内容未披露，可能与评估刺激重叠
**Severity**: Major
**Evidence Anchor**: absence: §6 and §7 — expected the crowd annotators' MST training procedure and materials, including whether MST-E images were used in training; checked §4, §6, §7, Appendix C, Appendix D, Appendix K, Appendix L
**Confidence**: 3 — 标注任务设计与训练-测试分离

论文多处称众包标注者"trained"（§7、§8 贡献 b），MST-E 本身也被定位为培训标注者的数据集，但正文和附录都没有描述培训材料、时长、合格标准，也没有说明培训中是否使用了 MST-E 的图像或受试者。如果用过，那么在 MST-E 上与参照标签的一致性就存在训练与测试的重叠，"可靠"和"与专家对齐"会被高估；即使没有用过，第三方也无法复现"受过培训的标注者"这一条件。建议：完整描述培训流程与材料（可作为附录发布），明确说明与评估图像或受试者的重叠情况；如有重叠，单独报告在未用于培训的受试者上的结果。

### W9: ICC 的具体形式和目标单位不清，缺少适合有序数据的补充指标
**Severity**: Minor
**Evidence Anchor**: text: §5 Inter-Rater Reliability "we use a two-way random, single score ICC where the subject and annotator are viewed as random effect"
**Confidence**: 4 — ICC 模型选择（McGraw & Wong）

专家部分写明了双向随机、单一评分 ICC，但没有说明是一致性型还是绝对一致型（ICC(C,1) 或 ICC(A,1)）。研究关心的是标注的绝对位置（与参照标签比较、地区间系统偏移），应采用绝对一致型并明确写出。"Per Subject"ICC 的目标单位也不清楚：同一受试者多张图像之间的变化（包括光照）是被算作目标内误差，还是先做了聚合？对于 10 点有序量表，把评分当作等距数据计算 ICC 可以接受，但应说明理由，并补充二次加权 kappa 或有序 Krippendorff's α 作为稳健性检验。

### W10: 专家逐图像检验没有控制多重比较
**Severity**: Minor
**Evidence Anchor**: table: Appendix E Figure 7(a) and 7(b) — 36 uncorrected per-image tests, three with p below .05 (S13 Golden 0.026888, S14 Golden 0.018119, S14 Challenging 0.048632)
**Confidence**: 4 — 多重比较与小样本非参数检验

共 36 次 Mann-Whitney 检验（2 种条件 × 18 张图像），未做校正，其中 3 次 p < .05。在全局零假设成立且各检验独立的情况下，期望假阳性数为 1.8，出现至少 3 次的概率约为 0.27（审稿人计算），因此这一结果与偶然水平相容。每组只有 5 人时，双侧精确检验能达到的最小 p 约为 0.008，高于 Bonferroni 阈值 0.0014，所以这一设计在校正后本来就无法检出逐图像差异。作者已将其定位为"suggestive"，这是恰当的。建议在正文写明上述期望假阳性数，报告效应量（如 rank-biserial 相关），并说明 p 值的计算方法（精确法还是渐近法、是否做了并列校正；AR10 无法重算）。Subject 14 在两种条件下都显著，这一点比"三张图像显著"更有信息量，值得单独说明。

### W11: 专家研究中光照条件与评定顺序完全混同
**Severity**: Minor
**Evidence Anchor**: text: §5 "Participants first annotated the Golden Images set and distractor images."
**Confidence**: 4 — 实验设计中的顺序效应

Golden 总是先评，Challenging 约一周后再评，没有平衡顺序。光照条件因此与评定场次、时间间隔和对任务的熟悉程度完全混同，Figure 3(a) 中美国专家 ICC 的下降无法归因于光照。由于专家研究被定位为探索性的，影响有限；建议在局限部分写明这一点，后续研究采用平衡顺序。

### W12: Open Images 扩展的检验未命名，且把不显著解读为相似
**Severity**: Minor
**Evidence Anchor**: text: §6 Extension to In-the-Wild Annotations "has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset"
**Confidence**: 4 — 信度系数比较与等价推断

比较 ICC 的 χ² 检验没有说明方法和自由度（AR8：只有 df = 4 时才能得到 p ≈ 0.99），"无显著差异"被解读为"similarly consistent"，而这需要等价检验，不显著并不足够。地区分布差异的统计量 V² = 0.0766 没有命名（AR11）；在约 8.7 万张人脸的样本量下，p < 0.05 几乎是必然的，应以效应量为主来解释。§7 说标注者在 Open Images 上"perform similarly"，但 Open Images 没有参照标注，只测了信度，不能据此说明准确性。建议：命名检验方法，报告自由度与区间；把"perform"改为"信度相近"；如有可能，从 Open Images 抽取一个子集请专家标注，以估计准确性。

### W13: Figure 8 的图注与内容不符，各行分母未报告
**Severity**: Minor
**Evidence Anchor**: figure: Figure 8(a) Global Annotation Confusion Matrix — row Intended MST 7 (single subject) shows 2 at column 5 and 2 at column 9, against the caption's median wording
**Confidence**: 3 — 由单元格粒度推断，取决于未报告的分母

图注称展示的是众包标注的中位数，但单元格数值的粒度与中位数不符。只有一名受试者的行（如 Global Golden 的 MST7 与 MST10）出现了 2% 的单元格；一张图像只有一个中位数，这些单元格只能是 0 或 100。即使理解为个体标注，一张图像最多 25 个标注，最小非零比例为 4%（AR7）。各行的分母（图像数 × 标注数、跳过情况、Global 池的构成）都没有报告，读者无法核对该图，也无法核对 W2 中基于该图的偏差估计。建议：更正图注，在每一行标出 n，并说明 Global 池的定义。

### W14: 美国专家的 83.4% 在设计所隐含的分母下不可达
**Severity**: Minor
**Evidence Anchor**: text: §5 Distance from Intended Annotations "88.9% in India and 83.4% in the United States"
**Confidence**: 3 — 粒度检验，依赖由设计推得的分母与取整约定
**Arithmetic Receipt**: AR3

按 §5 与脚注 4，每种条件有 18 张可与参照标签比较的图像（两种条件合计 36 张），每张图像由 5 名专家评定，中位数为整数。在这些分母下，最接近的可达值是 30/36 = 83.3% 与 31/36 = 86.1%，按就近取整得不到 83.4%。只有向上取整才能得到 83.4%，但向上取整又会使 §6 的 94.7%（18/19）变成 94.8%。印度的 88.9% 可以复现（AR2）。差异很小，不影响结论，但提示实际分母或计算方式可能与文中描述不一致。建议：报告每个百分比的分子与分母、是否合并两种条件，以及取整规则。

### W15: 美国专家的平均中位数距离 0.84 在同样分母下不可达
**Severity**: Minor
**Evidence Anchor**: text: §5 Distance from Intended Annotations "0.78 in India and 0.84 in the United States"
**Confidence**: 3 — 粒度检验，依赖由设计推得的分母与取整约定
**Arithmetic Receipt**: AR5

在同样的分母下，整数距离的均值只能取 k/36 的形式，最接近的是 0.833（取整为 0.83）与 0.861（取整为 0.86）。即使某张图像缺一名专家的评分、中位数变成半整数，也得不到 0.84。印度的 0.78（28/36）可以复现（AR4）。建议同 W14，并说明"average median distance"取的是绝对值还是带符号的差。

### W16: 分析代码、专家标注与 Open Images 标注未公开，统计软件未说明
**Severity**: Minor
**Evidence Anchor**: absence: Appendix C data card and Appendix J — expected release of the photographer annotations, the Open Images skin tone annotations and the analysis code, with the statistical software named; checked §4-§6, Appendix C, Appendix E, Appendix H, Appendix I, Appendix J, Appendix L
**Confidence**: 4 — 可复现性审查

论文公开了 MST-E 图像与众包标注，这是重要的优点（S1）。但文中没有说明是否公开摄影专家的标注、Open Images 的 MST 标注和分析代码，也没有写出所用软件以及 ICC、MANOVA 的具体实现。由于 ICC 形式、MANOVA 设定和 χ² 检验方法都不明确（W4、W9、W12），代码是复现这些结果的唯一途径。建议发布分析代码和上述标注，或说明不能发布的原因，并注明软件及其版本。

### W17: 众包标注者样本与缺失数据未报告
**Severity**: Minor
**Evidence Anchor**: absence: §6 Inter-Rater Reliability — expected the number of distinct annotators per region, per-annotator workload, skipped-annotation counts and any quality-control exclusions; checked §6, Appendix C, Appendix D, Appendix K
**Confidence**: 4 — 标注研究的样本与缺失数据报告

每个地区有多少名不同的标注者、每人标注了多少张、跳过和"difficult"标记各有多少、是否有质量控制排除，论文都没有报告，数据卡只提到部分图像少于 25 个标注。这些信息会影响单向 ICC 的解释（同一标注者评多张图像造成的依赖）、中位数的计算（标注数为偶数时中位数是半整数）以及地区比较。建议补充一张描述标注者与缺失情况的表格。

## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations "the consensus annotation agreed within 1 point for all but one subject (94.7%)"
reported_inputs: 报告比例 94.7%（一位小数）；全局众包池对 19 名 MST-E 受试者的共识标注；二元指标为是否落在参照标签 ±1 点内；正文写明为"all but one subject"
assumptions: 分析 N = 19 名受试者（§3 与 §6 所述众包标注覆盖完整 MST-E），每名受试者一个二元结果；论文未声明取整规则，按就近取整处理，理由是本值在向上取整下为 94.8%，AR2 与 AR4 的数值在截断下分别为 88.8% 与 0.77，三者只在就近取整下能同时复现
derivation: 二元均值的粒度为 1/19；18/19 = 0.947368，即 94.737%；该值落在 94.7% 的就近取整区间内
derived_value_or_range: 18/19 = 94.737%
comparison_rule: 可达值须落在报告值按一位小数就近取整所对应的区间内
rounding_interval: [94.65%, 94.75%)
nearest_achievable: 17/19 = 89.474%；18/19 = 94.737%；19/19 = 100%
status: consistent

### AR2
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations "88.9% in India"
reported_inputs: 印度摄影专家的共识标注落在参照标签 ±1 点内的比例 88.9%（一位小数）；每张图像由 5 名专家评定并取中位数
assumptions: 由 §5 与脚注 4 推得每种条件有 18 张可比较图像（19 名受试者减去因程序错误排除的 1 名），两种条件合计 N = 36；若只按单一条件计算则 N = 18，其可达集合是 N = 36 的子集；就近取整（理由见 AR1）
derivation: 二元均值的粒度为 1/36；32/36 = 16/18 = 88.889%，就近取整为 88.9%
derived_value_or_range: 32/36 = 88.889%
comparison_rule: 可达值须落在报告值按一位小数就近取整所对应的区间内
rounding_interval: [88.85%, 88.95%)
nearest_achievable: 31/36 = 86.111%；32/36 = 88.889%；33/36 = 91.667%
status: consistent

### AR3
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations "83.4% in the United States"
reported_inputs: 美国摄影专家的共识标注落在参照标签 ±1 点内的比例 83.4%（一位小数）；每张图像由 5 名专家评定并取中位数
assumptions: N = 36（两种条件合计）或 N = 18（单一条件），依据同 AR2；就近取整（理由见 AR1）；若改用向上取整，30/36 = 83.333% 会变为 83.4%，判定随之改变，但向上取整无法复现 AR1
derivation: 二元均值的粒度为 1/36；与 83.4% 相邻的可达值为 30/36 = 83.333%（取整为 83.3%）与 31/36 = 86.111%（取整为 86.1%）；区间 [83.35%, 83.45%) 内不存在 k/36 或 k/18 形式的值
derived_value_or_range: 30/36 = 83.333% 与 31/36 = 86.111% 之间没有落入区间的可达值
comparison_rule: 可达值须落在报告值按一位小数就近取整所对应的区间内
rounding_interval: [83.35%, 83.45%)
nearest_achievable: 30/36 = 83.333%；31/36 = 86.111%
status: mismatch
finding_ref: W14

### AR4
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations "0.78 in India"
reported_inputs: 印度摄影专家的平均中位数距离 0.78（两位小数）；5 名专家评分的中位数为整数，所以每张图像的距离为整数
assumptions: N = 36 或 N = 18（依据同 AR2）；距离无论取绝对值还是带符号都是整数，不影响粒度；就近取整（理由见 AR1）
derivation: 整数距离均值的粒度为 1/36；28/36 = 14/18 = 0.7778，就近取整为 0.78
derived_value_or_range: 28/36 = 0.7778
comparison_rule: 可达值须落在报告值按两位小数就近取整所对应的区间内
rounding_interval: [0.775, 0.785)
nearest_achievable: 27/36 = 0.7500；28/36 = 0.7778；29/36 = 0.8056
status: consistent

### AR5
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations "0.84 in the United States"
reported_inputs: 美国摄影专家的平均中位数距离 0.84（两位小数）；5 名专家评分的中位数为整数
assumptions: N = 36 或 N = 18（依据同 AR2）；就近取整（理由见 AR1）；若改用向上取整，30/36 = 0.8333 会变为 0.84，但向上取整无法复现 AR1
derivation: 整数距离均值的粒度为 1/36；与 0.84 相邻的可达值为 30/36 = 0.8333（取整为 0.83）与 31/36 = 0.8611（取整为 0.86）；即使有图像缺一名专家评分、中位数为半整数（粒度 1/72），60/72 = 0.8333 与 61/72 = 0.8472 也都不在区间 [0.835, 0.845) 内
derived_value_or_range: 30/36 = 0.8333 与 31/36 = 0.8611 之间没有落入区间的可达值
comparison_rule: 可达值须落在报告值按两位小数就近取整所对应的区间内
rounding_interval: [0.835, 0.845)
nearest_achievable: 30/36 = 0.8333；31/36 = 0.8611
status: mismatch
finding_ref: W15

### AR6
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations "The distance was 0.78 for both well lit and poorly lit images."
reported_inputs: 众包平均中位数距离 0.78（两位小数），Golden 与 Challenging 各 19 张图像；未说明来自全局池还是各地区平均
assumptions: 每种条件 19 张图像；全局池每张图像最多 25 个标注，跳过时中位数可能为半整数；聚合方式未说明
derivation: 若为全局池的整数中位数，可达值为 k/19，与 0.78 相邻的是 14/19 = 0.7368 与 15/19 = 0.7895，都不在 [0.775, 0.785) 内；若含半整数中位数（k/38），29/38 = 0.7632 与 30/38 = 0.7895 也不在区间内；若为五个地区值的平均（k/95），74/95 = 0.7789 落在区间内；结论取决于未报告的聚合方式
derived_value_or_range: 全局池读法下无可达值；地区平均读法下 74/95 = 0.7789
comparison_rule: 可达值须落在报告值按两位小数就近取整所对应的区间内
status: not_computable
not_computable_reason: aggregation_or_weighting_unknown

### AR7
procedure_id: grim
evidence_anchor: figure: Figure 8(a) Global Annotation Confusion Matrix — row Intended MST 10, cell at column 10 shows 2
reported_inputs: 单元格比例 2%（整数精度）；据数据卡与 Figure 7，MST10 只有 1 名受试者，Golden 集中对应 1 张图像；§6 与附录 C 称每张图像 25 个标注，跳过时更少；图注称展示的是中位数
assumptions: 若该行汇总的是这张图像的个体标注，则 N 不超过 25；Global 池的构成与该行的分母均未报告
derivation: 对任意不超过 25 的 N，最小非零比例为 1/25 = 4%，而 2% 的取整区间 [1.5%, 2.5%) 要求 N 至少为 40；按图注的中位数读法，一张图像只有一个中位数，单元格只能为 0 或 100；文中给出的两种读法都无法复现该单元格，但该行的实际分母未报告
derived_value_or_range: N 不超过 25 时最小非零可达比例为 4%；2% 要求 N 至少为 40
comparison_rule: 可达比例须落在报告值按整数就近取整所对应的区间 [1.5%, 2.5%) 内
status: not_computable
not_computable_reason: analytic_n_ambiguous

### AR8
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations "χ2 = 0.26, p = 0.99 > 0.05"
reported_inputs: 卡方统计量 0.26，p = 0.99；用于比较 Open Images 与 MST-E 的 ICC；自由度与检验程序均未报告
assumptions: 卡方分布按其分布族取上尾；不假设任何自由度
tail_convention: upper-tail
derivation: 在 df = 1 至 6 时，0.26 的上尾概率依次为 0.610、0.878、0.967、0.992、0.998、0.9997；只有 df = 4 时取整为 0.99，但论文没有报告 df，也没有说明检验程序，无法比较
derived_value_or_range: df 未知；df = 1 至 6 时 p 依次为 0.610、0.878、0.967、0.992、0.998、0.9997
comparison_rule: 重算的上尾 p 按两位小数取整后应等于 0.99
status: not_computable
not_computable_reason: missing_reported_value

### AR9
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Regional Differences in Annotation "Pillai’s trace = 1.97, p<0.05"
reported_inputs: MANOVA，Pillai's trace = 1.97，p < 0.05；自变量为 5 个地区，因变量为各受试者的 MST 标注；近似 F、假设与误差自由度、观测数均未报告
assumptions: 近似 F 按分布族取上尾；不假设观测单位或 N
tail_convention: upper-tail
derivation: 组数为 5、因变量至少 4 个时 s = 4，Pillai's trace 的理论上界为 4，1.97 在可行范围内；把它换算为近似 F 需要误差自由度，而误差自由度取决于未报告的观测单位与 N
derived_value_or_range: Pillai's trace 的理论范围为 0 至 4；p 无法推得
comparison_rule: 理论上界检查，以及由近似 F 得到的上尾 p 与 0.05 比较
status: not_computable
not_computable_reason: missing_reported_value

### AR10
procedure_id: p_from_test_statistic
evidence_anchor: table: Appendix E Figure 7(a) Golden Images — row MST6 S14, Value 24.0, p 0.018119
reported_inputs: Mann-Whitney U，表中 Value 列为 24.0，p = 0.018119；每组 5 名摄影师（美国与印度）；10 点有序评分，存在并列
assumptions: 视 Value 为 U 统计量；n1 = n2 = 5（§5 每个市场 5 名专家）；不假设尾向、精确法或渐近法、连续性校正或并列校正
tail_convention: unstated
derivation: 无并列时 U 的均值为 12.5，标准差为 √(5×5×11/12) = 4.787；正态近似 z = 2.402，two-tailed p = 0.0163，one-tailed p = 0.0081；加连续性校正后 two-tailed p = 0.0216，one-tailed p = 0.0108；精确分布 P(U ≥ 24) = 2/252 = 0.0079（单侧），双侧为 0.0159；这些都不等于 0.018119，报告值可能来自并列校正的渐近检验，而这需要论文未给出的原始并列结构
derived_value_or_range: two-tailed 0.0159 至 0.0216，one-tailed 0.0079 至 0.0108（不做并列校正的各种标准做法）；并列校正后的值无法推得
comparison_rule: 重算 p 在报告的六位小数精度下应等于 0.018119
status: not_computable
not_computable_reason: nonstandard_p_procedure

### AR11
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations "V2 = 0.0766, p < 0.05"
reported_inputs: 统计量记为 V² = 0.0766，p < 0.05；检验族、自由度与样本量均未报告
assumptions: 无可用假设；V² 可能指 Cramér's V 的平方或其他统计量，论文没有说明
tail_convention: unstated
derivation: 没有命名的检验族和自由度，无法由该统计量推得 p
derived_value_or_range: 无法推得
comparison_rule: 重算的 p 与 0.05 比较
status: not_computable
not_computable_reason: test_family_ambiguous


---

# 附录 B：期刊适配审稿人（EIC）审稿卡（Phase 2）

contract_role: eic
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: writing_and_structure
score: warn
trigger: "摘要或结论的措辞强于证据章节的表述"

## Review Body

本稿报告两项标注研究：§5 的摄影专家探索性研究，以及 §6 的众包标注研究和 Open Images 扩展。稿件同时发布 MST-E 数据集（19 名被摄者，1515 张图像，31 段视频）。从结构与表述看，稿件主干可以追溯：两个对齐指标在 §4 正文中定义；§5 与 §6 明确区分了探索性分析和确证性分析；数据卡（附录 C）、逐图检验表（附录 E）和对先前审稿意见的回应（附录 L）都提高了透明度。

问题集中在三处。第一，§7 讨论和 §8 结论中有几处表述强于 §6 实际给出的证据，涉及「经培训后对光照不变」「地域多元的标注池带来与量表本意的对齐」「不同心智模型导致系统性地区差异」「结论可推广至真实场景」四点。第二，核查这些表述所需的几项方法细节在正文和附录中都找不到，包括众包培训内容、困难图像集的筛选方式、Open Images 分析的统计设定，以及复本数建议所依据的判定阈值。第三，数据集发布是本稿的核心贡献之一，但其使用条款在 §3、附录 I 与 CC BY 声明之间相互矛盾。

这些问题都可以通过改写和补充报告来修复。核心发现在证据章节中可以找到依据：同一地区内标注者之间信度高，共识标注与量表作者的标注在 1 分以内吻合。因此 D2 评为 warn，而非 block。我不对任何具体期刊的契合度作判断。统计推断是否正确由方法学席位负责，下文凡涉及统计之处，只讨论读者能否定位并核查相应主张。

### S1: 对齐指标在正文中定义，并给出先行研究依据
§4 在正文中定义了「1 分内比例」和「平均中位距离」两个指标，并引用先行研究说明 1 分阈值的来源。读者无需翻阅附录即可理解 §5 和 §6 的对齐结果是如何计算的。
**Evidence Anchor**: text: §4 "the average median distance, the expected difference between the median annotation from a group of annotators and the oracle computed across all images"

### S2: 探索性研究与确证性研究的边界清楚
§6 明确把 §5 的专家研究定位为探索性研究，把众包研究定位为对 §5 所生成假设的检验。这让读者知道两部分结论应以不同强度来理解。
**Evidence Anchor**: text: §6 "Unlike the exploratory analysis of experts that used a subset of the MST-E dataset, in this setting we have enough statistical power"

### S3: 数据集文档较完整，并同时发布了众包标注
附录 C 的数据卡列出了字段定义、各 MST 等级的被摄者数、图像数和视频数，以及维护计划。逐地区的众包标注 CSV 也一并发布，读者可以据此独立复核 §6 的部分结果。
**Evidence Anchor**: dataset: MST-E data card (Appendix C) — per-MST-level counts of subjects, images and videos, plus the released per-region crowdsourced annotation CSV

### S4: 逐图检验结果完整列出
附录 E 列出了黄金集和困难集每张图像的 Mann-Whitney U 统计量与 p 值。读者可以直接核对 §5 中「三张图像差异显著」的说法。
**Evidence Anchor**: figure: Figure 7 — per-subject Mann-Whitney U values and p for the Golden and Challenging sets

### S5: 正文交代了选择摄影师作为专家的理由
§5 用预研究中的观察说明了为何不用皮肤科医生而用摄影师，把专家类型的选择与「社会感知」这一标注目标联系起来。这项设计决策的依据就在正文中。
**Evidence Anchor**: text: §5 "dermatologists interviewed in the pilot study were more likely to attempt to assess skin tone beneath clothing which was not depicted"

### S6: 局限性一节坦率说明了成本与范围
局限性一节正面承认建议的复本数远高于现行做法，并讨论了预算受限时的替代方案，也承认被摄者数量少。
**Evidence Anchor**: text: §7 "This is a very large jump from the status quo of 3 annotators per image"

### S7: 公开了对先前审稿意见的处理
附录 L 逐条说明了先前审稿意见以及本版的对应修改，便于读者了解稿件的演变过程。
**Evidence Anchor**: text: Appendix L "This paper was previously submitted to FAccT 2023"

### W1: 众包标注者所受培训从未被描述，但「经培训」是多项结论的限定语
**Severity**: Major
**Evidence Anchor**: absence: §6 众包标注流程 — expected 众包标注者所受 MST 培训的内容、时长、所用示例以及培训材料是否包含 MST-E 图像; checked §4, §6, §7, §8, 附录 C, 附录 D, 附录 K
**Confidence**: 4 — 逐节核对了正文和全部附录中关于标注者准备工作的描述

摘要使用了「trained crowdsourced annotators」的说法；§7 称众包标注者在任务前接受过 MST 标注培训；结论 (a)、(b)、(e) 都以「经培训」作为限定。然而 §6 只说标注者除了「the instructions they received for this task」之外没有领域专长，培训的内容、时长、示例来源和是否经过考核都没有描述。MST-E 同时又是评估集，读者因此无法判断培训材料是否与被评估的图像重叠。如果有重叠，§6 的一致性结果和对齐结果就需要另作解释。读者也无法复现「经培训标注者」这一实验条件。这一缺陷不会推翻一致性结果本身，但贯穿各条结论的「经培训」限定因此既无法核查，也无法复现。建议在 §6 正文中补充培训方案，或者在正文中明确指向载有该方案的附录，并说明培训材料与 MST-E 评估图像是否重叠。

### W2: 「学会对光照不变」的表述强于 §6 的证据
**Severity**: Major
**Evidence Anchor**: text: §7 "We find that annotators are able to learn to be invariant to environmental factors such as lighting quality"
**Confidence**: 4 — 对照了 §6 文字与图 3、图 5 的渲染图

§7、结论 (b)（「with training, can provide annotations invariant to lighting conditions」）和结论 (e) 都把结果写成标注者「学会」了对光照「不变」。这有两个问题。其一，研究中没有培训前后的对照，也没有未培训组的对照，「learn」一词在证据章节中找不到对应的依据。其二，§6 自己报告的结果显示，困难图像的 ICC 区间（0.82–0.95）低于黄金图像（0.9–0.96）。图 5 中困难图像曲线在每个复本数上都是最低的；图 3(a) 中美国专家在困难集上的 ICC（约 0.68）也明显低于黄金集（约 0.84）。§6 还据此建议对低质量图像使用 10 名标注者，这与「不变」的说法相矛盾。真正有证据支持的，是 §6 报告的共识距离在两种光照下都是 0.78。建议改写为：共识标注与量表作者标注之间的距离在两种光照下相近，但单个标注者的一致性在困难光照下有所下降。同时应删除「learn」，或者补充相应的对照证据。

### W3: 「地域多元的标注池带来对齐」缺少与单一地区标注池的对比
**Severity**: Major
**Evidence Anchor**: text: §8 "when collecting annotations from a diverse geographical pool, annotators are able to provide annotations that match the original intention behind the MST scale"
**Confidence**: 4 — 核对了 §6、§7、§8 的文字与附录 F 的图 8

结论 (c) 和 §7 都把与量表作者标注的对齐归因于标注池的地域多样性（§7 原文为「a geographically diverse annotator pool provides annotations that are in line with the intended use」）。但 §6 同时写道，平均中位距离对「every region and image condition」都小于 1，也就是说，单一地区的标注池在这一标准下同样达标。正文只报告了全局池的 94.7%，没有给出各地区的 1 分内比例或距离数值，也没有比较全局池与单一地区池。现有证据只能支持「各地区池和全局池都在 1 分以内」，读者无法从证据章节核查「多样性带来对齐」这一因果性表述。附录 F 图 8 中的逐地区混淆矩阵本可支撑这一比较，但正文没有汇总这些数据。建议在 §6 正文中增加一张表，列出各地区与全局池的 1 分内比例和平均中位距离。如果全局池并没有明显优于单一地区池，就应改写结论 (c) 和 §7，把推荐地域多元标注池的依据放在地区间的差异上，而不是放在对齐度上。

### W4: 复本数建议缺少明确的判定阈值，各节给出的建议也不一致
**Severity**: Major
**Evidence Anchor**: text: §6 "one rater per region likely suffices (5 total annotators). For more challenging images, two annotators per region is beneficial."
**Confidence**: 4 — 依据图 5 渲染图的目测读数与 §6、§7 文字对照得出，读数为近似值

这项建议基于图 5 的 Spearman-Brown 预测，但正文没有说明判断「suffices」或「beneficial」时用的是什么目标信度。从图 5 读数看，k=1 时预测信度已约为 0.89（困难集）至 0.94（黄金集），k=5 时约为 0.97–0.98，k=10 时约为 0.98–0.99。没有阈值，读者就无法核查为何选定 5 和 10。此外，§6 把 k 定义为所有地区的总复本数，而 Spearman-Brown 计算并不刻画「每个地区一名」这种结构。因此「one rater per region」「at least five different geographical regions」这类按地区分配的要求，无法从图 5 推出。各节的建议也不一致：§6 建议只对低质量图像使用 10 名标注者；§7 的建议清单写的是每张图像 10 份标注，并说尤其适用于困难图像；局限性一节则写「10 annotators per image if image quality is unknown」。建议在 §6 写明目标信度阈值及其依据，分开说明「总复本数」和「地区覆盖」这两项建议各自的证据来源，并统一全文的表述。

### W5: 「不同心智模型导致系统性地区差异」这一头条表述，在正文中只有一个总体检验支撑
**Severity**: Major
**Evidence Anchor**: text: Abstract "annotators from different geographic regions rely on different mental models of MST categories resulting in annotations that systematically vary across regions"
**Confidence**: 3 — 结构与表述层面的判断有把握，统计检验是否适用不在本席位的范围内

这是摘要中的两项头条发现之一。对众包数据，§6 只报告了一次 MANOVA 的总体结果（Pillai's trace = 1.97），而且把方向写反了：分析中地区是自变量，正文却写成「subject annotations were a significantly high predictor of the region」。Open Images 部分的「V2 = 0.0766」也没有说明是什么统计量。正文没有交代哪些地区在哪些 MST 区段偏深或偏浅、偏离幅度多大。唯一带方向的例子是 §5 专家研究中的 Subject 14（图 4），而作者自己把该研究定位为探索性研究。「mental model」在全文中没有定义，也没有操作化。§6 的信度段落又说众包标注者「using a shared mental model of the MST categories」，图 3(b) 中全局池的 ICC 也很高，读者无法从正文判断「共享」与「不同」如何同时成立。地区差异的存在本身有证据，但「系统性」和「不同心智模型」这两个更强的说法，在证据章节中找不到依据。建议在 §6 正文中报告各地区相对全局中位数的偏离方向与幅度（例如按 MST 区段计算的平均偏差），定义「mental model」或改用描述性措辞，并修正 MANOVA 的表述方向。

### W6: 数据集使用条款在三处相互矛盾
**Severity**: Major
**Evidence Anchor**: text: §3 "The images cannot be used to train machine learning models. The images and annotations are licensed under CC BY."
**Confidence**: 4 — 逐字对照了 §3、§7、附录 C 与附录 I；对 CC BY 条款含义的判断基于该许可的通行理解

CC BY 许可本身不限制用途，模型训练也包括在内，这与同一段中「不得用于训练」的条款直接冲突。§3 允许的用途是「research, model evaluations, or annotator-training purposes only」；附录 I 却写成「research or annotator-training purposes only」，并说明标注也只能用于这两类用途，其中没有模型评估。而 §7 和数据卡（附录 C 的 Dataset Use(s) 一栏）都把模型评估列为推荐用途。数据集发布是本稿的核心贡献之一，可使用者无法从文中确定自己可以合法地做什么。建议只采用一个许可：如果需要限制用途，应改用带用途限制的许可而不是 CC BY，或者分别说明图像和标注各自的许可；并在 §3、附录 C、附录 I 和数据集网站上使用一致的允许用途与禁止用途清单。

### W7: 专家研究的样本数与汇总方式表述不一致
**Severity**: Minor
**Evidence Anchor**: text: §5 "Experts were asked to annotate a total of 50 images, 19 from the MST-E Golden Images or Challenging Image sets"
**Confidence**: 4 — 对照了 §5 正文、脚注 4 与附录 E 的图 7

正文写的是 19 张，脚注 4 才说明有 1 名被摄者因程序错误被排除；附录 E 的图 7 实际只列出 18 名被摄者，其中没有 S16。§5 中的 88.9% 和 83.4% 没有说明分母是 18 张还是两轮合计的 36 张，也没有说明是否为两种光照条件的平均值。83.4% 不等于任何 n/18 的比例，可能是两轮比例的平均。建议在正文中直接写明实际分析的图像数，以及百分比的汇总方式。

### W8: 图 4 的文字描述与困难图像的分布不符
**Severity**: Minor
**Evidence Anchor**: figure: Figure 4(b) — US panel counts fall at MST4, MST5 and MST6, none at MST7
**Confidence**: 3 — 基于渲染图的目测读数

§5 说美国摄影师把 Subject 14 标得更深（MST5–MST7）。这对图 4(a) 的黄金图像成立，但在图 4(b) 的困难图像中，美国组的标注落在 MST4–MST6。另外，附录 E 显示该被摄者的量表作者标注为 MST6，正文没有说明两组中哪一组更接近这一标注，读者只能自己去对照附录。建议分别描述两张图像的标注分布，并注明参考标注。

### W9: 数据卡中数据主体与标注来源的描述有误
**Severity**: Minor
**Evidence Anchor**: text: Appendix C "Data about image search queries"
**Confidence**: 4 — 逐栏对照了数据卡与 §3 的数据集描述

数据卡「Data Subject(s)」一栏写的是「Data about image search queries」，与数据集的实际内容（19 名同意参与的模特的图像和视频）不符，看起来像是模板残留。数据卡在人类属性来源一栏只写了由量表作者标注，没有反映 §3 所述的两步流程：先由一名作者标注，再交量表作者确定。数据卡是该数据集文档的主要载体，建议逐栏核对。

### W10: 摘要与局限性一节未交代参考标注者的身份及锚定流程
**Severity**: Minor
**Evidence Anchor**: text: §3 "Images were first annotated by an author and sent to Dr. Monk for final golden annotations."
**Confidence**: 3 — 本条只涉及披露与表述，这一安排是否构成方法学问题由方法学席位判断

摘要说结果与「an expert in the MST scale」一致。§3 写的是「by the authors as well as the MST creator」，读起来像是作者团队之外的第三方。实际上 Dr. Monk 是本文作者之一，他的参考标注也是在另一名作者的初始标注基础上确认的。全文所有关于「对齐」的结论都以这一位标注者的判断为参照，而本文的主题恰恰是标注的主观性；局限性一节却没有讨论只用单一参考标注者这一点。建议在 §3 或 §4 中写明他的作者身份和锚定流程，并在局限性一节讨论单一参考标注可能带来的影响。

### W11: Open Images 扩展部分的结论范围超出了实际测量的内容
**Severity**: Minor
**Evidence Anchor**: text: §6 "this shows that recommendations based on annotator behaviors observed in our controlled studies likely translate to real-world scenarios"
**Confidence**: 4 — 对照了 §6 的 Open Images 段落、§7 与局限性一节

Open Images 没有参考标注，§6 在这部分实际只比较了 ICC 和各地区的标注分布。但 §6 结尾说各项建议「likely translate」，§7 说标注者在 Open Images 上「perform similarly」，局限性一节还说「we believe our results will translate to other domains」。对齐度结论和复本数建议都没有在 Open Images 上检验过。建议把措辞限定为：信度和地区差异这两项性质在 Open Images 上得到了重现。

### W12: Open Images 分析的统计设定在正文和附录中都找不到
**Severity**: Minor
**Evidence Anchor**: absence: §6 Extension to In-the-Wild Annotations — expected 每张人脸的标注复本数与地区分配、所用 ICC 形式、得出 χ2 = 0.26 与 V2 = 0.0766 的检验名称; checked §4, §6, §7, 附录 C, 附录 D, 附录 J
**Confidence**: 4 — 检索了列出的全部章节

正文没有说明以下几点：41,471 张图像、86,809 张人脸是否同样每个地区各有 5 份标注；ICC 采用的是哪种形式；比较两组 ICC 时所用的 χ² 检验是什么；「V2」又是什么统计量。读者因此无法核查 §6 的这三个数字。建议在正文中补充，或在正文中明确指向载有这些信息的附录。

### W13: 研究问题 (b) 问的是「质量」，结果回答的却是「差异」
**Severity**: Minor
**Evidence Anchor**: text: §1 "Does annotator location, a proxy for cultural context and lived experience, matter and have any effect on annotation quality?"
**Confidence**: 4 — 对照了 §1 的研究问题与 §6、§7、§8 的结论

§6 检验的是各地区的标注分布是否不同。本文对「质量」唯一的操作化是与参考标注的距离，而在这一指标上各地区都在 1 分以内。正文没有把结果逐一对应到 §1 提出的三个研究问题，贡献清单也只在结论中才出现。建议在引言末尾加入贡献清单，并在 §7 中逐一回答问题 (a)、(b)、(c)，使问题 (b) 中「质量」与「差异」的区别清晰可见。

### W14: 正文从未引用附录 F
**Severity**: Minor
**Evidence Anchor**: absence: §6 Distance from Intended Annotations — expected 指向附录 F 图 8 逐地区混淆矩阵的引用; checked §4, §5, §6, §7, §8
**Confidence**: 4 — 检索了正文中全部附录引用

附录 F 是全文唯一给出逐地区对齐证据的地方，但正文中没有任何指向它的引用，读者只有通读附录才会发现。建议在 §6「Distance from Intended Annotations」一段中加以引用。

### W15: 正文未说明被跳过的标注及「困难」标记如何处理
**Severity**: Minor
**Evidence Anchor**: text: Appendix C "Some images were too hard to annotate"
**Confidence**: 3 — 缺失数据对困难集结果的影响大小，需由方法学席位评估

数据卡说明部分图像被一些标注者跳过，因此不足 25 份标注。但正文没有报告被跳过的数量、跳过比例在不同光照条件之间是否有差别，也没有说明中位数和 ICC 如何处理缺失。被跳过的往往正是困难图像，这直接关系到如何解读困难集的结果。§6 还提到标注者可以把图像标为「difficult」，但这一标记的分布同样没有报告。建议在 §6 中报告缺失的数量及处理方式。

### W16: 困难图像集的筛选标准未说明
**Severity**: Minor
**Evidence Anchor**: absence: §3 Challenging Images set — expected 困难图像的筛选者与筛选标准以及光照条件的界定方式; checked §3, §4, §5, 附录 B, 附录 C
**Confidence**: 4 — 检索了列出的全部章节

光照稳健性的结论依赖黄金集与困难集之间的对比。但 §3 只说困难集「mirrored the Golden Images set with different lighting conditions」，没有说明由谁、按什么标准挑选，也没有说明各被摄者的困难程度是否可比。附录 B 只给出了图像，数据卡中 lighting 字段也只有 well_lit 这一个示例值。建议补充筛选流程，并给出 lighting 字段所有取值的定义。

### W17: 背景部分有个别引用与所支撑的表述不匹配
**Severity**: Minor
**Evidence Anchor**: text: §2 "studies find that expert and crowdsource annotators tend toward fairly similar annotations on the FST [33, 48, 50]"
**Confidence**: 2 — 仅依据参考文献列表中的标题判断，未查阅原文

作者强调这一点「Critically for this work」，但从标题看，[50] 讨论的是 COVID-19 皮肤表现相关文献中缺少深色皮肤图像，与专家和众包标注的一致性没有明显关联。此外，§2 把 Casual Conversations 数据集归于 Hazirbas et al. [38]，附录 A.3 中同一段内容却归于 Liu et al. [51]。建议核对这些引用。


---

# 附录 C：两位审稿人看论文前预先写下的评分标准（Phase 1）

## 方法学审稿人

## Contract Paraphrase

D1（methodology_rigor）：从方法学严谨性的角度，这一维度要求研究设计、数据处理、统计报告和可复现条件都达到本领域同行评审的门槛。对以标注共识与主观性为主题的研究，具体意味着五点。第一，"准确性""一致性""可靠性"等核心构念要有明确且站得住的操作化定义和参照标准。第二，所选的一致性或信度指标要与评分量表的测量水平（例如有序等级）相匹配，并报告置信区间等不确定性。第三，组间比较要有恰当的模型设定，并控制多重比较、报告效应量。第四，任何稳健性或不变性结论都要有足以支撑它的设计。第五，数据、标注说明和培训材料要足以让他人复现。这是合同中唯一的强制维度，也是我作为方法学审稿人唯一负责评分的维度：致命问题直接导致拒稿，评为 block 或 warn 都会导致大修。

D2（writing_and_structure）：这一维度关注稿件的组织结构、论述是否清晰，以及是否符合方法类论文的期刊惯例。它是普通优先级维度，只由主编（eic）角色评分，不在我的评分范围内。从方法学视角看，它和 D1 的关联在于：方法、分析流程和结果的写法是否清楚到读者能准确理解并复核所做的分析。D2 评为 warn 或更差时触发小修。

## Scoring Plan

### D1: methodology_rigor
dimension_id: D1
what_to_look_for: 核心构念（准确性、一致性、可靠性、与专家对齐）的操作化定义及参照标准是否合理；一致性或信度指标是否与有序量表的测量水平匹配（ICC 模型与类型的选择依据、加权 kappa 或 Krippendorff's alpha 等替代指标），是否报告置信区间；组间差异检验的模型设定（是否考虑标注者与刺激的随机效应结构）、多重比较校正与效应量；稳健性或不变性结论所依赖的设计（顺序效应是否平衡、刺激数量与代表性）；数据、标注说明与培训材料的公开程度和可复现性。
what_triggers_block: 存在动摇核心结论、但可以通过重新分析或补充报告修复的方法缺陷，例如：信度或一致性指标与数据测量水平不匹配且未给出理由或替代分析；关键估计值没有置信区间等不确定性报告；组间比较未控制多重比较或未报告效应量；"可靠""与专家对齐"等结论超出了所报告分析能支撑的范围。
what_triggers_warn: 方法总体能支撑主要结论，但有需要澄清或补充的次要问题，例如：ICC 模型与类型或 Spearman-Brown 校正的选择依据未说明；容差阈值或共识规则缺少敏感性分析；样本量、刺激数量或标注者招募与排除标准报告不完整；数据或培训材料的公开计划不够具体。
what_triggers_fatal: 研究设计从根本上无法回答所提出的问题，且无法通过修订挽救，例如：作为"准确性"判据的参照标准缺乏效度依据而主要结论完全依赖于它；设计中存在无法分离的混淆（顺序或刺激效应与比较因素完全混同），使核心比较或稳健性结论失效；关键结果无法按所述程序复现，或数据处理存在严重错误。

criteria_binding_unavailable

[CONTRACT-ACKNOWLEDGED]


## 期刊适配审稿人

## Contract Paraphrase

D1（methodology_rigor，强制维度）：从编辑监督的角度看，这一维度检验研究设计、数据处理、统计报告以及可复现性支持是否达到该领域同行评审的通行标准。它的评分权属于方法学审稿人，我不为其制定评分计划，也不对其打分；但我清楚它在合同中的分量最重：任何审稿人在此维度给出致命问题即导向拒稿，给出阻断或警告级评分则都要求大修，因此它是决定稿件走向的首要关口。

D2（writing_and_structure，普通维度）：这一维度由我负责，考察稿件的组织方式、表述清晰度，以及是否遵循方法类论文的一般写作惯例。具体来说，我会检查各项独立贡献是否被清楚地定位和区分，摘要与结论中的主张是否与证据章节的内容相符，关键方法细节能否在正文中找到而不是只放在附录里，以及整体结构是否让读者能够找到并核查每项主张的依据。由于没有作者确认的目标期刊，我只依据方法类论文的一般惯例作判断，不作任何期刊契合度判断。任一审稿人在此维度给出警告或更严重的评分会触发小修条件，而只有全部维度都通过时才可能接受。

## Scoring Plan

### D2: writing_and_structure
dimension_id: D2
what_to_look_for: 各项独立贡献是否被清楚陈述且彼此可区分；摘要与结论中的每项主张能否在正文证据章节中找到对应依据且强度一致；复现与核查所需的关键方法细节（数据来源、处理流程、评估设置、统计报告要点）是否可在正文中直接定位而非仅见于附录；章节组织与表述是否让读者能从主张追溯到其依据。
what_triggers_block: 结构或表述缺陷使读者无法定位或核查至少一项核心主张的依据，例如摘要或结论中的核心主张在正文证据章节中找不到任何对应支撑，或核查核心主张所必需的方法细节只存在于附录且正文没有给出可定位的指引。
what_triggers_warn: 核心主张的依据整体可追溯，但存在局部问题，例如贡献之间界限模糊或相互重叠、摘要或结论的措辞强于证据章节的表述、部分次要方法细节需到附录查找且正文指引不足，或章节组织提高了核查成本但不妨碍最终完成核查。

criteria_binding_unavailable

[CONTRACT-ACKNOWLEDGED]
