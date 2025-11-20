"""项目全局配置"""

# 登录页面URL（核心配置）
LOGIN_PAGE_URL = "https://192.168.20.247:2582/fireworkssmw/#/login?isLogout=true"

# 登录成功后跳转的目标路径（用于验证）
LOGIN_SUCCESS_REDIRECT_PATH = "/dashboard"

# 浏览器配置
BROWSER = {
    "type": "chromium",  # 可选：chromium, firefox, webkit
    "headless": True,    # 无头模式（True：不显示浏览器窗口，False：显示）
    "ignore_https_errors": True  # 忽略HTTPS证书错误（适合内部测试环境）
}

# 超时配置（毫秒）
TIMEOUT = {
    "page_load": 30000,    # 页面加载超时
    "element_wait": 10000  # 元素等待超时
}


# # 测试数据配置（可选：存放通用测试账号）
# TEST_ACCOUNTS = {
#     "valid_user": {
#         "username": "test_valid",
#         "password": "Valid@123",
#         "verification_code": "1234"
#     },
#     "locked_user": {
#         "username": "test_locked",
#         "password": "Any@123",
#         "verification_code": "1234"
#     }
# }