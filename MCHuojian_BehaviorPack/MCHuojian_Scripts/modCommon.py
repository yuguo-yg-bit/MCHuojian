# -*- coding: utf-8 -*-
"""
modCommon.py —— 跨端公共常量
======================================
本文件存放服务端/客户端共用的常量（命名空间、System名、UI名、事件名）。
服务端和客户端任何一端需要引用对方注册的 System/Event 时，
都要保证两端用的字符串完全一致，因此集中放在这里。

PRD 依据：4.6 调试 UI 按钮（互相传送方便调试）

文档依据：
- 命名空间规范 [mcguide/20-玩法开发/13-模组SDK编程/20-制作规范.md]
  建议 [团队名]_[Mod名]
- RegisterSystem 签名 [mcdocs/1-ModAPI/接口/通用/System.md#registersystem]
- ListenForEvent / NotifyToServer 签名 [mcdocs/1-ModAPI/接口/通用/事件.md]
"""

# ------------------------------------------------------------------
# Mod 命名空间（与 modMain.py 中的 @Mod.Binding name 保持一致）
# ------------------------------------------------------------------
MOD_NAMESPACE = "huojian_team_mchuojian"

# ------------------------------------------------------------------
# 调试传送系统（4.6 调试 UI 按钮）
# ------------------------------------------------------------------
DEBUG_CLIENT_SYSTEM_NAME = "MCHuojianDebugClientSys"
DEBUG_SERVER_SYSTEM_NAME = "MCHuojianDebugServerSys"

# 客户端系统类路径（modMain.RegisterSystem 用）
DEBUG_CLIENT_SYSTEM_CLS_PATH = "MCHuojian_Scripts.ui.debugTeleportClientSys.MCHuojianDebugClientSys"
# 服务端系统类路径
DEBUG_SERVER_SYSTEM_CLS_PATH = "MCHuojian_Scripts.ui.debugTeleportServerSys.MCHuojianDebugServerSys"

# 调试 UI 名（与 RP 端 ui/debugTeleportUI.json 文件名一致，30-UI说明文档.md 第11行硬规定）
DEBUG_TELEPORT_UI_NAME = "debugTeleportUI"
# UI Python 类路径（clientApi.RegisterUI 用）
DEBUG_TELEPORT_UI_PY_CLS_PATH = "MCHuojian_Scripts.ui.debugTeleportUINode.DebugTeleportScreenNode"
# UI 画布路径（"namespace.screenName"，namespace = JSON 文件 namespace 字段；screenName = main）
DEBUG_TELEPORT_UI_SCREEN_DEF = "debugTeleportUI.main"

# 客户端 → 服务端 事件名（按钮点击后客户端通知服务端）
DEBUG_TELEPORT_EVENT = "MCHuojian_DebugTeleportEvent"

# 维度 ID（来自 PRD 4.1.1，文档 [1-自定义维度.md:15] 确认 22+ 是可用自定义维度ID）
DIM_OVERWORLD = 0   # 主世界（原版）
DIM_NEAR_SPACE = 22 # 近地太空（自定义）
DIM_MOON = 23       # 月球（自定义）
DIM_MARS = 24       # 火星（自定义）

# 调试传送的目标坐标（每个维度一个安全出生点）
# 文档 [玩家/行为.md:225] 备注："成功切换维度时 pos 为玩家头的位置，即比设定位置低1.62"
# 故 Y 取 100，玩家脚部约在 98
DEBUG_TELEPORT_POS = {
    DIM_OVERWORLD:   (0, 100, 0),
    DIM_NEAR_SPACE:  (0, 100, 0),
    DIM_MOON:        (0, 100, 0),
    DIM_MARS:        (0, 100, 0),
}
