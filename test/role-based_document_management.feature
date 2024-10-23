Feature: Role-Based Document Access
  In order to ensure document confidentiality
  As an employee
  I want documents to be accessible based on assigned roles

  Background:
    Given the user is logged in

  Scenario: View role-specific documents
    Given the user has the role test
    When the user accesses the document management section
    Then the user sees only private and role related documents

  Scenario: Upload a new document
    Given the user is in the document management section
    When the user uploads a new document
    Then the document is added in the document list

  Scenario: Delete a document
    Given the user is in the document management section
    When the user deletes a document
    Then the document is removed from the document list