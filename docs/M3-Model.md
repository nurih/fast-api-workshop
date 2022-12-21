# Invoke With Parameters

In this lab we will explore using models via `pydantic` to shape the API's complex parameters and some related functionality.

## Model Behavior

We will define a `Superhero` model, each superhero has a set of `Superpower`s.

The superpowers are modeled as an Enum to constrain a hero's superpowers to only contain well known ones. Copy the code below into your file:

```python
class Superpower(str, Enum):
    strong = 'strong'
    fly = 'fly'
    laser_eyes = 'laser'
    gadgets = 'gadgets'
```

Now define a `Superhero`. Copy the code below into your file, below the `Superpower`.

```python
class Hero(BaseModel):
    name: str = Field(title='Hero name', description='The hero name known to the public')
    civilian_name: str | None = Field(title='The secret identity!', regex=r'^(?!(Mrs?|Captain))')
    wears_cape: bool | None = True
    superpowers: Set[Superpower]
```

Let's examin the model above:

- The `name` field is an `str` (a string), mandatory, and has a `title` and a `description`. Those are useful for documenting the schema.
- The `civilian_name` field is an optional `str`. In case a name _is_ supplied, it must not begin with "Mr", "Mrs" or "Captain" - those are reserved hero name prefixes.
- The `wears_cap` field is boolean, and is optional. It has a default value of `True`, as we expect many superheroes ware capes.
- The  `superpowers` field is a set of `Superpower` items.

Next, let's create a bunch of superheroes. Copy the code below into your file:

```python
heroes = (
    {'name': 'Captain Marvel',  'civilian_name': 'Carol', 'superpowers': {
        Superpower.fly, Superpower.laser_eyes, Superpower.strong}},
    {'name': 'Batman', 'civilian_name': 'Bruce',
        'wears_cape': True, 'superpowers': {Superpower.gadgets}},
    {'name': 'Luke Cage', 'civilian_name': 'Luke',
        'wears_cape': False, 'superpowers': {Superpower.strong}},
    {'name': 'Flaming Carrot',
        'wears_cape': False, 'superpowers': {Superpower.gadgets}},

)
```

## Validation

1. Create a `post` enpoint with the path `/heroes`, on function name `create_one`.
1. Define a single parameter named `hero` of type `Hero`.
1. The body of the function should return `{'ok': hero}`.
1. Run the program, and navigate to `/docs` Swagger endpoint and test the model validation:
    1. Try to submit a hero that is valid. Ensure the result returns ok.
    1. Try to submit a hero with the `civilian_name` "Captain Obvious". Ensure an error is produced.
    1. Try to submit a hero with an un-listed superpower. Ensure an error is produced
    1. Try to submit a hero with no `name`. Ensure an error is produced

Now let's explore validation to an input parameter.

1. Create a `get` enpoint with the path `/heroes/{offset:int}`, a `response_model` set to the type `Hero`, on function name `a_hero`.
    > The annotation `/heroes/{offset:int}` includes the type `int` in order to distinguish it from other methods later on which have a string path suffix. Without it, the order of the methods must be carefully coordinated so that this rout doesn't catch paths such as `/heroes/abc`.
1. Define a single parameter named `offset` of `int`.
1. Constrain the offset using the Path() object. Ensure that the offset value is always a valid offset into the list of `heroes`.
    > Hint: 0 < offset < len(heroes)
1. The function should return the hero with the offset supplied from the `heroes` list: `return heroes[offset]`
1. Run the program, navigate to `/docs` and test the validation:
    1. Enter a valid offset and ensure a hero is returned.
    1. Enter a negative offset and ensure an error is produced.
    1. Enter an offset of _4_ and ensure a _validation error_ is produced

## Return Shaping

Create each of the the endpoints described below, adding the appropriate named parameter to the `get()` decorator.

Each one should be annotated with `response_model=List[Hero]`.

Each method body should just return the hero list: `return heroes`.

Path|Method Name| Desired Behavior
----|----|----
`/heroes/plain`|`as_is()`| Just the list of heroes as it is.
`/heroes/no_empties`|`no_empties()`| Trim away empty fields.
`/heroes/trim_the_obvious`|`trim_the_obvious()`| Trim away fields which are explicitly set to their default value.
`/heroes/no_doxing`|`no_doxing()`| Prevent the field `civilian_name` from being returned.

## What Have We Done?

The power of the model to validate constrain the API messages is integrated into the JSON API and schema tools take advantage of this.

1. Navigate to the bottom of the `/docs` page, and examin the **Schemas** section.
1. Expand the **Hero** schema, and expand each of the fields to show the relevant validation rules, titles, descriptions, default values, and allowed enum members.

> Swagger is nice, but other tools understand the schema. Such is the power of standards. FAST API exposes a _Redocly_  api documentation as well. Check out the same schema at `/redoc#operation/create_one_heroes_post` visualized differently.
