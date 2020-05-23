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

const form = document.getElementById('form')
const Name = document.getElementById('Name')
const DOB = document.getElementById('DOB')
const About = document.getElementById('About')

form.addEventListener('submit', (e) =>{
    e.preventDefault();
    console.log('clicked')
    checkInputs();
    console.log('checked')
    sendPatch()
    console.log('patch')

})

function checkInputs() {
    const NameValue = Name.value
    const DOBValue = DOB.value
    const AboutValue = About.value

    if (NameValue === ''){
        //show error class
        setError(Name, 'Name can not be blank')
    }else {
        //susses class
        setsuccess(Name)
    }

    if (DOBValue === ''){
        //show error class
        setError(DOB, 'DOB can not be blank')
    }else {
        //susses class
        setsuccess(DOB)
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
        "Name" : Name,
        "DOB": DOB,
        "About": About
}

console.log(data)
}


