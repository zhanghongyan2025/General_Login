LOGIN_TESTCASE_TEMPLATE = """
import time
import pytest
import os  # 补充os模块导入（用于路径处理）
import sys  # 补充sys模块导入（用于路径添加）
from playwright.sync_api import sync_playwright  

# 获取项目根目录（根据实际结构调整路径）
# 假设 test_suits 文件夹的父目录是项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将根目录加入搜索路径

from pages.login_page import LoginPage

@pytest.fixture(scope="function")  # 每个测试方法都创建新实例
def login_page():
    # 1. 初始化：启动浏览器并创建页面实例
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 在这里添加浏览器启动逻辑
        page = browser.new_page()
        login_page = LoginPage(page)  # 将playwright的page对象传入LoginPage
        yield login_page  # 提供给测试方法使用
        # 3. 测试后清理：关闭浏览器
        browser.close()

class TestLogin:
    {% for scenario in TEST_SCENARIOS %}
    # {{ scenario }}场景测试数据
    {{ scenario }}_cases = [
        {% if scenario == "empty" %}
        # 空值场景：遍历基础字段生成用例
        {% for field in TEST_FIELDS %}
        (
            "{{ field }}_{{ scenario }}",  # 用例标识：字段名_场景名
            {% if field == "username" %}
            "",  # username 空值
            "{{ TEST_ACCOUNTS['success']['password'] }}",  # 复用成功场景的密码（非空）
            {% else %}
            "{{ TEST_ACCOUNTS['success']['username'] }}",  # 复用成功场景的账号（非空）
            "",  # password 空值
            {% endif %}
            "{{ TEST_ERROR_MESSAGES[scenario][field + '_' + scenario] }}",  # 动态获取错误信息
        ){% if not loop.last %},{% endif %}
        {% endfor %}
        {% elif scenario == "username_password_not_match" %}
        # 账号密码不匹配场景
        (
            "non_existent_user",  # 用例标识
            "{{ TEST_ACCOUNTS['non_existent_user']['username'] }}",  # 对应TEST_ACCOUNTS的username
            "{{ TEST_ACCOUNTS['non_existent_user']['password'] }}",  # 对应TEST_ACCOUNTS的password
            "{{ TEST_ERROR_MESSAGES[scenario]['non_existent_user'] }}",  # 错误信息
        ),
        (
            "wrong_password",  # 用例标识
            "{{ TEST_ACCOUNTS['wrong_password']['username'] }}",  # 对应TEST_ACCOUNTS的username
            "{{ TEST_ACCOUNTS['wrong_password']['password'] }}",  # 对应TEST_ACCOUNTS的password
            "{{ TEST_ERROR_MESSAGES[scenario]['wrong_password'] }}",  # 错误信息
        )
        {% elif scenario == "lock_account" %}
        # 账号锁定场景
        (
            "locked_user",  # 用例标识
            "{{ TEST_ACCOUNTS['locked_user']['username'] }}",  # 对应TEST_ACCOUNTS的username
            "{{ TEST_ACCOUNTS['locked_user']['password'] }}",  # 对应TEST_ACCOUNTS的password
            "{{ TEST_ERROR_MESSAGES[scenario]['locked_user'] }}",  # 错误信息
        )
        {% elif scenario == "success" %}
        # 登录成功场景
        (
            "valid_login",  # 用例标识
            "{{ TEST_ACCOUNTS['success']['username'] }}",  # 对应TEST_ACCOUNTS的username
            "{{ TEST_ACCOUNTS['success']['password'] }}",  # 对应TEST_ACCOUNTS的password
            "登录成功",  # 成功场景标识
        )
        {% else %}
        # 通用场景处理（适配未来新增场景）
        {% for case_id in TEST_ERROR_MESSAGES[scenario].keys() %}
        (
            "{{ case_id }}",  # 用例标识
            "{{ TEST_ACCOUNTS[case_id]['username'] if case_id in TEST_ACCOUNTS else '' }}",  # 动态匹配TEST_ACCOUNTS
            "{{ TEST_ACCOUNTS[case_id]['password'] if case_id in TEST_ACCOUNTS else '' }}",  # 动态匹配TEST_ACCOUNTS
            "{{ TEST_ERROR_MESSAGES[scenario][case_id] }}",  # 错误信息
        ){% if not loop.last %},{% endif %}
        {% endfor %}
        {% endif %}
    ]
    {{ scenario }}_ids = [case[0] for case in {{ scenario }}_cases]  # 用例ID

    @pytest.mark.parametrize(
        "case_id, username, password, expected_error",  # 调整参数顺序：匹配用例元组结构
        {{ scenario }}_cases,
        ids={{ scenario }}_ids
    )
    def test_{{ scenario }}(self, login_page, case_id, username, password, expected_error):
        # 填充表单（使用TEST_ACCOUNTS中的真实数据）
        time.sleep(0.5)
        login_page.fill_username(username)
        login_page.fill_password(password)
        {% if scenario in ["lock_account"] %}
        # 执行登录操作（重复点击处理）
        # 锁定相关场景：按提取的次数重复点击（LOCKED_COUNT是整数）
        for _ in range({{ LOCKED_COUNT }}):  # range()接收整数，确保LOCKED_COUNT是整数
            time.sleep(0.5)  # 短暂等待，模拟用户连续点击
            login_page.click_login()  
            time.sleep(0.5) 
        {% endif %}  
        # 普通场景单次点击
        login_page.click_login()
    
        # 验证结果（区分成功/失败场景）
        {% if scenario == "success" %}
        assert login_page.is_login_success(), "登录成功场景验证失败"
        {% else %}
        # 保留使用login_page.get_error_message(expected_error)的断言逻辑
        assert login_page.get_error_message(expected_error) is True, \\
        f"预期错误信息：{expected_error}，实际未显示或不匹配"
        {% endif %}
    {% endfor %}
"""