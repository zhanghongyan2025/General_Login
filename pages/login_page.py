from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import time

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        page.goto("http://192.168.50.220:8888/sdqdv/#/login?redirect=%2Fsdq%2Fqydj%2F#")
        
        self.username = page.get_by_role("textbox", name="用户名")  # 角色+名称  # 移除外层引号
        
        self.password = page.get_by_role("textbox", name="密码")  # 角色+名称  # 移除外层引号
        
        self.unknown_element = page.get_by_role("button", name="企业备案")  # 角色+名称  # 移除外层引号
        
        self.login = page.get_by_role("button", name="登 录")  # 角色+名称  # 移除外层引号
        

    
    def fill_username(self, value: str, test_fields: str = None):
        """填写username输入框"""
        if test_fields:
            pass
        self.username.fill(value)  # 直接调用定位器的fill方法
    
    def fill_password(self, value: str, test_fields: str = None):
        """填写password输入框"""
        if test_fields:
            pass
        self.password.fill(value)  # 直接调用定位器的fill方法
    

    
    def click_unknown_element(self, test_fields: str = None):
        """点击unknown_element按钮"""
        if test_fields:
            pass
        self.unknown_element.click()  # 直接调用定位器的click方法
    
    def click_login(self, test_fields: str = None):
        """点击login按钮"""
        if test_fields:
            pass
        self.login.click()  # 直接调用定位器的click方法
    
    
    def get_error_message(self, error_message: str, timeout: int = 30000, test_fields: str = None) -> bool:
        """获取错误提示信息"""
        if test_fields:
            pass
        
        try:
        # 定位所有匹配文本的元素，取第一个并等待其可见
            self.page.get_by_text( text=error_message ).first.wait_for( state="visible",  timeout=timeout)
            time.sleep(0.5)
            return True
        except PlaywrightTimeoutError:
            return False

        except Exception as e:
        # 其他异常（如定位器错误）
            print(f"等待文字出现时发生错误: {str(e)}")
            return False
            
    def is_login_success(
        self,
        success_url_contains: str = None,  # 登录成功后URL应包含的关键字（如"/home"）
        success_selector: str = None,  # 登录成功后应出现的元素（如用户头像）
        logout_selector: str = None,  # 登录成功后应出现的退出按钮
        timeout: int = 10000  # 等待超时时间（毫秒）
) -> bool:
     """
    判断登录是否成功（通过登录后的页面特征验证）

    参数:
        success_url_contains: 登录成功后URL包含的关键字（如"/dashboard"）
        success_selector: 登录成功后出现的元素选择器（如".user-avatar"）
        logout_selector: 登录成功后出现的退出按钮选择器（如".logout-btn"）
        timeout: 等待验证的超时时间（默认10秒）

    返回:
        True: 登录成功
        False: 登录失败或超时
    """
     try:
        # 1. 等待页面加载完成（处理登录后的跳转）
        self.page.wait_for_load_state("load", timeout=timeout)

        # 2. 验证URL（如果提供了成功URL关键字）
        if success_url_contains:
            current_url = self.page.url.lower()
            if success_url_contains.lower() not in current_url:
                return False

        # 3. 验证成功元素（如果提供了成功元素选择器）
        if success_selector:
            # 等待元素可见（确保是登录后动态加载的）
            self.page.locator(success_selector).wait_for(state="visible", timeout=timeout)

        # 4. 验证退出按钮（如果提供了退出按钮选择器）
        if logout_selector:
            self.page.locator(logout_selector).wait_for(state="visible", timeout=timeout)

        # 所有验证条件通过 → 登录成功
        time.sleep(0.5)
        return True

     except PlaywrightTimeoutError:
        # 超时未满足验证条件 → 登录失败
        return False
     except Exception as e:
        # 其他异常 → 登录失败
        print(f"验证登录状态时发生错误：{str(e)}")
        return False