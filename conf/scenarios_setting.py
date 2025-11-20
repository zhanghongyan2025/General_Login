TEST_FIELDS = ['username', 'password']

TEST_SCENARIOS = [
    "success",
    "empty",
    "username_password_not_match",
    "lock_account"
]

TEST_ERROR_MESSAGES = {
    "empty": {
        "username_empty": "请输入您的用户名",
        "password_empty": "请输入您的密码"
    },
    "username_password_not_match": {
        "non_existent_user": "登录用户：test_valid 不存在",
        "wrong_password": "您已输错1次密码，若在24小时内连续输错5次密码，您的账号将被锁定24小时"
    },
    "lock_account": {
        "locked_user": "密码输入错误5次，帐户锁定30分钟"
    }
}

TEST_ACCOUNTS = {
    "non_existent_user": {
        "username": "test_valid",
        "password": "Valid@123"
    },
    "wrong_password": {
        "username": "SDQDXS002013",
        "password": "Valid@123"
    },
    "success": {
        "username": "SDQDXS002013",
        "password": "2vEnxkZu"
    },
    "locked_user": {
        "username": "SDQDXS002013",
        "password": "2vEnxkZu1"
    }
}
