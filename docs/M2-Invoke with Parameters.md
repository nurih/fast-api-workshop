# Invoke With Parameters

In this lab we will pass values into the API.

## URL and Parameters

### Fair Game

1. Create POST API endpoint:
    - Route the path `/order1`
    - Name the method `create_order1`
    - The method should two parameters:
        - A string value named `item`
        - A numeric value named `quantity`
1. The body of the method should simply return the values. For example `return {"item": item, "quantity": quantity}`
1. Run and check the method:
    1. Supply an item and a quantity, then execute.
        > Ensure the result is as epected.
    1. Supply an item name and no quantity, then execute.
        > Observe the error produced.
    1. Supply a number for the item name, and a number for the quantity, then execute.
        > Observe whether an error produced.

### We Have Options

1. Create POST API endpoint:
    - Route the path `/order2`
    - Name the method `create_order2`
    - The method should two parameters:
        - A string value named `item`
        - A numeric value named `quantity`, assigned an `Optional[int]` value of **1**
1. The body of the method should simply return the values. For example `return {"item": item, "quantity": quantity}`
1. Run and check the method:
    1. Supply an item and a quantity, then execute.
        > Ensure the result is as epected.
    1. Supply an item name and no quantity, then execute.
        > Observe that this time _no error is produced_. The quantity returned should be the value **1**.
    1. Supply an itme name and the value **-3** (negative quantity). Does this produce an error?

### Attention to Detail

1. Create POST API endpoint:
    - Route the path `/order3`
    - Name the method `create_order3`
    - The method should two parameters:
        - A string value named `item`
        - A numeric value named `quantity`, assigned a `Query` value:
            1. With a default value of **1**
            1. With validation that the value must be a positive number, 1 or greater (you may use greater-equal or greater semantics, but zero should not be acceptable)
1. The body of the method should simply return the values. For example `return {"item": item, "quantity": quantity}`
1. Run and check the method:
    1. Supply an item and a quantity, then execute.
        > Ensure the result is as epected.
    1. Supply an item name and no quantity, then execute.
        > Observe that this time _no error is produced_. The quantity returned should be the value **1**.
    1. Supply an itme name and the value **-3** (negative quantity)
        > Observe that the error produced corresponds to the validation rule you added
1. Strings can be checked to adhere to a `regex` (regular expression). Assign the `item` parameter a `rexex` option with validation using a regular expression:
    - The item must be exactly 3 characters long
    - The item must contain only upper-case letters and numbers
    - The item must begin with a letter
1. Run and check the method:
    1. Supply the following item names, and ensure error _is not_ produced
        - A10
        - CMU
        - B4Q
    1. Supply the following item names, and ensure an error _is_ produced
        - 900
        - X4
        - C3PO
        - abc

#### Bonus

Observe what happens when an invalid query parameter is attempted via `/docs`.
Enter an invalid request, and hit **Execute**.
An error appears in the browser.
Flip to replit's console, and take a look at the log. Did the request even go out to the API from the browser?

> Because of the tight OpenAPI integration, Swagger UI is able to intercept values it knows the server wont accept.

### Patch

Patch is the undersung hero of thrifty API. Ok, maybe not everyon's favorite. But lets use it.
We will simulate updating a data item by supplying an id and only fields we want to update on the item, alongside their values.

1. Create PATCH API endpoint:
    - Route the path `/order3`
    - Name the method `change_order3`
    - The method should two parameters:
        - An int parameter named `id`
        - A `dict` parameter named `fields`, with no default
1. The body of the method should return the fields to be patched. For example `return {"item_id": id, "updated_fields": fields}`
1. Run and check the method:
    1. Supply a numeric `item_id` of your choice
    1. Edit the dictionary to contain a couple of fileds, for example

        ```json
        {
            "name": "bob",
            "city": "springfield"
        }
        ```

    1. Execute the patch
        > Observe that the values from the dictionary are accepted.

> When dealing with large JSON objects, it is more efficient to transmit the values requiring change rather than the whole object. The `PATCH` method helps forster this efficiency and makes it possible for the API endpoint to know that it needs to only update those fields. The `PUT` method does not carry these semantics, and can run into issues where fields become stale or are updated unnecessarily.

## Takehome

- Use type annotation to control parameter type
- Use type annotation to validate values
- Use `Query` object as the default value provider to add validation constraints
  - `gt`,`ge`,`lt`,`le`
  - `regex`
- Intercept HTTP verbs via Fast API: `get`, `post`, `put`, `patch`
