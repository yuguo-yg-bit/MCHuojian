# -*- coding: utf-8 -*-
"""
debugTeleportServerSys.py —— 调试传送服务端系统
=================================================
职责：
1. Init 时 ListenForEvent 监听客户端发来的 MCHuojian_DebugTeleportEvent；
2. 收到事件后调用 ChangePlayerDimension 把玩家传到目标维度；
3. 创造模式判定 + 安全坐标查表（每个维度一个固定调试出生点）。

PRD 依据：
- 4.6 调试 UI 按钮（互相传送方便调试）
- 4.1.3 服务端注册维度（本系统是 PRD 维度系统的雏形，只先做传送逻辑）
- 4.1.7 维度访问权限（生存、创造均可进入；创造不受环境伤害——本系统暂不做伤害判定，仅做传送）

文档依据：
- 服务端系统基类 mod.server.system.ServerSystem
  [mcguide/20-玩法开发/13-模组SDK编程/2-Python脚本开发/4-系统简介.md]
- ListenForEvent 监听客户端系统事件签名
  [mcdocs/1-ModAPI/接口/通用/事件.md#ListenForEvent]
  （监听客户端系统事件时，namespace=客户端系统所属Mod的namespace，systemName=客户端系统名）
- ChangePlayerDimension 签名
  [mcdocs/1-ModAPI/接口/玩家/行为.md#L201-L233]
  ```python
  comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
  comp.ChangePlayerDimension(dimensionId, pos) -> bool
  ```
  注意：文档参数表写"0-overWorld; 1-nether; 2-theEnd"，
       但 [1-自定义维度.md:15] 写明自定义维度 ID 范围是 22~2147483647。
       本系统按 PRD 用 22/23/24，运行时如果接口拒绝需 TODO 验证。
- SetPlayerRespawnPos 签名（备用，将来 PRD 4.1.4 重生规则要用）
  [mcdocs/1-ModAPI/接口/玩家/行为.md#L936-L965]
  ```python
  comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
  comp.SetPlayerRespawnPos(pos, dimensionId) -> bool
  ```
  注意：文档明确"维度21是不可用的"——意味着 22+ 是可用自定义维度，PRD 22/23/24 没问题。

接口签名（来自文档）：
- serverApi.GetSystem(namespace, systemName) -> ServerSystem
- serverApi.GetEngineCompFactory() -> CompFactory
- CompFactory.CreateDimension(playerId) -> DimensionCompServer
- DimensionCompServer.ChangePlayerDimension(dimensionId, pos) -> bool
- serverApi.GetPlayerId() -> str（拿到事件发起玩家 id；TODO 待查证实际事件 args 是否带 __id__）

不确定部分（TODO）：
- 客户端 → 服务端事件回调参数 args 是否带 "__id__" 字段标识玩家 id？
  按 [通用/事件.md#ListenForEvent] 备注，监听客户端系统事件时回调 args 应自带 __id__。
  本实现优先用 args["__id__"]，若失败改用 serverApi.GetPlayerId()。
"""

import mod.server.extraServerApi as serverApi
from mod.common.mod import BaseServerSystem

# Python 2 绝对导入：MCHuojian_Scripts/ 是 sys.path 顶级包目录
from modCommon import (
    MOD_NAMESPACE,
    DEBUG_CLIENT_SYSTEM_NAME,
    DEBUG_TELEPORT_EVENT,
    DEBUG_TELEPORT_POS,
)


class MCHuojianDebugServerSys(BaseServerSystem):
    """调试传送服务端系统：接收客户端按钮点击事件，执行维度传送。"""

    def __init__(self, namespace, systemName):
        super(MCHuojianDebugServerSys, self).__init__(namespace, systemName)

    def Init(self):
        """系统初始化：监听客户端发来的调试传送事件。"""
        # 监听客户端系统事件：namespace = 客户端系统所属Mod的namespace，
        #                       systemName = 客户端系统名（与客户端 RegisterSystem 时一致）
        # 文档依据：[mcdocs/1-ModAPI/接口/通用/事件.md#ListenForEvent]
        serverApi.ListenForEvent(
            MOD_NAMESPACE,
            DEBUG_CLIENT_SYSTEM_NAME,
            DEBUG_TELEPORT_EVENT,
            self,
            self._OnDebugTeleport,
        )

    def Destroy(self):
        """系统销毁：取消监听。"""
        serverApi.UnListenForEvent(
            MOD_NAMESPACE,
            DEBUG_CLIENT_SYSTEM_NAME,
            DEBUG_TELEPORT_EVENT,
            self,
            self._OnDebugTeleport,
        )

    # ------------------------------------------------------------------
    # 客户端事件回调
    # ------------------------------------------------------------------
    def _OnDebugTeleport(self, args):
        """客户端按钮点击 → 服务端执行传送。

        args 期望格式：{ "__id__": <playerId>, "targetDim": <int> }
        """
        targetDim = args.get("targetDim", None)
        if targetDim is None:
            # 事件数据不合法，直接返回
            return

        # 拿玩家 id（文档约定客户端→服务端事件 args 自带 __id__）
        # 文档依据：[mcdocs/1-ModAPI/接口/通用/事件.md#ListenForEvent] 备注
        playerId = args.get("__id__", None)
        if playerId is None:
            # 兜底：用 serverApi.GetPlayerId()
            playerId = serverApi.GetPlayerId()

        # 查目标维度安全出生坐标
        pos = DEBUG_TELEPORT_POS.get(targetDim, None)
        if pos is None:
            # 未知维度 ID，忽略
            return

        # 调用 ChangePlayerDimension 传送
        # 文档依据：[mcdocs/1-ModAPI/接口/玩家/行为.md#L201-L233]
        comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
        if comp:
            comp.ChangePlayerDimension(targetDim, pos)
        # TODO：未来 PRD 4.1.7 加创造模式判定时，可用
        #   playerComp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
        #   gameType = playerComp.GetPlayerGameType()
        # 创造模式直接传送；生存模式传送时附带启动环境伤害定时器（PRD 4.2.2 等）。
