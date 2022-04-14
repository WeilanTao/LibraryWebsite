function Add_to_List(book_name) {
  // console.log(book_name);

  $("#exampleModal").on("show.bs.modal", function (event) {
    // var button = event.relatedTarget;
    // console.log("hihihi");
    // // Extract info from data-bs-* attributes

    // var recipient = button.getAttribute("data-bs-whatever");
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector(".modal-title");
    modalTitle.textContent = book_name;
  });
  $("#exampleModal").modal("show");
}
