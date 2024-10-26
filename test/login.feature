Feature: User Login via Microsoft Entra ID
  In order to access the document management system
  As an employee
  I want to log in through Microsoft Entra ID

  Scenario: Redirect unauthorized user to login page
    Given the user attempts to access the application
    Then the user is redirected to the Microsoft Entra ID login page

  Scenario: Successful login
    Given the user navigates to the Microsoft Entra ID login page
    When the user enters valid credentials
    Then the user is redirected to the main page

  Scenario: Failed login
    Given the user navigates to the Microsoft Entra ID login page
    When the user enters invalid credentials
    Then the user remains on the login page and receives an error message

  Scenario: Token invalidation
    Given the user is logged in
    And the user's authentication token is invalid
    When the user clicks on the chat menu item
    Then the user is redirected to the Microsoft Entra ID login page