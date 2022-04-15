const { list } = require("tar");

function Add_to_List_Modal(book_name) {
  // console.log(book_name);

  $("#exampleModal").on("show.bs.modal", function (event) {
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector(".modal-title");
    modalTitle.textContent = book_name;

    $.get("/users/getUserBookLists/", function (data) {
      if (data["status"] === 200) {
        console.log(data);
        document.getElementById("book_list").innerHTML = "";
        for (let d in data.userbooklist) {
          booklistobj = data.userbooklist[d];
          console.log(booklistobj["booklist_title"]);

          const booklist_li = document.createElement("li");
          booklist_li.innerText = booklistobj["booklist_title"];
          document.getElementById("book_list").appendChild(booklist_li);
        }
      }
    });
  });
  $("#exampleModal").modal("show");
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
          
          const booklist_li = document.createElement("li");
          booklist_li.innerText = booklist_title;
          document.getElementById("book_list").appendChild(booklist_li);
        }
      }
    );
  }
}
