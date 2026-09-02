# -*- coding: utf-8 -*-
"""
debugTeleportClientSys.py —— 调试传送客户端系统
=================================================
职责：
1. Init 时监听 UiInitFinished 引擎事件；
2. 在 UiInitFinished 回调里 RegisterUI + 直接 PushScreen（开机自显）；
3. UI 显示在屏幕右上角。

PRD 依据：4.6 调试 UI 按钮（玩家一进去就直接显示在右上角）

文档依据：
- ClientSystem 基类与实例方法 ListenForEngineEvent
  [mcguide/18-界面与交互/2-从零开始创建UI.md#L250-L254]
  ```python
  def InitClient(self):
      import mod.client.extraClientApi as clientApi
      self.ListenForEngineEvent(UiInitFinishedEvent, self, self.OnUIInitFinished)
  ```
- RegisterUI 签名
  [mcdocs/1-ModAPI/接口/自定义UI/通用.md#L503-L543]
- PushScreen 签名（开机自显用）
  [mcdocs/1-ModAPI/接口/自定义UI/通用.md#L460-L499]

接口签名（来自文档）：
- self.ListenForEngineEvent(eventName, instance, callback) -> None  [ClientSystem 实例方法]
- clientApi.RegisterUI(nameSpace, uiKey, clsPath, uiScreenDef) -> bool
- clientApi.PushScreen(namespace, uiname, createParams=None) -> ScreenNode

不确定部分（TODO）：
- UiInitFinishedEvent 常量的导入路径文档没写，本实现用字符串 "UiInitFinished"。
  若运行时引擎报"未识别事件名"，改回 ListenForEvent(GetEngineNamespace(),
  GetEngineSystemName(), "UiInitFinished", ...) 三参数写法。
"""

import mod.client.extraClientApi as clientApi
from mod.common.mod import BaseClientSystem

from modCommon import (
    MOD_NAMESPACE,
    DEBUG_TELEPORT_UI_NAME,
    DEBUG_TELEPORT_UI_PY_CLS_PATH,
    DEBUG_TELEPORT_UI_SCREEN_DEF,
)


class MCHuojianDebugClientSys(BaseClientSystem):
    """调试传送客户端系统：开机自显 UI。"""

    def __init__(self, namespace, systemName):
        super(MCHuojianDebugClientSys, self).__init__(namespace, systemName)
        self._uiRegistered = False

    def Init(self):
        # 文档依据：[2-从零开始创建UI.md#L250-L254]
        self.ListenForEngineEvent(
            "UiInitFinished",
            self,
            self._OnUiInitFinished,
        )

    def Destroy(self):
        self.UnListenForEngineEvent(
            "UiInitFinished",
            self,
            self._OnUiInitFinished,
        )

    # ------------------------------------------------------------------
    # 引擎事件回调
    # ------------------------------------------------------------------
    def _OnUiInitFinished(self, args):
        """UI 初始化完成事件回调：注册 + 直接弹出 UI（开机自显）。"""
        # RegisterUI 只需注册一次
        # 文档依据：[通用.md#RegisterUI]
        if not self._uiRegistered:
            clientApi.RegisterUI(
                MOD_NAMESPACE,
                DEBUG_TELEPORT_UI_NAME,
                DEBUG_TELEPORT_UI_PY_CLS_PATH,
                DEBUG_TELEPORT_UI_SCREEN_DEF,
            )
            self._uiRegistered = True

        # PushScreen 开机自显（PRD 4.6：玩家一进去就显示在右上角）
        # 文档依据：[通用.md#PushScreen]
        clientApi.PushScreen(MOD_NAMESPACE, DEBUG_TELEPORT_UI_NAME, {})

    # ------------------------------------------------------------------
    # 对外方法（备用，按键触发可调用）
    # ------------------------------------------------------------------
    def OpenTeleportUI(self):
        """手动打开调试传送面板。"""
        if not self._uiRegistered:
            clientApi.RegisterUI(
                MOD_NAMESPACE,
                DEBUG_TELEPORT_UI_NAME,
                DEBUG_TELEPORT_UI_PY_CLS_PATH,
                DEBUG_TELEPORT_UI_SCREEN_DEF,
            )
            self._uiRegistered = True
        clientApi.PushScreen(MOD_NAMESPACE, DEBUG_TELEPORT_UI_NAME, {})
