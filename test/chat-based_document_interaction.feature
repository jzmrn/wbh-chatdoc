Feature: Chat-Based Document Interaction
  In order to interact with documents easily
  As an employee
  I want to ask questions and receive answers via chat

  Background:
    Given the user with role test is logged in
    And document Ist-Analyse.pdf with role test is uploaded
    And document Kommunikationsplan.pdf with role test is uploaded
    And no other documents are uploaded

  Scenario: Ask questions and use context
    Given the user is in the chat section
    When the user asks the question Welches Budget wurde für das Projekt geschätzt?
    Then the answer contains 50.000 € and a link to Ist-Analyse.pdf
    When the user asks the question Auf welcher Seite finde ich das?
    Then the answer contains Seite 9 and a link to Ist-Analyse.pdf

  Scenario: Ask english question and get english answer
    Given the user is in the chat section
    When the user asks the question What is the deadline for the project?
    Then the answer contains 18th of December 2024 and a link to Ist-Analyse.pdf
