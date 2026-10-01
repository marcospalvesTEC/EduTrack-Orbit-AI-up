// Stores academic tasks related to subjects for each user
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // The user who owns this task
    int user_id {
      table = "user"
    }
  
    // The subject this task belongs to
    int subject_id {
      table = "subjects"
    }
  
    text title filters=trim
    text description? filters=trim
    date due_date?
    enum status?=Pendente {
      values = ["Pendente", "Em andamento", "Concluída", "Atrasada"]
    }
  
    enum priority?="Média" {
      values = ["Baixa", "Média", "Alta"]
    }
  
    decimal weight? filters=min:0
    int estimated_minutes? filters=min:0
    int actual_minutes? filters=min:0
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
  ]
}