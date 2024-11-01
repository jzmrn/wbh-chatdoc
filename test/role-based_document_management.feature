Feature: Role-Based Document Access
  In order to ensure document confidentiality
  As an employee
  I want documents to be accessible based on assigned roles

  Scenario: View role-specific documents
    Given the user with role invisible is logged in
    And document IT-Sicherheit und Datenschutz.pdf with role invisible is uploaded
    And document Systemtestplan.pdf with role private is uploaded
    And the user with role test is logged in
    And document Ist-Analyse.pdf with role test is uploaded
    And document Kommunikationsplan.pdf with role private is uploaded
    And no other documents are uploaded
    When the user accesses the document management section
    Then the user sees the documents Ist-Analyse.pdf
    And the user sees the documents Kommunikationsplan.pdf
    And the user does not see the documents IT-Sicherheit und Datenschutz.pdf
    And the user does not see the documents Systemtestplan.pdf

  Scenario: Upload a new document
    Given the user is logged in
    And the user is in the document management section
    When the user uploads a new document
    Then the document is added in the document list

  Scenario: Delete a document
    Given the user is logged in
    And the user is in the document management section
    When the user deletes a document
    Then the document is removed from the document list