# -*- coding: utf-8 -*-
import os

import pytest

if __name__ == "__main__":
    pytest.main()
    os.system("allure generate report/allure_json -o report/allure_html --clean")
