import socket
import threading
from multiprocessing import Queue

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 8888))
user_dict = {}    # 线程共享资源，所以可以在主进程中设置字典存放客户端地址


def server_recv(s, q):
    # 返回data和addr
    sender, sender_addr = s.recvfrom(1024)
    # 返回data
    recipient = s.recv(1024)
    data = s.recv(1024)

    # 收件人地址
    recipient_addr = None
    for k, v in user_dict.items():
        if k == recipient.decode():
            recipient_addr = user_dict[k]

    # 发送方有没有在字典中
    sender_not_in_dict = True
    for v in user_dict.values():
        if v == sender_addr:
            sender_not_in_dict = False

    # 收到“请求连接”消息
    if data == "请求连接".encode() and sender_not_in_dict:
        user_dict[sender.decode()] = sender_addr
        q.put((sender, sender_addr, data, recipient, recipient_addr))
    # 收到正常消息
    else:
        q.put((sender, sender_addr, data, recipient, recipient_addr))


def server_send(s, q):
    global user_dict
    sender, sender_addr, data, recipient, recipient_addr = q.get()

    # 收到“请求连接”消息
    if data == "请求连接".encode():
        s.sendto("服务器".encode(), sender_addr)
        s.sendto("连接成功".encode(), sender_addr)
    # 收到正常消息
    else:
        s.sendto(sender, recipient_addr)
        s.sendto(data, recipient_addr)


print('> 服务器部署成功')
while True:
    q = Queue()
    t1 = threading.Thread(target=server_recv, args=(s, q))
    t2 = threading.Thread(target=server_send, args=(s, q))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
