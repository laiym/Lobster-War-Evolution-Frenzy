import random
from .agent import LobsterAgent
from .models import Lobster, Session

class BattleSimulator:
    """战斗模拟器，处理回合制对战"""
    
    def __init__(self, lobster_id1, lobster_id2):
        self.agent1 = LobsterAgent(lobster_id1)
        self.agent2 = LobsterAgent(lobster_id2)
        self.round = 0
        self.max_rounds = 20
        self.log = []
        
    def run(self):
        """执行战斗，返回胜利者ID和日志"""
        health1 = self.agent1.lobster.health
        health2 = self.agent2.lobster.health
        
        while self.round < self.max_rounds and health1 > 0 and health2 > 0:
            self.round += 1
            # 决定行动（简化：轮流攻击）
            # 实际可根据速度决定行动顺序
            action1 = self.agent1.decide_action(self._build_context(health1, health2))
            action2 = self.agent2.decide_action(self._build_context(health2, health1))
            
            # 应用动作效果（简化）
            damage1 = self._calc_damage(self.agent1, self.agent2, action1)
            health2 -= damage1
            self.log.append(f"回合{self.round}: 龙虾{self.agent1.lobster_id} 使用动作{action1} 造成{damage1}伤害")
            
            if health2 <= 0:
                break
                
            damage2 = self._calc_damage(self.agent2, self.agent1, action2)
            health1 -= damage2
            self.log.append(f"回合{self.round}: 龙虾{self.agent2.lobster_id} 使用动作{action2} 造成{damage2}伤害")
        
        # 判定胜负
        if health1 <= 0:
            winner_id = self.agent2.lobster_id
            loser_id = self.agent1.lobster_id
        elif health2 <= 0:
            winner_id = self.agent1.lobster_id
            loser_id = self.agent2.lobster_id
        else:
            # 平局，比较剩余血量
            if health1 > health2:
                winner_id = self.agent1.lobster_id
                loser_id = self.agent2.lobster_id
            else:
                winner_id = self.agent2.lobster_id
                loser_id = self.agent1.lobster_id
        
        # 记录战斗
        self.agent1.record_battle(loser_id if winner_id==self.agent1.lobster_id else winner_id,
                                   'win' if winner_id==self.agent1.lobster_id else 'lose',
                                   self.log)
        self.agent2.record_battle(loser_id if winner_id==self.agent2.lobster_id else winner_id,
                                   'win' if winner_id==self.agent2.lobster_id else 'lose',
                                   self.log)
        return winner_id, self.log
        
    def _build_context(self, my_health, enemy_health):
        return {
            'my_health': my_health,
            'enemy_health': enemy_health,
            'round': self.round
        }
        
    def _calc_damage(self, attacker, defender, action):
        """计算伤害（示例）"""
        base_damage = attacker.lobster.attack
        # 动作类型影响：0普通攻击，1防御，2语言攻击，3技能1，4技能2，5终极技
        if action == 0:
            return base_damage
        elif action == 1:
            return 0  # 防御本回合无伤害
        elif action == 2:
            # 语言攻击伤害受对方防御和性格影响
            return int(base_damage * Config.LANGUAGE_DAMAGE_MULTIPLIER)
        else:
            return base_damage * 2  # 技能伤害翻倍
        return base_damage

# 为了简化，没有导入Config，实际需要
from .config import Config
