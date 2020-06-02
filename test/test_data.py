import os
import subprocess

os.system('ssh -i ~/.ssh/id_rsa -t hjmrunning@10.10.198.94')
os.system('ssh -t test2-basics')
os.system('redis-cli -n 8 flushdb')

num0='ssh -i ~/.ssh/id_rsa -t hjmrunning@10.10.198.94'
num1='ssh -t test2-basics'
num2="redis-cli -n 8 flushdb"


cmd = num0 + " && " + num1+" && "+num2

#如下两种都可以运行
subprocess.Popen(cmd, shell=True)
# subprocess.call(cmd,shell=True)