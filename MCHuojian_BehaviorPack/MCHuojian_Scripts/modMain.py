# -*- coding: utf-8 -*-
"""
modMain.py —— Python 逻辑入口（必须存在）
==========================================

用法：
  1. @Mod.Binding 绑定一个 Mod 名称 + 版本（纯元信息，不影响 manifest.json 里的 version）
  2. @InitServer / @InitClient   → 注册 ServerSystem / ClientSystem、组件、命令、事件监听等
  3. @DestroyServer / @DestroyClient → 退出时清理、保存持久化数据等

命名空间（namespace）建议：团队名 + 下划线 + Mod名，例 huojian_team_mchuojian
  - 所有自定义方块/物品/实体/方块实体 JSON 中 identifier 的前缀
  - modMain.py 里 RegisterSystem 的第一个参数

参考：
  官方代码文档/mcguide/20-玩法开发/13-模组SDK编程/2-Python脚本开发/0-脚本开发入门.md
    第219~263行（modMain 结构与 4 个生命周期装饰器）
  官方代码文档/mcguide/20-玩法开发/13-模组SDK编程/20-制作规范.md 第29~56行（命名空间规范）
"""

from mod.common.mod import Mod


# PRD 到达后替换 name / version / 命名空间
MOD_NAME_SPACE = "huojian_team_mchuojian"
MOD_DISPLAY_NAME = "MCHuojianMod"


@Mod.Binding(name=MOD_DISPLAY_NAME, version="0.0.1")
class MCHuojianMod(object):

    def __init__(self):
        pass

    # --------------------------------------------------------
    # 服务端初始化 —— 注册服务端系统/组件/命令/事件
    # --------------------------------------------------------
    @Mod.InitServer()
    def _InitServer(self):
        # TODO(PRD): 在此注册 ServerSystem
        #   serverApi = __import__("mod.server.extraServerApi")
        #   serverApi.RegisterSystem(
        #       MOD_NAME_SPACE,
        #       "MCHuojianServerSystem",
        #       "MCHuojian_Scripts.modSystem.mchuojianServerSystem.MCHuojianServerSystem"
        #   )
        pass

    # --------------------------------------------------------
    # 服务端销毁 —— 保存持久化数据 / 清理定时器 / 卸载组件
    # --------------------------------------------------------
    @Mod.DestroyServer()
    def _DestroyServer(self):
        pass

    # --------------------------------------------------------
    # 客户端初始化 —— 注册客户端系统/UI/渲染/特效
    # --------------------------------------------------------
    @Mod.InitClient()
    def _InitClient(self):
        # TODO(PRD): 在此注册 ClientSystem
        #   clientApi = __import__("mod.client.extraClientApi")
        #   clientApi.RegisterSystem(
        #       MOD_NAME_SPACE,
        #       "MCHuojianClientSystem",
        #       "MCHuojian_Scripts.modSystem.mchuojianClientSystem.MCHuojianClientSystem"
        #   )
        pass

    # --------------------------------------------------------
    # 客户端销毁 —— 关闭 UI / 解绑观察者
    # --------------------------------------------------------
    @Mod.DestroyClient()
    def _DestroyClient(self):
        pass
