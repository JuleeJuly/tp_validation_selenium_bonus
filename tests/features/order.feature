Feature: Place an order  
    As a user,  
    I want to be able to place an order  

    Scenario: Placing an order
        Given I am on the website http://automationexercise.com
        When I add products to the cart
        And I create my account
        And I complete the order
        Then I can download the invoice

    Scenario: Add and Remove Products from the Cart
        Given I am on the website http://automationexercise.com
        When I search for products
        And I add these products to the cart
        And I log in
        Then I can remove the products from the cart