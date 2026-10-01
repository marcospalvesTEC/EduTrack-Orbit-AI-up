// Authenticates a user
// Log in to an existing account
query "auth/login" verb=POST {
  api_group = "EduTrack"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $is_valid
  
    precondition ($is_valid) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }
  
    security.create_auth_token {
      table = "user"
      extras = {name: $user.name}
      expiration = 86400
      id = $user.id
    } as $token
  }

  response = {
    authToken: $token
    user     : $user|unpick:["password", "password_reset"]
  }
}