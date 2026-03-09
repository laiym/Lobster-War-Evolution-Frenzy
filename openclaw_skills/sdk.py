"""
客户端SDK，封装与服务器的HTTP通信
"""
import requests

class OpenClawSDK:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        
    def register(self, username, password, email=''):
        """用户注册"""
        resp = requests.post(f'{self.base_url}/register', json={
            'username': username,
            'password': password,
            'email': email
        })
        if resp.status_code == 201:
            return resp.json()
        else:
            raise Exception(resp.json().get('error', '注册失败'))
            
    def login(self, username, password):
        """用户登录"""
        resp = requests.post(f'{self.base_url}/login', json={
            'username': username,
            'password': password
        })
        if resp.status_code == 200:
            data = resp.json()
            self.token = data['token']
            self.user_id = data['user_id']
            return data
        else:
            raise Exception(resp.json().get('error', '登录失败'))
            
    def create_lobster(self, name, ai_type):
        """创建新智虾"""
        if not self.token:
            raise Exception('请先登录')
        resp = requests.post(f'{self.base_url}/lobsters', json={
            'user_id': self.user_id,
            'name': name,
            'ai_type': ai_type
        }, headers={'Authorization': f'Bearer {self.token}'})
        if resp.status_code == 201:
            return resp.json()
        else:
            raise Exception(resp.json().get('error', '创建失败'))
            
    def get_lobster(self, lobster_id):
        """获取智虾信息"""
        resp = requests.get(f'{self.base_url}/lobsters/{lobster_id}')
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json().get('error', '获取失败'))
            
    def battle(self, lobster_id1, lobster_id2):
        """发起战斗"""
        resp = requests.post(f'{self.base_url}/battle', json={
            'lobster_id1': lobster_id1,
            'lobster_id2': lobster_id2
        })
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json().get('error', '战斗失败'))
            
    def get_battle_records(self, lobster_id):
        """获取战斗记录"""
        resp = requests.get(f'{self.base_url}/lobsters/{lobster_id}/records')
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json().get('error', '获取记录失败'))
