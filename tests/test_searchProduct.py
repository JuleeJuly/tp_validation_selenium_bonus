import pytest
import pytest_bdd
import time

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_bdd import parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pytest_bdd import scenario, given, when, then

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@scenario('features/order.feature', "Add and Remove Products from the Cart")
def test_search():
    pass

@given('I am on the website http://automationexercise.com')
def open_browser_windows_page(browser):
    browser.get('http://automationexercise.com')
    browser.fullscreen_window()
    
@when('I search for products')
def add_product(browser):
    browser.find_element(By.XPATH,"//button[@class='fc-button fc-cta-consent fc-primary-button']").click()
    #L'utilisateur clique sur le bouton "Produits"
    assert browser.find_element(By.XPATH,"//a[.=' Products']").is_enabled()
    browser.find_element(By.XPATH,"//a[.=' Products']").click()
    #L'utilisateur est dirigé vers la page "TOUS LES PRODUITS"
    assert browser.find_element(By.XPATH,"//h2[@class='title text-center']").is_displayed()
    assert browser.find_element(By.XPATH,"//h2[@class='title text-center']").text == "ALL PRODUCTS"
    #L'utilisateur entre un nom de produit dans la barre de recherche et clique sur "Rechercher"
    assert browser.find_element(By.ID,"search_product").is_enabled()
    browser.find_element(By.ID,"search_product").send_keys('Dress')
    browser.find_element(By.ID,"submit_search").click()
    #"PRODUITS RECHERCHÉS" est visible
    assert browser.find_element(By.XPATH,"//h2[@class='title text-center']").is_displayed()
    assert browser.find_element(By.XPATH,"//h2[@class='title text-center']").text == "SEARCHED PRODUCTS"
    #Tous les produits correspondants sont affichés
    list_products(browser)

@when('I add these products to the cart')
def add_product(browser):
    #L'utilisateur ajoute ces produits au panier
    browser.fullscreen_window()
    products = browser.find_elements(By.XPATH,"//div[@class='productinfo text-center']/a[.='Add to cart']")
    if products:
        for product in products:
            product.click()
            button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,"//div[@class='modal-footer']//button"))
            )
            button.click() 
    else:
        print("Aucun élément trouvé")
    verify_products(browser)
    
@when('I log in')
def log_in(browser):
    #L'utilisateur clique sur "Inscription/Connexion" et se connecte
    browser.find_element(By.XPATH,"//a[contains(.,'Signup / Login')]").click()
    browser.find_element(By.XPATH,"//input[@name='password']").send_keys('Test01234!')
    browser.find_element(By.XPATH,"//div[@class='login-form']//input[@name='email']").send_keys('toto@tutu.fr')
    browser.find_element(By.XPATH,"//button[.='Login']").click()

@then('I can remove the products from the cart')
def remove_product(browser):
    #L'utilisateur retourne à la page Panier
    #Les produits ajoutés sont toujours visibles
    verify_products(browser)
    #L'utilisateur supprime tous les produits du panier
    products = browser.find_elements(By.XPATH,"//tbody/tr/td[@class='cart_delete']/a")
    if products:
        for product in products:
            product.click()
    else:
        print("Aucun élément trouvé")
    #Le message "Le panier est vide ! Cliquez ici pour acheter des produits." est visible
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID,"empty_cart")))
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"//b[.='Cart is empty!']")))

def list_products(browser):
    products = browser.find_elements(By.XPATH,"//div[@class='productinfo text-center']/h2")
    if products:
        for product in products:
            text = product.text
            assert text.count("Rs") >= 1  
    else:
        print("Aucun élément trouvé")
    
def verify_products(browser):
    #L'utilisateur clique sur le bouton "Panier"
    browser.find_element(By.XPATH,"//a[contains(.,'Cart')]").click()
    #Les produits ajoutés sont visibles dans le panier
    products = browser.find_elements(By.XPATH,"//tbody/tr")
    if products:
        descriptions = browser.find_elements(By.XPATH,"//tbody//td[@class='cart_price']/p")
        for desc in descriptions:
            text = desc.text
            assert text.count("Rs") >= 1 
    else:
        print("Aucun élément trouvé")