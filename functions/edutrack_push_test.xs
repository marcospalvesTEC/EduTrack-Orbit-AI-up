function edutrack_push_test {
  input {
    // what is this argument about?
    text some_argument? filters=trim
  }

  stack {
    var $some_variable {
      value = "with some value"
    }
  }

  response = $some_variable
}