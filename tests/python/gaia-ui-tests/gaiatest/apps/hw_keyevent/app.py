from marionette_driver import expected, By, Wait
from gaiatest.apps.base import Base

class HardwareKeyboardEvents(Base):

    name = 'test-hw-keyevent' # the testing app'name

    # If the class name is different from the testing app's name,
    # you have to define the manifest_url for yoursrlf, because
    # the default manifest is:
    #   app://lower(YOUR_CLASS_NAME).gaiamobile.org/manifest.webapp
    # the default manifest_url here is:
    #   app://hardwarekeyboardevents.gaiamobile.org/manifest.webapp
    manifest_url = '{}{}.gaiamobile.org/manifest.webapp'.format(Base.DEFAULT_PROTOCOL,name)

    _input_text_locator = (By.ID, 'input')
    _reset_button_locator = (By.ID, 'reset')
    _events_logger_table = (By.ID, 'eventslogger')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

    def launch(self):
        #Base.launch(self, launch_timeout=120000)
        Base.launch(self)

        #Wait(self.marionette).until(expected.element_displayed(
            #Wait(self.marionette).until(expected.element_present(
                #*self._input_text_locator))))

        #Wait(self.marionette).until(expected.element_displayed(
            #Wait(self.marionette).until(expected.element_present(
                #*self._reset_button_locator))))

        Wait(self.marionette).until(expected.element_displayed(
            Wait(self.marionette).until(expected.element_present(
                *self._events_logger_table))))

    def tap_input_text(self):
        input_text = Wait(self.marionette).until(
            expected.element_present(*self._input_text_locator))
        Wait(self.marionette).until(expected.element_displayed(input_text))
        input_text.tap()

    def tap_reset_button(self):
        reset_button = Wait(self.marionette).until(
            expected.element_present(*self._reset_button_locator))
        Wait(self.marionette).until(expected.element_displayed(reset_button))
        reset_button.tap()

    def get_input_text(self):
        return self.marionette.find_element(*self._input_text_locator).get_attribute('value')
