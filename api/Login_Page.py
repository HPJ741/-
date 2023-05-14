import json
import random

import requests

from common.ResquestsApi import CommonRequest


class LoginPage(CommonRequest):
    _host = "127.0.0.1:8888"
    _login_api = "api/private/v1/login"
    _register_api = "api/private/v1/users"

    def login(self, data: dict):
        url = f"http://{self._host}/api/private/v1/login"
        response = self.send_request("get", url, data)
        return response

    def register(self, data: dict):
        url = f"http://{self._host}/api/private/v1/users"
        response = self.send_request("post", url, data, self.headers)
        return response

    def ChangeUserInfo(self, user_id: int, data: dict):
        url = f"http://{self._host}/api/private/v1/users/{user_id}"
        response = self.send_request("put", url, json=data, headers=self.headers)
        return response

    def ChangeUserStatus(self, data):
        url = f"http://{self._host}/api/private/v1/users/%(uid)d/state/%(type)s" % data
        response = self.send_request("put", url, headers=self.headers)
        return response

    def delUser(self, user_id):
        url = f"http://{self._host}/api/private/v1/users/{user_id}"
        response = self.send_request("delete", url, headers=self.headers)
        return response


if __name__ == "__main__":
    lp = LoginPage(requests.Session())

    # 登录接口
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    login_response = lp.login(login_data)
    print(login_response.text)

    # 提取Token
    token = json.loads(login_response.text)["data"]["token"]
    lp.token = token
    lp.headers["Authorization"] = token

    # 注册接口
    register_data = {
        "username": f"hpj{random.randint(0,1000)}",
        "password": "123456"
    }
    register_response = lp.register(register_data)
    print(register_response.text)

    # 修改用户信息接口
    ChangeUserInfo_userid = 525
    ChangeUserInfo_data = {
        "email": str(random.randint(0, 1000)),
        "mobile": str(random.randint(1000, 2000))
    }
    ChangeUserInfo_response = lp.ChangeUserInfo(ChangeUserInfo_userid, ChangeUserInfo_data)
    print(ChangeUserInfo_response.text)

    # 修改用户状态
    ChangeUserStatus_data = {
        "uid": 525,
        "type": "true"
    }
    ChangeUserStatus_response = lp.ChangeUserStatus(ChangeUserStatus_data)
    print(ChangeUserStatus_response.text)

    # 删除某个用户
    delete_user_id = 545
    del_response = lp.delUser(delete_user_id)
    print(del_response.text)
