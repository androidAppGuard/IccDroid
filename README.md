# AutoSQDroid Prototype
AutoSQDroid is a fully automated version of [SQDroid](https://github.com/androidAppGuard/SQDroid). SQDroid is a semantic-driven testing tool for Android apps via Q-learning, while it needs to manually collect the basic functions of each app to calculate the reward and does not take advantage of the dataflow information of these functions. To resolve the problem, AutoSQDroid can automatically extract the dataflow functions in apps from Q-learning exploration stage and once again utilizes these functions to guide the agent generating the meaningful test cases related to dataflow and discovering the abnormal dataflow behaviors.

# Update
All the source code of AutoSQDroid is also publicly available for facilitating the development of automated testing. Next, we will integrate the dataflow acquisition function into the Android framework.

# Getting Started
## Virtual Machine Requirements
* Python: 3.6
* Android SDK: API 23 (make sure adb and aapt commands are available)
* Linux: Ubantu 16.04
* [UiAutomator2](https://github.com/openatx/uiautomator2): 2.16.3 (pip install uiautomator2== 2.16.3)
## Android Emulator (AVD) Requirements
* System images: Android 6.0 x86_64 (Marshmallow)
* RAM: 2048M
* SD card: 512M

The above version of the software has been tested in our experiment and can run successfully. In addition, please start the emulator before running AutoSQDroid (you can see this [link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to creating and using [avdmanager](https://developer.android.com/studio/command-line/avdmanager)). 

## Subject Requirements([video tutorial](https://1drv.ms/u/s!AhrQLCaSmZgwamuImvbWUv_1pek?e=fiWDdt))
AutoSQDroid can test both on open-source and closed-source apps:
* Closed-source apps: the users can directly run “python main.py apk_path” to test the apk.
* Open-source apps: If users want to obtain code coverage and dataflow information, the app under test should be instrumented with [plugins/Jacoco](https://github.com/androidAppGuard/AutoSQDroid/tree/main/plugins/jacoco) and [plugins/dataflow/DataFlowAnalysis.java](https://github.com/androidAppGuard/AutoSQDroid/tree/main/plugins/dataflow) files first, and built as an apk file. Then users can run “python main.py apk_path” to test the apk (the detailed process is in the [video tutorial](https://1drv.ms/u/s!AhrQLCaSmZgwamuImvbWUv_1pek?e=fiWDdt)). 

## Settings
Before running AutoSQDroid, please update the [configure.py](https://github.com/androidAppGuard/AutoSQDroid/blob/main/AutoSQDroid/configure.py) as follows:
```python
  # Dataflow Server info
  SERVER_HOST = "127.0.0.1"
  SERVER_PORT = 9999

  # Device info
  DEVICE_ID = "emulator-5554"
  DEVICE_SCREEN_HEIGHT = 1920
  DEVICE_SCREEN_WIDTH = 1020

  # Time Setting(s)
  STAGE_ONE_TIME = 3600 # (Q-learning exploration time)
  STAGE_TWO_TIME = 3600 # (Q-learning Inter-Function Exploration time)

```
Other configuration information of the configure.py can be selected according to user customization or default configuration.

## Running
For applications that require permission or login, you should install apk on the emulator and grant the permissions or login the account begore testing. Then you start AutoSQdroid by:
```shell
  # enter workspace of AutoSQDroid
  cd /opt/AutoSQDroid 
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
In order to better reproduce AutoSQDroid, we provide the app’s ``Link``, ``Version``, ``Strategy`` and the revealed bugs.
## Target Apps
|APK Name| Executable Lines of Codes| Version|Strategy|GIthub Link|
|---|---|---|---|---|
| AmazeFileManager | Confirmed | NullPointerException | <https://github.com/TeamAmaze/AmazeFileManager/issues/3311> |
| AntennaPod | Confirmed | XmlPullParserException | <https://github.com/AntennaPod/AntennaPod/issues/5885> |
| Batterydog | Unresponse | ArrayIndexOutOfBoundsException | <https://sourceforge.net/p/andbatdog/discussion/957397/thread/97a9f569f4/> |
| AlarmClock | Unresponse | ActivityNotFoundException | <https://github.com/yuriykulikov/AlarmClock/issues/451> |
| Aadr2  | Confirmed | NullPointerException | <https://github.com/itkach/aard2-android/issues/90> |
| AnyMemo  | Unresponse | ExpatParser$ParseException | <https://github.com/helloworld1/AnyMemo/issues/525> |
| AnyMemo  | Unresponse | StringIndexOutOfBoundsException | <https://github.com/helloworld1/AnyMemo/issues/526> |
| BookCatalogue  | Confirmed | DeadObjectException | <https://github.com/eleybourn/Book-Catalogue/issues/877> |
| BookCatalogue  | Unresponse | NullPointerException | <https://github.com/eleybourn/Book-Catalogue/issues/878> |
| APhotoManager  | Unresponse | RuntimeException | <https://github.com/k3b/APhotoManager/issues/200> |
| Betterbatterystats  | Unresponse | BatteryInfoUnavailableException  | <https://github.com/asksven/BetterBatteryStats/issues/888> |
| Budgetwatch | Unresponse | FileNotFoundException | <https://github.com/brarcher/budget-watch/issues/216> |
| CatimaLoyalty | Fixed | IllegalArgumentException | <https://github.com/CatimaLoyalty/Android/issues/881> |
| CatimaLoyalty | Confirmed | ActivityNotFoundException | <https://github.com/CatimaLoyalty/Android/issues/880> |
| Gadgetbridg | Unresponse | IllegalStateException | <https://codeberg.org/Freeyourgadget/Gadgetbridge/issues/2659> |
| Runnerup | Unresponse | ConnectionException | <https://github.com/jonasoreland/runnerup/issues/1109> |
| SimpleFileManager | Real | NullPointerException | <https://github.com/mick88/filemanager/issues/13> |
| Simpletask | Real | IllegalArgumentException | <https://github.com/mpcjanssen/simpletask-android/issues/1172> |
| Swiftp | Unresponse | ActivityNotFoundException  | <https://github.com/ppareit/swiftp/issues/174> |
