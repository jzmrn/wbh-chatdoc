Feature: Document Management Menu
  In order to manage my documents effectively
  As an employee
  I want to access the document management section from the menu

  Scenario: Access document management section
    Given the user is logged in
    When the user clicks on the "Document Management" menu item
    Then the user is navigated to the document management section

  Scenario: View document details
    Given the user is in the document management section
    When the user selects a document
    Then the user can see the document's name, upload date, role, and options to delete or open
