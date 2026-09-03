# 文档依据：
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md  L29-L31 (PlayerHurtEvent)
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md  L739-L761 (PlayerRespawnEvent)
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md  L764-L786 (PlayerRespawnFinishServerEvent)
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md  L201-L225 (DimensionChangeFinishServerEvent)
  - 官方代码文档/mcdocs/1-ModAPI/事件/世界.md  L811-L826 (OnScriptTickServer)
  - 官方代码文档/mcdocs/1-ModAPI/事件/玩家.md  L26-L28 (PlayerDieEvent)
  - 官方代码文档/mcdocs/1-ModAPI/接口/玩家/背包.md  L302-L335 (GetPlayerItem)
  - 官方代码文档/mcdocs/1-ModAPI/接口/实体/属性.md  L109-L140 (GetAttrValue)
  - 官方代码文档/mcdocs/1-ModAPI/接口/实体/属性.md  L797-L834 (SetAttrValue)
  - 官方代码文档/mcdocs/1-ModAPI/接口/实体/属性.md  L238-L263 (GetEntityDimensionId)
  - 官方代码文档/mcdocs/1-ModAPI/接口/玩家/行为.md  L201-L232 (ChangePlayerDimension)
  - 官方代码文档/mcdocs/1-ModAPI/枚举值/ItemPosType.md  L12-L17 (ItemPosType)
  - 官方代码文档/mcdocs/1-ModAPI/枚举值/ArmorSlotType.md  L12-L17 (ArmorSlotType)
  - 官方代码文档/mcdocs/1-ModAPI/枚举值/AttrType.md  L14-L25 (AttrType)

MCHuojian 火箭模组 - 服务端系统
负责：环境伤害（真空扣血/宇航服判定）、重生规则、维度事件
"""

import mod.server.extraServerApi as serverApi
from mod_log import logger as logger

# ============================================================
# 配置常量（文档依据：1-自定义维度.md L13-L15 维度ID范围22~int最大值）
# ============================================================

# 太空维度ID列表
SPACE_DIMENSIONS = [22, 23, 24]  # dm22近地太空, dm23月球, dm24火星

# 真空伤害配置
VACUUM_DAMAGE = 1                # 每次扣血值
VACUUM_DAMAGE_INTERVAL = 40      # 扣血间隔（tick），40 tick = 2秒（1秒=20 tick）

# 宇航服物品标识符（TODO: 等物品注册后填入正式identifier）
# 文档依据：ItemPosType.md - ARMOR=3盔甲栏, ArmorSlotType.md - HEAD=0/BODY=1/LEG=2/FOOT=3
SPACESUIT_HELMET = "mchuojian:spacesuit_helmet"    # 宇航服头盔
SPACESUIT_CHESTPLATE = "mchuojian:spacesuit_chestplate"  # 宇航服胸甲
SPACESUIT_LEGGINGS = "mchuojian:spacesuit_leggings"      # 宇航服护腿
SPACESUIT_BOOTS = "mchuojian:spacesuit_boots"            # 宇航服靴子

# 重生配置
# 太空维度重生点：默认回到主世界出生点
# 文档依据：PlayerRespawnFinishServerEvent.md L764-L786
RESPAWN_DIMENSION = 0            # 默认重生维度（主世界）
RESPAWN_POS = (0, 64, 0)        # 默认重生坐标（TODO: 根据实际出生点调整）


class RocketServerSystem(object):
    """MCHuojian 服务端系统"""

    def __init__(self):
        self.tick_counter = 0
        # 记录在太空维度中的玩家，避免重复扣血
        self.space_players = {}  # {playerId: tick_count}

    def Init(self):
        """初始化系统，注册所有事件监听"""
        logger.info("[MCHuojian] RocketServerSystem.Init() 开始注册事件")

        # 1. 监听服务端tick，用于真空伤害定时器
        # 文档依据：世界.md L811-L826 OnScriptTickServer
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "OnScriptTickServer",
            self,
            self.OnScriptTickServer
        )

        # 2. 监听玩家受伤事件，用于真空伤害保护判定
        # 文档依据：玩家.md L29-L31 PlayerHurtEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "PlayerHurtEvent",
            self,
            self.OnPlayerHurt
        )

        # 3. 监听玩家死亡事件
        # 文档依据：玩家.md L26-L28 PlayerDieEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "PlayerDieEvent",
            self,
            self.OnPlayerDie
        )

        # 4. 监听玩家复活完成事件，用于重生规则
        # 文档依据：玩家.md L764-L786 PlayerRespawnFinishServerEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "PlayerRespawnFinishServerEvent",
            self,
            self.OnPlayerRespawnFinish
        )

        # 5. 监听维度切换完成事件，用于状态重置
        # 文档依据：玩家.md L201-L225 DimensionChangeFinishServerEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "DimensionChangeFinishServerEvent",
            self,
            self.OnDimensionChangeFinish
        )

        # 6. 监听玩家加入事件
        # 文档依据：世界.md L190-L218 AddServerPlayerEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "AddServerPlayerEvent",
            self,
            self.OnAddServerPlayer
        )

        # 7. 监听玩家离开事件
        # 文档依据：世界.md L385-L405 DelServerPlayerEvent
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "DelServerPlayerEvent",
            self,
            self.OnDelServerPlayer
        )

        logger.info("[MCHuojian] RocketServerSystem.Init() 事件注册完成")

    # ============================================================
    # 事件回调
    # ============================================================

    def OnScriptTickServer(self, args):
        """
        服务端tick事件，每秒30次。
        用于真空伤害定时器。
        文档依据：世界.md L811-L826
        """
        self.tick_counter += 1
        if self.tick_counter % VACUUM_DAMAGE_INTERVAL != 0:
            return

        # 遍历所有在太空维度中的玩家，施加真空伤害
        for player_id in list(self.space_players.keys()):
            try:
                self._apply_vacuum_damage(player_id)
            except Exception as e:
                logger.error("[MCHuojian] 真空伤害处理异常 playerId=%s, error=%s", player_id, str(e))

    def OnPlayerHurt(self, args):
        """
        玩家受伤事件。
        如果玩家穿着完整宇航服，免疫真空伤害。
        文档依据：玩家.md L29-L31
        """
        player_id = args.get('id', '')
        if not player_id:
            return

        # 检查玩家是否在太空维度
        dimension_id = self._get_player_dimension(player_id)
        if dimension_id not in SPACE_DIMENSIONS:
            return

        logger.debug("[MCHuojian] 玩家 %s 在太空维度受伤, dimension=%d", player_id, dimension_id)

    def OnPlayerDie(self, args):
        """
        玩家死亡事件。
        记录死亡时所在维度，供重生规则使用。
        文档依据：玩家.md L26-L28
        """
        player_id = args.get('id', '')
        if not player_id:
            return

        dimension_id = self._get_player_dimension(player_id)
        if dimension_id in SPACE_DIMENSIONS:
            logger.info("[MCHuojian] 玩家 %s 在太空维度死亡, dimension=%d", player_id, dimension_id)
            # 清除太空玩家记录
            if player_id in self.space_players:
                del self.space_players[player_id]

    def OnPlayerRespawnFinish(self, args):
        """
        玩家复活完成事件。
        太空维度死亡后重生规则：传送回主世界出生点。
        文档依据：玩家.md L764-L786
        """
        player_id = args.get('playerId', '')
        if not player_id:
            return

        current_dimension = self._get_player_dimension(player_id)
        logger.info("[MCHuojian] 玩家 %s 复活完成, 当前维度=%d", player_id, current_dimension)

        # 如果重生后仍在太空维度，传送回主世界
        # TODO: 后续可扩展为在对应维度内复活（如月球基地复活点）
        if current_dimension in SPACE_DIMENSIONS:
            logger.info("[MCHuojian] 玩家 %s 在太空维度复活，传送回主世界", player_id)
            self._teleport_player(player_id, RESPAWN_DIMENSION, RESPAWN_POS)

    def OnDimensionChangeFinish(self, args):
        """
        维度切换完成事件。
        维度切换时更新太空玩家列表，重置相关状态。
        文档依据：玩家.md L201-L225
        """
        player_id = args.get('playerId', '')
        to_dimension = args.get('toDimensionId', -1)
        from_dimension = args.get('fromDimensionId', -1)

        if not player_id:
            return

        logger.info("[MCHuojian] 玩家 %s 维度切换: %d -> %d", player_id, from_dimension, to_dimension)

        if to_dimension in SPACE_DIMENSIONS:
            # 进入太空维度：加入真空伤害列表
            self.space_players[player_id] = 0
            self._on_enter_space(player_id, to_dimension)
        else:
            # 离开太空维度：从真空伤害列表移除
            if player_id in self.space_players:
                del self.space_players[player_id]
            self._on_leave_space(player_id, from_dimension)

    def OnAddServerPlayer(self, args):
        """
        玩家加入事件。
        文档依据：世界.md L190-L218
        """
        player_id = args.get('id', '')
        if not player_id:
            return
        logger.info("[MCHuojian] 玩家加入: %s", player_id)

        # 检查玩家当前维度，如果在太空维度则加入列表
        dimension_id = self._get_player_dimension(player_id)
        if dimension_id in SPACE_DIMENSIONS:
            self.space_players[player_id] = 0
            logger.info("[MCHuojian] 玩家 %s 当前在太空维度 %d", player_id, dimension_id)

    def OnDelServerPlayer(self, args):
        """
        玩家离开事件。
        文档依据：世界.md L385-L405
        """
        player_id = args.get('id', '')
        if not player_id:
            return
        logger.info("[MCHuojian] 玩家离开: %s", player_id)

        if player_id in self.space_players:
            del self.space_players[player_id]

    # ============================================================
    # 核心逻辑
    # ============================================================

    def _apply_vacuum_damage(self, player_id):
        """
        对玩家施加真空伤害。
        先检查宇航服，如果穿着完整宇航服则免疫伤害。
        文档依据：
          - 背包.md L302-L335 GetPlayerItem
          - 实体/属性.md L797-L834 SetAttrValue
          - 枚举值/ItemPosType.md ARMOR=3
          - 枚举值/ArmorSlotType.md HEAD=0/BODY=1/LEG=2/FOOT=3
        """
        # 1. 检查宇航服
        if self._is_wearing_spacesuit(player_id):
            return  # 穿着完整宇航服，免疫真空伤害

        # 2. 获取当前生命值
        try:
            attr_comp = serverApi.GetEngineCompFactory().CreateAttr(player_id)
            current_health = attr_comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        except Exception as e:
            logger.error("[MCHuojian] 获取玩家 %s 生命值失败: %s", player_id, str(e))
            return

        if current_health <= 0:
            return  # 已死亡，不扣血

        # 3. 施加真空伤害
        new_health = max(0, current_health - VACUUM_DAMAGE)
        try:
            attr_comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, new_health)
            logger.debug("[MCHuojian] 真空伤害: playerId=%s, health=%d->%d", player_id, current_health, new_health)
        except Exception as e:
            logger.error("[MCHuojian] 设置玩家 %s 生命值失败: %s", player_id, str(e))

    def _is_wearing_spacesuit(self, player_id):
        """
        检查玩家是否穿着完整宇航服。
        遍历盔甲栏四个槽位（HEAD/BODY/LEG/FOOT），检查是否均为宇航服部件。
        文档依据：
          - 背包.md L302-L335 GetPlayerItem
          - 枚举值/ItemPosType.md ARMOR=3
          - 枚举值/ArmorSlotType.md HEAD=0/BODY=1/LEG=2/FOOT=3
        """
        try:
            item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
            armor_pos_type = serverApi.GetMinecraftEnum().ItemPosType.ARMOR

            # 检查四个盔甲槽位
            required_slots = {
                0: SPACESUIT_HELMET,      # HEAD
                1: SPACESUIT_CHESTPLATE,  # BODY
                2: SPACESUIT_LEGGINGS,     # LEG
                3: SPACESUIT_BOOTS,        # FOOT
            }

            for slot, expected_item in required_slots.items():
                item_dict = item_comp.GetPlayerItem(armor_pos_type, slot)
                if not item_dict:
                    return False
                item_name = item_dict.get('itemName', '')
                if item_name != expected_item:
                    return False

            return True
        except Exception as e:
            logger.error("[MCHuojian] 检查宇航服失败 playerId=%s, error=%s", player_id, str(e))
            return False

    def _on_enter_space(self, player_id, dimension_id):
        """
        玩家进入太空维度时的处理。
        TODO: 添加进入太空的提示/效果
        """
        logger.info("[MCHuojian] 玩家 %s 进入太空维度 %d", player_id, dimension_id)
        # TODO: 可添加进入太空的音效/提示文字

    def _on_leave_space(self, player_id, dimension_id):
        """
        玩家离开太空维度时的处理。
        """
        logger.info("[MCHuojian] 玩家 %s 离开太空维度 %d", player_id, dimension_id)

    # ============================================================
    # 工具方法
    # ============================================================

    def _get_player_dimension(self, player_id):
        """
        获取玩家当前所在维度ID。
        文档依据：实体/属性.md L109-L140 GetAttrValue
        TODO: 确认获取维度ID的正确API（可能需用GetPlayerDimensionId或其他接口）
        """
        try:
            # 通过实体组件获取维度ID
            # TODO: 使用正确的API获取维度，当前使用entity组件
            comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            dimension_id = comp.GetPlayerDimensionId()
            return dimension_id
        except Exception as e:
            logger.error("[MCHuojian] 获取玩家 %s 维度失败: %s", player_id, str(e))
            return -1

    def _teleport_player(self, player_id, target_dimension, target_pos):
        """
        传送玩家到指定维度和坐标。
        文档依据：TODO - 查找传送API
        """
        try:
            x, y, z = target_pos
            comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            # TODO: 使用正确的传送API
            # comp.ChangePlayerDimension(target_dimension, (x, y, z))
            logger.info("[MCHuojian] 传送玩家 %s 到维度 %d 坐标 (%d, %d, %d)",
                        player_id, target_dimension, x, y, z)
        except Exception as e:
            logger.error("[MCHuojian] 传送玩家 %s 失败: %s", player_id, str(e))

    # ----------------------------------------------------------
    # 以下为 ListenForEvent 的封装方法
    # 文档依据：ModSDK 标准事件注册方式
    # ----------------------------------------------------------
    def ListenForEvent(self, namespace, system_name, event_name, instance, func):
        """注册事件监听"""
        serverApi.ListenForEvent(namespace, system_name, event_name, instance, func)

    def UnListenForEvent(self, namespace, system_name, event_name, instance, func):
        """取消事件监听"""
        serverApi.UnListenForEvent(namespace, system_name, event_name, instance, func)