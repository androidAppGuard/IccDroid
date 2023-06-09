import os
import sys
import shutil



def analyzeApk(apkPath, resPath, sdk):
    id=0
    logDir = resPath+"/logs"
    outputDir = resPath+"/output"
    if(not os.path.exists(logDir)): 
        os.makedirs(logDir) 
    if(not os.path.exists(outputDir)): 
        os.makedirs(outputDir) 
        
    if(os.path.exists(apkPath)): 
        apks = os.listdir(apkPath)
        extraArgs = "" #"-noLibCode "# 
        for apk in apks:
            if apk[-4:] ==".apk":
                id+=1
                print ("\n\n\nThis is the "+str(id)+"th app " +apk)
                resFile = logDir+"/"+apk[:-4]+".txt"
                if(not os.path.exists(resFile)): 
                    print("java -jar "+jarFile+"  -path "+ apkPath +" -name "+apk+" -androidJar "+ sdk +"/platforms  "+ extraArgs +" -time 30 -maxPathNumber 100 -client MainClient  -outputDir "+outputDir+" >> "+logDir+"/"+apk[:-4]+".txt")
                    os.system("java -jar "+jarFile+"  -path "+ apkPath +" -name "+apk+" -androidJar "+ sdk +"/platforms "+ extraArgs +" -time 30 -maxPathNumber 100 -client MainClient -outputDir "+outputDir+" >> "+logDir+"/"+apk[:-4]+".txt")


if __name__ == '__main__' :
    apkPath = "C:/Users/engyhui/Desktop/IccResults/apk" #sys.argv[1]
    resPath = "C:/Users/engyhui/Desktop/IccResults/static" #sys.argv[2]
    jarFile = "C:/Users/engyhui/Desktop/IccResults/ICCBot.jar"

    if not os.path.exists(jarFile):
        print("ICCBot.jar not found! Please run \"scripts/mvn.py\" to build ICCBot first!")

    sdk = "C:/Users/engyhui/AppData/Local/Android/Sdk"    
    analyzeApk(apkPath, resPath, sdk)
