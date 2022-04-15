function getBooks(booklist_id) {
  $.getJSON(
    "/users/getBookList/",
    { booklist_id: booklist_id },
    function (data) {
      //   console.log(data);

      document.getElementById("books_li").innerHTML = "";

      for (let b in data.books) {
        bookobj = data.books[b];
        const book_li = document.createElement("li");

        book_li.innerHTML =
          book_li.innerHTML +
          "<button type='button' onclick=\"goToBook('" +
          bookobj["book_tag"] +
          "')\" >" +
          bookobj["book_tag"] +
          "</button> <button type = 'button' onclick =\"deleteBookFromList('" +
          bookobj["book_tag"] +
          "')\" >  Delete Book</button>";

        document.getElementById("books_li").appendChild(book_li);
      }
    }
  );
}

function goToBook(book_tag) {
  console.log(book_tag);
}

function deleteBookFromList(book_tag) {
  console.log("delete", book_tag);
}
