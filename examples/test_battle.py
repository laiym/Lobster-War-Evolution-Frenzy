"""
测试战斗模拟器
"""
import sys
sys.path.append('..')
from openclaw_skills.game import BattleSimulator
from openclaw_skills.models import Session, Lobster

# 创建两个测试智虾（如果不存在）
session = Session()
lobster1 = session.query(Lobster).filter_by(name='Test1').first()
if not lobster1:
    lobster1 = Lobster(user_id=1, name='Test1', ai_type='berserk')
    session.add(lobster1)
lobster2 = session.query(Lobster).filter_by(name='Test2').first()
if not lobster2:
    lobster2 = Lobster(user_id=1, name='Test2', ai_type='analytical')
    session.add(lobster2)
session.commit()
session.close()

sim = BattleSimulator(lobster1.id, lobster2.id)
winner, log = sim.run()
print(f"Winner: {winner}")
for line in log:
    print(line)
