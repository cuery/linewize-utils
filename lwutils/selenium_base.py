from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class SeleniumBase:

    def setup_selenium(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

    def disconnect(self):
        self.driver.quit()

    def get_element(self, id=None, xpath=None, name=None, element=None, css=None, text=None):
        try:
            if id:
                element = self.driver.find_element_by_id(id)
            elif xpath:
                element = self.driver.find_element_by_xpath(xpath)
            elif name:
                element = self.driver.find_element_by_name(name)
            elif css:
                element = self.driver.find_element_by_css_selector(css)
            elif isinstance(text, tuple):
                element = self.find_element_by_text(*text)
            elif text:
                element = self.find_element_by_text(text)
        except NoSuchElementException:
            return None
        return element

    def find_element_by_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None
        return element

    def find_element_by_text(self, text, element="*"):
        return self.find_element_by_xpath("//{}[contains(text(), '{}')]".format(element, text))

    def check_exists_by_id(self, id):
        return self.get_element(id=id)

    def check_exists_by_xpath(self, xpath):
        return self.get_element(xpath=xpath)

    def check_exists_by_link_text(self, text):
        return self.get_element(text=text)

    def clickOptions(self, option):
        self.driver.find_element_by_xpath("//a[contains(text(), 'Actions')]").click()
        self.driver.find_element_by_xpath("//a[contains(text(), '" + option + "')]").click()

    def check_checkbox_selected(self, name):
        return self.driver.find_element_by_name(name).get_attribute("checked")

    def select(self, name):
        if self.driver.find_element_by_name(name).get_attribute("checked"):
            self.driver.find_element_by_name(name).click()

        self.driver.find_element_by_name(name).click()

    def check_selected(self, name):
        return self.driver.find_element_by_name(name).get_attribute(name)

    def setValue(self, name, value):
        self.driver.find_element_by_name(name).clear()
        self.driver.find_element_by_name(name).send_keys(value)

    def set_value(self, element, value):
        element.clear()
        element.send_keys(value)

    def check_form_element_value(self, name, value):
        name = self.driver.find_element_by_name(name)
        assert name.get_attribute("value") == value

    def select_option(self, name=None, id=None, xpath=None, value=None):
        if name:
            self.driver.find_element_by_xpath("//select[@name='" + name + "']/option[contains(text(), '" + value + "')]").click()
        if id:
            self.driver.find_element_by_xpath("//select[@id='" + id + "']/option[contains(text(), '" + value + "')]").click()
        if xpath:
            self.driver.find_element_by_xpath(xpath + "/option[text()='" + value + "']").click()

    def set_choserval(self, id, value):
        select_js = "$(\"#" + id + "\").find(\"option:contains('" + value + "')\").each("\
            "function(){"\
            "if( $(this).text() == '" + value + "' ) {"\
            "$(this).attr(\"selected\",\"selected\");"\
            "}"\
            "});"

        self.driver.execute_script(select_js)
        self.driver.execute_script("$('#" + id + "').trigger('chosen:updated');")

    def check_select_current_value(self, name, value):
        name = self.driver.find_element_by_name(name).get_attribute("value")
        assert name == value

    def check_choserval(self, id, expected_value):
        return self.driver.execute_script("$('#" + id + "').val()")
