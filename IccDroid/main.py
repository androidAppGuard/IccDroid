import os

from configure import Configuration
from exploration import IccDroid
from staticAnalysis import StaticAnalysis
from util.util import Util

if __name__ == '__main__':

    apk_dir = r'F:\apk_all_uiexploration'
    for apk_name in os.listdir(apk_dir):
        if apk_name.endswith(".apk"):
            apk_path = os.path.join(apk_dir,apk_name)
            staticAanlysis = StaticAnalysis(apk_path,
                                            sdk_platform=r'E:\LearningSoft\SoftPackbag\Android\SDK\platforms',
                                            iccBot_path=r'.\tool\ICCBot.jar')
            icc_result = staticAanlysis.analyzeIccCallGraph()
            autoSQDroid = IccDroid(apk_path, icc_result)
            autoSQDroid.exploration()

