const { list } = require("tar");

function Add_to_List_Modal(book_name, book_tag) {
  // console.log(book_name);
  console.log(book_name, book_tag);
  $("#exampleModal").on("show.bs.modal", function (event) {
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector(".modal-title");
    modalTitle.textContent = book_name;

    // If user not signed in then ...empty... eyyyy

    $.get("/users/getUserBookLists/", function (data) {
      if (data["status"] === 200) {
        console.log(data);
        document.getElementById("book_list").innerHTML = "";
        for (let d in data.userbooklist) {
          booklistobj = data.userbooklist[d];
          console.log(booklistobj["booklist_title"]);

          const booklist_li = document.createElement("li");
          booklist_li.innerHTML =
            booklist_li.innerHTML +
            "<button type='button' onclick=\"addBook('" +
            booklistobj["booklist_id"] +
            ":" +
            book_tag +
            "')\" >" +
            booklistobj["booklist_title"] +
            "</button>";

          document.getElementById("book_list").appendChild(booklist_li);
        }
      }
    });
  });
  $("#exampleModal").modal("show");
}

function addBook(inputstr) {
  var book_list_id = inputstr.split(":")[0];
  var book_tag = inputstr.split(":")[1];
  console.log(book_list_id, book_tag);

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
  console.log("hihihi");

  var booklist_title = $("#booklist_title").val().trim();

  if (booklist_title.length) {
    $.getJSON(
      "/users/createBookList/",
      { booklist_title: booklist_title },
      function (data) {
        console.log(data);
        if (data["status"] === 403) {
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

          // const booklist_li = document.createElement("li");
          // booklist_li.innerHTML =
          //   booklist_li.innerHTML +
          //   "<button type='button' onclick=\"addBook('" +
          //   booklist_id +
          //   ":" +
          //   book_tag +
          //   "')\" >" +
          //   bbooklist_title +
          //   "</button>";

          // document.getElementById("book_list").appendChild(booklist_li);
        }
      }
    );
  }
}
