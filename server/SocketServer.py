#! /usr/bin/env python
#coding=utf-8
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from ByteArray import ByteArray
import types
#导入协议模块
import Protocols
class SocketServer(Protocol):
    #初始化 构造函数 将类内的属性在此初始化
    def __init__(self):
        pass
    #客户端链接成功
    def connectionMade(self):
        print "login", self.transport.client
        self.factory.login(self)
    #客户端链接断开
    def connectionLost(self, reason):
        print "lost", self.transport.client, reason

    def dataReceived(self, data):
        #pass
        print "data", data

class SocketFactory(Factory):
    protocol = SocketServer
    #初始化 构造函数
    def __init__(self):
        #存放客户端mapde
        self.clientMap = {}

    #登录方法
    def login(self, client):
        #pass
        self.clientMap[client] = client
        self.send(client, write_multi_data(1, ["akb", 1, 48]))

    #向客户端发消息
    def send(self, c, msg):
        c.transport.write(msg)

#写入数据
#id 协议号
#data 需要写入的数据
def write_data(id, data):
    #获取协议号 + 内容 以后的长度
    length = get_bytes_len(id) + get_bytes_len(data)
    #print id, length, data
    ba = ByteArray()
    ba.endian = '!'
    ba.writeInt(length)
    ba.writeInt(id)
    #print type(data)
    #根据data类型 写入ba
    if type(data) == types.StringType:
        ba.writeUTFBytes(data)
    elif type(data) == types.IntType:
        ba.writeInt(data)
    elif type(data) == types.BooleanType:
        ba.writeBoolean(data)
    return ba.data

#写入多个数据
#id 协议号
#params 一个存放数据的列表
def write_multi_data(id, params):
    length = get_bytes_len(id)
    for i in range(0, len(params)):
        length += get_bytes_len(params[i])
    ba = ByteArray()
    ba.endian = '!'
    ba.writeInt(length)
    ba.writeInt(id)
    #根据data类型 写入ba
    for i in range(0, len(params)):
        data = params[i]
        if type(data) == types.StringType:
           ba.writeUTFBytes(data)
        elif type(data) == types.IntType:
           ba.writeInt(data)
        elif type(data) == types.BooleanType:
           ba.writeBoolean(data)
    return ba.data


#获取数据的字节长度
#data 需要获取长度的数据
def get_bytes_len(data):
    b = ByteArray()
    if type(data) == types.StringType:
       b.writeUTFBytes(data)
    elif type(data) == types.IntType:
       b.writeInt(data)
    elif type(data) == types.BooleanType:
       b.writeDouble(data)
    return len(b.data)

def main():
    reactor.listenTCP(8000, SocketFactory())
    reactor.run()


if __name__ == "__main__":
    main()

print write_multi_data(1, ["as", "s", 1])