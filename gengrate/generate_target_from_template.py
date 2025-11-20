# generate_login.py
from jinja2 import Template
from templates.login_template import LOGIN_PAGE_TEMPLATE
import conf.scenarios_setting as scenarios_setting
from utils.file_util import *
from utils.scenario_utils import *
from templates.testcase_template import LOGIN_TESTCASE_TEMPLATE


def generate_login_page(elements: list, url, output_file: str = "pages/login_page.py"):
    """生成LoginPage类代码（若文件已存在，会先清空原有内容）"""
    template = Template(LOGIN_PAGE_TEMPLATE)
    # 渲染模板时传入elements和TEST_FIELDS
    code = template.render(
        elements=elements,
        url=url,
        TEST_FIELDS=scenarios_setting.TEST_FIELDS
    )

    ensure_file_clear(output_file)

    # 关键：使用 'w' 模式打开文件，会自动清空原有内容后写入新内容
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code.strip())

    print(f"LoginPage类已生成到 {output_file}")

def generate_testcase(target_url, output_path: str = "test_suits/test_login.py"):
    """根据元素列表和场景生成测试用例"""
    locked_count, _ = extract_lock_info(scenarios_setting.TEST_ERROR_MESSAGES["lock_account"].get("locked_user", ""))
    render_data = {
        "LOCKED_COUNT": locked_count,
        "TARGET_URL": target_url,
        "TEST_SCENARIOS": scenarios_setting.TEST_SCENARIOS,
        "TEST_FIELDS": scenarios_setting.TEST_FIELDS,
        "TEST_ERROR_MESSAGES": scenarios_setting.TEST_ERROR_MESSAGES,
        "TEST_ACCOUNTS": scenarios_setting.TEST_ACCOUNTS
    }

    template = Template(LOGIN_TESTCASE_TEMPLATE)
    rendered_code = template.render(render_data)

    ensure_file_clear(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_code.strip())

    print(f"测试用例已生成到 {output_path}")