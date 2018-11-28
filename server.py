#coding:utf-8
import tornado.web
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
import redis
import json

r = redis.StrictRedis('localhost',6379)
class ChatHandler(WebSocketHandler):
    def open(self):
        #添加用户到集合
        r.sadd('users',self.request.remote_ip)
        users = r.smembers('users')
        user_list = []
        for i in users:
            i_str = i.decode('utf-8')
            user_list.append(i_str)
        self.write_message(json.dumps(user_list))
        #广播新登陆用户
    def on_close(self):
        r.srem('users',self.request.remote_ip)


    def check_origin(self,origin):
        return True






if __name__ == "__main__":
    chat_server = tornado.web.Application([
        ('/',ChatHandler)
    ])
    chat_server.listen(8080)
    tornado.ioloop.IOLoop.current().start()
