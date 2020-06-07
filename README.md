# FSND Capstone Project

This application is an API that lets the user look for books authour and coutried in order to determin what books have been banneded in what countries and why.
This application was built as part of th Udacity Full Stack Web developer nanodegrtee
and was orginally built to show my proficiance in:

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

- API is hosted live via Heroku

##local installation

Clone this repository 
Install the requirement in the requirement document
RUN the app: `FLASK_APP=app.py FLASK_DEBUG=true flask run`



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

- 422: unprocessable

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



