Feature: Document Upload
  In order to add new documents to the system
  As an employee
  I want to manually upload documents

  Scenario: Upload a valid document
    Given the user is in the document upload section
    When the user uploads a document in PDF or text format
    Then the document is successfully added to the system

  Scenario: Upload an invalid document format
    Given the user is in the document upload section
    When the user attempts to upload a document in an unsupported format
    Then the system displays an error message
    And the document is not uploaded