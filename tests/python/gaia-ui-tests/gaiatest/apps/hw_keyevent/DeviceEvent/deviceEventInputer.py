import mozdevice    # to simulate hardware event
import re           # to parse string

# Define constants
#   Ported from https://github.com/torvalds/linux/blob/master/include/uapi/linux/input.h
# ==================================================
class EventType:
    EV_SYN = 0x00
    EV_KEY = 0x01
    EV_REL = 0x02
    EV_ABS = 0x03
    EV_MSC = 0x04
    EV_SW  = 0x05
    EV_LED = 0x11
    EV_SND = 0x12
    EV_REP = 0x14
    EV_FF = 0x15
    EV_PWR = 0x16
    EV_FF_STATUS = 0x17
    EV_MAX = 0x1f
    EV_CNT = EV_MAX + 1

class SynchronizationEvent:
    SYN_REPORT = 0
    SYN_CONFIG = 1
    SYN_MT_REPORT = 2
    SYN_DROPPED = 3
    SYN_MAX = 0xf
    SYN_CNT = SYN_MAX + 1

class KeysAndButtons:
    # Abbreviations in the comments:
    #   AC - Application Control
    #   AL - Application Launch Button
    #   SC - System Control
    KEY_RESERVED = 0
    KEY_ESC = 1
    KEY_1 = 2
    KEY_2 = 3
    KEY_3 = 4
    KEY_4 = 5
    KEY_5 = 6
    KEY_6 = 7
    KEY_7 = 8
    KEY_8 = 9
    KEY_9 = 10
    KEY_0 = 11
    KEY_MINUS = 12
    KEY_EQUAL = 13
    KEY_BACKSPACE = 14
    KEY_TAB = 15
    KEY_Q = 16
    KEY_W = 17
    KEY_E = 18
    KEY_R = 19
    KEY_T = 20
    KEY_Y = 21
    KEY_U = 22
    KEY_I = 23
    KEY_O = 24
    KEY_P = 25
    KEY_LEFTBRACE = 26
    KEY_RIGHTBRACE = 27
    KEY_ENTER = 28
    KEY_LEFTCTRL = 29
    KEY_A = 30
    KEY_S = 31
    KEY_D = 32
    KEY_F = 33
    KEY_G = 34
    KEY_H = 35
    KEY_J = 36
    KEY_K = 37
    KEY_L = 38
    KEY_SEMICOLON = 39
    KEY_APOSTROPHE = 40
    KEY_GRAVE = 41
    KEY_LEFTSHIFT = 42
    KEY_BACKSLASH = 43
    KEY_Z = 44
    KEY_X = 45
    KEY_C = 46
    KEY_V = 47
    KEY_B = 48
    KEY_N = 49
    KEY_M = 50
    KEY_COMMA = 51
    KEY_DOT	= 52
    KEY_SLASH = 53
    KEY_RIGHTSHIFT = 54
    KEY_KPASTERISK = 55
    KEY_LEFTALT = 56
    KEY_SPACE = 57
    KEY_CAPSLOCK = 58
    KEY_F1 = 59
    KEY_F2 = 60
    KEY_F3 = 61
    KEY_F4 = 62
    KEY_F5 = 63
    KEY_F6 = 64
    KEY_F7 = 65
    KEY_F8 = 66
    KEY_F9 = 67
    KEY_F10 = 68
    KEY_NUMLOCK	= 69
    KEY_SCROLLLOCK = 70
    KEY_KP7 = 71
    KEY_KP8	= 72
    KEY_KP9 = 73
    KEY_KPMINUS	= 74
    KEY_KP4 = 75
    KEY_KP5	= 76
    KEY_KP6	= 77
    KEY_KPPLUS = 78
    KEY_KP1 = 79
    KEY_KP2	= 80
    KEY_KP3	= 81
    KEY_KP0	= 82
    KEY_KPDOT = 83

    KEY_ZENKAKUHANKAKU = 85
    KEY_102ND = 86
    KEY_F11 = 87
    KEY_F12 = 88
    KEY_RO = 89
    KEY_KATAKANA = 90
    KEY_HIRAGANA = 91
    KEY_HENKAN = 92
    KEY_KATAKANAHIRAGANA = 93
    KEY_MUHENKAN = 94
    KEY_KPJPCOMMA = 95
    KEY_KPENTER = 96
    KEY_RIGHTCTRL = 97
    KEY_KPSLASH = 98
    KEY_SYSRQ = 99
    KEY_RIGHTALT = 100
    KEY_LINEFEED = 101
    KEY_HOME = 102
    KEY_UP = 103
    KEY_PAGEUP = 104
    KEY_LEFT = 105
    KEY_RIGHT = 106
    KEY_END = 107
    KEY_DOWN = 108
    KEY_PAGEDOWN = 109
    KEY_INSERT = 110
    KEY_DELETE = 111
    KEY_MACRO = 112
    KEY_MUTE = 113
    KEY_VOLUMEDOWN = 114
    KEY_VOLUMEUP = 115
    KEY_POWER = 116	# SC System Power Down
    KEY_KPEQUAL	= 117
    KEY_KPPLUSMINUS = 118
    KEY_PAUSE = 119
    KEY_SCALE = 120	# AL Compiz Scale (Expose)

    KEY_KPCOMMA = 121
    KEY_HANGEUL = 122
    KEY_HANGUEL = KEY_HANGEUL
    KEY_HANJA = 123
    KEY_YEN = 124
    KEY_LEFTMETA = 125
    KEY_RIGHTMETA = 126
    KEY_COMPOSE = 127

    KEY_STOP = 128 # AC Stop
    KEY_AGAIN = 129
    KEY_PROPS = 130	# AC Properties
    KEY_UNDO = 131 # AC Undo
    KEY_FRONT = 132
    KEY_COPY = 133 # AC Copy
    KEY_OPEN = 134 # AC Open
    KEY_PASTE = 135	# AC Paste
    KEY_FIND = 136 # AC Search
    KEY_CUT = 137 # AC Cut
    KEY_HELP = 138 # AL Integrated Help Center
    KEY_MENU = 139 # Menu (show menu)
    KEY_CALC = 140 # AL Calculator
    KEY_SETUP = 141
    KEY_SLEEP = 142	# SC System Sleep
    KEY_WAKEUP = 143 # System Wake Up
    KEY_FILE = 144 # AL Local Machine Browser
    KEY_SENDFILE = 145
    KEY_DELETEFILE = 146
    KEY_XFER = 147
    KEY_PROG1 = 148
    KEY_PROG2 = 149
    KEY_WWW	= 150 # AL Internet Browser
    KEY_MSDOS = 151
    KEY_COFFEE = 152 # AL Terminal Lock/Screensaver
    KEY_SCREENLOCK = KEY_COFFEE
    KEY_ROTATE_DISPLAY = 153 # Display orientation for e.g. tablets
    KEY_DIRECTION = KEY_ROTATE_DISPLAY
    KEY_CYCLEWINDOWS = 154
    KEY_MAIL = 155
    KEY_BOOKMARKS = 156	# AC Bookmarks
    KEY_COMPUTER = 157
    KEY_BACK = 158 # AC Back
    KEY_FORWARD = 159 # AC Forward
    KEY_CLOSECD = 160
    KEY_EJECTCD	= 161
    KEY_EJECTCLOSECD = 162
    KEY_NEXTSONG = 163
    KEY_PLAYPAUSE = 164
    KEY_PREVIOUSSONG = 165
    KEY_STOPCD = 166
    KEY_RECORD = 167
    KEY_REWIND = 168
    KEY_PHONE = 169 # Media Select Telephone
    KEY_ISO = 170
    KEY_CONFIG = 171 # AL Consumer Control Configuration
    KEY_HOMEPAGE = 172 # AC Home
    KEY_REFRESH = 173 # AC Refresh
    KEY_EXIT = 174 # AC Exit
    KEY_MOVE = 175
    KEY_EDIT = 176
    KEY_SCROLLUP = 177
    KEY_SCROLLDOWN = 178
    KEY_KPLEFTPAREN	= 179
    KEY_KPRIGHTPAREN = 180
    KEY_NEW	= 181 # AC New
    KEY_REDO = 182 # AC Redo/Repeat

class KeyValue:
    UP = 0
    DOWN = 1

KEYS_MAP = {
    '1': KeysAndButtons.KEY_1,
    '2': KeysAndButtons.KEY_2,
    '3': KeysAndButtons.KEY_3,
    '4': KeysAndButtons.KEY_4,
    '5': KeysAndButtons.KEY_5,
    '6': KeysAndButtons.KEY_6,
    '7': KeysAndButtons.KEY_7,
    '8': KeysAndButtons.KEY_8,
    '9': KeysAndButtons.KEY_9,
    '0': KeysAndButtons.KEY_0,
    '-': KeysAndButtons.KEY_MINUS,
    '=': KeysAndButtons.KEY_EQUAL,
    'BACKSPACE': KeysAndButtons.KEY_BACKSPACE,
    # '': KeysAndButtons.KEY_TAB,
    '[': KeysAndButtons.KEY_LEFTBRACE,
    ']': KeysAndButtons.KEY_RIGHTBRACE,
    'ENTER': KeysAndButtons.KEY_ENTER,
    # '': KeysAndButtons.KEY_LEFTCTRL,
    ';': KeysAndButtons.KEY_SEMICOLON,
    '\'': KeysAndButtons.KEY_APOSTROPHE,
    # '': KeysAndButtons.KEY_GRAVE,
    # '': KeysAndButtons.KEY_LEFTSHIFT,
    '\\': KeysAndButtons.KEY_BACKSLASH,
    ',': KeysAndButtons.KEY_COMMA,
    '.': KeysAndButtons.KEY_DOT,
    '/': KeysAndButtons.KEY_SLASH,
    # '': KeysAndButtons.KEY_RIGHTSHIFT,
    # '': KeysAndButtons.KEY_KPASTERISK,
    # '': KeysAndButtons.KEY_LEFTALT,
    ' ': KeysAndButtons.KEY_SPACE,
    # '': KeysAndButtons.KEY_CAPSLOCK,
    # '': KeysAndButtons.KEY_NUMLOCK,
    # '': KeysAndButtons.KEY_SCROLLLOCK,
    'ArrowUp': KeysAndButtons.KEY_UP,
    'ArrowLeft': KeysAndButtons.KEY_LEFT,
    'ArrowRight': KeysAndButtons.KEY_RIGHT,
    'ArrowDown': KeysAndButtons.KEY_DOWN,
}
KEYS_MAP.update(dict.fromkeys(['a', 'A'], KeysAndButtons.KEY_A))
KEYS_MAP.update(dict.fromkeys(['b', 'B'], KeysAndButtons.KEY_B))
KEYS_MAP.update(dict.fromkeys(['c', 'C'], KeysAndButtons.KEY_C))
KEYS_MAP.update(dict.fromkeys(['d', 'D'], KeysAndButtons.KEY_D))
KEYS_MAP.update(dict.fromkeys(['e', 'E'], KeysAndButtons.KEY_E))
KEYS_MAP.update(dict.fromkeys(['f', 'F'], KeysAndButtons.KEY_F))
KEYS_MAP.update(dict.fromkeys(['g', 'G'], KeysAndButtons.KEY_G))
KEYS_MAP.update(dict.fromkeys(['h', 'H'], KeysAndButtons.KEY_H))
KEYS_MAP.update(dict.fromkeys(['i', 'I'], KeysAndButtons.KEY_I))
KEYS_MAP.update(dict.fromkeys(['j', 'J'], KeysAndButtons.KEY_J))
KEYS_MAP.update(dict.fromkeys(['k', 'K'], KeysAndButtons.KEY_K))
KEYS_MAP.update(dict.fromkeys(['l', 'L'], KeysAndButtons.KEY_L))
KEYS_MAP.update(dict.fromkeys(['m', 'M'], KeysAndButtons.KEY_M))
KEYS_MAP.update(dict.fromkeys(['n', 'N'], KeysAndButtons.KEY_N))
KEYS_MAP.update(dict.fromkeys(['o', 'O'], KeysAndButtons.KEY_O))
KEYS_MAP.update(dict.fromkeys(['p', 'P'], KeysAndButtons.KEY_P))
KEYS_MAP.update(dict.fromkeys(['q', 'Q'], KeysAndButtons.KEY_Q))
KEYS_MAP.update(dict.fromkeys(['r', 'R'], KeysAndButtons.KEY_R))
KEYS_MAP.update(dict.fromkeys(['s', 'S'], KeysAndButtons.KEY_S))
KEYS_MAP.update(dict.fromkeys(['t', 'T'], KeysAndButtons.KEY_T))
KEYS_MAP.update(dict.fromkeys(['u', 'U'], KeysAndButtons.KEY_U))
KEYS_MAP.update(dict.fromkeys(['v', 'V'], KeysAndButtons.KEY_V))
KEYS_MAP.update(dict.fromkeys(['w', 'W'], KeysAndButtons.KEY_W))
KEYS_MAP.update(dict.fromkeys(['x', 'X'], KeysAndButtons.KEY_X))
KEYS_MAP.update(dict.fromkeys(['y', 'Y'], KeysAndButtons.KEY_Y))
KEYS_MAP.update(dict.fromkeys(['z', 'Z'], KeysAndButtons.KEY_Z))


# Modules for simulating hardware events
# ==================================================
class InputDevices:

    def __init__(self):
        self.dmADB = mozdevice.DeviceManagerADB()
        self.devices = self.getDeviceEvents()

    def getDeviceEvents(self):
        devices = dict()

        # Get output string of input devices
        devInputPath = '/proc/bus/input/devices'
        cmdlist = ['grep', '-E', '\'Name|event\'', devInputPath]
        res = self.dmADB.shellCheckOutput(cmdlist)

        # parse output into a name-event map
        if res != '':
            elementIter = iter(res.split('\n'))
            for ele in elementIter:
                #name = re.search('Name="(.+?)"', ele).group(1)
                #event = re.search('event(.+?)', next(elementIter)).group(1)
                nameMatch = re.search('Name="(.+?)"', ele)
                eventMatch = re.search('event(.+?)', next(elementIter))
                if nameMatch and eventMatch:
                    name = nameMatch.group(1)
                    event = eventMatch.group(1)
                    devices[name] = event

        return devices

    def getDevicesByContainingName(self, name):
        return  [(key, value) for (key, value) in self.devices.iteritems() if name in key]


class InputEvent:

    def __init__(self, devicePort, eventType, code, value):
        self.device = int(devicePort)
        self.type = int(eventType)
        self.code = int(code)
        self.value = int(value)

    def toSendEvtCmdList(self):
        return ['sendevent', 'dev/input/event' + str(self.device), str(self.type), str(self.code), str(self.value)]


class KeyboardEvents:

    def __init__(self, keys = [], devieName = 'qwerty'):
        self.keys = keys
        self.devieName = devieName
        self.dmADB = mozdevice.DeviceManagerADB()

    def getDevicePort(self):
        inDev = InputDevices()
        keyboardPorts = inDev.getDevicesByContainingName(self.devieName)
        return keyboardPorts[0][1] # return the first matching item's port

    def sendEvent(self):
        devPort = self.getDevicePort()
        for i in self.keys:
            # keydown
            keydown = InputEvent(devPort, EventType.EV_KEY, KEYS_MAP[i], KeyValue.DOWN)
            keydownEvent = keydown.toSendEvtCmdList()
            # sync report
            syn = InputEvent(devPort, EventType.EV_SYN, SynchronizationEvent.SYN_REPORT, 0)
            synEvent = syn.toSendEvtCmdList()
            # keyup
            keyup = InputEvent(devPort, EventType.EV_KEY, KEYS_MAP[i], KeyValue.UP)
            keyupEvent = keyup.toSendEvtCmdList()

            cmdList = keydownEvent + [';'] + synEvent + [';'] + keyupEvent + [';'] + synEvent
            # print cmdList
            self.dmADB.shellCheckOutput(cmdList)
