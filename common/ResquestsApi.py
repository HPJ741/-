import json
import time

import requests


class CommonRequest:
    def __init__(self, session):
        """基类初始化
                """
        self.session = session
        # self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
        }
        self.token = None  # 在后续新建的方法中获取token赋值

    def send_request(self, method: str, url: str, data: dict = None, headers=None, files=None, **kwargs):

        if method.lower() == "get":
            response = self.session.request(method=method, url=url, params=data, headers=headers)
        elif method.lower() == "post":
            response = self.session.request(method=method, url=url, json=data, headers=headers)
        elif method.lower() == "put":
            if "json" in kwargs.keys():
                response = self.session.request(method=method, url=url, json=kwargs["json"],
                                                headers=headers)
            else:
                response = self.session.request(method=method, url=url, headers=headers)
        elif method.lower() == "patch":
            pass
        elif method.lower() == "delete":
            response = self.session.request(method=method, url=url, headers=headers)
        elif method.lower() == "head":
            response = self.session.request(method=method, url=url, headers=headers)
        else:
            response = self.session.request(method=method, url=url, headers=headers)

        return response


if __name__ == '__main__':
    cq = CommonRequest(requests.Session())

    # get请求
    login_res = cq.send_request("get", "http://127.0.0.1:8888/api/private/v1/login",
                                {"username": "admin", "password": "123456"})

    # 提取Token
    token = json.loads(login_res.text)["data"]["token"]
    cq.token = token
    cq.headers["Authorization"] = token

    # post请求
    AddUser_response = cq.send_request("post", "http://127.0.0.1:8888/api/private/v1/users",
                                       {"username": "hpj1", "password": "123456"}, cq.headers)

    # put请求
    id = 514
    url = f"http://127.0.0.1:8888/api/private/v1/users/{id}"
    ChangeUser_response = cq.send_request("put", url,
                                          headers=cq.headers, json={"email": "22222", "mobile": "333333"})
    print(ChangeUser_response.text)

    # 修改某个用户状态
    change_data = {
        "uid": 525,
        "type": "true"
    }
    change_url = "http://127.0.0.1:8888/api/private/v1/users/%(uid)d/state/%(type)s" % change_data
    ChangeState_response = cq.send_request("put", change_url, headers=cq.headers)

    print(ChangeState_response.text)

    # 删除某个用户
    delete_data = {
        "id": 514
    }
    delete_url = "http://127.0.0.1:8888/api/private/v1/users/%(id)d" % delete_data
    response = cq.send_request("delete", delete_url, headers=cq.headers)
    json_response = json.loads(response.text)
    json_response2 = json.dumps(json_response)
    print(type(json_response), json_response)
    print(type(json_response2), json_response2)
    print("请求地址：", response.request.url)
    print("请求头：", response.request.headers)
    print("请求头：", response.text)
    print("响应头：", response.headers)
