# -*- coding: utf-8 -*-
"""
文档依据：
  - 官方代码文档/mcguide/20-玩法开发/15-自定义游戏内容/4-自定义维度/1-自定义维度.md
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md
  - 官方代码文档/mcdocs/1-ModAPI/事件/实体.md
  - 官方代码文档/mcdocs/1-ModAPI/事件/世界.md

MCHuojian 火箭模组 - modMain 入口
本周PRD：第4章 自定义维度配置（dm22近地太空/dm23月球/dm24火星）
"""

from mod.common.mod import Mod
from mod.common.system import System
from mod_log import logger as logger

# 注册服务端系统
from server_system import RocketServerSystem

# 维度ID常量（文档依据：1-自定义维度.md L13-L15）
DIM_DM22_ORBIT = 22   # 近地太空
DIM_DM23_LUNAR = 23   # 月球
DIM_DM24_MARS = 24    # 火星


@Mod.Binding("RocketMod", "1.0.0")
class RocketMod(object):
    """MCHuojian 火箭模组主入口"""

    def __init__(self):
        pass

    def InitServer(self):
        logger.info("[MCHuojian] 初始化服务端系统...")
        server_system = RocketServerSystem()
        server_system.Init()
        logger.info("[MCHuojian] 服务端系统初始化完成")

    def InitClient(self):
        logger.info("[MCHuojian] 初始化客户端系统...")
        # 客户端系统（周四传送到客户端时补充）
        logger.info("[MCHuojian] 客户端系统初始化完成")

    def DestroyServer(self):
        logger.info("[MCHuojian] 服务端系统销毁")

    def DestroyClient(self):
        logger.info("[MCHuojian] 客户端系统销毁")