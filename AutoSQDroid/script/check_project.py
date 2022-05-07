import os
import socket
import subprocess
from lxml import html


def check_jacoco(package, classes_path, jacococli_path, output):
    # generate coverage.ec
    subprocess.check_call('adb shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE', shell=True,
                          cwd=output)
    # pull coverage.ec
    subprocess.check_call('adb pull  /data/data/' + package + '/files/coverage.ec ' + output + '\coverage.ec',
                          shell=True)

    # generate jacoco report
    jacoco_cmd = 'java -jar ' + jacococli_path + ' report ' + output + '\coverage.ec --classfiles ' + classes_path + ' --html report'
    subprocess.check_call(jacoco_cmd, shell=True, cwd=output)

    # get instruction coverage
    html_res = html.parse(output + r'/report/index.html')
    coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
    print("coverage: ", coverage_info[2].text, "total lines: ", coverage_info[8].text)


def check_dataflow_info():
    # set socket port forward
    subprocess.check_call("adb -s emulator-5554 forward tcp:9999 tcp:9999", shell=True)
    subprocess.check_call("adb -s emulator-5554 shell am broadcast -a edu.dhu.cs.816space", shell=True)

    client = socket.socket()
    client.connect(("127.0.0.1", 9999))
    client.send("state\n".encode("utf-8"))
    data = client.recv(1024).decode("utf-8").strip()
    print(data)

    client.send("getActivityDataflow\n".encode("utf-8"))
    data = client.recv(1024).decode("utf-8").strip()
    print(data)

    client.send("getFragementDataflow\n".encode("utf-8"))
    data = client.recv(1024).decode("utf-8").strip()
    print(data)

    client.send("exit\n".encode("utf-8"))
    data = client.recv(1024).decode("utf-8").strip()
    print(data)


app_packages = {
    '1': ['batterydog.andbatdog.sf.net.batterydog',
          r'F:\Tmp\AutoSQDroid\target_app\1_Batterydog-Fdroid\app\build\intermediates\classes\debug'],
    '2': ['com.gsnathan.pdfviewer',
          r'F:\Tmp\AutoSQDroid\2_PdfViewer-v3.0\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '3': ['itkach.aard2',
          r'F:\Tmp\AutoSQDroid\3_aard2-0.40\aard2-android\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '4': ['com.better.alarm',
          r'F:\Tmp\AutoSQDroid\4_AlarmClock-3.02.02\app\build\intermediates\javac\developDebug\compileDevelopDebugJavaWithJavac\classes'],
    '5': ['com.android.a47_alogcat',
          r'F:\Tmp\AutoSQDroid\5_alogcat-FDroid\app\build\intermediates\javac\debug\classes'],
    '6': ['com.amaze.filemanager',
          r'F:\Tmp\AutoSQDroid\6_AmazeFileManager-3.3.2\app\build\intermediates\classes\fdroid\debug'],
    '7': ['com.ichi2.anki',
          r'F:\Tmp\AutoSQDroid\7_Anki-Android-v2.9alpha24\AnkiDroid\build\intermediates\classes\debug'],
    '8': ['de.danoeh.antennapod.debug',
          r'F:\Tmp\AutoSQDroid\8_AntennaPod-1.7.1\app\build\intermediates\classes\free\debug'],
    '9': ['org.liberty.android.fantastischmemodev',
          r'F:\Tmp\AutoSQDroid\9_AnyMemo-10.11.3\app\build\intermediates\javac\devApi16Debug\compileDevApi16DebugJavaWithJavac\classes'],
    '10': ['de.k3b.android.androFotoFinder',
           r'F:\Tmp\AutoSQDroid\10_APhotoManager-v0.8.1.200212\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '11': ['com.asksven.betterbatterystats_xdaedition',
           r'F:\Tmp\AutoSQDroid\11_BetterBatteryStats-master\app\build\intermediates\javac\xdaeditionDebug\classes'],
    '12': ['com.eleybourn.bookcatalogue',
           r'F:\Tmp\AutoSQDroid\12_Book-Catalogue-v5.2.2\build\intermediates\classes\debug'],
    '13': ['protect.budgetwatch',
           r'F:\Tmp\AutoSQDroid\13_budget-watch-v0.21.4\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '14': ['me.hackerchick.catima.debug',
           r'F:\Tmp\AutoSQDroid\14_CatimaLoyalty-v1.6.0\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '15': ['org.billthefarmer.currency',
           r'F:\Tmp\AutoSQDroid\15_currency-v1.37\build\intermediates\javac\debug\classes'],
    '16': ['com.fabienli.dokuwiki',
           r'F:\Tmp\AutoSQDroid\16_Dokuwiki-v0.17\app\build\intermediates\javac\debug\classes'],
    '17': ['eu.faircode.email',
           r'F:\Tmp\AutoSQDroid\17_FairEmail-1.200\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '18': ['com.nononsenseapps.feeder.debug',
           r'F:\Tmp\AutoSQDroid\18_Feeder-1.8.30\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '19': ['nodomain.freeyourgadget.gadgetbridge',
           r'F:\Tmp\AutoSQDroid\19_Gadgetbridge-0.46.0\app\build\intermediates\javac\debug\classes'],
    '20': ['com.fsck.k9.debug', r'F:\Tmp\AutoSQDroid\20_k-9_5.731\app\k9mail\build\intermediates\javac\debug\classes'],
    '21': ['io.github.hidroh.materialistic',
           r'F:\Tmp\AutoSQDroid\21_materialistic-78\app\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '22': ['org.totschnig.myexpenses.fortest',
           r'F:\Tmp\AutoSQDroid\22_MyExpenses-r398\myExpenses\build\intermediates\javac\conscriptForTest\classes'],
    '23': ['org.billthefarmer.notes', r'F:\Tmp\AutoSQDroid\23_Notes-v1.10\build\intermediates\javac\debug\classes'],
    '24': ['com.android.a39_passwordmaker',
           r'F:\Tmp\AutoSQDroid\24_passwordmaker-fdroid\app\build\intermediates\javac\debug\classes'],
    '25': ['org.secuso.privacyfriendlynotes',
           r'F:\Tmp\AutoSQDroid\25_privacy-friendly-notes-v1.0.2\app\build\intermediates\javac\debug\classes'],
    '26': ['org.runnerup.debug',
           r'F:\Tmp\AutoSQDroid\26_runnerup-v2.0.3.0\app\build\intermediates\javac\latestDebug\classes'],
    '27': ['org.thoughtcrime.securesms',
           r'F:\Tmp\AutoSQDroid\27_Signal-Android-v5.5.0\app\build\intermediates\javac\playProdDebug\classes'],
    '28': ['com.simplemobiletools.filemanager.pro.debug',
           r'F:\Tmp\AutoSQDroid\28_Simple-File-Manager-v6.9.4\app\build\intermediates\javac\debug\classes'],
    '29': ['nl.mpcjanssen.simpletask.debug',
           r'F:\Tmp\AutoSQDroid\29_simpletask-10.9.0\app\build\intermediates\javac\cloudlessDebug\classes'],
    '30': ['com.forrestguice.suntimeswidget',
           r'F:\Tmp\AutoSQDroid\30_SuntimesWidget-v0.14.3\app\build\intermediates\classes\debug'],
    '31': ['be.ppareit.swiftp_free',
           r'F:\Tmp\AutoSQDroid\31_swiftp-v2.19\app\build\intermediates\javac\fdroid_freeDebug\compileFdroid_freeDebugJavaWithJavac\classes'],
    '32': ['it.fossoft.timberfoss.dev', r'F:\Tmp\AutoSQDroid\32Timber-v1.6.1\app\build\intermediates\classes\debug'],
    '33': ['org.tomdroid',
           r'F:\Tmp\AutoSQDroid\33_tomdroid-fdroid\build\intermediates\javac\debug\compileDebugJavaWithJavac\classes'],
    '34': ['org.zephyrsoft.trackworktime',
           r'F:\Tmp\AutoSQDroid\34_trackworktime-v1.1.2\app\build\intermediates\javac\debug\classes'],
    '35': ['org.isoron.uhabits', r'F:\Tmp\AutoSQDroid\35_uhabits-v1.7.11\app\build\intermediates\classes\debug'],
    '36': ['ch.blinkenlights.android.vanilla',
           r'F:\Tmp\AutoSQDroid\36_vanilla-1.1.0\app\build\intermediates\javac\debug\classes'],
    '37': ['de.freewarepoint.whohasmystuff',
           r'F:\Tmp\AutoSQDroid\37_whohasmystuff-1.0.38\build\intermediates\javac\debug\classes'],
    '38': ['org.wikipedia.alpha',
           r'F:\Tmp\AutoSQDroid\38_wikipedia-r2.7.50350-r-2021-04-02\app\build\intermediates\javac\alphaDebug\classes'],
}
# key_index = '1'
# check_jacoco(package=app_packages[key_index][0], classes_path=app_packages[key_index][1],
#              jacococli_path=r'F:\Tmp\AutoSQDroid\evaluation\AutoSQDroid\tool\jacococli.jar',
#              output='F:\Tmp')
# check_dataflow_info()

# app_path = r'F:\Tmp\AutoSQDroid\11_BetterBatteryStats-master\app\build\outputs\apk\xdaedition\debug\betterbatterystats_xdaedition_debug_2.6.apk'
# subprocess.check_call("aapt dump badging " + app_path + "| findstr package:", shell=True)

# get increase coverage info

def get_increase_coverage(jacococli_path, classes_path, coverage_dir):
    files = os.listdir(coverage_dir)
    merge_dest_file = None
    for i in range(0, len(files)):
        file_path = os.path.join(coverage_dir, files[i])
        if i == 0:
            jacoco_cmd = 'java -jar ' + jacococli_path + ' report ' + file_path + ' --classfiles ' + classes_path + ' --html report'
            subprocess.check_call(jacoco_cmd, shell=True, cwd=coverage_dir)
            # # get instruction coverage
            html_res = html.parse(coverage_dir + r'/report/index.html')
            coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
            print("coverage: ", coverage_info[2].text, "total lines: ", coverage_info[8].text)
        else:
            if i == 1:
                file_last_path = os.path.join(coverage_dir, files[i - 1])
            else:
                file_last_path = merge_dest_file
            # merge
            merge_dest_file = os.path.join(coverage_dir, 'coverage_' + str(i - 1) + '-' + str(i) + '.ec')
            merge_cmd = 'java -jar ' + jacococli_path + ' merge ' + file_path + ' ' + file_last_path + ' --destfile ' + merge_dest_file
            subprocess.check_call(merge_cmd, shell=True, cwd=coverage_dir)
            # jacoco report
            jacoco_cmd = 'java -jar ' + jacococli_path + ' report ' + merge_dest_file + ' --classfiles ' + classes_path + ' --html report'
            subprocess.check_call(jacoco_cmd, shell=True, cwd=coverage_dir)
            # # get instruction coverage
            html_res = html.parse(coverage_dir + r'/report/index.html')
            coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
            print("coverage: ", coverage_info[2].text, "total lines: ", coverage_info[8].text)


key_index = '1'
package = app_packages[key_index][0]
jacococli_path = r'F:\Tmp\AutoSQDroid\evaluation\AutoSQDroid\tool\jacococli.jar'
classes_path = app_packages[key_index][1]
coverage_dir = r'F:\Tmp\AutoSQDroid\evaluation\AutoSQDroid\tool\1_Batterydog-Fdroid\coverage'
# generate jacoco report
get_increase_coverage(jacococli_path,classes_path,coverage_dir)