function canSumbit() {
  console.log("hihihihihi");
  var canSumbit = true;

  var $email = $("#email_input");
  var $password_input = $("#password_input");
  var email = $email.val().trim();
  var password = $password_input.val().trim();

  if (!email || !password) {
    canSumbit = false;
  }

  return canSumbit;
}
