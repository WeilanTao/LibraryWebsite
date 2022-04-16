function getBooks(booklist_id) {
  $.getJSON(
    "/users/getBookList/",
    { booklist_id: booklist_id },
    function (data) {
      //   console.log(data);

      document.getElementById("books_li").innerHTML = "";

      for (let b in data.books) {
        const bookobj = data.books[b];

        getBookInfo(bookobj["book_tag"]).then((response) => {
          // console.log("get...", response.book[0]);

          const book = response.book[0];
          // console.log("hihihi", book.book_name);
          const book_li = document.createElement("li");

          book_li.innerHTML =
            book_li.innerHTML +
            "<button type='button' onclick=\"goToBook('" +
            book.author_tag +
            ":" +
            book.book_tag +
            "')\" >" +
            book.book_name +
            "</button> <button type = 'button' onclick =\"deleteBookFromList('" +
            book.book_tag +
            ":" +
            booklist_id +
            "')\" >Remove</button>";

          document.getElementById("books_li").appendChild(book_li);
        });
      }
    }
  );
}

function getBookInfo(book_tag) {
  return $.ajax({
    url: "/get/book/infor/ma/tion/",
    data: { book_tag: book_tag },
    async: false,
    done: function (data) {
      return data;
    },
  });
}

function goToBook(inputstr) {
  const author_tag = inputstr.split(":")[0];
  const book_tag = inputstr.split(":")[1];
  url =
    "http://" +
    window.location.hostname +
    ":" +
    window.location.port +
    "/" +
    author_tag +
    "/" +
    book_tag;
  console.log(url);
  window.location.href = url;
}

function deleteBookFromList(inputstr) {
  const booklist_id = inputstr.split(":")[1];
  const book_tag = inputstr.split(":")[0];
  // console.log("delete", book_tag, booklist_id);

  $.getJSON(
    "/users/deleteBookFromList",
    { book_tag: book_tag, booklist_id: booklist_id },
    function (data) {
      //refersh the booklist page after successful deletion
      getBooks(booklist_id);
    }
  );
}

function deleteBookList(booklist_id) {
  console.log(booklist_id);

  $.getJSON(
    "/users/deleteBookList",
    { booklist_id: booklist_id },
    function (data) {
      // console.log(data);

      //refersh the booklist page after successful deletion
      $("#booklist_list").load(window.location.href + " #booklist_list");
      $("#books_li").load(window.location.href + " #books_li");
      // window.location.reload();
    }
  );
}
