// Registers a new user
// Create a new user account
query "auth/signup" verb=POST {
  api_group = "EduTrack"

  input {
    text name filters=trim
    email email filters=trim|lower
    password password
  }

  stack {
    db.has user {
      field_name = "email"
      field_value = $input.email
    } as $exists
  
    precondition (!$exists) {
      error_type = "inputerror"
      error = "Este e-mail já está em uso."
    }
  
    db.add user {
      data = {
        name    : $input.name
        email   : $input.email
        password: $input.password
        role    : "member"
      }
    } as $user
  
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