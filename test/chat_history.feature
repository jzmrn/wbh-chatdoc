Feature: Chat History
  In order to review previous interactions
  As an employee
  I want to access my chat history

  Background:
    Given the user is logged in

  Scenario: View chat history
    Given the user has a previous chat history
    When the user selects a previous chat
    Then the chat conversation is displayed
    And the user can continue the conversation if needed

  Scenario: View large chat history
    Given the user has a previous chat history greater than 30000 characters
    When the user selects the large chat
    Then the chat conversation is displayed
    And the user can't continue the conversation
