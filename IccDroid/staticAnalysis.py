import os
from util.util import Util



class StaticAnalysis(object):
    def __init__(self, apk_path, sdk_platform, iccBot_path):
        self.apk_path = apk_path
        self.iccBot_path = iccBot_path
        self.out_dir = os.path.dirname(apk_path) + r'/' + os.path.basename(apk_path).split('.')[0]
        if os.path.exists(self.out_dir) == False:
            os.mkdir(self.out_dir)
        self.sdk_platform = sdk_platform

    def analyzeIccCallGraph(self):
        icc_result = None
        apk_dir = os.path.dirname(self.apk_path)
        apk_name = os.path.basename(self.apk_path).split('.')[0]
        if self.apk_path[-4:] == ".apk":
            print("start static analyze: ", apk_name)
            out_path = os.path.join(self.out_dir, 'icc_static')
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            cmd = 'java -jar ' + self.iccBot_path + ' -path ' + apk_dir + ' -name ' + os.path.basename(self.apk_path) + ' -androidJar ' + self.sdk_platform + ' -time 30 -maxPathNumber 100 -client CTGClient -outputDir ' + out_path
            os.system(cmd)

            # read icc results
            icc_result = dict()
            icc_file_path = os.path.join(os.path.join(os.path.join(out_path, apk_name), 'CTGResult'),
                                         apk_name + '_CTG.txt')
            with open(icc_file_path, 'r', encoding='utf-8') as icc_file:
                icc_lines = icc_file.readlines()
                for icc_line in icc_lines:
                    icc_line = icc_line.strip()
                    if '->' in icc_line and len(
                            icc_line.split('->')) == 2 and 'Service' not in icc_line and 'service' not in icc_line:
                        send_component = icc_line.split('->')[0]
                        target_component = icc_line.split('->')[1]
                        key = send_component + "->" + target_component
                        key = key.strip()
                        if key not in icc_result.keys():
                            icc_result.update(
                                {key:1})
                        else:
                            icc_result[key] = icc_result[key] + 1
        return icc_result

# apk_path = r'C:\Users\engyhui\Desktop\IccResults\apk\1_Batterydog.apk'
# sdk_platform = r'C:\Users\engyhui\AppData\Local\Android\Sdk\platforms'
# iccBot_path = r'.\tool\ICCBot.jar'
# staticAanlysis = StaticAnalysis(apk_path,sdk_platform= r'C:\Users\engyhui\AppData\Local\Android\Sdk\platforms',iccBot_path=r'.\tool\ICCBot.jar')
# icc_result = staticAanlysis.analyzeIccCallGraph()
# print(icc_result)

# if (os.path.exists(apk_dir)):
#     apks = os.listdir(apk_dir)
#     for apk_name in apks:
#         if apk_name[-4:] == ".apk":
#             print("start static analyze: ", apk_name)
#             apk_path = os.path.join(apk_dir, apk_name)
#             iccBot_path = r'.\tool\ICCBot.jar'
#             out_path = os.path.join(apk_dir, 'iccout')
#             if not os.path.exists(out_path):
#                 os.makedirs(out_path)
#             cmd = 'java -jar ' + iccBot_path + ' -path ' + apk_dir + ' -name ' + apk_name + ' -androidJar ' + sdk_platform + ' -time 30 -maxPathNumber 100 -client CTGClient -outputDir ' + out_path
#             # os.system(cmd)
#             icc_file_path = os.path.join(os.path.join(os.path.join(out_path, apk_name[:-4]), 'CTGResult'),
#                                          apk_name[:-4] + '_CTG.txt')
#             with open(icc_file_path, 'r', encoding='utf-8') as icc_file:
#                 icc_lines = icc_file.readlines()
#                 for icc_line in icc_lines:
#                     icc_line = icc_line.strip()
#                     if '->' in icc_line and len(icc_line.split('->')) == 2 and 'Service' not in icc_line and 'service' not in icc_line:
#                         send_component = icc_line.split('->')[0]
#                         target_component = icc_line.split('->')[1]
#                         if apk_name[:-4] not in icc_results.keys():
#                             icc_results.update({apk_name[:-4]:dict()})
#                         icc_results[apk_name[:-4]].update({send_component+target_component: [send_component,target_component]})

            # break
    # 有可能有的apk没有分析出ICC/ 不能用flowdroid，应该采用其它或者不需要其它工具
    # 统计apk的ICC相关的ICC代码与ICCbot找到的代码
    # for apk_key in icc_results.keys():
    #     print(apk_key,len(icc_results[apk_key].keys()))
# 读取文件,并转换为graph，用于Q-learning探索
