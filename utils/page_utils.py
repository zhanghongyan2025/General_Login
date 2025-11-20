import time

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def is_login_success(
        page: Page,
        success_url_contains: str = None,  # 登录成功后URL应包含的关键字（如"/home"）
        success_selector: str = None,  # 登录成功后应出现的元素（如用户头像）
        logout_selector: str = None,  # 登录成功后应出现的退出按钮
        timeout: int = 10000  # 等待超时时间（毫秒）
) -> bool:
    """
    判断登录是否成功（通过登录后的页面特征验证）

    参数:
        page: Playwright Page 对象（当前页面）
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
        page.wait_for_load_state("load", timeout=timeout)

        # 2. 验证URL（如果提供了成功URL关键字）
        if success_url_contains:
            current_url = page.url.lower()
            if success_url_contains.lower() not in current_url:
                return False

        # 3. 验证成功元素（如果提供了成功元素选择器）
        if success_selector:
            # 等待元素可见（确保是登录后动态加载的）
            page.locator(success_selector).wait_for(state="visible", timeout=timeout)

        # 4. 验证退出按钮（如果提供了退出按钮选择器）
        if logout_selector:
            page.locator(logout_selector).wait_for(state="visible", timeout=timeout)

        # 所有验证条件通过 → 登录成功
        return True

    except PlaywrightTimeoutError:
        # 超时未满足验证条件 → 登录失败
        return False
    except Exception as e:
        # 其他异常 → 登录失败
        print(f"验证登录状态时发生错误：{str(e)}")
        return False


# from playwright.sync_api import sync_playwright
#
#
# def test_login():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto("http://192.168.40.61:3333/")  # 打开登录页
#
#         # 执行登录操作
#         page.get_by_role("textbox", name="账号").fill("fenghuang_123")
#         page.get_by_role("textbox", name="密码").fill("Aa123123!")
#         page.get_by_role("button", name="登 录").click()
#
#         time.sleep(1)
#
#         # 判断登录是否成功（根据目标网站特征调整参数）
#         login_success = is_login_success(
#             page=page,
#             logout_selector="退出"  # 成功后显示退出按钮
#         )
#
#         if login_success:
#             print("登录成功！")
#         else:
#             print("登录失败！")
#
#         browser.close()

