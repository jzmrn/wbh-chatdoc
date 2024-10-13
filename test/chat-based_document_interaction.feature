Feature: Chat-Based Document Interaction
  In order to interact with documents easily
  As an employee
  I want to ask questions and receive answers via chat

  Scenario: Ask a question in chat
    Given the user is in the chat section
    When the user asks a question about a document
    Then the system provides a relevant answer based on document content

  Scenario: View source of the answer
    Given the user received an answer in chat
    When the user wants to verify the information
    Then the system provides a link to the source document

  Scenario: Continue conversation in context
    Given the user is in an ongoing chat
    When the user asks a follow-up question
    Then the system responds considering the context of the previous questions and answers