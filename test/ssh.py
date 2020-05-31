import paramiko

# # 首先指定你的私钥在哪个位置（ssh是自动找到这个位置，Python不行，必须指定）
# private_key = paramiko.RSAKey.from_private_key_file('testtest')
#
# # 创建SSH对象
# ssh = paramiko.SSHClient()
#
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# # 连接服务器
# ssh.connect(hostname='120.132.70.125', username='hjmrunning', pkey=private_key)
#
# # 执行命令
# code='ssh -i ~/.ssh/testtest -t hjmrunning@120.132.70.125 'ssh -t test2-basics "redis-cli -n 8 flushdb"''
# stdin, stdout, stderr = ssh.exec_command(code)
#
# # 获取命令结果
# result = stdout.read().decode()
# print(result)
#
# # 关闭连接
# ssh.close()
# client = paramiko.SSHClient()
# private_key = paramiko.RSAKey.from_private_key_file('/Users/administrator/.ssh/testtest')


for i in range(100):
    print('1')