import os
import sys
import subprocess
import shutil
import datetime
from git import Repo

host = '192.168.1.129'
user = 'root'
password = 'Sushile123.'
database = 'tag'


# 导出提交数据库
def export_sql():
    try:
        # 导航到 D:\phpstudy_pro\Extensions\MySQL5.7.26\bin 目录
        os.chdir(r"D:\phpstudy_pro\Extensions\MySQL5.7.26\bin")
        # 导出数据库到SQL文件  C:\Users\ASUS\Desktop\CK\app_sql
        dump_file = os.path.join("tag.sql")
        dump_cmd = f'mysqldump -u{user} -p{password} -h{host} {database} > {dump_file}'
        subprocess.run(dump_cmd, shell=True)
        print(f"SQL file exported to: {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error exporting SQL file: {e}")
        with open("error.log", "a") as f:
            f.write(f"Error exporting SQL file: {e}\n")
    except Exception as e:
        print(f"Unexpected error: {e}")
        with open("error.log", "a") as f:
            f.write(f"Unexpected error: {e}\n")


def commit_sql():
    # 获取当前脚本所在目录
    dirfile = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    # 目标文件路径
    target_file = os.path.join(dirfile, "tag.sql")
    # 源文件路径（假设在与可执行文件相同目录下）
    source_file = "tag.sql"
    # 复制文件
    shutil.copy(source_file, target_file)

    try:
        # 创建 Repo 对象
        repo = Repo(dirfile)
        # 获取 Git 命令对象
        g = repo.git
        # 添加 tag.sql 文件到暂存区
        g.add("tag.sql")
        # 提交变更,添加提交消息
        # 当前的时间
        now = datetime.datetime.now()
        print(now)
        g.commit("-m 'Auto update tag.sql'")
        # 推送到远程仓库
        g.push()
        print("Successful push!")
    except Exception as e:
        print(f"Error executing Git commands: {e}")
        with open("error.log", "a") as f:
            f.write(f"Error executing Git commands: {e}\n")


if __name__ == '__main__':
    export_sql()
    commit_sql()
