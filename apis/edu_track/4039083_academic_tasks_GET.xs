// List all academic tasks for the authenticated user
// List all my tasks
query academic_tasks verb=GET {
  api_group = "EduTrack"
  auth = "user"

  input {
    int page?=1
    int per_page?=20
    int subject_id? {
      table = "subjects"
    }
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id ==? $input.subject_id
      sort = {due_date: "asc"}
      return = {
        type  : "list"
        paging: {page: $input.page, per_page: $input.per_page}
      }
    } as $tasks
  }

  response = $tasks
}