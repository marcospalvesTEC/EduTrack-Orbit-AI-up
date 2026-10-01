// Update an existing task
// Update task details
query "academic_tasks/{task_id}" verb=PATCH {
  api_group = "EduTrack"
  auth = "user"

  input {
    int task_id {
      table = "academic_tasks"
    }
  
    int subject_id? {
      table = "subjects"
    }
  
    text title? filters=trim
    text description? filters=trim
    date due_date?
    enum status? {
      values = ["Pendente", "Em andamento", "Concluída", "Atrasada"]
    }
  
    enum priority? {
      values = ["Baixa", "Média", "Alta"]
    }
  
    decimal weight? filters=min:0
    int estimated_minutes? filters=min:0
    int actual_minutes? filters=min:0
  }

  stack {
    // Check ownership first
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
      error = "Você não tem permissão para editar esta tarefa."
    }
  
    // Verify subject ownership if subject_id is provided
    conditional {
      if ($input.subject_id != null) {
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
      }
    }
  
    // Prepare updates
    var $updates {
      value = {}
    }
  
    conditional {
      if ($input.subject_id != null) {
        var.update $updates {
          value = $updates
            |set:"subject_id":$input.subject_id
        }
      }
    }
  
    conditional {
      if ($input.title != null) {
        var.update $updates {
          value = $updates|set:"title":$input.title
        }
      }
    }
  
    conditional {
      if ($input.description != null) {
        var.update $updates {
          value = $updates
            |set:"description":$input.description
        }
      }
    }
  
    conditional {
      if ($input.due_date != null) {
        var.update $updates {
          value = $updates|set:"due_date":$input.due_date
        }
      }
    }
  
    conditional {
      if ($input.status != null) {
        var.update $updates {
          value = $updates|set:"status":$input.status
        }
      }
    }
  
    conditional {
      if ($input.priority != null) {
        var.update $updates {
          value = $updates|set:"priority":$input.priority
        }
      }
    }
  
    conditional {
      if ($input.weight != null) {
        var.update $updates {
          value = $updates|set:"weight":$input.weight
        }
      }
    }
  
    conditional {
      if ($input.estimated_minutes != null) {
        var.update $updates {
          value = $updates
            |set:"estimated_minutes":$input.estimated_minutes
        }
      }
    }
  
    conditional {
      if ($input.actual_minutes != null) {
        var.update $updates {
          value = $updates
            |set:"actual_minutes":$input.actual_minutes
        }
      }
    }
  
    precondition (($updates|is_empty) == false) {
      error_type = "inputerror"
      error = "Nenhuma alteração fornecida."
    }
  
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.task_id
      data = $updates
    } as $updated_task
  }

  response = $updated_task
}