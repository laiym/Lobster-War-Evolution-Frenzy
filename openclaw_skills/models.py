from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import Config

engine = create_engine(Config.DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # 实际应用需加密
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Lobster(Base):
    __tablename__ = 'lobsters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # 外键
    name = Column(String(50), nullable=False)
    ai_type = Column(String(20), nullable=False)  # 'analytical', 'berserk', 'charm', 'mech', 'cultivator', 'chaos'
    
    # 基础属性
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    health = Column(Integer, default=Config.BASE_HEALTH)
    attack = Column(Integer, default=Config.BASE_ATTACK)
    defense = Column(Integer, default=Config.BASE_DEFENSE)
    speed = Column(Integer, default=10)
    
    # AI成长数据（存储为JSON）
    memory_vectors = Column(JSON, default=list)  # 记忆向量
    neural_weights = Column(JSON, default=dict)  # 神经网络权重（简化）
    skill_tree = Column(JSON, default=dict)      # 已解锁技能
    personality = Column(JSON, default=dict)     # 性格权重
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class BattleRecord(Base):
    __tablename__ = 'battle_records'
    id = Column(Integer, primary_key=True)
    lobster_id = Column(Integer, nullable=False)
    opponent_id = Column(Integer, nullable=False)
    result = Column(String(10))  # 'win' or 'lose'
    battle_log = Column(JSON)    # 战斗日志
    created_at = Column(DateTime, default=datetime.utcnow)

# 创建表
Base.metadata.create_all(engine)
