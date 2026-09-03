# -*- coding: utf-8 -*-
"""
debugTeleportUINode.py —— 调试传送 UI 节点类（客户端）
==========================================================
继承 ScreenNode，负责：
1. UI 创建时给 4 个维度按钮 + 关闭按钮各自绑定点击回调；
2. 按钮被点击 → 调用 clientApi.NotifyToServer 把目标维度发给服务端；
3. 关闭按钮 → 调用 clientApi.PopScreen() 关掉本界面。

PRD 依据：4.6 调试 UI 按钮（互相传送方便调试）

文档依据：
- UI Python 类继承 ScreenNode
  [mcguide/18-界面与交互/30-UI说明文档.md#L1555-L1563]
  ```python
  class TestScreen(ScreenNode):
      def __init__(self, namespace, name, param):
          ScreenNode.__init__(self, namespace, name, param)
  ```
- 按钮回调绑定（@ViewBinder.binding 装饰器方式）
  [mcguide/18-界面与交互/30-UI说明文档.md#L1617-L1637]
  ```python
  @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#scoreboard_grid.item_count")
  def OnStarkGridResize(self): return ...
  ```
- ScreenNode 生命周期 Create
  [mcdocs/1-ModAPI/接口/自定义UI/UI界面.md#L113-L126]
- clientApi.NotifyToServer 签名（服务端用 ListenForEvent 接收）
  [mcdocs/1-ModAPI/接口/通用/事件.md#NotifyToServer]

接口签名（来自文档）：
- clientApi.GetScreenNodeCls() -> type(ScreenNode)  [通用.md#L211]
- clientApi.GetViewBinderCls() -> type(ViewBinder)  [通用.md#L337]
- clientApi.PopScreen() -> bool  [通用.md#L395]
- clientApi.NotifyToServer(eventName, eventData) -> bool  [通用/事件.md#NotifyToServer]

不确定部分（TODO）：
- 按钮点击事件的具体 binding_name 是否需要与 JSON 中 button 的 bindings 数组对齐？
  本实现采用 @ViewBinder.binding 装饰器，binding_name 在 JSON 按钮的 bindings 数组里
  以 "binding_name" : "#<按钮名>.click" 形式声明。如果运行时按钮点击未触发回调，
  改用 $pressed_button_name = "%<类简名>.<方法名>" 方式（[30-UI说明文档.md:490]）。
"""

import mod.client.extraClientApi as clientApi

# 从 modCommon 引入命名空间与事件名（保持与服务端字符串一致）
# Python 2 绝对导入：MCHuojian_Scripts/ 是 sys.path 顶级包目录
from modCommon import (
    MOD_NAMESPACE,
    DEBUG_SERVER_SYSTEM_NAME,
    DEBUG_TELEPORT_EVENT,
    DIM_OVERWORLD,
    DIM_NEAR_SPACE,
    DIM_MOON,
    DIM_MARS,
)

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()


class DebugTeleportScreenNode(ScreenNode):
    """调试传送 UI 节点。每个按钮点击后通知服务端执行 ChangePlayerDimension。"""

    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)

    def Create(self):
        """UI 创建完成时调用（[UI界面.md#Create]）。本 UI 无需在 Create 里做事。"""
        pass

    def Destroy(self):
        """UI 销毁时调用（[UI界面.md#Destroy]）。"""
        pass

    # ------------------------------------------------------------------
    # 4 个维度传送按钮 + 关闭按钮
    # 每个 binding_name 必须与 JSON 中对应按钮的 bindings 数组里的 binding_name 一致
    # ------------------------------------------------------------------
    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#btnOverworld.click")
    def OnTeleportOverworld(self, args=None):
        self._TeleportTo(DIM_OVERWORLD)

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#btnNearSpace.click")
    def OnTeleportNearSpace(self, args=None):
        self._TeleportTo(DIM_NEAR_SPACE)

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#btnMoon.click")
    def OnTeleportMoon(self, args=None):
        self._TeleportTo(DIM_MOON)

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#btnMars.click")
    def OnTeleportMars(self, args=None):
        self._TeleportTo(DIM_MARS)

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#btnClose.click")
    def OnClose(self, args=None):
        # 关闭本界面（使用 PushScreen 创建的界面必须用 PopScreen 关闭）
        # 文档依据：[通用.md#PopScreen] + [通用.md#PushScreen] 备注
        clientApi.PopScreen()

    def _TeleportTo(self, targetDim):
        """把目标维度发给服务端调试系统。"""
        # clientApi.NotifyToServer 签名：NotifyToServer(eventName, eventData)
        # 文档依据：[mcdocs/1-ModAPI/接口/通用/事件.md#NotifyToServer]
        clientApi.NotifyToServer(
            DEBUG_TELEPORT_EVENT,
            {
                "targetDim": targetDim,
            }
        )
        # 发完即关闭 UI，避免遮挡
        clientApi.PopScreen()
