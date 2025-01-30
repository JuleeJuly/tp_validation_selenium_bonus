import pytest
import pytest_bdd
import time
import random

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    #Le navigateur est lancé
    #L'utilisateur accède à http://automationexercise.com
    browser.get('http://automationexercise.com')
    browser.fullscreen_window()
    
@when('I add products to the cart')
def add_product(browser):
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@class='fc-button fc-cta-consent fc-primary-button']"))
    )
    button.click()
    #L'utilisateur ajoute des produits au panier
    browser.find_element(By.XPATH,"//a[.=' Products']").click()
    browser.fullscreen_window()
    #L'utilsiateur ajoute 6 produits au panier
    for i in range(1, 6):
        xpath = f"//div[@class='features_items']//div[@class='col-sm-4']//a[@data-product-id='{i}'][1]"
        add = browser.find_element(By.XPATH, xpath)
        add.click()
        button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,"//div[@class='modal-footer']//button"))
        )
        button.click()

@when('I create my account')
def create_account(browser):
    #L'utilisateur clique sur "Procéder au paiement" et s'inscrit
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[contains(.,'Cart')]"))
    )
    button.click()
    checkout_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[.='Proceed To Checkout']"))
    )
    checkout_button.click()
    login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[.='Register / Login']"))
    )
    login_button.click()
    browser.find_element(By.XPATH,"//input[@name='name']").send_keys('Toto')
    # Générer une adresse email unique
    random_email = f"toto{random.randint(1000, 9999)}@tutu.fr"
    browser.find_element(By.XPATH,"//div[@class='signup-form']//input[@name='email']").send_keys(random_email)
    browser.find_element(By.XPATH,"//button[.='Signup']").click()
    mister_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Mr.')]"))
    )
    mister_button.click()
    assert browser.find_element(By.ID,"name").get_attribute("value") == "Toto"
    assert browser.find_element(By.ID,"email").get_attribute("value") == random_email
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

@when('I complete the order')
def order_complete(browser):
    #"Account Created!" est visible
    assert browser.find_element(By.XPATH,"//b[.='Account Created!']").is_displayed()
    browser.find_element(By.XPATH,"//a[.='Continue']").click()
    browser.find_element(By.XPATH,"//a[contains(.,'Cart')]").click()
    checkout = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[.='Proceed To Checkout']"))
    )
    checkout.click()
    place_order = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[.='Place Order']"))
    )
    place_order.click()
    #L'utilisateur finalise sa commande avec des informations de paiement valides
    browser.find_element(By.XPATH,"//input[@name='name_on_card']").send_keys('GGGGGG')
    browser.find_element(By.XPATH,"//input[@name='card_number']").send_keys('1111 1111 1111 1111')
    browser.find_element(By.XPATH,"//input[@name='cvc']").send_keys('123')
    browser.find_element(By.XPATH,"//input[@name='expiry_month']").send_keys('10')
    browser.find_element(By.XPATH,"//input[@name='expiry_year']").send_keys('2025')
    browser.find_element(By.XPATH,"//button[@id='submit']").click()
    #Le message "Félicitations ! Votre commande a été confirmée !" est visible
    assert browser.find_element(By.XPATH,"//b[.='Order Placed!']").is_displayed()

@then('I can download the invoice')
def download_invoice(browser):
    #L'utilisateur clique sur "Télécharger la facture"
    #La facture est téléchargée avec succès
    invoice = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[.='Download Invoice']"))
    )
    invoice.click()