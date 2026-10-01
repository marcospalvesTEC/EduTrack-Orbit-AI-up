// Create a new academic task
// Create a new task for a subject
query academic_tasks verb=POST {
  api_group = "EduTrack"
  auth = "user"

  input {
    int subject_id {
      table = "subjects"
    }
  
    text title filters=trim
    text description? filters=trim
    date due_date?
    enum status?=Pendente {
      values = ["Pendente", "Em andamento", "Concluída", "Atrasada"]
    }
  
    enum priority?="Média" {
      values = ["Baixa", "Média", "Alta"]
    }
  
    decimal weight? filters=min:0
    int estimated_minutes? filters=min:0
    int actual_minutes? filters=min:0
  }

  stack {
    // Verify subject ownership
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada."
    }
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "A disciplina informada não pertence ao seu usuário."
    }
  
    // Add task
    db.add academic_tasks {
      data = {
        user_id          : $auth.id
        subject_id       : $input.subject_id
        title            : $input.title
        description      : $input.description
        due_date         : $input.due_date
        status           : $input.status
        priority         : $input.priority
        weight           : $input.weight
        estimated_minutes: $input.estimated_minutes
        actual_minutes   : $input.actual_minutes
      }
    } as $task
  }

  response = $task
}