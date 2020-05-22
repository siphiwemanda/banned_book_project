function searchFunction() {

}

const deleteBook = document.getElementsByClassName("delete-button");

for (let i = 0; i < deleteBook.length; i++) {
        const button = deleteBook[i];
        button.onclick = function(e) {
            console.log("click");
          const bookID = e.target.dataset['id'];
          fetch('/book/delete/' + bookID, {
            "method": 'DELETE'

          })
             .then(function () {
                window.location.href = `/`;
                 })
            .catch(function (e) {
                console.log('error', e)
             })
    }
  }