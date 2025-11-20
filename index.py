# from conf.scenarios_setting import TEST_BASIC_SCENARIOS
from conf.scenarios_setting import TEST_SCENARIOS
from gengrate.generate_target_from_template import generate_testcase
from utils.scenario_utils import generate_scenarios_setting_based_on_fields
from utils.process_utils import process_page_elements_to_loginpage, process_page_elements_to_conf_file


# 使用示例
if __name__ == "__main__":
    target_url = "http://192.168.50.220:8888/sdqdv/#/login?redirect=%2Fsdq%2Fqydj%2F#"  # 可替换为任意目标URL
    process_page_elements_to_conf_file(target_url)
    generate_scenarios_setting_based_on_fields()
    process_page_elements_to_loginpage(target_url)
    generate_testcase(target_url,output_path="test_suits/test_login.py")

