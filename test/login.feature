Feature: User Login via Microsoft Entra ID
  In order to access the document management system
  As an employee
  I want to log in through Microsoft Entra ID

  Scenario: Redirect unauthorized user to login page
    Given the user is not authenticated
    When the user attempts to access the application
    Then the user is redirected to the Microsoft Entra ID login page

  Scenario: Successful login
    Given the user navigates to the Microsoft Entra ID login page
    When the user enters valid credentials
    Then the user is authenticated and redirected to the main page

  Scenario: Failed login
    Given the user navigates to the Microsoft Entra ID login page
    When the user enters invalid credentials
    Then the user receives an error message
    And the user remains on the login page

  Scenario: Token expiration
    Given the user is logged in
    And the user's authentication token has expired
    When the user attempts to perform an action
    Then the user is redirected to the Microsoft Entra ID login page