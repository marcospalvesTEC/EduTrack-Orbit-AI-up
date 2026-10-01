// Update an existing subject
// Update subject details
query "subjects/{subject_id}" verb=PATCH {
  api_group = "EduTrack"
  auth = "user"

  input {
    int subject_id {
      table = "subjects"
    }
  
    text name? filters=trim
    text code? filters=trim
    text professor? filters=trim
    int workload_hours? filters=min:0
    text description? filters=trim
    date start_date?
    date end_date?
    text color_hex? filters=trim
  }

  stack {
    // Check ownership first
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
      error = "Você não tem permissão para editar esta disciplina."
    }
  
    // Prepare updates
    var $updates {
      value = {}
    }
  
    conditional {
      if ($input.name != null) {
        var.update $updates {
          value = $updates|set:"name":$input.name
        }
      }
    }
  
    conditional {
      if ($input.code != null) {
        var.update $updates {
          value = $updates|set:"code":$input.code
        }
      }
    }
  
    conditional {
      if ($input.professor != null) {
        var.update $updates {
          value = $updates|set:"professor":$input.professor
        }
      }
    }
  
    conditional {
      if ($input.workload_hours != null) {
        var.update $updates {
          value = $updates
            |set:"workload_hours":$input.workload_hours
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
      if ($input.start_date != null) {
        var.update $updates {
          value = $updates
            |set:"start_date":$input.start_date
        }
      }
    }
  
    conditional {
      if ($input.end_date != null) {
        var.update $updates {
          value = $updates|set:"end_date":$input.end_date
        }
      }
    }
  
    conditional {
      if ($input.color_hex != null) {
        var.update $updates {
          value = $updates|set:"color_hex":$input.color_hex
        }
      }
    }
  
    precondition (($updates|is_empty) == false) {
      error_type = "inputerror"
      error = "Nenhuma alteração fornecida."
    }
  
    db.patch subjects {
      field_name = "id"
      field_value = $input.subject_id
      data = $updates
    } as $updated_subject
  }

  response = $updated_subject
}