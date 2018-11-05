Installation with docker-compose
================================

```
docker-compose up --build
```

API description
===============
```
GET /book # list of books
POST /book # create a book
GET /book/<id> # show the book
PUT /book/<id> # edit the book
DELETE /book/<id> # delete the book
```

`GET /book` supports filtering, pass in the request body any subset of the following fields:
```
{
    "annotation": "substring",
    "isbn": "13 digits",
    "title": "substring"
}
```

`POST`/`PUT` need the following fields:
```
{
    "annotation": "long text",
    "isbn": "13 digits",
    "title": "string"
}
```
