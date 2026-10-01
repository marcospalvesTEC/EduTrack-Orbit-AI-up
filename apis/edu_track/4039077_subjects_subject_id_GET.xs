// Get a specific subject by ID
// Get subject details
query "subjects/{subject_id}" verb=GET {
  api_group = "EduTrack"
  auth = "user"

  input {
    int subject_id {
      table = "subjects"
    }
  }

  stack {
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
      error = "Você não tem permissão para acessar esta disciplina."
    }
  }

  response = $subject
}