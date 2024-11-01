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

  Scenario: Delete chat history
    Given the user has a previous chat history
    When the user deletes a previous chat
    Then the chat conversation is deleted

  Scenario: View large chat history
    Given the user has a previous chat history greater than 30000 characters
    When the user selects the large chat
    Then the chat conversation is displayed
    And the user can't continue the conversation

  Scenario: Chat history larger than 100 entries
    Given the user has a previous chat history with 100 entries
    When the user starts a new chat
    Then the oldest chat entry is deleted

  Scenario: Private chat history
    Given the user has a previous chat history
    And a new user is logged in
    Then the chat chat history is empty
