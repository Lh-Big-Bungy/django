import os
import json
from bs4 import BeautifulSoup


def parse_html():

 # 读取 HTML 文件
 with open(".\\report.html", "r", encoding="utf-8") as file:

  html_content = file.read()

 # 解析 HTML 内容
 soup = BeautifulSoup(html_content, 'html.parser')

 # 查找并提取内容
 passed_content = soup.find("span", class_="passed").text
 skipped_content = soup.find("span", class_="skipped").text
 failed_content = soup.find("span", class_="failed").text
 error_content = soup.find("span", class_="error").text
 passed_num = int(passed_content.split()[0])
 skipped_num = int(skipped_content.split()[0])
 failed_num = int(failed_content.split()[0])
 error_num = int(error_content.split()[0])
 summary = passed_num + skipped_num + failed_num + error_num
 success_rate = (passed_num / summary) * 100
 preset_rate = int(os.environ.get('preset_rate'))
 stage_type = os.environ.get('stage_type')
 AGILE_PIPELINE_BUILD_ID = os.environ.get('AGILE_PIPELINE_BUILD_ID')
 AGILE_PIPELINE_BUILD_NUMBER = os.environ.get('AGILE_PIPELINE_BUILD_NUMBER')
 link_url = 'https://devops.swhysc.com:9000/osc/fxch_yanfa/new-ipipe/pipelines/8498/history/{}/?versions={}-{}&groupId=&viewId='.format(AGILE_PIPELINE_BUILD_ID, AGILE_PIPELINE_BUILD_NUMBER, AGILE_PIPELINE_BUILD_ID)
 if preset_rate <= success_rate:
  print('测试通过')
  test_result  =  "PASS"
  fail_reason = ''
 else:
  print("测试未通过")
  test_result = "FAIL"
  fail_reason = "用例成功率低于预设值，测试不通过"

 result_json = {}
 result_json['test_tool'] = 'pytest'
 result_json['test_stage'] = stage_type
 result_json['case_count'] = str(summary)
 result_json['success_case'] = str(passed_num)
 result_json['fail_case'] = str(failed_num+error_num)
 result_json['real_rate'] = str(success_rate)
 result_json['preset_success_rate'] = str(preset_rate)
 result_json['test_result'] = test_result
 result_json['link_url'] = link_url
 result_json['fail_reason'] = fail_reason
 cmd2 = "out -k pytest_json -val '{}'".format(
     json.dumps(result_json))  # val值需要用双、单引号引起来，不然会截掉空格之后的部分
 os.system(cmd2)

 print(result_json)
 # 输出结果
 print("用例成功率：{}".format(success_rate))
 print("通过用例数：{}".format(passed_num))
 print("跳过用例数：{}".format(skipped_num))
 print("failed用例数：{}".format(failed_num))
 print("error用例数：{}".format(error_num))

if __name__ == '__main__':
    parse_html()