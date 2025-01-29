import pytest
import pytest_bdd
import time

from selenium.webdriver.support.ui import Select
from pytest_bdd import parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytest_bdd import scenario, given, when, then

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@scenario('features/order.feature', "Placing an order")
def test_order():
    pass

@given('I am on the website http://automationexercise.com')
def open_browser_windows_page(browser):
    browser.get('http://automationexercise.com')
    browser.fullscreen_window()
    time.sleep(1)
    
@when('I add products to the cart')
def add_product(browser):
    browser.find_element(By.XPATH,"//button[@class='fc-button fc-cta-consent fc-primary-button']").click()
    browser.find_element(By.XPATH,"//a[.=' Products']").click()
    browser.fullscreen_window()
    for i in range(1, 6):
        xpath = f"//div[@class='features_items']//div[@class='col-sm-4']//a[@data-product-id='{i}'][1]"
        add = browser.find_element(By.XPATH, xpath)
        add.click()
        time.sleep(1)
        browser.find_element(By.XPATH,"//div[@class='modal-footer']//button").click()
        time.sleep(1)

@when('I create my account')
def create_account(browser):
    browser.find_element(By.XPATH,"//a[contains(.,'Cart')]").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//a[.='Proceed To Checkout']").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//a[.='Register / Login']").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//input[@name='name']").send_keys('Toto')
    browser.find_element(By.XPATH,"//div[@class='signup-form']//input[@name='email']").send_keys('toto15@tutu.fr')
    browser.find_element(By.XPATH,"//button[.='Signup']").click()
    time.sleep(1)
    browser.find_element(By.XPATH, "//label[contains(.,'Mr.')]").click()
    assert browser.find_element(By.ID,"name").get_attribute("value") == "Toto"
    assert browser.find_element(By.ID,"email").get_attribute("value") == "toto15@tutu.fr"
    browser.find_element(By.ID,"password").send_keys('Test01234!')
    select_day = Select(browser.find_element(By.ID, 'days'))
    select_day.select_by_visible_text('10')
    select_month = Select(browser.find_element(By.ID, 'months'))
    select_month.select_by_visible_text('March')
    select_year = Select(browser.find_element(By.ID, 'years'))
    select_year.select_by_visible_text('2009')
    browser.find_element(By.ID,"first_name").send_keys('Toto')
    browser.find_element(By.ID,"last_name").send_keys('Toto')
    browser.find_element(By.ID,"address1").send_keys('adresse')
    select_country = Select(browser.find_element(By.ID, 'country'))
    select_country.select_by_visible_text('Australia')
    browser.find_element(By.ID,"state").send_keys('my state')
    browser.find_element(By.ID,"city").send_keys('my city')
    browser.find_element(By.ID,"zipcode").send_keys('12345')
    browser.find_element(By.ID,"mobile_number").send_keys('0102030102')
    browser.find_element(By.XPATH,"//button[.='Create Account']").click()
    time.sleep(1)

@when('I complete the order')
def order_complete(browser):
    assert browser.find_element(By.XPATH,"//b[.='Account Created!']").is_displayed()
    browser.find_element(By.XPATH,"//a[.='Continue']").click()
    browser.find_element(By.XPATH,"//a[contains(.,'Cart')]").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//a[.='Proceed To Checkout']").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//a[.='Place Order']").click()
    time.sleep(1)
    browser.find_element(By.XPATH,"//input[@name='name_on_card']").send_keys('GGGGGG')
    browser.find_element(By.XPATH,"//input[@name='card_number']").send_keys('1111 1111 1111 1111')
    browser.find_element(By.XPATH,"//input[@name='cvc']").send_keys('123')
    browser.find_element(By.XPATH,"//input[@name='expiry_month']").send_keys('10')
    browser.find_element(By.XPATH,"//input[@name='expiry_year']").send_keys('2025')
    browser.find_element(By.XPATH,"//button[@id='submit']").click()
    time.sleep(2)
    assert browser.find_element(By.XPATH,"//b[.='Order Placed!']").is_displayed()
    time.sleep(1)

@then('I can download the invoice')
def download_invoice(browser):
    browser.find_element(By.XPATH,"//a[.='Download Invoice']").click()
    time.sleep(1)