Feature: Chat-Based Document Interaction
  In order to interact with documents easily
  As an employee
  I want to ask questions and receive answers via chat

  Background:
    Given the user is logged in

  Scenario: Ask german questions
    Given the user is in the chat section
    When the user asks the question Welches Budget wurde für das Projekt geschätzt?
    Then the answer contains 50.000€ and a link to Ist-Analyse.pdf
    When the user asks the question Was ist die Deadline für das Projekt?
    Then the answer contains 18.12.2024 and a link to Ist-Analyse.pdf

  Scenario: Ask english questions
    Given the user is in the chat section
    When the user asks the question What budget was estimated for the project?
    Then the answer contains 50.000€ and a link to Ist-Analyse.pdf
    When the user asks the question What is the deadline for the project?
    Then the answer contains 18th of December 2024 and a link to Ist-Analyse.pdf
