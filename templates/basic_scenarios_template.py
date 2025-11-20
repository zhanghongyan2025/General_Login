# # 网约房房东端
# TEST_BASIC_SCENARIOS_TEMPLATE = ["success" ,"empty","username_password_not_match", "invalid_verification_code","lock_account"]
#
# TEST_ERROR_MESSAGES_TEMPLATE  = {
#     "empty": {
#         "username_empty": "请输入您的账号",
#         "password_empty": "请输入您的密码",
#         "verification_code_empty": "请输入您的验证码"
#     },
#     "username_password_not_match": {
#         "non_existent_user": "用户不存在或密码错误",
#         "wrong_password": "用户不存在或密码错误"
#     },
#     "lock_account": {
#         "locked_user": "密码输入错误5次，帐户锁定10分钟"
#     },
#     "invalid_verification_code": {
#         "invalid_verification_code": "请输入验证码"
#     },
# }
#
# TEST_ACCOUNTS_TEMPLATE  = {
#     "non_existent_user": {
#         "username": "test_valid",
#         "password": "Valid@123",
#     },
#     "wrong_password": {
#         "username": "fenghuang_123",
#         "password": "Valid@123",
#     },
#     "success": {
#         "username": "fenghuang_123",
#         "password": "Aa123123!",
#     },
#     "locked_user": {
#         "username": "existing_user_456",
#         "password": "ValidP@ss456&",
#     }
# }

# 射钉器射钉弹流向登记模块
TEST_BASIC_SCENARIOS_TEMPLATE = [ "success","empty","username_password_not_match", "invalid_verification_code","lock_account"]


TEST_ACCOUNTS_TEMPLATE  = {
    "success": {
        "username": "SDQDXS002013",
        "password": "2vEnxkZu",
    },
    "non_existent_user": {
        "username": "test_valid",
        "password": "Valid@123",
    },
    "wrong_password": {
        "username": "SDQDXS002013",
        "password": "Valid@123",
    },
    "locked_user": {
        "username": "SDQDXS002013",
        "password": "2vEnxkZu1",
    }
}


TEST_ERROR_MESSAGES_TEMPLATE  = {
    "empty": {
        "username_empty": "请输入您的用户名",
        "password_empty": "请输入您的密码",
        "verification_code_empty": "请输入您的验证码"
    },
    "username_password_not_match": {
        "non_existent_user": f"登录用户：{TEST_ACCOUNTS_TEMPLATE['non_existent_user']['username']} 不存在",
        "wrong_password": "您已输错1次密码，若连续输错5次密码，您的账号将被锁定30分钟"
    },
    "lock_account": {
        "locked_user": "密码输入错误5次，帐户锁定30分钟"
    },
    "invalid_verification_code": {
        "invalid_verification_code": "请输入验证码"
    }
}


def get_error_message(error_type, sub_type, account_type=None):
    """
    获取替换了账号信息的错误消息

    :param error_type: 错误类型（如"username_password_not_match"）
    :param sub_type: 具体错误子类型（如"non_existent_user"）
    :param account_type: 账号类型（用于获取对应的账号信息）
    :return: 替换后的错误消息
    """
    # 获取原始错误消息模板
    try:
        msg_template = TEST_ERROR_MESSAGES_TEMPLATE[error_type][sub_type]
    except KeyError:
        return f"未找到错误类型: {error_type}.{sub_type}"

    # 如果需要替换账号信息且存在对应账号信息
    if account_type and account_type in TEST_ACCOUNTS_TEMPLATE:
        account_info = TEST_ACCOUNTS_TEMPLATE[account_type]
        # 替换模板中的占位符
        try:
            return msg_template.format(**account_info)
        except KeyError as e:
            return f"错误消息模板中存在未定义的占位符: {e}"

    return msg_template

