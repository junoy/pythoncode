#!/user/bin/python
# coding=utf8
import os
import json
import urllib2
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
class Chat(object):
    key = 你申请的api key
    server = "http://www.tuling123.com/openapi/api"
 
    def init(self):
        os.system("clear")
        print("聊天demo")
        print("---------------")
 
    def get(self):
        print("你:")
        string = raw_input()
        if string == "quit":
            print("tengteng: byebye")
            return True
        self.send(string)
 
    def send(self, string):
        uri = self.server + "?key=" + self.key + "&info=" + string
        res = urllib2.urlopen(uri).read()
        res_dict = json.loads(res)
        code = self.checkCode(res_dict["code"])
        if code == False:
            return False
        else:
            msg = self.productMsg(res_dict, code)
        output = "tengteng: " + msg
        print(output)
        self.get()
         
 
    # 这里处理错误的相应码
    def checkCode(self, code):
        if code == 40001:
            print("key 长度错误(32位)")
            return False
        elif code == 40002:
            print("请求的内容是空")
            return False
        elif code == 40003:
            print("当天请求的次数超限制")
            return False
        elif code == (40004 or 40005 or 40006 or 40007):
            error_msg = "api服务器错误 #" + code
            print(error_msg)
            return False
        else:
            return code
 
    # 这里生成输出的信息 里面的代码可以去文档里看
    def productMsg(self, res_dict, code):
        output = res_dict["text"] + "\r\n"
        text = ""
        if code == 200000:
            text = "请打开 " +  res_dict["url"]
        elif code == 302000:
            ablist = res_dict['list']
            for index in range(len(ablist)):
                alist = ablist[index]
                tmp = alist["article"] + "--" + alist["source"] + "——详情:" + alist["detailurl"] + "\r\n"
                text += tmp
        elif code == 304000:
            ablist = res_dict['list']
                        for index in range(len(ablist)):
                                alist = ablist[index]
                                tmp = alist["name"] + "--" + alist["count"] + "——详情" + alist["detailurl"] + "\r\n"
                                text += tmp
        elif code == 305000:
            ablist = res_dict['list']
                        for index in range(len(ablist)):
                                alist = ablist[index]
                                tmp = alist["trainnum"] + "--" + alist["start"] + "(" + alist["starttime"] + ")->" + alist["terminal"] + "(" + alist["endtime"] + ")详情" + alist["detailurl"] + "\r\n"
                                text += tmp
        elif code == 306000:
            ablist = res_dict['list']
            for index in range(len(ablist)):
                                alist = ablist[index]
                                tmp = alist["flight"] + "--" + alist["route"] + "--起飞时间:" + alist["starttime"] + "--到达时间:" + alist["endtime"] + "--状态:" + alist["state"] + "--详情:" + alist["detailurl"] + "\r\n"
                                text += tmp
        elif code == 308000:
            ablist = res_dict['list']
                        for index in range(len(ablist)):
                                alist = ablist[index]
                                tmp = alist["name"] + "--" + alist["info"] + "——详情:" + alist["detailurl"] + "\r\n"
                                text += tmp
        elif code == 309000:
            ablist = res_dict['list']
                        for index in range(len(ablist)) :
                                alist = ablist[index]
                                tmp = alist["name"] + "-------" + alist["price"] + "--------" + alist["satisfaction"]
                    text += tmp
        elif code == 311000:
            ablist = res_dict['list']
                        for index in range(len(ablist)) :
                                alist = ablist[index]
                                tmp = alist["name"] + "-------" + alist["price"] + "--详情：" + alist["detailurl"]
                                text += tmp
        elif code == 500000:
            text += "不知道你说的什么"
         
        return output + text
 
if __name__ == "__main__":
    chat = Chat()
    chat.init()
    chat.get()