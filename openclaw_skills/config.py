import os

class Config:
    # 服务器配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///lobster.db'
    
    # OpenClaw训练配置
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    MEMORY_SIZE = 10000
    TRAINING_FREQUENCY = 100  # 每100步训练一次
    
    # 游戏平衡参数
    BASE_ATTACK = 10
    BASE_DEFENSE = 5
    BASE_HEALTH = 100
    LANGUAGE_DAMAGE_MULTIPLIER = 1.2
