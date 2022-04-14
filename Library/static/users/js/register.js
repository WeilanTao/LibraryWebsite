var email_not_exists = false;

$(function () {
  console.log("hihihi");

  var $email = $("#email_input"); // this is refering to the id of the element in the template html file!
  var $password = $("#password_input");
  var $confirmpassword = $("#confirm_password_input");
  var password = "";

  $email.change(function () {
    var email = $email.val().trim();

    if (email.length) {
      //check if user exists
      $.getJSON("/users/userverify/", { email: email }, function (data) {
        console.log(data);
        var $email_info = $("#email_info");

        if (data["status"] === 200) {
          email_not_exists = true;
          $email_info.html("Valid account").css("color", "green");
        } else if (data["status"] === 901) {
          $email_info
            .html("Account exists. Please use another email")
            .css("color", "red");
        }
      });
    }
  });

  $password.change(function () {
    password = $password.val().trim();
  });

  $confirmpassword.change(function () {
    var confirmpassword = $confirmpassword.val().trim();

    var $confirm_password_info = $("#confirm_password_info");
    if (password !== confirmpassword) {
      $confirm_password_info
        .html("Password missmatch. Please reenter your password")
        .css("color", "red");
    } else {
      $confirm_password_info.html("");
    }
  });
});

function canSumbit() {
  var canSumbit = true;
  var $username = $("#name_input");
  var $email = $("#email_input");
  var $password = $("#password_input");
  var $confirmpassword = $("#confirm_password_input");

  var user_name = $username.val().trim();
  var email = $email.val().trim();
  var password = $password.val().trim();
  var confirmpassword = $confirmpassword.val().trim();

  console.log(email_not_exists);
  if (
    !user_name ||
    !email ||
    !password ||
    !confirmpassword ||
    password !== confirmpassword
  ) {
    canSumbit = false;
  }
  if (!email_not_exists) {
    canSumbit = false;
  }

  return canSumbit;
}
