Feature: Menu
  In order to use all functionalities of chatdoc easily
  As an employee
  I want to access the the function from the menu

  Background:
    Given the user is logged in

  Scenario: Access document management section
    When the user clicks on the document management menu item
    Then the user is navigated to the document management section

  Scenario: Access chat section
    When the user clicks on the chat menu item
    Then the user is navigated to the chat section
