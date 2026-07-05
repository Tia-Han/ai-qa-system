import subprocess
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"命令执行失败: {cmd}")
            print(f"错误信息: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("        推送到GitHub远程仓库")
    print("=" * 60)
    print("\n请按照以下步骤操作：")
    print("1. 登录GitHub：https://github.com")
    print("2. 创建一个新仓库（选择Public）")
    print("3. 获取仓库的SSH地址（格式：git@github.com:用户名/仓库名.git）")
    print("\n注意：请确保您的SSH公钥已添加到GitHub账户")
    print("SSH公钥：ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDLirL1BCsnMwoaYPcTMSsfkoMe5peFoqkdRarsrR5sx invitation@example.com")
    print("\n" + "=" * 60)
    
    repo_url = input("请输入GitHub仓库的SSH地址：").strip()
    
    if not repo_url:
        print("错误：请输入有效的仓库地址")
        sys.exit(1)
    
    print("\n正在推送代码到远程仓库...")
    
    commands = [
        f"git remote add origin {repo_url}",
        "git branch -M main",
        "git push -u origin main"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print("\n推送失败，请检查仓库地址是否正确")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 代码推送成功！")
    print(f"仓库地址：{repo_url}")
    print("=" * 60)

if __name__ == "__main__":
    main()