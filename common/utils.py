# -*- coding: utf-8 -*-

import os

import yaml


class utils:
    _root_dir = r"D:\PycharmProjects\电商接口自动化项目"
    _log_dir = os.path.join(_root_dir, "log")
    _img_dir = os.path.join(_root_dir, "img")
    _report_dir = os.path.join(_root_dir, "report")
    _report_allure_json = os.path.join(_report_dir, "allure_json")
    _report_allure_html = os.path.join(_report_dir, "allure_html")
    _case_dir = os.path.join(_root_dir, "case_data")


def get_allure_dir():
    _allure_file_list = (utils._report_dir, utils._report_allure_json, utils._report_allure_html)
    _file_exit = [os.mkdir(i) for i in _allure_file_list if not os.path.exists(i)]
    return _allure_file_list


def get_log_dir():
    os.mkdir(utils._log_dir) if not os.path.exists(utils._log_dir) else 1
    return utils._log_dir


def get_img_dir():
    os.mkdir(utils._img_dir) if not os.path.exists(utils._img_dir) else 1
    return utils._img_dir


def get_case_dir():
    os.mkdir(utils._case_dir) if not os.path.exists(utils._case_dir) else 1
    return utils._case_dir


def get_data(path):
    path = os.path.join(get_case_dir(), path)
    with open(path, "r", encoding="utf-8") as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value


def write_data(path, data):
    path = os.path.join(get_case_dir(), path)
    with open(path, "w+", encoding="utf-8") as f:
        yaml.safe_dump(data=data, stream=f, allow_unicode=True, sort_keys=False, indent=4)
    print("数据写入完毕")


if __name__ == '__main__':
    allure = get_allure_dir()
    print(allure)

    log_dir = get_log_dir()
    print(log_dir)

    img_dir = get_img_dir()
    print(img_dir)

    # data = [{'request_data': {'username': 'admin', 'password': '123456'}, 'response_data': {'msg': '登录成功'}},
    #         {'request_data': {'username': 'linken', 'password': '123456'}, 'response_data': {'msg': '该用户已经被禁用'}},
    #         {'request_data': {'username': 'asdf1', 'password': '123456'}, 'response_data': {'msg': '密码错误'}},
    #         {'request_data': {'username': 'hpj1', 'password': '123456'}, 'response_data': {'msg': '该用户没有权限登录'}}]
    #
    # write_data("login_case.yaml", data)
    print(get_data("login_case.yaml"))
