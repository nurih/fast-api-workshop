# Open API & Swagger

This activity explores OpenAPI and how FastAPI exposes the API so things are easily consumed by compliant applications.

## Global\

### API Description Text

Add a description to appear at the top of the Swagger UI.

1. To the `FastAPI()` constructor, supply the parameter `description`.
1. Assign the description body some text of your liking.
1. Run and ensure your text shows at the top of the Swagger page.

Try some markdown too: A description such as

```python
"""
## Fun Starts Here!

- Yip
- Yup
- Yap

----

### ... And never ends

> The following is about the function `doSomething(s:thing)`

var|desc
---|---
`foo`| The fooness of things
`bar`| The place around the corner

"""
```

### Swagger UI Route

Change the url for the API UX.

1. Supply the parameter `docs_url` to the constructor
    > Ensure it starts with a `/`, and contains valid path characters only.
1. Navigate to that relative URL.
1. Ensure that the UI is available at the path you specified.
1. Ensure that the UI is **not** at its default `/docs` url.

#### Swagger Behavior

Change some default Swagger appearance / behavior.

1. Create a variable containing a _dict_ as follows:

   ```python
   my_behavior = {
     'tryItOutEnabled': True,
     'docExpansion': 'full'
   }
   ```

1. Assign `my_behavior` to the FastAPI constructor parameter `swagger_ui_parameters`.
1. Navigate to the UI and observe the page behavior:

    - All collapsible nodes should be expanded now
    - The **Execute** button should be enabled already - the **Try it out** button is in its already-clicked mode, which shows **Cancel**

## Parameter Level

Add tags to organize the methods into groups in the UI

1. Add the following API endpoints:

    ```python
    @api.get("/meta/a")
    async def open_api_a(): return {'ack': 'a'}
    @api.get("/meta/b")
    async def open_api_b(): return {'ack': 'b'}
    @api.get("/meta/c")
    async def open_api_c(): return {'ack': 'c'}
    ```

1. Add the import `from enum import Enum` to the top of the file.
1. Create an enum to constrain the tag values:

    ```python
    class Tags(Enum):
        marklar="Marklar"
        smurf="Smurf"
    ```

1. To each of the routes / api methods, add one of the tags.
    - The parameter name is `tags`
    - The parameter value is a list of tags, so wrap the enum value in `[` `]`
    - Assign the tags in interleaved fashion:
        Route|Tag
        ----|----
        `/meta/a`| `Tags.marklar`
        `/meta/b`| `Tags.smurf`
        `/meta/c`| `Tags.marklar`

1. Run and observe the methods were collected int the group. They are no longer in global route declaration order.

Add some metadata at the method / route level

1. Pick a route to enhance. Any `@api.get()` would do.
1. Add a parameter `summary` with text value of your choice.
1. Add a parameter `description` with text value of your choice. Make this value long: use the `"""` style string literal and put some line breaks within the text.
1. Run and check that the title and the description are shown in the UI.

> use the endpoint for `redoc` and see how it appears there too.
  OpenAPI just exposes values. It's up to UI implementors to make use of it.

Example:

```python
@api.get('/route_level_decore', 
    summary='My Getter',
    description='''My description of my getter.
         
         It has multiple lines
         Like, here is another...
         ''')
async def m1(x: int|None):
    return {'ack': x}
```

## Model Level

Add metadata to show at a model field level.

1. Create a class based on the pydantic base model:

    ```python
    class Thing(BaseModel):
            """
            This thing documents the model - a docstrig.
            """
        name: str = Field(
            title='My field title', 
            description='My field description')

    ```

1. Create a route and method that takes a single parameter of type `Thing`

    ```python
    @api.get('/meta/model_decore')
    async def open_api_e(thing:Thing): return thing
    ```

1. Run, and ensure the model field decorations worked.

-------

## Takehome

- Shaping the UX (Swagger / redoc)
- Changing url of docs
- pydantic flows metadata about the model to OpenAPI
- FastAPI flows metadata from routes
