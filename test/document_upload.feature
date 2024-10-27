Feature: Document Upload
  In order to add new documents to the system
  As an employee
  I want to manually upload documents

  Background:
    Given the user is logged in

  Scenario Outline: Upload a valid document
    Given the user is in the document upload section
    When the user uploads a document in <format> format
    Then the document is successfully added to the system

    Examples:
      | format |
      | pdf    |
      | text   |

  Scenario: Upload a valid document greater than 10MB
    Given the user is in the document upload section
    When the user uploads a document in pdf format greater than 10MB
    Then the document is not uploaded

  Scenario: Upload an invalid document format
    Given the user is in the document upload section
    When the user attempts to upload a document in an unsupported format
    Then the document is not uploaded
