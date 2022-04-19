const { list } = require("tar");

function Add_to_List_Modal(book_name, book_tag) {
  // console.log(book_name);
  // console.log(book_name, book_tag);
  $("#exampleModal").on("show.bs.modal", function (event) {
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector(".modal-title");
    modalTitle.textContent = book_name;
    var modalBookTag = exampleModal.querySelector(".modal-book-tag");
    modalBookTag.textContent = book_tag;

    // If user not signed in then ...empty... eyyyy

    $.get("/users/getUserBookLists/", function (data) {
      if (data["status"] === 200) {
        // console.log(data);
        document.getElementById("book_list").innerHTML = "";
        for (let d in data.userbooklist) {
          booklistobj = data.userbooklist[d];
          // console.log(booklistobj["booklist_title"]);

          const booklist_li = document.createElement("li");
          booklist_li.innerHTML =
            booklist_li.innerHTML +
            "<button  class='btn btn-outline-dark btn-sm' type='button' onclick=\"addBook('" +
            booklistobj["booklist_id"] +
            ":" +
            book_tag +
            "')\" >" +
            booklistobj["booklist_title"] +
            "</button>";

          document.getElementById("book_list").appendChild(booklist_li);
        }
      } else {
        console.log("user not logged in");
      }
    });
  });
  $("#exampleModal").modal("show");
}

function addBook(inputstr) {
  var book_list_id = inputstr.split(":")[0];
  var book_tag = inputstr.split(":")[1];
  // console.log(book_list_id, book_tag);

  $.getJSON(
    "/users/addBookToList/",
    { book_list_id: book_list_id, book_tag: book_tag },
    function (data) {
      console.log(data);
      if (data["status"] === 200) {
        console.log("book add to book list ");
      }
    }
  );
}
function Add_to_List() {
  var booklist_title = $("#booklist_title").val().trim();
  var book_tag = document.getElementById("modal-book-tag").textContent;
  // console.log(book_tag);

  if (booklist_title.length) {
    $.getJSON(
      "/users/createBookList/",
      { booklist_title: booklist_title },
      function (data) {
        // console.log(data);
        if (data["status"] === 301) {
          // if user not logged in, redirect to the log in page
          $("#exampleModal")
            .on("hidden.bs.modal", function () {
              url =
                "http://" +
                window.location.hostname +
                ":" +
                window.location.port +
                "/users/login";
              console.log(url);
              window.location.href = url;
            })
            .modal("hide");
        } else {
          console.log("book list has been created");
          var booklist_id = data["booklist_id"];

          //if user logged in, and the new booklist has been created successfully, we will add a new button for this list to the above booklist list, and enable the button for adding new books
          const booklist_li = document.createElement("li");
          booklist_li.innerHTML =
            booklist_li.innerHTML +
            "<button  class='btn btn-outline-dark btn-sm' type='button' onclick=\"addBook('" +
            booklist_id +
            ":" +
            book_tag +
            "')\" >" +
            booklist_title +
            "</button>";

          document.getElementById("book_list").appendChild(booklist_li);
        }
      }
    );
  }
}
