# base page operations
import os

from core.original_page_analyzer import get_visible_elements, generate_playwright_locator, get_element_variable_name
from gengrate.generate_target_from_template import generate_login_page
from utils.file_util import ensure_file_clear


def process_page_elements_to_loginpage(url):
    """处理页面元素并生成所有可见元素的定位器，同时生成LoginPage类"""
    # 获取可见元素
    visible_elements = get_visible_elements(url)
    if not visible_elements:
        print("未找到可见的input或button元素")
        return

    # 构建生成LoginPage所需的元素列表
    login_elements = []
    var_names = []  # 单独收集所有var_name
    for html in visible_elements:
        locator = generate_playwright_locator(html)
        var_name = get_element_variable_name(html)
        # 提取元素类型
        element_type = "input" if "input" in html.lower() else "button"
        login_elements.append({
            "var_name": var_name,
            "locator": locator,
            "type": element_type
        })
        var_names.append(var_name)  # 只收集var_name
        print(f"{var_name} = {locator}")

    # 生成login.py
    generate_login_page(login_elements,url)


def process_page_elements_to_conf_file(url, conf_file_path="conf/scenarios_setting.py"):
    """处理页面元素并在指定配置文件中写入TEST_BASIC_FIELDS常量（仅包含input元素的var_name）"""
    visible_elements = get_visible_elements(url)
    if not visible_elements:
        print("未找到可见的input或button元素")
        return

    # 仅收集input类型元素的var_name
    var_names = []
    for html in visible_elements:
        # 判断元素是否为input类型
        if "input" in html.lower():
            var_name = get_element_variable_name(html)
            var_names.append(var_name)

    if not var_names:
        print("未找到可见的input元素，无需更新TEST_BASIC_FIELDS常量")
        return

    # 确保文件存在且内容为空
    ensure_file_clear(conf_file_path)

    # 构建新的常量定义
    new_constant = f"TEST_FIELDS = {var_names}\n"

    # 直接写入新内容（文件已清空，无需处理原有内容）
    with open(conf_file_path, 'w', encoding='utf-8') as f:
        f.write(new_constant)

    print(f"已在{conf_file_path}中更新TEST_FIELDS常量（仅包含input元素）")
