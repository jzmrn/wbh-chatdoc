Feature: Chat History
  In order to review previous interactions
  As an employee
  I want to access my chat history

  Scenario: View chat history
    Given the user is logged in
    And the user navigates to the chat history section
    When the user selects a previous chat
    Then the chat conversation is displayed
    And the user can continue the conversation if needed