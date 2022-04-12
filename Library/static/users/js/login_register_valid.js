$(function () {
  console.log("hihihi");

  var $email = $("#email_input"); // this is refering to the id of the element in the template html file!

  $email.change(function () {
    var email = $email.val().trim();

    if (email.length()) {
      //check if user exists
      $.getJSON("/users/userverify/", { email: email }, function (data) {
        console.log(data);
      });
    }
  });
});
