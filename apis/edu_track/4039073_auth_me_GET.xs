// Returns the currently authenticated user's profile
// Get the current user's profile
query "auth/me" verb=GET {
  api_group = "EduTrack"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "Usuário não encontrado."
    }
  }

  response = $user
    |unpick:["password", "password_reset"]
}