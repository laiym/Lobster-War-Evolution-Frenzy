from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Session, User, Lobster, BattleRecord
from .agent import LobsterAgent
from .game import BattleSimulator
import uuid

app = Flask(__name__)
CORS(app)
app.config.from_object('openclaw_skills.config.Config')

@app.before_request
def before_request():
    g.db_session = Session()

@app.teardown_request
def teardown_request(exception=None):
    db_session = g.pop('db_session', None)
    if db_session:
        db_session.close()

# ---------- 用户相关 ----------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password:
        return jsonify({'error': '用户名和密码必填'}), 400
    # 检查重复
    user = g.db_session.query(User).filter_by(username=username).first()
    if user:
        return jsonify({'error': '用户名已存在'}), 400
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    g.db_session.add(user)
    g.db_session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = g.db_session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = str(uuid.uuid4())  # 简化token，实际用JWT
        return jsonify({'token': token, 'user_id': user.id})
    return jsonify({'error': '用户名或密码错误'}), 401

# ---------- 智虾相关 ----------
@app.route('/api/lobsters', methods=['POST'])
def create_lobster():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    ai_type = data.get('ai_type')
    if ai_type not in ['analytical', 'berserk', 'charm', 'mech', 'cultivator', 'chaos']:
        return jsonify({'error': '无效的AI类型'}), 400
    lobster = Lobster(
        user_id=user_id,
        name=name,
        ai_type=ai_type
    )
    g.db_session.add(lobster)
    g.db_session.commit()
    return jsonify({'id': lobster.id, 'name': lobster.name}), 201

@app.route('/api/lobsters/<int:lobster_id>', methods=['GET'])
def get_lobster(lobster_id):
    lobster = g.db_session.query(Lobster).get(lobster_id)
    if not lobster:
        return jsonify({'error': '智虾不存在'}), 404
    return jsonify({
        'id': lobster.id,
        'name': lobster.name,
        'ai_type': lobster.ai_type,
        'level': lobster.level,
        'exp': lobster.exp,
        'health': lobster.health,
        'attack': lobster.attack,
        'defense': lobster.defense,
        'speed': lobster.speed,
        'skill_tree': lobster.skill_tree
    })

@app.route('/api/lobsters/<int:lobster_id>/train', methods=['POST'])
def train_lobster(lobster_id):
    """触发AI在线学习（通常异步）"""
    agent = LobsterAgent(lobster_id)
    agent._train_from_memory()
    return jsonify({'status': 'training started'})

# ---------- 战斗 ----------
@app.route('/api/battle', methods=['POST'])
def battle():
    data = request.json
    lobster_id1 = data.get('lobster_id1')
    lobster_id2 = data.get('lobster_id2')
    # 检查是否存在
    lobster1 = g.db_session.query(Lobster).get(lobster_id1)
    lobster2 = g.db_session.query(Lobster).get(lobster_id2)
    if not lobster1 or not lobster2:
        return jsonify({'error': '智虾不存在'}), 404
    
    sim = BattleSimulator(lobster_id1, lobster_id2)
    winner_id, log = sim.run()
    return jsonify({
        'winner_id': winner_id,
        'log': log
    })

# ---------- 战斗记录 ----------
@app.route('/api/lobsters/<int:lobster_id>/records', methods=['GET'])
def get_records(lobster_id):
    records = g.db_session.query(BattleRecord).filter_by(lobster_id=lobster_id).all()
    return jsonify([{
        'id': r.id,
        'opponent_id': r.opponent_id,
        'result': r.result,
        'created_at': r.created_at.isoformat()
    } for r in records])

if __name__ == '__main__':
    app.run(debug=True)
