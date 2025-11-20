import json
import re

from templates.basic_scenarios_template import (
    TEST_BASIC_SCENARIOS_TEMPLATE,
    TEST_ERROR_MESSAGES_TEMPLATE,
    TEST_ACCOUNTS_TEMPLATE
)

def generate_scenarios_setting_based_on_fields(
        output_path: str = "conf/scenarios_setting.py"
):
    # 读取现有文件中的TEST_BASIC_FIELDS
    test_basic_fields = []
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('TEST_FIELDS ='):
                    # 提取字段列表（假设格式规范）
                    start = line.find('[')
                    end = line.find(']')
                    if start != -1 and end != -1:
                        fields_str = line[start + 1:end].strip()
                        test_basic_fields = [
                            field.strip().strip("'\"")
                            for field in fields_str.split(',')
                            if field.strip()
                        ]
                    break
    except FileNotFoundError:
        # 文件不存在时默认无verification_code
        pass

    # 复制模板进行修改
    basic_scenarios = TEST_BASIC_SCENARIOS_TEMPLATE.copy()
    error_messages = TEST_ERROR_MESSAGES_TEMPLATE.copy()  # 假设原模板是字典类型
    accounts = TEST_ACCOUNTS_TEMPLATE.copy()  # 假设原模板是字典/列表类型

    # 处理验证码相关配置
    if 'verification_code' not in test_basic_fields:
        # 移除场景中的验证码验证项
        if "invalid_verification_code" in basic_scenarios:
            basic_scenarios.remove("invalid_verification_code")

        # 移除空值校验中的验证码提示
        if "empty" in error_messages:
            error_messages["empty"].pop("verification_code_empty", None)

        # 移除验证码错误配置
        error_messages.pop("invalid_verification_code", None)

    # 准备每个变量的格式化内容（带缩进的JSON格式）
    scenarios_str = f"TEST_SCENARIOS = {json.dumps(basic_scenarios, ensure_ascii=False, indent=4)}"
    error_msg_str = f"TEST_ERROR_MESSAGES = {json.dumps(error_messages, ensure_ascii=False, indent=4)}"
    accounts_str = f"TEST_ACCOUNTS = {json.dumps(accounts, ensure_ascii=False, indent=4)}"

    # 拼接内容，变量之间用一个空行分隔
    content = f"\n{scenarios_str}\n\n{error_msg_str}\n\n{accounts_str}\n"

    # 追加写入文件
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(content)

def extract_lock_info(message):
    """
    从错误消息中提取锁定次数和锁定时间

    参数:
        message (str): 包含锁定信息的错误消息字符串

    返回:
        tuple: (锁定次数, 锁定时间)，如果匹配失败则返回 (None, None)
    """
    # 正则表达式模式：匹配"密码*错误xx次，*锁定*xx分钟"格式
    pattern = r'密码.*?错误(\d+)次，.*?锁定.*?(\d+)分钟'
    match = re.search(pattern, message)

    if match:
        # 提取次数和时间并转换为整数
        lock_count = int(match.group(1))
        lock_time = int(match.group(2))
        return (lock_count, lock_time)
    else:
        return (None, None)
