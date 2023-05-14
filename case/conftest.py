# -*- coding: utf-8 -*-
import datetime

import allure
import pytest

from common.MysqlConnect import mysql
from common.utils import *


@pytest.fixture
def data(request):
    param = request.param
    # param['password'] = "admin"
    print(f" 获取用户名: {param['request_data']['username']} 获取密码：{param['request_data']['password']}")
    yield param


@pytest.fixture
def db():
    db = mysql()
    yield db
    db.close()


@pytest.fixture(scope="session", autouse=True)
def init():
    # 清除日志
    log_dir = get_log_dir()
    # clear_log_dir = [os.remove(os.path.join(log_dir, i)) for i in os.listdir(log_dir)]

    case_dir = get_case_dir()
    allure_dir = get_allure_dir()
    img_dir = get_img_dir()
    print("初始化完毕")


@pytest.fixture(scope="class", autouse=True)
def funcInfo():
    print('用例启动测试！')
    yield
    print("用例测试完毕！")

    log_dir = get_log_dir()
    log_list = [os.path.join(log_dir, i) for i in os.listdir(log_dir) if i == datetime.today().strftime("%Y-%m-%d")]
    for i in log_list:
        with open(i, "rb") as f:
            allure.attach(f.read(), os.path.basename(i), allure.attachment_type.TEXT)

