
const deleteBook = document.getElementsByClassName("delete-button");

for (let i = 0; i < deleteBook.length; i++) {
    const button = deleteBook[i];
    button.onclick = function (e) {
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

const form = document.getElementById('form')
const Name = document.getElementById('Name')
const DOB = document.getElementById('DOB')
const About = document.getElementById('About')
const book_form = document.getElementById('book-form')
const book_name = document.getElementById('book-Name')
const book_synopsis = document.getElementById('book-synopsis')
const book_cover = document.getElementById('book-cover')


function edit_writer() {
    console.log('clicked')
    sendPatch()
    console.log('patch')
}

function bookchecked() {
    console.log('clicked')
    AddBook()
}

function checkInputs() {
    const NameValue = Name.value
    const DOBValue = DOB.value

    if (NameValue === '') {
        //show error class
        setError(Name, 'Name can not be blank')
    } else {
        //susses class
        setsuccess(Name)
    }

    if (DOBValue === '') {
        //show error class
        setError(DOB, 'DOB can not be blank')
    } else {
        //susses class
        setsuccess(DOB)
    }

    if (book_name === '') {
        //show error class
        setError(book_name, 'DOB can not be blank')
    } else {
        //susses class
        setsuccess(book_name)
    }
}

function setError(input, message) {
    const formControl = input.parentElement; //form control div
    const small = formControl.querySelector('small'); // update the error message
    small.innerText = message

    formControl.className = 'form-control error';
}

function setsuccess(input) {
    const formControl = input.parentElement; //form control div
    formControl.className = 'form-control success';
}

function sendPatch() {
    let data = {
        "name": Name.value,
        "dob": DOB.value,
        "about": About.value
    }
    console.log(data)
    const buttonID = document.getElementById('submit-author')
    const WriterID = buttonID.getAttribute('data-id')
    console.log(WriterID)
    fetch('/authors/edit/submit/' + WriterID, {
        "method": `PATCH`,
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then((response) => {
        return response.json();
    }).then((myJson) => {
        if (myJson['success'] === true) {
            window.location.href = '/'
        }
    });
}

function AddBook() {
    let data = {
        "title": book_name.value,
        "synopsis": book_synopsis.value,
        "link": book_cover.value
    }
    console.log(data)
    fetch('/addbook/submit', {
        "method": `POST`,
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then((response) => {
        return response.json();
    }).then((myJson) => {
        if (myJson['success'] === true) {
            window.location.href = '/'
        }
    })
}

function storeJwt() {
    let jwt = window.location.href
    console.log(jwt)

}