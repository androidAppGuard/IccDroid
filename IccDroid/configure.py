class Configuration(object):
    # Server info
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 9999

    # Device info
    DEVICE_ID = "emulator-5554"
    DEVICE_SCREEN_HEIGHT = 1920
    DEVICE_SCREEN_WIDTH = 1020
    DEVICE_PACKAGE = ['com.android.packageinstaller',
                      'com.android.camera',]
                      # 'com.android.gallery',  # photos
                      # 'com.google.android.gms',  # contacts
                      # 'com.android.documentsui',  # download
                      # 'com.android.settings']

    # Action type ui action
    ACTION_TYPE_CLICK = 0X0001
    ACTION_TYPE_LONGCLICK = 0X0002
    ACTION_TYPE_EDIT = 0X0003
    # system action
    SYSTEM_ACTION_PROBABILITY = 0.05
    ACTION_TYPE_SCROLL = 0X0100
    ACTION_TYPE_BACK = 0X0200
    ACTION_TYPE_RESTART = 0X0300
    SYSTEM_ACTIONS = [
        ACTION_TYPE_SCROLL,
        ACTION_TYPE_BACK,
        ACTION_TYPE_RESTART
    ]

    # Q-table
    Q_TABLE_INITVALUE = 500.0
    Q_TABLE_LEARNING_RATE = 0.9
    Q_TABLE_GAMMY = 0.9

    STAGE_ONE_TIME = 7200
    STAGE_TWO_TIME = 3600

    SOCKET_FLAG = False
