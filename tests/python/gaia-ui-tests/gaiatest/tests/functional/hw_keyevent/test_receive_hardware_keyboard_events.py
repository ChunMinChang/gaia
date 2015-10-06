from gaiatest import GaiaTestCase
from gaiatest.apps.hw_keyevent.app import HardwareKeyboardEvents
from gaiatest.apps.hw_keyevent.DeviceEvent import deviceEventInputer

class TestReceiveHardwareKeyboardEvents(GaiaTestCase):

    def test_receive_hardware_keyboard_events(self):

        def addEventListeners():
            self.marionette.execute_script("""
                window.wrappedJSObject.inputResults = [];
                function keyEvtHandler(evt) {
                    window.wrappedJSObject.inputResults.push( evt.type + ':' + evt.key);
                }
                window.addEventListener('keydown', keyEvtHandler);
                window.addEventListener('keypress', keyEvtHandler);
                window.addEventListener('keyup', keyEvtHandler);
            """)

        def getResultsOfEventListeners():
            return self.marionette.execute_script("""
              return window.wrappedJSObject.inputResults;
            """)

        # default language: zh-Hans-Pinyin
        def enableIME(language=u'\u62fc\u97f3'):
            # Import settings app
            from gaiatest.apps.settings.app import Settings

            # Open settings app
            settings = Settings(self.marionette)
            settings.launch()

            # Tap Keyboard setting
            keyboard_settings = settings.open_keyboard()

            # Tap 'add more keyboards' button
            add_more_keyboards = keyboard_settings.tap_add_more_keyboards()

            # Select keyboard language, then click back to make it "stick"
            add_more_keyboards.select_language(language)
            add_more_keyboards.go_back()

            keyboard_settings.wait_for_built_in_keyboard(language)

        def deactivateIME():
            # Save the testing app's frame
            currentFrame = self.marionette.get_active_frame()

            # Import system app
            from gaiatest.apps.system.app import System
            system = System(self.marionette)

            # Switch to system app's frame
            self.marionette.switch_to_frame()

            # Deactivate keyboard app
            self.marionette.execute_script("""
              window.wrappedJSObject.inputWindowManager.hideInputWindowImmediately();
            """)

            # Switch back to testing app's frame
            self.marionette.switch_to_frame(currentFrame)

        def sendKeysWhenIMEIsInactive():
            print 'case 1: Send keys when IME is inactive'
            # Deactivate IME
            deactivateIME()

            # Simulate hardware keyboard events
            keys = ['\\', 'o', '/', ' ', 'h', 'e', 'l', 'l', 'o', ',', '[', '3', '-', '2', '=', '1', ']', '.']
            kbevt = deviceEventInputer.KeyboardEvents(keys)
            # for red-tai reference device: kbevt = deviceEventInputer.KeyboardEvents(keys, devieName = 'keypad')
            kbevt.sendEvent()

            # Expected result
            print '==> expected result: ' + ''.join(keys)

            # Get the result of input text
            print '==> Results of input text: ' + self.hw_kb_evt.get_input_text()

            # Check whether or not the output is same as expectation
            self.assertEqual(self.hw_kb_evt.get_input_text(), ''.join(keys))

        def IMEConsumeSendedKeys():
            print 'case 2: Send Keys when IME is active, and IME will consume these keys'
            # Reset
            self.hw_kb_evt.tap_reset_button()

            # Switch to keyboard frame and switch input-method
            self.kbApp.keyboard.switch_to_keyboard()
            self.kbApp.keyboard.tap_keyboard_language_key()

            # Check input-method
            self.assertEqual(self.kbApp.current_keyboard, 'zh-Hans-Pinyin')

            # Get expected result: Send keys via IME and get its result
            keys = ['t', 'a', 'i', 'w', 'a', 'n', 'd', 'u', 'l', 'i']
            self.kbApp.send(''.join(keys))
            self.kbApp.tap_enter()
            expectedResult = self.hw_kb_evt.get_input_text()

            # Clear the value in input text
            self.hw_kb_evt.tap_reset_button()

            # Simulate hardware keyboard events
            keys.append('ENTER');# append Enter to keys
            kbevt = deviceEventInputer.KeyboardEvents(keys)
            # for red-tai reference device: kbevt = deviceEventInputer.KeyboardEvents(keys, devieName = 'keypad')
            kbevt.sendEvent()

            # Expected result
            print '==> expected result: ' + expectedResult

            # Get the result of input text
            print '==> Results of input text: ' + self.hw_kb_evt.get_input_text()

            # Check whether or not the output is same as expectation
            # self.assertEqual(self.hw_kb_evt.get_input_text(), expectedResult)
            # ********** Un-commented the above line to test bug 1110030 **********

        def IMEIgnoreSendedKeys():
            print 'case 3: Send Keys when IME is active, but IME won\'t consume these keys'
            # Reset
            self.hw_kb_evt.tap_reset_button()

            # Add event listener
            addEventListeners()

            # Simulate hardware keyboard events
            keys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']
            kbevt = deviceEventInputer.KeyboardEvents(keys)
            kbevt.sendEvent()

            expectedResult = []
            for key in keys:
                for evt in ['keydown', 'keypress', 'keyup']:
                    expectedResult.append(unicode(evt + ':' +key, "utf-8"))

            # Expected result
            print '==> expected result: ' + ','.join(expectedResult)

            # Get the results of event listeners
            print '==> Results of input text: ' + ','.join(getResultsOfEventListeners())

            # Check whether or not the output is same as expectation
            self.assertEqual(expectedResult, getResultsOfEventListeners())

        def init():
            # enable IME
            enableIME()

            # Launch the testing app
            self.hw_kb_evt = HardwareKeyboardEvents(self.marionette)
            self.hw_kb_evt.launch()
            self.kbApp = self.hw_kb_evt.keyboard

        # Initialize this test
        init()

        # case 1: Send keys when IME is inactive
        sendKeysWhenIMEIsInactive()

        # case 2: Send Keys when IME is active, and IME will consume these keys
        IMEConsumeSendedKeys()

        # case 3: Send Keys when IME is active, but IME won't consume these keys
        # e.g. non-pritable keys
        IMEIgnoreSendedKeys()
