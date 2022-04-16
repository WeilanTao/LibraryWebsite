function getBooks(booklist_id) {
  $.getJSON(
    "/users/getBookList/",
    { booklist_id: booklist_id },
    function (data) {
      //   console.log(data);

      document.getElementById("books_li").innerHTML = "";

      for (let b in data.books) {
        const bookobj = data.books[b];

        const book = getBookInfo(bookobj["book_tag"]);
        console.log("get...", book);

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
          "')\" >  Delete Book</button>";

        document.getElementById("books_li").appendChild(book_li);
      }
    }
  );
}

function getBookInfo(book_tag) {
  console.log(book_tag);
  $.getJSON(
    "/get/book/infor/ma/tion/",
    { book_tag: book_tag },
    function (data) {
      console.log("HIHIHI", data.book[0]);
      return data.book[0];
    }
  );
}
function goToBook(inputstr) {
  const author_tag = inputstr.split(":")[0];
  const book_tag = inputstr.split(":")[1];
  console.log(author_tag, book_tag);
}

function deleteBookFromList(book_tag) {
  console.log("delete", book_tag);
}
