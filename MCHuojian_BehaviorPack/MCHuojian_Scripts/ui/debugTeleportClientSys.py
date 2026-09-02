# -*- coding: utf-8 -*-
"""
debugTeleportClientSys.py —— 调试传送客户端系统
=================================================
职责：
1. 在 Init 时监听 UiInitFinished 引擎事件（界面初始化完成事件）；
2. 在 UiInitFinished 回调里 RegisterUI + 不主动创建（避免开机弹窗）；
3. 提供一个 OpenTeleportUI() 方法供其他系统/按键调用打开调试面板。
   （PRD 4.6 注：调试初期可通过指令/按键触发，本文件只提供方法。）

PRD 依据：4.6 调试 UI 按钮（互相传送方便调试）

文档依据：
- 客户端系统基类 mod.client.system.ClientSystem
  [mcguide/20-玩法开发/13-模组SDK编程/2-Python脚本开发/4-系统简介.md]
- ListenForEvent 引擎事件监听签名
  [mcdocs/1-ModAPI/接口/通用/事件.md#ListenForEvent]
  （引擎命名空间/系统名通过 GetEngineNamespace() / GetEngineSystemName() 获取）
- RegisterUI 签名
  [mcdocs/1-ModAPI/接口/自定义UI/通用.md#L503-L543]
  RegisterUI(nameSpace, uiKey, clsPath, uiScreenDef) -> bool
- PushScreen 签名
  [mcdocs/1-ModAPI/接口/自定义UI/通用.md#L460-L499]
  PushScreen(namespace, uiname, createParams=None) -> ScreenNode
- UiInitFinished 事件
  [mcdocs/1-ModAPI/事件/UI.md#UiInitFinished]（30-UI说明文档.md#L1701 提及）

接口签名（来自文档）：
- clientApi.GetSystem(namespace, systemName) -> ServerSystem/ClientSystem
- clientApi.GetEngineNamespace() -> str
- clientApi.GetEngineSystemName() -> str
- clientApi.RegisterUI(nameSpace, uiKey, clsPath, uiScreenDef) -> bool
- clientApi.PushScreen(namespace, uiname, createParams=None) -> ScreenNode

不确定部分（TODO）：
- UiInitFinished 事件名是否拼写正确：本文档 30-UI说明文档.md#L1701 写法为
  "UiInitFinished"，但 mcdocs/1-ModAPI/事件/UI.md 的实际事件 ID 应再确认一遍。
"""

import mod.client.extraClientApi as clientApi
from mod.common.mod import BaseClientSystem

# Python 2 绝对导入：MCHuojian_Scripts/ 是 sys.path 顶级包目录
from modCommon import (
    MOD_NAMESPACE,
    DEBUG_CLIENT_SYSTEM_NAME,
    DEBUG_TELEPORT_UI_NAME,
    DEBUG_TELEPORT_UI_PY_CLS_PATH,
    DEBUG_TELEPORT_UI_SCREEN_DEF,
)


class MCHuojianDebugClientSys(BaseClientSystem):
    """调试传送客户端系统：负责 UI 注册 + 提供打开方法。"""

    def __init__(self, namespace, systemName):
        super(MCHuojianDebugClientSys, self).__init__(namespace, systemName)
        self._uiRegistered = False

    def Init(self):
        """系统初始化：监听 UiInitFinished 引擎事件。"""
        # 监听引擎事件用 ListenForEvent(engineNamespace, engineSystemName, eventName, instance, callback)
        # 文档依据：[mcdocs/1-ModAPI/接口/通用/事件.md#ListenForEvent]
        clientApi.ListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "UiInitFinished",
            self,
            self._OnUiInitFinished,
        )

    def Destroy(self):
        """系统销毁：取消监听。"""
        clientApi.UnListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "UiInitFinished",
            self,
            self._OnUiInitFinished,
        )

    # ------------------------------------------------------------------
    # 引擎事件回调
    # ------------------------------------------------------------------
    def _OnUiInitFinished(self, args):
        """引擎 UI 初始化完成事件回调（[30-UI说明文档.md#L1701]）。

        在此之后才能 RegisterUI / PushScreen。
        """
        if not self._uiRegistered:
            # RegisterUI 只需注册一次
            # 文档依据：[mcdocs/1-ModAPI/接口/自定义UI/通用.md#L503-L543]
            clientApi.RegisterUI(
                MOD_NAMESPACE,
                DEBUG_TELEPORT_UI_NAME,
                DEBUG_TELEPORT_UI_PY_CLS_PATH,
                DEBUG_TELEPORT_UI_SCREEN_DEF,
            )
            self._uiRegistered = True

    # ------------------------------------------------------------------
    # 对外暴露的方法（其他系统/按键绑定/聊天指令调用）
    # ------------------------------------------------------------------
    def OpenTeleportUI(self):
        """打开调试传送面板（PushScreen 方式）。

        文档依据：[通用.md#PushScreen]
        """
        if not self._uiRegistered:
            # 兜底：万一 UiInitFinished 未触发或错过了，这里再注册一次
            clientApi.RegisterUI(
                MOD_NAMESPACE,
                DEBUG_TELEPORT_UI_NAME,
                DEBUG_TELEPORT_UI_PY_CLS_PATH,
                DEBUG_TELEPORT_UI_SCREEN_DEF,
            )
            self._uiRegistered = True

        # PushScreen 使用堆栈方式创建 UI，关闭时用 PopScreen
        # 文档依据：[通用.md#PushScreen]
        clientApi.PushScreen(MOD_NAMESPACE, DEBUG_TELEPORT_UI_NAME, {})
