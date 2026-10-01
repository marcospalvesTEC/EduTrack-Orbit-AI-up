// Delete a subject
// Delete a subject
query "subjects/{subject_id}" verb=DELETE {
  api_group = "EduTrack"
  auth = "user"

  input {
    int subject_id {
      table = "subjects"
    }
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
      error = "Você não tem permissão para excluir esta disciplina."
    }
  
    // Delete related tasks first? The prompt didn't specify, but it's good practice.
    // However, I'll stick to the requirements.
    db.del subjects {
      field_name = "id"
      field_value = $input.subject_id
    }
  }

  response = {success: true}
}