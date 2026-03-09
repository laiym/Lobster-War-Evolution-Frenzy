"""
命令行客户端示例，演示如何使用SDK
"""
import sys
sys.path.append('..')
from openclaw_skills.sdk import OpenClawSDK

def main():
    sdk = OpenClawSDK(base_url='http://localhost:5000/api')
    
    while True:
        print("\n=== 龙虾战争·进化狂潮 CLI ===")
        print("1. 注册")
        print("2. 登录")
        print("3. 创建智虾")
        print("4. 查看智虾")
        print("5. 发起战斗")
        print("6. 查看战斗记录")
        print("0. 退出")
        choice = input("请选择: ")
        
        if choice == '1':
            username = input("用户名: ")
            password = input("密码: ")
            email = input("邮箱(可选): ")
            try:
                result = sdk.register(username, password, email)
                print(f"注册成功! 用户ID: {result['id']}")
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '2':
            username = input("用户名: ")
            password = input("密码: ")
            try:
                result = sdk.login(username, password)
                print(f"登录成功! 用户ID: {result['user_id']}")
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '3':
            if not sdk.token:
                print("请先登录!")
                continue
            name = input("智虾名称: ")
            print("AI类型: analytical, berserk, charm, mech, cultivator, chaos")
            ai_type = input("选择类型: ")
            try:
                result = sdk.create_lobster(name, ai_type)
                print(f"智虾创建成功! ID: {result['id']}")
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '4':
            lobster_id = input("智虾ID: ")
            try:
                lobster = sdk.get_lobster(lobster_id)
                print(f"名称: {lobster['name']}")
                print(f"类型: {lobster['ai_type']}")
                print(f"等级: {lobster['level']} (经验 {lobster['exp']})")
                print(f"属性: 生命 {lobster['health']} 攻击 {lobster['attack']} 防御 {lobster['defense']} 速度 {lobster['speed']}")
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '5':
            id1 = input("我方智虾ID: ")
            id2 = input("敌方智虾ID: ")
            try:
                result = sdk.battle(id1, id2)
                print(f"胜利者ID: {result['winner_id']}")
                print("战斗日志:")
                for line in result['log']:
                    print(line)
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '6':
            lobster_id = input("智虾ID: ")
            try:
                records = sdk.get_battle_records(lobster_id)
                print("战斗记录:")
                for r in records:
                    print(f"对手ID: {r['opponent_id']}, 结果: {r['result']}, 时间: {r['created_at']}")
            except Exception as e:
                print(f"错误: {e}")
                
        elif choice == '0':
            break

if __name__ == '__main__':
    main()
