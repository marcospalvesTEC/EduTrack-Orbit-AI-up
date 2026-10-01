// Get a specific task by ID
// Get task details
query "academic_tasks/{task_id}" verb=GET {
  api_group = "EduTrack"
  auth = "user"

  input {
    int task_id {
      table = "academic_tasks"
    }
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.task_id
    } as $task
  
    precondition ($task != null) {
      error_type = "notfound"
      error = "Tarefa não encontrada."
    }
  
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você não tem permissão para acessar esta tarefa."
    }
  }

  response = $task
}