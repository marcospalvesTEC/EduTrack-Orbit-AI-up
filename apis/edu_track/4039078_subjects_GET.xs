// List all subjects for the authenticated user
// List all my subjects
query subjects verb=GET {
  api_group = "EduTrack"
  auth = "user"

  input {
    int page?=1
    int per_page?=20
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      sort = {created_at: "desc"}
      return = {
        type  : "list"
        paging: {page: $input.page, per_page: $input.per_page}
      }
    } as $subjects
  }

  response = $subjects
}