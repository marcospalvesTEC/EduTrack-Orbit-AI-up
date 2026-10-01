// Stores academic subjects for each user
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // The user who owns this subject
    int user_id {
      table = "user"
    }
  
    text name filters=trim
    text code? filters=trim
    text professor? filters=trim
    int workload_hours? filters=min:0
    text description? filters=trim
    date start_date?
    date end_date?
    text color_hex? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}