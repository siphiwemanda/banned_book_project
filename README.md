# FSND Capstone Project

This application is an API that lets the user determine what books have been banned in what countries and why.

Over the course of history various regiemes have banned books for primarily (but not limited to) political reasons. Particularly in todays climate it is vital to understand how information and ideas have historically been exchanged and surpressed.


This application was built as part of the Udacity Full Stack Web developer nanodegree
and was originally built to show my ability in:

####Data modeling

- Architect relational database models in Python
- Utilize SQLAlchemy to conduct database queries

####API Architecture and Testing

- Follow RESTful principles of API development using Flask
- Structure endpoints to perform CRUD operations, as well as error handling
- Demonstrate validity of API behavior using the unittest library

####Third Party Authentication

- Configure Role Based Authentication and roles-based access control (RBAC) in a Flask application utilizing Auth0
- Decode and verify JWTs from Authorization headers

####Deployment

- API is hosted live via Heroku - https://bannedbooks.herokuapp.com/

##Local installation

Clone this repository and move to the head directory
```
git clone https://github.com/siphiwemanda/banned_book_project.git
cd banned_book_project/
```

Install the requirements in the `requirements.txt` script
```
pip3 install -r requirements.txt
```

Set the environment variables in the `setup.sh` file
```
source setup.sh
```
Start the development server using the command
```
FLASK_APP=app.py FLASK_DEBUG=true flask run
```

##Roles
Datamanger - access to delete, post and patch

Editor - acesss to patch

postman collection can be used to get JWT if current variables set in the setup.sh file  have expired



##API Reference

Errors are returned as JSON in the following format:

```json
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

#####The Api will return the following errors

- 400: Bad Request

- 404: Response not found

- 422: Unprocessable

- 405: Method not allowed

#####These API calls are available to the public 

`GET/book`

````json
{
  "books": {
    "2": "Another Country ", 
    "25": "Lord of the Rings", 
    "27": "The Hobbit", 
    "28": "Catch-22", 
    "29": "The Struggle Is My Life", 
    "3": "1984", 
    "4": "All Quiet on the Western Front"
  }, 
  "success": true
}
````


`GET/authors`

````json
{
  "authors": {
    "1": "George Orwell", 
    "2": "James Baldwin", 
    "4": "Erich Maria Remarque", 
    "5": "Karl Marks", 
    "6": "Nelson Mandela", 
    "7": "J.R.R Tolkien", 
    "8": "Joseph Heller"
  }, 
  "success": true
}
````


`GET/countries`

```json

{
  "countries": {
    "1": "Russia", 
    "2": "USA", 
    "3": "France", 
    "4": "China"
  }, 
  "success": true
}
```

#####delete book 

`DELETE/book/delete/2`

```json
{
  "deleted": 2,
  "success": true
}
```


#####add a book

`POST/addbook`

```json
{
  "created": "test book",
  "success": true
}
```
#####edit author

`PATCH/authors/edit/1`

```json

{
  "Author": "George",
  "success": true
}
```



