from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def generate_playwright_locator(html: str) -> str:
    """为单个HTML元素生成最优的Playwright定位器"""
    soup = BeautifulSoup(html.strip(), 'html.parser')
    element = soup.find()
    if not element:
        return "无效的HTML元素"

    tag = element.name
    attrs = element.attrs.copy()

    # 处理class属性（列表转字符串）
    if 'class' in attrs and isinstance(attrs['class'], list):
        attrs['class'] = ' '.join(attrs['class'])

    # 1. ID定位（最高优先级）
    if 'id' in attrs:
        return f'page.locator("{tag}#{attrs["id"]}")  # ID定位'

    # 2. get_by_role()
    role = attrs.get('role')
    if not role:
        # 标签隐式role映射
        role_map = {
            'button': 'button',
            'input': 'textbox' if attrs.get('type') in ['text', '', 'search', 'number', 'email', 'password'] else None,
            'checkbox': 'checkbox',
            'radio': 'radio',
            'select': 'combobox',
            'textarea': 'textbox',
            'a': 'link' if 'href' in attrs else None,
            'h1': 'heading', 'h2': 'heading', 'h3': 'heading',
            'h4': 'heading', 'h5': 'heading', 'h6': 'heading',
            'img': 'img', 'ul': 'list', 'ol': 'list', 'li': 'listitem',
            'dialog': 'dialog', 'nav': 'navigation', 'main': 'main', 'form': 'form'
        }
        role = role_map.get(tag)

    if role:
        # 提取可访问性名称
        name_sources = [
            attrs.get('aria-label'),
            element.text.strip() if element.text.strip() else None,
            attrs.get('placeholder') if tag == 'input' else None,
            attrs.get('title')
        ]
        name = next((src for src in name_sources if src is not None), None)

        if name:
            return f'page.get_by_role("{role}", name="{name}")  # 角色+名称'
        else:
            return f'page.get_by_role("{role}")  # 角色定位'

    # 3. get_by_text()
    text_content = element.text.strip()
    if text_content:
        return f'page.get_by_text("{text_content}")  # 文本内容'

    # 4. get_by_label()（表单控件）
    if tag in ['input', 'select', 'textarea', 'checkbox', 'radio']:
        if 'aria-labelledby' in attrs:
            return f'page.get_by_label("关联元素文本")  # 需替换为id="{attrs["aria-labelledby"]}"的文本'

    # 5. get_by_placeholder()
    if 'placeholder' in attrs:
        return f'page.get_by_placeholder("{attrs["placeholder"]}")  # 占位符'

    # 6. get_by_alt_text()
    if 'alt' in attrs and attrs['alt'].strip():
        return f'page.get_by_alt_text("{attrs["alt"]}")  # 替代文本'

    # 7. get_by_title()
    if 'title' in attrs:
        return f'page.get_by_title("{attrs["title"]}")  # title属性'

    # 8. get_by_test_id()
    test_id_attr = 'data-testid'
    if test_id_attr in attrs:
        return f'page.get_by_test_id("{attrs[test_id_attr]}")  # 测试属性'

    # 最低优先级：标签定位
    return f'page.locator("{tag}")  # 标签定位'

def get_visible_elements(url):
    """获取指定URL中可见的input和button元素的HTML代码列表"""
    with sync_playwright() as p:
        # 启动浏览器并创建上下文（忽略HTTPS错误）
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")  # 等待页面加载完成

            # 执行JS获取可见元素
            visible_htmls = page.evaluate("""
                () => {
                    const elements = [...document.querySelectorAll('input, button')];
                    return elements.filter(el => {
                        const style = getComputedStyle(el);
                        // 过滤可见元素
                        return style.display !== 'none' &&
                               style.visibility !== 'hidden' &&
                               parseFloat(style.opacity) > 0 &&
                               el.offsetParent !== null;
                    }).map(el => el.outerHTML);
                }
            """)
            return visible_htmls

        finally:
            browser.close()

def get_element_variable_name(html: str) -> str:
    """
    根据HTML元素内容确定变量名称：
    - 包含账号/用户名/username/loginname/login_name → username
    - 包含密码/password → password
    - 包含登录（含空格分隔如“登 录”）/sign in/log in/login → login
    - 其他情况 → unknown_element
    """
    # 预处理：移除HTML中的所有空格，统一小写，便于匹配带空格的关键词
    processed_html = html.lower().replace(" ", "")

    # 用户名相关关键词
    username_keywords = ["账号", "用户名", "username", "loginname", "login_name", "userid"]
    # 密码相关关键词
    password_keywords = ["密码", "password"]
    #验证码相关关键词
    verification_code_keywords = ["验证", "校验"]
    # 登录相关关键词（处理带空格的情况，如“登 录”）
    login_keywords = ["登录", "signin", "login", "login"]  # 移除关键词中的空格以便匹配

    # 检查用户名关键词
    if any(keyword in processed_html for keyword in username_keywords):
        return "username"
    # 检查密码关键词
    elif any(keyword in processed_html for keyword in password_keywords):
        return "password"
    # 检查登录关键词（已处理空格情况）
    elif any(keyword in processed_html for keyword in login_keywords):
        return "login"
    elif any(keyword in processed_html for keyword in verification_code_keywords):
        return "verification_code"
    return "unknown_element"