# Database

Create a database backend. This activity will use a model for the API, store its content to a database, and retreive content from the database.

## Connection Setup

1. Open the secrets store. On Replit, click the lock icon on the function access panel
1. Create a new secret:
    * Name the secret `MONGO_URL`
    * Place the URL provided by the instructor as the value.
    > If you have your own public MongoDB instance, you may use that URL
1. Save and close the panel

## Library

Create a MongoDB client object.

> MongoDB supplies `pymongo`, which is greate, but synchronous. A derrivative driver `motor` provides close to the same functional syntax, but supports async operations. Since FastAPI is async-capable, it would be fitting to use `motor` rather than `pymongo`.

1. Import **Motor**'s `asyncio` mongo client, as well as other libraries. Leave the current imports you have, just ensure those are added / merged.

    ```python
    from pydantic import BaseModel
    from pydantic.fields import Field
    from fastapi import FastAPI, status, HTTPException
    from enum import Enum
    import uvicorn
    import os
    from pymongo.errors import DuplicateKeyError
    import motor.motor_asyncio
    ```

1. Set up a `Person` `pydantic` model, with the fields `id`, `name`, `GPA`. Inherit `BaseModel` for this class.
1. Create a variable named `db` to hold the singleton reference to the Motor MongoDB client. To do so safely, place it in a try/catch

    ```python
    try:
        mongo_url = os.environ["MONGO_URL"]
        db = motor.motor_asyncio.AsyncIOMotorClient(mongo_url).get_default_database()
    except Exception as e:
        print('Oh nos!', e)

    ```

1. Create a pydantic model for people. A person is defined as:

  ```python
  class Person(BaseModel):
    id: str = Field(title='Email of the person')
    name: str = Field(title='Name of the person')
    GPA: float | None = Field(title='Grade point average', ge=.0, le=4.0, default= None)
  ```

1. Lastly, a cheap way to handle the pydantic <--> MongoDB translation is to use these couple of functions:

    ```python
    def modelize(doc):
    doc['id'] = doc.pop('_id')
    return doc

    def documentize(model: BaseModel):
    doc = model.dict()
    doc['_id'] = doc.pop('id')
    return doc
    ```

## API Endpoints

> The `Motor` driver variation we imported uses asyncio. This means we can finally make use of the pesky `async def` tacked on every method we define.
  Using `await` on async methods lets the main program thread free up to handle other tasks while I/O is happening (network is I/O too!).
  This makes a single API deployment handle more concurrent requests.

### Get People

1. Create an enpoint to list people from the database.

  ```python
  @api.get("/people", tags="Mongo")
  async def people():
    docs= [modelize(d) async for d in db.people.find({})]
    return docs
  ```

1. Run and ensure that you see results.

> Note the syntax for async inside list comprehension `[`__foo__ `async for` __bar__ `in` __some_async_iterable__ `]`.
  `docs` is just a variable, and will be assigned the value after all awaiting is exhausted.

### Get Person by Id

1. Create an enpoint to get a single person by id.
    1. The route is  `@api.get("/people/{id}", tags="Mongo")`. Same as above, but add a path parameter `{id}`
    1. Define an async function named `get_person` that takes an `id: str` as the sole parameter
    1. use `Motor`'s `db.people.find_one({'_id': id})` function to get a single document match. This function is an async function, so you must `await` it.
    1. Return the value of the document
    1. Run and test this method. Supply the id via Swagger __"bob@bob.bob"__ (without quotation marks)
    1. Run with the id __"marklar"__. Observe any errors.
      > We should handle the case that there is no person to return. HTTP 404 was made for this!
    1. Add a test to see if the db found anything. `find_one()` returns  `None` if no documents matched the criteria
        * If it did not, then `raise` an `HTTPException("some meaninful message")`
        * If it did, return the document
    1. Run again with the id __"marklar"__. Ensure you got a 404.
    1. We made a `Person` pydantic model already. Let's put it to good use!
        1. Add the parameter `response_model=Person` to the route annotation
        1. Instead of returning the raw result from the database, wrap it in the function `modelize()`. If your document varibale is named `doc` then `modelize(doc)` 
        1. Run again and ensur it works.
        1. Refresh Swagger web page. Ensure the model got registered and reporter (towards the bottom of the page)


## Create Person

Where will we be if we could not create a person?

1. Create and enpoint to create a single person.
1. The route is `@api.post("/people", tags="Mongo")`. The HTTP verb `post` signals creation semantics.
1. Define the method `add_person()`. It should be async, and tage a single, non-optional parameter `person: Person`
1. Await the value from the call `result = await db.people.insert_one(documentize(person))`. Note that we "documentize" the `person` parameter value before insertion.
1. Return a simple value `return 'ok'` for now
1. Run and ensure it works. Use the document `{"id": "your_email_here", "name": "your name here", "GPA": 4.0}` and place your own or some unique email.
1. If it ran OK, run it again with the same exact document. Observer the error.
    > We are using the `id` field as a primary key. In MongoDB it is always the `_id` field. You can't create two people with the same exact id. Other tutorials skirt this and create surrogate keys but those come with. **DON'T GET ME STARTED** about surrogate and natural keys! 
1. Everything is as it should be actually. But it would be nicer to have the API flow the error state using proper HTTP responses.
    1. Add a try/except block around the method call
    1. Catch the specific error `DuplicateKeyError` first. Raise `HTTPException(status.HTTP_409_CONFLICT,detail=f'Person with id {person.id} already exists. Can't create twice')`
    1. Catch any other error right after. `except: raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Oh snap! My bad...')
  
  > The first catch is a user error: User should not have attempted to create and existing person.
    The second error is a server error - if the driver failed to dutifully create the user otherwise, it's not the user's fault.
    For this reason, the first is a 400 level error (user error), and the second a 500 level (server error)

## Takehome

* MongoDB and document oriented databases are a natural fit for JSON / document-like object interfaces
* `pydantic` maps into and out of  `dict` so it's naturally suitable... except for... `id`
* If using MongoDB, need to add a bit of boiler plate code to hadle the fact that pydantic fiercely ignores any field name that starts with `_`. This includes the ever so important Mongo `_id` field. But easy fix.
