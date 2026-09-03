# PRD 第 4 章：自定义维度配置（网易版 ModSDK）

> **文档定位**：本 PRD 仅描述需求，不写代码。每条需求项旁边标注「**实现位置**」+「**文档依据**」+「**是否需脚本**」，开发按此拆任务。
>
> **文档依据来源**：`官方代码文档/mcguide/20-玩法开发/15-自定义游戏内容/4-自定义维度/`
> - [1-自定义维度.md](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md)（dmXXX.json 文件格式与 components 表）
> - [2-群系地貌.md](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md)（群系源/自定义高度/生物 tag）
> - [3-生物生成.md](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/3-%E7%94%9F%E7%89%A9%E7%94%9F%E6%88%90.md)（spawn_rules 关闭原版生物）

---

## 4.1 维度基础规范（三个星际维度共用规则）

### 4.1.1 维度 ID 规则

| 维度 | 维度 ID | dmXXX.json 文件名 |
|---|---|---|
| 近地太空 | 22 | `dm22.json` |
| 月球 | 23 | `dm23.json` |
| 火星 | 24 | `dm24.json` |

**禁止**使用 0、1、2（原版主世界/下界/末地 ID）。

> **文档依据**：[1-自定义维度.md:15](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L15)
> "还可以通过配置添加编号为 22 到 2147483647 的新自定义维度"
>
> [1-自定义维度.md:21](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L21)
> "添加一个以维度id命名的json文件：如dm23333.json"
>
> **实现位置**：BP 端 `MCHuojian_BehaviorPack/netease_dimension/dm22.json` 等 3 个文件（**注意是 `netease_dimension/` 不是 PRD 原文写的 `dimensions/`**，PRD 原文有误，已按官方文档纠正）。
> **是否需脚本**：否。dmXXX.json 文件存在即视为维度声明，引擎自动注册。

### 4.1.2 文件结构

**纠正 PRD 原文**：PRD 原文写"放置在 mod 的 dimensions 文件夹下"是错的，官方文档明确是 `netease_dimension/` 文件夹。

| 路径 | 内容 |
|---|---|
| `behavior_pack/netease_dimension/dm22.json` | 近地太空维度声明 |
| `behavior_pack/netease_dimension/dm23.json` | 月球维度声明 |
| `behavior_pack/netease_dimension/dm24.json` | 火星维度声明 |
| `behavior_pack/netease_biomes/dm22/<群系>.json` | 近地太空群系配置（继承原版群系） |
| `behavior_pack/netease_biomes/dm23/<群系>.json` | 月球群系配置 |
| `behavior_pack/netease_biomes/dm24/<群系>.json` | 火星群系配置 |
| `behavior_pack/spawn_rules/<生物>.json` | 生物生成规则（关闭原版生物用） |

> **文档依据**：[14-配置与JSON文件关系.md:92-96](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/14-%E9%85%8D%E7%BD%AE%E4%B8%8EJSON%E6%96%87%E4%BB%B6%E5%85%B3%E7%B3%BB.md#L92-L96)
> 自定义维度配置对应文件 = `behavior_pack_xxxxxx/netease_dimension/维度配置名称.json`
> 自定义生物群系对应文件 = `behavior_pack_xxxxxx/netease_biomes/生物群系配置名称.json`

### 4.1.3 服务端/客户端同步

| 子项 | 实现 |
|---|---|
| 维度注册必须服务端注册 | dmXXX.json 文件存在即注册，**无需在脚本里手动调用注册接口**（未在文档找到对应 RegisterDimension 接口，存疑，TODO 查 mcdocs） |
| 客户端同步维度信息 | 引擎自动处理，无需配置 |
| 单机/租赁服/多人联机均可进入 | 引擎自动支持（自定义维度本身支持联机） |
| 不修改原版任何维度配置 | 不写 `overworld.json` / `nether.json` / `the end.json` 即可（[1-自定义维度.md:40](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L40) 写明原生维度对应文件名，"请勿使用维度id命名"） |

> **是否需脚本**：否。维度声明纯靠 JSON 文件，引擎自动加载。

### 4.1.4 重生规则

| 条件 | 行为 |
|---|---|
| 玩家在星际维度死亡 + 该维度内设置了重生点 | 在本维度重生 |
| 玩家在星际维度死亡 + 未设置重生点 | 返回主世界的重生点，**不会**在太空/月球/火星原地复活 |

> **文档依据**：⚠️ 维度 json 的 components 表里**没有**重生规则字段（[1-自定义维度.md:46-65](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L46-L65) 全 14 个字段已枚举，无重生相关）。
>
> **实现位置**：脚本。监听 `OnLocalPlayerDieServerEvent`（玩家死亡事件，需查 mcdocs/1-ModAPI/事件/玩家.md 确认事件名），判断死亡维度 id，按规则设置 `SetPlayerSpawnPos` 类接口。**具体接口名 TODO，待查 mcdocs**。
>
> **是否需脚本**：是。

### 4.1.5 原版生物生成开关（三个维度全关）

近地太空 / 月球 / 火星：**关闭原版生物生成**（僵尸、骷髅、牛羊等原版生物不生成），只生成模组自定义生物。

> **文档依据**：[3-生物生成.md:77-126](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/3-%E7%94%9F%E7%89%A9%E7%94%9F%E6%88%90.md#L77-L126)
> 文档示例"在 dm5 维度冰原上不会生成兔子"的方法：重写 rabbit 的 `spawn_rules`，在 `minecraft:biome_filter` 中加 `{ "test": "has_biome_tag", "operator": "!=", "value": "dm5" }`。
>
> **实现位置**：
> 1. **群系层打 tag**：dm22/dm23/dm24 群系 json 里 components 下加 `"dm22": {}` / `"dm23": {}` / `"dm24": {}`（[2-群系地貌.md:176](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L176) "群系开发模板自动添加的标签"）。
> 2. **spawn_rules 重写**：在 `behavior_pack/spawn_rules/` 下为每个原版生物（zombie.json / skeleton.json / cow.json / sheep.json 等）重写 spawn_rules，加 `minecraft:biome_filter: { "test": "has_biome_tag", "operator": "!=", "value": "dm22" }` × 3 个维度。
>
> **是否需脚本**：否。纯 JSON 配置。

### 4.1.6 世界生成（自定义地形，不用原版超平坦/普通）

使用自定义地形生成器，生成对应星球地貌。

> **文档依据**：[1-自定义维度.md:49-54](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L49-L54) 维度 components 表里有 3 个生成器可选：
> - `netease:generator_noise` - 噪声生成器（默认，随机凹凸地面）
> - `netease:generator_flat` - 超平坦（仅主世界/下界类型可用）
> - `netease:generator_legacy` - 旧版有限地图（仅主世界类型）
>
> 另有 [2-群系地貌.md:213-400](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L213-L400) 提供的「自定义高度」`netease:overworld_surface` 组件（fill/move/replace 三类节点），可在群系 json 里精细控制每个高度区间的方块。
>
> **实现位置**：dmXXX.json 设 `"netease:generator_noise": {}`；群系 json 用 `netease:overworld_surface` 精细配置星球地貌（详见 4.2/4.3/4.4 各维度章节）。
>
> **是否需脚本**：否。纯 JSON。

### 4.1.7 维度访问权限

| 模式 | 是否可进入 | 环境伤害 |
|---|---|---|
| 生存 | 可 | 受真空/有毒大气环境伤害惩罚 |
| 创造 | 可 | 不受环境伤害 |

不做指令锁。

> **实现位置**：环境伤害由脚本判断（见 4.1.4 同款脚本实现）。脚本里用 `GetGameMode(playerId)` 判断玩家游戏模式，创造模式直接 return 不扣血。
>
> **是否需脚本**：是（仅"环境伤害对生存惩罚"这一项需脚本；"可进入"本身引擎默认允许，无需配置）。

---

## 4.2 近地太空维度（dm22.json）

### 4.2.1 维度基础信息

| PRD 字段 | PRD 值 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 维度名称 | 近地太空 | `texts/zh_CN.lang`：`dimension.dm22=近地太空` | TODO 查 lang 文件维度名格式（疑似 `dimension.<id>` 或 `dimension.dm22`，未在文档找到对证） | 否 |
| 维度 ID | 22 | 文件名 `dm22.json` | [1-自定义维度.md:21](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L21) | 否 |
| 显示名称 | 近地太空 | 同维度名称（同 lang 文件） | 同上 | 否 |
| 环境：永久黑夜 | 无昼夜循环 | **脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段 | **是** |
| 天气：固定晴朗 | 禁止雨/雪/雷暴 | **脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段 | **是** |
| 光照：星空天空盒 | 自定义天空盒子 | **客户端脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段 | **是** |
| 重力系数 | 0.5 | **脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段，TODO 查 mcdocs 是否有 `SetDimensionGravity` 类接口 | **是** |
| 地面高度 | Y=0~256 | 无需配置 | [2-群系地貌.md:223](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L223) "现阶段自定义维度高度区间为[0, 256]" | 否 |
| 水：禁止水方块生成 | 太空无液态水 | **群系 json** 配 `minecraft:surface_parameters.sea_material` 改为非水方块（如 `minecraft:air`） | [2-群系地貌.md:943-950](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L943-L950) dm5 示例 | 否 |
| 岩浆：允许岩浆方块 | — | **群系 json** 配 `minecraft:surface_parameters.sea_material: "minecraft:lava"` | 同上 | 否 |

### 4.2.2 环境伤害逻辑（和宇航服联动）

PRD 原文明确写"此部分是游戏逻辑，不在 dm22.json 中配置，需要脚本实现"。

| 条件 | 行为 |
|---|---|
| 生存模式 + 未穿戴完整宇航服 | 每秒缓慢扣生命值 |
| 生存模式 + 穿戴全套宇航服 | 免疫环境伤害 |
| 创造模式 | 完全不受环境伤害 |

> **实现位置**：服务端脚本。
> - 监听维度进入事件（TODO 查 `AddServerPlayerEvent` / 维度切换事件名），启动定时器。
> - 定时器每秒：判断玩家当前 dimensionId == 22，且 GameMode == Survival，且未穿戴全套宇航服 → `SetHealth(playerId, curHealth - N)`。
> - **所有判定必须在服务端做**，防止客户端作弊。
>
> **是否需脚本**：是。

### 4.2.3 生成规则

| 项 | 内容 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 原版生物 | 全部关闭 | 见 4.1.5 | 4.1.5 已述 | 否 |
| 矿石/碎石方块生成 | 太空冰晶矿石、轨道碎石 | `netease_features/` + `netease_feature_rules/` | TODO 查 4-自定义特征.md | 否 |
| 结构生成 | 小型空间站残骸、卫星残骸 | `netease_features/` + 结构文件 `structures/` | 同上 | 否 |
| 树木/原版植物 | 不生成 | dm22.json 配 `"netease:ban_vanilla_feature": {}` | [1-自定义维度.md:52](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L52) "清除原版feature，可解决类似空岛玩法天空悬浮结构问题" | 否 |

### 4.2.4 传送进入规则

| 触发 | 行为 |
|---|---|
| 主世界 Y >= 1200 | 自动触发传送进入近地太空维度（升空逻辑） |
| 在近地太空使用道具 | 可去往月球 |

> **实现位置**：服务端脚本。
> - 监听玩家位置更新事件（TODO 查 `OnCarriedNewPlayerHitPlaceServerEvent` 类或 player tick 事件），判断 dimensionId == 0 且 posY >= 1200 → 调用 `ChangePlayerDimension` 类接口（接口名 TODO 查 mcdocs）传送到 dm22 的安全出生坐标。
> - 道具传送月球：玩家使用道具触发 `ServerItemUseOnEvent`（TODO 查事件名）→ 校验当前 dimensionId == 22 → 传送到 dm23。
>
> **是否需脚本**：是。

---

## 4.3 月球维度（dm23.json）

### 4.3.1 维度基础信息

| PRD 字段 | PRD 值 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 维度名称 | 月球 | `texts/zh_CN.lang` | 同 4.2.1 | 否 |
| 维度 ID | 23 | 文件名 `dm23.json` | [1-自定义维度.md:21](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L21) | 否 |
| 显示名称 | 月球 | 同维度名称 | 同上 | 否 |
| 环境：无昼夜循环 | 恒定星空 | **脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段 | **是** |
| 天气：无任何天气 | — | **脚本** | ⚠️ components 表无对应字段 | **是** |
| 天空盒子：深空星空，可见地球 | — | **客户端脚本** | ⚠️ components 表无对应字段 | **是** |
| 重力系数 | 0.2 | **脚本** | ⚠️ components 表无对应字段 | **是** |
| 高度范围 | Y=0~256 | 无需配置 | [2-群系地貌.md:223](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L223) | 否 |
| 水：禁止液态水 | — | **群系 json** | [2-群系地貌.md:943-950](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L943-L950) | 否 |
| 岩浆：允许 | — | **群系 json** | 同上 | 否 |

### 4.3.2 环境伤害逻辑（脚本实现）

| 条件 | 行为 |
|---|---|
| 生存 + 未穿全套宇航服 | 快速持续扣血（比近地太空快） |
| 生存 + 全套宇航服 | 免疫真空伤害 |
| 创造 | 不受伤害 |

> **实现位置**：服务端脚本，同 4.2.2 套路，区别在于扣血速率更快。
> **是否需脚本**：是。

### 4.3.3 生成规则

| 项 | 内容 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 原版生物 | 关闭 | 见 4.1.5 | 4.1.5 | 否 |
| 矿石方块 | 月岩、月光结晶、月球矿石 | `netease_features/` + `netease_feature_rules/` | TODO 查 4-自定义特征.md | 否 |
| 结构 | 陨石坑、废弃登月舱、远古月球遗迹 | `netease_features/` + `structures/` | 同上 | 否 |
| 原版植物/动物 | 无 | dm23.json 配 `"netease:ban_vanilla_feature": {}` | [1-自定义维度.md:52](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6.md#L52) | 否 |

### 4.3.4 传送规则

| 触发 | 行为 |
|---|---|
| 在【近地太空】维度使用导航信标道具 | 传送到月球 |
| 直接从主世界跨级传送月球 | **禁止**（脚本拒绝） |

> **实现位置**：服务端脚本。
> - 监听 `ServerItemUseOnEvent`（道具使用事件，TODO 查事件名）
> - 校验：玩家当前 dimensionId == 22 → 允许传送到 dm23
> - 校验：玩家当前 dimensionId != 22 → 拒绝并提示"必须先到近地太空"
>
> **是否需脚本**：是。

---

## 4.4 火星维度（dm24.json）

### 4.4.1 维度基础信息

| PRD 字段 | PRD 值 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 维度名称 | 火星 | `texts/zh_CN.lang` | 同 4.2.1 | 否 |
| 维度 ID | 24 | 文件名 `dm24.json` | [1-自定义维度.md:21](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%9A%E7%BB%B4%E5%BA%A6.md#L21) | 否 |
| 显示名称 | 火星 | 同维度名称 | 同上 | 否 |
| 环境：开启昼夜循环 | 昼夜速度是主世界 2 倍 | **脚本**（维度 json 无此字段） | ⚠️ components 表无对应字段 | **是** |
| 天空：橘红色沙尘天空盒子 | — | **客户端脚本** | ⚠️ components 表无对应字段 | **是** |
| 天气：可随机触发沙尘暴 | PRD 原文"json只能开启天气系统" | ⚠️ **PRD 描述与文档不符**：维度 components 表无天气字段。需查群系 json 是否有天气字段（TODO），若群系层也无，则只能纯脚本实现 | ⚠️ TODO | **是**（脚本部分） |
| 重力系数 | 0.6 | **脚本** | ⚠️ components 表无对应字段 | **是** |
| 高度范围 | Y=0~256 | 无需配置 | [2-群系地貌.md:223](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L223) | 否 |
| 水：禁止液态水 | — | **群系 json** | [2-群系地貌.md:943-950](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/2-%E7%BE%A4%E7%B3%BB%E5%9C%B0%E8%B2%8C.md#L943-L950) | 否 |
| 岩浆：允许 | — | **群系 json** | 同上 | 否 |

### 4.4.2 环境伤害逻辑（脚本实现）

| 条件 | 行为 |
|---|---|
| 生存 + 未穿全套宇航服 | 同时扣生命值 + 饥饿值 |
| 生存 + 全套宇航服 | 免疫有毒大气伤害 |
| 创造 | 不受伤害 |

> **实现位置**：服务端脚本。扣生命值用 `SetHealth`，扣饥饿值用 `SetHunger` 类接口（TODO 查 mcdocs 确认接口名）。
> **是否需脚本**：是。

### 4.4.3 生成规则

| 项 | 内容 | 实现位置 | 文档依据 | 是否需脚本 |
|---|---|---|---|---|
| 原版生物 | 关闭 | 见 4.1.5 | 4.1.5 | 否 |
| 矿石方块 | 火星赤铁矿、火星能源结晶 | `netease_features/` + `netease_feature_rules/` | TODO 查 4-自定义特征.md | 否 |
| 结构 | 废弃殖民基地、火星洞穴、火山遗迹 | `netease_features/` + `structures/` | 同上 | 否 |
| 原版植物 | 无法自然生成 | dm24.json 配 `"netease:ban_vanilla_feature": {}` | [1-自定义维度.md:52](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%9A%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%9A%E7%BB%B4%E5%BA%A6.md#L52) | 否 |
| 火星专属自定义植被 | 生成 | `netease_features/` + 自定义植被 feature | TODO 查 4-自定义特征.md | 否 |

### 4.4.4 传送规则

| 触发 | 行为 |
|---|---|
| 在【月球】维度使用星际跃迁装置 | 传送到火星 |
| 主世界直接传送火星 | **禁止**（脚本拒绝） |

> **实现位置**：服务端脚本。同 4.3.4 套路，校验当前 dimensionId == 23 才允许传送 dm24。
> **是否需脚本**：是。

---

## 4.5 开发自测点（PRD 备注）

1. **dmXXX.json 只负责维度基础配置**：ID、天空、重力、天气、世界生成、重生。
   > ⚠️ **文档对证结果**：dmXXX.json 的 components 表实际只能配 `dimension_type` / 3 个 generator / `ban_vanilla_feature` / `spawn_biomes` / `biome_source` / 一堆 `ban_vanilla_*` 结构屏蔽。**天空、重力、天气、重生规则文档中均无对应字段**，这些 PRD 项必须脚本实现。
2. **真空伤害、宇航服判定、沙尘暴、传送逻辑**全部需要脚本（PRD 原文写 lua，但 ModSDK 中国版是 **Python 2**，[0-脚本开发入门.md:38](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.md#L38) "我们的python脚本开发使用的python版本是python 2，而不是python 3"）。**已纠正 PRD 原文 lua → Python**。
3. **所有环境伤害、宇航服防护必须在服务端脚本做判断**，不能客户端判断，防止作弊。
   > **文档对证**：[0-脚本开发入门.md:264-268](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/0-%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8.md#L264-L268) "服务端与客户端的脚本需要互相独立，两部分的代码不要互相import"。环境伤害放 `mtrServerSystem.py`（应为 `mchuojianServerSystem.py`，命名按本项目）。
4. **维度切换状态重置**：离开星际维度后，清空太空环境伤害状态。
   > **实现位置**：服务端脚本。监听玩家维度切换事件，新维度不是 22/23/24 时，关闭环境伤害定时器、移除 debuff。

## 4.6 调试 UI 按钮（PRD 新增项）

开发初期，增加一个 UI 按钮，可以互相传送方便调试。

| 项 | 内容 |
|---|---|
| UI 类型 | 客户端自定义 UI（`ui/` 目录 JSON + Python ScreenNode 类） |
| 显示条件 | 仅开发模式/调试模式显示（TODO 定义开关，建议常驻但仅服务端有权限者可见） |
| 按钮行为 | 4 个按钮：[传送至主世界] [传送至近地太空] [传送至月球] [传送至火星] |
| 实现位置 | RP 端 `ui/debugTeleportUI.json` + BP 端 `MCHuojian_Scripts/ui/debugTeleportUI.py` |
| 通信 | 客户端按钮点击 → `NotifyToServer("DebugTeleportEvent", {targetDim: 22})` → 服务端校验权限后传送 |
| 文档依据 | TODO 查 mcguide/18-界面与交互/ 下 UI 创建文档；TODO 查 mcdocs/1-ModAPI/接口/自定义UI/ |

> **是否需脚本**：是（客户端 UI 逻辑 + 服务端传送逻辑）。

---

## 附录 A：维度 json 真实字段速查（来自 [1-自定义维度.md:46-65](file:///workspace/官方代码文档/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6/1-%E8%87%AA%E5%AE%9A%E4%B9%9A%E7%BB%B4%E5%BA%A6.md#L46-L65)）

```json
{
  "format_version": "1.14.0",
  "netease:dimension_info": {
    "components": {
      "netease:dimension_type": "minecraft:overworld",  // 必填，可选 minecraft:overworld / minecraft:nether / minecraft:the_end
      "netease:generator_noise": {},                    // 噪声生成器（默认）
      "netease:generator_flat": {},                      // 超平坦（仅主世界/下界）
      "netease:generator_legacy": {},                    // 旧版有限地图（仅主世界）
      "netease:ban_vanilla_feature": {},                 // 清除原版 feature（树木/植物/小型结构）
      "netease:spawn_biomes": ["dm22_xxx"],              // 玩家出生群系列表
      "netease:biome_source": [...],                      // 群系源（自定义布局，详见 2-群系地貌.md:537）
      "netease:ban_vanilla_mineshaft": {},               // 屏蔽废弃矿井
      "netease:ban_vanilla_monument": {},                // 屏蔽海底遗迹
      "netease:ban_vanilla_mansion": {},                 // 屏蔽林地府邸
      "netease:ban_vanilla_temple": {},                  // 屏蔽神庙
      "netease:ban_vanilla_pillageroutpost": {},         // 屏蔽掠夺者前哨
      "netease:ban_vanilla_ruinedportal": {},            // 屏蔽破坏的传送门
      "netease:ban_vanilla_ruins": {},                   // 屏蔽水下遗迹
      "netease:ban_vanilla_shipwreck": {},               // 屏蔽沉船
      "netease:ban_vanilla_stronghold": {},              // 屏蔽要塞
      "netease:ban_vanilla_village": {}                  // 屏蔽村庄
    }
  }
}
```

**文档对证结论**：PRD 里的"天空盒子 / 重力系数 / 天气 / 昼夜循环 / 重生规则"5 类字段，**官方维度 components 表全部没有**，必须脚本实现。

## 附录 B：PRD 项 vs 文档可配置项 总表

| PRD 需求 | 维度 dmXXX.json 可配？ | 群系 json 可配？ | 脚本必须？ |
|---|---|---|---|
| 维度 ID 22/23/24 | ✅ 文件名 | — | 否 |
| 维度名/显示名 | — | — | 否（lang 文件，TODO 验证格式） |
| 维度类型（主世界/下界/末地） | ✅ `dimension_type` | — | 否 |
| 世界生成器 | ✅ `generator_noise` 等 | — | 否 |
| 屏蔽原版结构（矿井/遗迹等） | ✅ `ban_vanilla_*` | — | 否 |
| 屏蔽原版 feature（树/植物） | ✅ `ban_vanilla_feature` | — | 否 |
| 群系布局 | ✅ `biome_source` | — | 否 |
| 出生群系 | ✅ `spawn_biomes` | — | 否 |
| 禁止水生成 | ⚠️ 间接 | ✅ `sea_material` | 否 |
| 允许岩浆 | ⚠️ 间接 | ✅ `sea_material: lava` | 否 |
| 自定义高度 | — | ✅ `netease:overworld_surface` | 否 |
| 关闭原版生物 | — | ✅（群系加 tag） | 否（spawn_rules 也需配） |
| 自定义生物生成 | — | ✅（spawn_rules + biome tag） | 否 |
| 永久黑夜 / 无昼夜循环 | ❌ | ❌ | **是** |
| 固定晴朗 / 禁雨雪 | ❌ | ❌ | **是** |
| 自定义天空盒子 | ❌ | ❌ | **是（客户端）** |
| 重力系数 | ❌ | ❌ | **是** |
| 重生规则 | ❌ | ❌ | **是** |
| 环境伤害（真空/有毒大气） | ❌ | ❌ | **是（服务端）** |
| 沙尘暴天气 | ❌ | ⚠️ TODO 验证 | **是** |
| 昼夜速度 2 倍 | ❌ | ❌ | **是** |
| 维度传送规则 | ❌ | ❌ | **是（服务端）** |
| 调试 UI 按钮 | ❌ | ❌ | **是（客户端+服务端）** |

---

## 附录 C：待查文档清单（TODO）

以下 PRD 项因维度/群系 json 无对应字段，必须在 mcdocs 里查接口实现，下次集中查证：

| 待查接口/事件 | 用途 | 查证位置 |
|---|---|---|
| 维度切换/玩家进入维度事件 | 检测玩家进入星际维度触发环境伤害 | `mcdocs/1-ModAPI/事件/玩家.md` |
| `SetTime` / 时间控制接口 | 永久黑夜/昼夜 2 倍速 | `mcdocs/1-ModAPI/接口/世界/时间.md` |
| 天气控制接口 | 固定晴朗 / 沙尘暴触发 | `mcdocs/1-ModAPI/接口/世界/天气.md` |
| `SetDimensionGravity` 或类似 | 重力系数 0.2/0.5/0.6 | `mcdocs/1-ModAPI/接口/` 全文搜 gravity |
| 玩家死亡事件 + 重生点设置 | 4.1.4 重生规则 | `mcdocs/1-ModAPI/事件/玩家.md` + `接口/玩家/` |
| `SetHealth` / `SetHunger` | 环境伤害扣血扣饥饿 | `mcdocs/1-ModAPI/接口/玩家/属性.md` |
| 维度切换传送接口 | 4.2.4/4.3.4/4.4.4 传送规则 | `mcdocs/1-ModAPI/接口/玩家/` 或 `世界/` |
| 宇航服穿戴判定接口 | 4.2.2 环境伤害免疫 | `mcdocs/1-ModAPI/接口/玩家/背包.md` |
| `GetGameMode` | 创造模式免伤 | `mcdocs/1-ModAPI/接口/玩家/游戏模式.md` |
| 玩家位置/tick 事件 | Y>=1200 自动升空 | `mcdocs/1-ModAPI/事件/玩家.md` |
| UI ScreenNode 创建接口 | 4.6 调试按钮 | `mcguide/18-界面与交互/` + `mcdocs/1-ModAPI/接口/自定义UI/` |
| 自定义特征/结构生成配置 | 4.2.3/4.3.3/4.4.3 矿石/结构 | `mcguide/20-玩法开发/15-自定义游戏内容/4-自定义维度/4-自定义特征.md` |
| 维度名 lang 文件格式 | 维度名/显示名 | `mcguide/20-玩法开发/15-自定义游戏内容/` 多语言相关章节 |
