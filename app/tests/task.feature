Feature: Task CRUD
  Scenario: User creates, reads, updates, and deletes a task
    Given a logged in user
    When the user creates a task
    Then the task is created
    When the user reads the task
    Then the task details are correct
    When the user updates the task
    Then the task is updated
    When the user deletes the task
    Then the task is deleted
