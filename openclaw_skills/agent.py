import random
import numpy as np
from datetime import datetime
from .models import Lobster, BattleRecord, Session
from .config import Config

# 模拟OpenClaw框架接口（实际使用时替换为真实openclaw导入）
class OpenClawBaseAgent:
    """模拟的OpenClaw基础Agent类"""
    def __init__(self, learning_rate=0.001):
        self.learning_rate = learning_rate
        self.memory = []  # 经验回放
        self.model = None  # 神经网络模型占位
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > Config.MEMORY_SIZE:
            self.memory.pop(0)
            
    def act(self, state, epsilon=0.1):
        """根据当前策略选择动作（随机或贪婪）"""
        if random.random() < epsilon:
            return random.randint(0, self.action_space - 1)
        # 实际应调用模型预测，这里模拟
        return 0
        
    def replay(self, batch_size):
        """从记忆中采样训练"""
        if len(self.memory) < batch_size:
            return
        # 模拟训练更新权重
        # 实际应使用梯度下降等
        pass

class LobsterAgent(OpenClawBaseAgent):
    """智虾AI代理，封装成长逻辑"""
    
    def __init__(self, lobster_id):
        super().__init__(learning_rate=Config.LEARNING_RATE)
        self.lobster_id = lobster_id
        self.load_from_db()
        self.action_space = 6  # 攻击、防御、语言攻击、技能1、技能2、终极技
        
    def load_from_db(self):
        """从数据库加载智虾数据"""
        session = Session()
        self.lobster = session.query(Lobster).get(self.lobster_id)
        if not self.lobster:
            raise ValueError(f"Lobster {self.lobster_id} not found")
        # 初始化神经网络权重（从数据库恢复或新建）
        if self.lobster.neural_weights:
            self.model_weights = self.lobster.neural_weights
        else:
            self.model_weights = self._init_weights()
        session.close()
        
    def _init_weights(self):
        """初始化简易神经网络权重（示例：线性层）"""
        return {
            'layer1': np.random.randn(10, 64).tolist(),
            'layer2': np.random.randn(64, self.action_space).tolist()
        }
        
    def get_state(self, battle_context):
        """构建状态向量供AI决策"""
        # 包含自身属性、敌人属性、战场环境等
        state = [
            self.lobster.health / 100.0,
            self.lobster.attack / 20.0,
            self.lobster.defense / 10.0,
            battle_context.get('enemy_health', 1.0),
            battle_context.get('enemy_attack', 0.5),
            battle_context.get('round', 0) / 10.0,
            battle_context.get('distance', 1.0),
            # 可加入更多特征
        ]
        return np.array(state, dtype=np.float32)
        
    def decide_action(self, state, epsilon=0.1):
        """根据状态选择动作（重写act以使用状态）"""
        if random.random() < epsilon:
            action = random.randint(0, self.action_space - 1)
        else:
            # 模拟前向传播（简化）
            # 实际应使用神经网络预测Q值
            q_values = np.random.randn(self.action_space)  # 模拟
            action = np.argmax(q_values)
        return action
        
    def record_battle(self, opponent_id, result, battle_log):
        """记录战斗结果并更新经验"""
        session = Session()
        record = BattleRecord(
            lobster_id=self.lobster_id,
            opponent_id=opponent_id,
            result=result,
            battle_log=battle_log
        )
        session.add(record)
        session.commit()
        session.close()
        
        # 触发经验增长和训练
        self._gain_exp(10 if result == 'win' else 2)
        self._train_from_memory()
        
    def _gain_exp(self, amount):
        """经验增长，可能触发升级"""
        session = Session()
        lobster = session.query(Lobster).get(self.lobster_id)
        lobster.exp += amount
        if lobster.exp >= lobster.level * 100:  # 升级阈值
            lobster.level += 1
            lobster.exp = 0
            # 属性提升
            lobster.health += 10
            lobster.attack += 2
            lobster.defense += 1
            # 技能树解锁逻辑
        session.commit()
        session.close()
        
    def _train_from_memory(self):
        """从战斗记忆中学习，更新神经网络权重"""
        # 模拟训练
        self.replay(Config.BATCH_SIZE)
        # 保存更新后的权重到数据库
        session = Session()
        lobster = session.query(Lobster).get(self.lobster_id)
        lobster.neural_weights = self.model_weights
        lobster.updated_at = datetime.utcnow()
        session.commit()
        session.close()
        
    def mutate(self):
        """随机突变，产生新特性（混沌型专属）"""
        if self.lobster.ai_type == 'chaos':
            # 随机改变一个属性
            attr = random.choice(['attack', 'defense', 'speed'])
            delta = random.randint(-5, 5)
            session = Session()
            lobster = session.query(Lobster).get(self.lobster_id)
            setattr(lobster, attr, getattr(lobster, attr) + delta)
            session.commit()
            session.close()
            return f"突变：{attr} 改变 {delta}"
        return None
