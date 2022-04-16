function getBooks(author_tag) {
  $.getJSON("/getbooks/", { author_tag: author_tag }, function (data) {
    console.log(data);
  });
}
