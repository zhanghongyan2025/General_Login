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
    
    # empty场景测试数据
    empty_cases = [
        
        # 空值场景：遍历基础字段生成用例
        
        (
            "username_empty",  # 用例标识：字段名_场景名
            
            "",  # username 空值
            "2vEnxkZu",  # 复用成功场景的密码（非空）
            
            "请输入您的用户名",  # 动态获取错误信息
        ),
        
        (
            "password_empty",  # 用例标识：字段名_场景名
            
            "SDQDXS002013",  # 复用成功场景的账号（非空）
            "",  # password 空值
            
            "请输入您的密码",  # 动态获取错误信息
        )
        
        
    ]
    empty_ids = [case[0] for case in empty_cases]  # 用例ID

    @pytest.mark.parametrize(
        "case_id, username, password, expected_error",  # 调整参数顺序：匹配用例元组结构
        empty_cases,
        ids=empty_ids
    )
    def test_empty(self, login_page, case_id, username, password, expected_error):
        # 填充表单（使用TEST_ACCOUNTS中的真实数据）
        time.sleep(0.5)
        login_page.fill_username(username)
        login_page.fill_password(password)
          
        # 普通场景单次点击
        login_page.click_login()
    
        # 验证结果（区分成功/失败场景）
        
        # 保留使用login_page.get_error_message(expected_error)的断言逻辑
        assert login_page.get_error_message(expected_error) is True, \
        f"预期错误信息：{expected_error}，实际未显示或不匹配"
        
    
    # username_password_not_match场景测试数据
    username_password_not_match_cases = [
        
        # 账号密码不匹配场景
        (
            "non_existent_user",  # 用例标识
            "test_valid",  # 对应TEST_ACCOUNTS的username
            "Valid@123",  # 对应TEST_ACCOUNTS的password
            "登录用户：test_valid 不存在",  # 错误信息
        ),
        (
            "wrong_password",  # 用例标识
            "SDQDXS002013",  # 对应TEST_ACCOUNTS的username
            "Valid@123",  # 对应TEST_ACCOUNTS的password
            "您已输错1次密码，若在24小时内连续输错5次密码，您的账号将被锁定24小时",  # 错误信息
        )
        
    ]
    username_password_not_match_ids = [case[0] for case in username_password_not_match_cases]  # 用例ID

    @pytest.mark.parametrize(
        "case_id, username, password, expected_error",  # 调整参数顺序：匹配用例元组结构
        username_password_not_match_cases,
        ids=username_password_not_match_ids
    )
    def test_username_password_not_match(self, login_page, case_id, username, password, expected_error):
        # 填充表单（使用TEST_ACCOUNTS中的真实数据）
        time.sleep(0.5)
        login_page.fill_username(username)
        login_page.fill_password(password)
          
        # 普通场景单次点击
        login_page.click_login()
    
        # 验证结果（区分成功/失败场景）
        
        # 保留使用login_page.get_error_message(expected_error)的断言逻辑
        assert login_page.get_error_message(expected_error) is True, \
        f"预期错误信息：{expected_error}，实际未显示或不匹配"
        
    
    # lock_account场景测试数据
    lock_account_cases = [
        
        # 账号锁定场景
        (
            "locked_user",  # 用例标识
            "SDQDXS002013",  # 对应TEST_ACCOUNTS的username
            "2vEnxkZu1",  # 对应TEST_ACCOUNTS的password
            "密码输入错误5次，帐户锁定1,440分钟",  # 错误信息
        )
        
    ]
    lock_account_ids = [case[0] for case in lock_account_cases]  # 用例ID

    @pytest.mark.parametrize(
        "case_id, username, password, expected_error",  # 调整参数顺序：匹配用例元组结构
        lock_account_cases,
        ids=lock_account_ids
    )
    def test_lock_account(self, login_page, case_id, username, password, expected_error):
        # 填充表单（使用TEST_ACCOUNTS中的真实数据）
        time.sleep(0.5)
        login_page.fill_username(username)
        login_page.fill_password(password)
        
        # 执行登录操作（重复点击处理）
        # 锁定相关场景：按提取的次数重复点击（LOCKED_COUNT是整数）
        for _ in range(5):  # range()接收整数，确保LOCKED_COUNT是整数
            time.sleep(0.5)  # 短暂等待，模拟用户连续点击
            login_page.click_login()  
            time.sleep(0.5) 
          
        # 普通场景单次点击
        login_page.click_login()
    
        # 验证结果（区分成功/失败场景）
        
        # 保留使用login_page.get_error_message(expected_error)的断言逻辑
        assert login_page.get_error_message(expected_error) is True, \
        f"预期错误信息：{expected_error}，实际未显示或不匹配"
        
    
    # success场景测试数据
    success_cases = [
        
        # 登录成功场景
        (
            "valid_login",  # 用例标识
            "SDQDXS002013",  # 对应TEST_ACCOUNTS的username
            "2vEnxkZu",  # 对应TEST_ACCOUNTS的password
            "登录成功",  # 成功场景标识
        )
        
    ]
    success_ids = [case[0] for case in success_cases]  # 用例ID

    @pytest.mark.parametrize(
        "case_id, username, password, expected_error",  # 调整参数顺序：匹配用例元组结构
        success_cases,
        ids=success_ids
    )
    def test_success(self, login_page, case_id, username, password, expected_error):
        # 填充表单（使用TEST_ACCOUNTS中的真实数据）
        time.sleep(0.5)
        login_page.fill_username(username)
        login_page.fill_password(password)
          
        # 普通场景单次点击
        login_page.click_login()
    
        # 验证结果（区分成功/失败场景）
        
        assert login_page.is_login_success(), "登录成功场景验证失败"