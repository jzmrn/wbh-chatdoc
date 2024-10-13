Feature: Role-Based Document Access
  In order to ensure document confidentiality
  As an employee
  I want documents to be accessible based on assigned roles

  Scenario: View role-specific documents
    Given the user is logged in
    And the user has a specific role
    When the user accesses the document management section
    Then the user sees only documents assigned to their role

  Scenario: Upload a new document
    Given the user is in the document management section
    When the user uploads a new document
    And the document is successfully processed
    Then the document appears in the user's document list

  Scenario: Delete a document
    Given the user is in the document management section
    And the user has permission to delete a document
    When the user deletes a document
    Then the document is removed from the document list