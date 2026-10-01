// Create a new subject
// Create a new academic subject
query subjects verb=POST {
  api_group = "EduTrack"
  auth = "user"

  input {
    text name filters=trim
    text code? filters=trim
    text professor? filters=trim
    int workload_hours? filters=min:0
    text description? filters=trim
    date start_date?
    date end_date?
    text color_hex? filters=trim
  }

  stack {
    db.add subjects {
      data = {
        user_id       : $auth.id
        name          : $input.name
        code          : $input.code
        professor     : $input.professor
        workload_hours: $input.workload_hours
        description   : $input.description
        start_date    : $input.start_date
        end_date      : $input.end_date
        color_hex     : $input.color_hex
      }
    } as $subject
  }

  response = $subject
}