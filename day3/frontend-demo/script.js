function book_to_row(b) {
  return `<tr>
        <td>${b.id}</td>
        <td>${b.title}</td>
        <td>${b.author}</td>
        <td>${b.publisher}</td>
        <td>${b.price}</td>
    </tr>`;
}

function get_books() {
  const url = 'http://127.0.0.1:8080/api/books';
  fetch(url)
    .then((resp) => resp.json())
    .then((data) => {
      data = data.map(book_to_row);
      data = data.join('');
      document.getElementById('book_list_tbody').innerHTML = data;
    });
}

get_books();
