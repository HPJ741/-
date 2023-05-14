import json
import random
import sys
import time

import allure
import pytest
import requests

from api.Login_Page import LoginPage
from common.LogHandle import Logger
from common.utils import *

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@allure.epic("user接口测试")
class TestApi:
    NewUserId = []

    def setup_class(self):
        session = requests.Session()
        self.lp = LoginPage(session)
        self.logger = Logger("test_api")

    @allure.step("登录")
    @pytest.mark.parametrize("data", get_data("login_case.yaml"), indirect=True)
    def test_login(self, data):
        start_time = time.time()
        response = self.lp.login(data["request_data"])
        end_time = time.time()
        count_time = int((end_time - start_time) * 1000)

        # 输出日志
        self.logger.info(
            f"test_login：请求地址：{response.url}  请求头：{response.request.headers} "
            f"响应状态码：{response.status_code}   响应数据：{response.text} 请求耗时：{count_time}ms")

        # 提取登录态token
        try:
            token = json.loads(response.text)["data"]["token"]
            self.lp.token = token
            self.lp.headers["Authorization"] = token
        except Exception as e:
            print(f"登录失败！error:{e}")

        assert response.status_code == 200
        assert count_time < 200
        assert json.loads(response.text)["meta"]["msg"] == data["response_data"]["msg"]

    @allure.step("注册")
    @pytest.mark.parametrize("data", [{
        "username": f"hpj{random.randint(0,1000)}",
        "password": "123456",
        "msg": "创建成功"
    }])
    def test_regist(self, data, db):
        start_time = time.time()
        response = self.lp.register(data)
        end_time = time.time()
        count_time = int((end_time - start_time) * 1000)

        try:
            self.NewUserId.append(json.loads(response.text)["data"]["id"])
        except Exception as e:
            self.logger.critical(f"id获取失败！error:{e}")

        # 输出日志
        self.logger.info(
            f"test_regist：请求地址：{response.url}  请求头：{response.request.headers} "
            f"响应状态码：{response.status_code}   响应数据：{response.text} 请求耗时：{count_time}ms")

        # 数据库校验结果
        sql = f'select mg_id from sp_manager where mg_id = {json.loads(response.text)["data"]["id"]}'
        result = db.search_execute(sql)
        self.logger.info(f"test_regist：数据库校验结果：{result}")

        assert response.status_code == 200
        assert count_time < 300
        assert json.loads(response.text)["meta"]["msg"] == data["msg"]
        assert result is True

    @allure.step("修改用户信息")
    # 修改用户信息接口
    @pytest.mark.parametrize("data", [{
        "email": str(random.randint(0, 1000)),
        "mobile": str(random.randint(1000, 2000))
    }])
    def test_changeinfo(self, data, db):
        start_time = time.time()
        response = self.lp.ChangeUserInfo(self.NewUserId[0], data)
        end_time = time.time()
        count_time = int((end_time - start_time) * 1000)

        # 输出日志
        self.logger.info(
            f"test_changeinfo：请求地址：{response.url}  请求头：{response.request.headers} "
            f"响应状态码：{response.status_code}   响应数据：{response.text} 请求耗时：{count_time}ms")

        # 数据库校验结果
        sql = f'select mg_id,mg_email,mg_mobile from sp_manager where mg_id={self.NewUserId[0]} and mg_email={data["email"]} and mg_mobile={data["mobile"]}'
        result = db.search_execute(sql)
        self.logger.info(f"test_changeinfo：数据库校验结果：{result}")

        assert response.status_code == 200
        # assert count_time < 200
        assert result is True

    @allure.step("修改用户状态")
    @pytest.mark.parametrize("data", [{
        "type": "true"
    }])
    def test_changestatus(self, data, db):
        data["uid"] = self.NewUserId[0]
        start_time = time.time()
        response = self.lp.ChangeUserStatus(data)
        end_time = time.time()
        count_time = int((end_time - start_time) * 1000)

        # 输出日志
        self.logger.info(
            f"test_changestatus：请求地址：{response.url}  请求头：{response.request.headers} "
            f"响应状态码：{response.status_code}   响应数据：{response.text} 请求耗时：{count_time}ms")
        time.sleep(2)
        # 数据库校验结果
        type = 1 if data["type"] == "true" or data["type"] == 1 else 0
        sql = f'select mg_id,mg_state from sp_manager where mg_id = {self.NewUserId[0]} and mg_state={type}'
        result = db.search_execute(sql)
        self.logger.info(f"test_regist：数据库校验结果：{result}")

        assert response.status_code == 200
        # assert count_time < 200
        assert result is True

    @allure.step("删除")
    # 删除某个用户
    def test_deluser(self, db):
        start_time = time.time()
        response = self.lp.delUser(self.NewUserId[0])
        end_time = time.time()
        count_time = int((end_time - start_time) * 1000)

        # 输出日志
        self.logger.info(
            f"test_deluser：请求地址：{response.url}  请求头：{response.request.headers} "
            f"响应状态码：{response.status_code}   响应数据：{response.text} 请求耗时：{count_time}ms")

        # 数据库校验结果
        sql = f'select mg_id from sp_manager where mg_id={self.NewUserId[0]}'
        result = db.search_execute(sql)
        self.logger.info(f"test_changeinfo：数据库校验结果：{result}")

        assert response.status_code == 200
        # assert count_time < 200
        assert result is False

    @allure.title("测试失败")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_fail(self):
        with allure.step("失败用例1"):
            print("失败用例1失败用例1失败用例1失败用例1失败用例1")
            assert 1 == 1

        with allure.step("失败用例2"):
            print("失败用例2失败用例2失败用例2失败用例2失败用例2失败用例2")
            assert 1 == 0
