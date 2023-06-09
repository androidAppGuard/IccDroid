# IccDroid Prototype
IccDroid is an automated testing tool based on reinforcement learning to find ICC-related bugs in Android apps. IccDroid leverages hybrid analysis to build a more complete ICC call graph. Based on this graph, IccDroid further designs an ICC-guided exploration strategy based on Q-learning to improve the testing effectiveness in bug finding. So far, IccDroid has found 13 previously unknown ICC-related bugs, all of which have been confirmed by the app developers and five have already been fixed.

# Update
All the source code of IccDroid is also publicly available for facilitating the development of automated testing. 

# Getting Started
## Virtual Machine Requirements
* Python: 3.6
* Android SDK: API 23 (make sure adb and aapt commands are available)
* Linux: Ubantu 16.04
* [UiAutomator2](https://github.com/openatx/uiautomator2): 2.16.3 (pip install uiautomator2== 2.16.3)
## Android Emulator (AVD) Requirements
* System images: Android 7.0 x86_64 (Marshmallow)
* RAM: 2048M
* SD card: 512M

The above version of the software has been tested in our experiment and can run successfully. In addition, please start the emulator before running IccDroid (you can see this [link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to creating and using [avdmanager](https://developer.android.com/studio/command-line/avdmanager)). 

<!-- ## Subject Requirements([video tutorial](https://1drv.ms/u/s!AhrQLCaSmZgwamuImvbWUv_1pek?e=fiWDdt))
IccDroid can test both on open-source and closed-source apps:
* Closed-source apps: the users can directly run “python main.py apk_path” to test the apk.
* Open-source apps: If users want to obtain code coverage and dataflow information, the app under test should be instrumented with [plugins/Jacoco](https://github.com/androidAppGuard/IccDroid/tree/main/plugins/jacoco) and [plugins/dataflow/DataFlowAnalysis.java](https://github.com/androidAppGuard/IccDroid/tree/main/plugins/dataflow) files first, and built as an apk file. Then users can run “python main.py apk_path” to test the apk (the detailed process is in the [video tutorial](https://1drv.ms/u/s!AhrQLCaSmZgwamuImvbWUv_1pek?e=fiWDdt)).  -->

## Settings
Before running IccDroid, please update the [configure.py](https://github.com/androidAppGuard/IccDroid/blob/main/IccDroid/configure.py) as follows:
```python
  # Dataflow Server info
  SERVER_HOST = "127.0.0.1"
  SERVER_PORT = 9999

  # Device info
  DEVICE_ID = "emulator-5554"
  DEVICE_SCREEN_HEIGHT = 1920
  DEVICE_SCREEN_WIDTH = 1020

  # Time Setting(s)
  STAGE_ONE_TIME = 3600 # (Graph Enhancement Exploration time)
  STAGE_TWO_TIME = 3600 # (ICC-Guided Exploration time)

```
Other configuration information of the configure.py can be selected according to user customization or default configuration.

## Running
For applications that require permission or login, you should install apk on the emulator and grant the permissions or login the account begore testing. Then you start IccDroid by:
```shell
  # enter workspace of IccDroid
  cd /opt/IccDroid 
  # start testing
  python main.py apk_path
```
## Output
The output contents are placed in folder ``<apk_dir>/<apk_name>`` and contain coverage and log directory:
* coverage -- These files in the folder are used to calculate the final code coverage. (code coverage is recorded every 2 seconds)

* log -- The folder contains two types of files:
	* crash_event_X: record the event sequence triggered the ``crash X``. 
	* crash_log_X: record the exception stack log of crash ``crash X``.

# Detailed Description
In order to better reproduce IccDroid, we provide the app’s ``Link``, ``Version``, ``Strategy`` and the revealed bugs.
## Target Apps
|APK Name| Executable Lines of Codes| Version|Strategy|GIthub Link|
|---|---|---|---|---|
| PDFViewer | 1108 | v3.0 | Read | <https://github.com/JavaCafe01/PdfViewer/tree/v3.0> |
| Swiftp | 5248 |v2.19 | Tool | <https://github.com/ppareit/swiftp/tree/v2.19> |
| Privacy-friendly-notes | 3330 |v1.0.2 | Read | <https://github.com/SecUSo/privacy-friendly-notes/tree/v1.0.2> |
| Dokuwiki | 5344 |v0.17 | Education | <https://github.com/fabienli/DokuwikiAndroid/tree/v0.17> |
| CatimaLoyalty | 6131 |v1.6.0 | Tool | <https://github.com/CatimaLoyalty/Android/tree/v1.6.0> |
| Aard2 | 6619 |0.40 | Education | <https://github.com/itkach/aard2-android/tree/0.40> |
| Budget-watch | 7430 |v0.21.4 | Finance | <https://github.com/brarcher/budget-watch/tree/v0.21.4> |
| tomdroid | 8076 |master | Finance | <https://github.com/tomboy-notes/tomdroid> |
| AlarmClock | 9092 |3.02.02 | Tool | <https://github.com/yuriykulikov/AlarmClock/tree/3.02.02>  |
| Trackworktime | 10689| v1.1.2 | Finance | <https://github.com/mathisdt/trackworktime/tree/v1.1.2> |
| FairEmail | 18073 |1.200 |Sociality | <https://github.com/M66B/FairEmail/tree/1.200> |
| Vanilla | 18604 |1.1.0 | Music | <https://github.com/vanilla-music/vanilla/tree/1.1.0> |
| Timber | 20238 |v1.6.1 | Sociality | <https://github.com/fabmazz/Timber/tree/v1.6.1>  |
| Materialistic | 21919 |78 | Music | <https://github.com/hidroh/materialistic/tree/78> |
| BetterBatteryStats | master |1.200 | Tool | <https://github.com/asksven/BetterBatteryStats/tree/master> |
| AnyMemo | 23486 |10.11.3 |Music | <https://github.com/helloworld1/AnyMemo/tree/10.11.3> |
| Wikipedia | 29557 | r2.7.50350-r-2021-04-02 | Education | <https://github.com/wikimedia/apps-android-wikipedia/tree/r/2.7.50350-r-2021-04-02> |
| Feeder | 31358 |1.8.30 | Read | <https://gitlab.com/spacecowboy/Feeder/-/tree/1.8.30> |
| Runnerup | 34714 | v2.0.3.0 | Sport | <https://github.com/jonasoreland/runnerup/tree/v2.0.3.0> |
| AmazeFileManager | 34790 |v3.3.2 | Tool | <https://github.com/TeamAmaze/AmazeFileManager/tree/v3.3.2>  |
| APhotoManager | 36606 |v0.8.1.200212 | Tool | <https://github.com/k3b/APhotoManager/tree/v0.8.1.200212> |
| Book-Catalogue | 41638 |v5.2.2 | Education | <https://github.com/eleybourn/Book-Catalogue/tree/v5.2.2> |
| AntennaPod | 47555 | 1.7.1 | Music | <https://github.com/AntennaPod/AntennaPod/tree/1.7.1> |
| SuntimesWidget | 47947 |v0.14.3 | Weather | <https://github.com/forrestguice/SuntimesWidget/tree/v0.14.3>  |
| Anki-Android | 50707 | v2.9alpha24 | Education | <https://github.com/ankidroid/Anki-Android/tree/v2.9alpha24> |
| MyExpenses | 63275 | r398 | Finance | <https://github.com/mtotschnig/MyExpenses/tree/r398> |
| Gadgetbridge | 79798 | 0.46.0 | Reader | <https://codeberg.org/Freeyourgadget/Gadgetbridge/src/tag/0.46.0> |
| K-9 | 93455 | 5.731 | Sociality | <https://github.com/k9mail/k-9/tree/5.731> |

## Revealed Bugs
|APK Name| Issue State | Cause | Details |
|---|---|---|---|
| AmazeFileManager | Confirmed | NullPointerException | <https://github.com/TeamAmaze/AmazeFileManager/issues/3311> |
| AntennaPod | Confirmed | XmlPullParserException | <https://github.com/AntennaPod/AntennaPod/issues/5885> |
| AlarmClock | Fixed | ActivityNotFoundException | <https://github.com/yuriykulikov/AlarmClock/issues/451> |
| Aadr2  | Fixed | NullPointerException | <https://github.com/itkach/aard2-android/issues/90> |
| AnyMemo  | Confirmed | ExpatParserException | <https://github.com/helloworld1/AnyMemo/issues/525> |
| BookCatalogue  | Confirmed | DeadObjectException | <https://github.com/eleybourn/Book-Catalogue/issues/877> |
| BookCatalogue  | Confirmed | NullPointerException | <https://github.com/eleybourn/Book-Catalogue/issues/878> |
| APhotoManager  | Confirmed | RuntimeException | <https://github.com/k3b/APhotoManager/issues/200> |
| Betterbatterystats  | Confirmed | BatteryInfoUnavailableException  | <https://github.com/asksven/BetterBatteryStats/issues/888> |
| CatimaLoyalty | Fixed | IllegalArgumentException | <https://github.com/CatimaLoyalty/Android/issues/881> |
| CatimaLoyalty | Fixed | ActivityNotFoundException | <https://github.com/CatimaLoyalty/Android/issues/880> |
| Runnerup | Confirmed | ConnectionException | <https://github.com/jonasoreland/runnerup/issues/1109> |
| Swiftp | Fixed | ActivityNotFoundException  | <https://github.com/ppareit/swiftp/issues/174> |
| Simpletask | Confirmed | IllegalArgumentException | <https://github.com/mpcjanssen/simpletask-android/issues/1172> |
