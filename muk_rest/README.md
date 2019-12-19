# Restful API

Enables a REST API for the Odoo server. The API has routes to authenticate and retrieve a token. Afterwards, a set of routes to interact with the server are provided.

## Setup

In case the module should be active in every database just change the auto install flag to "True". To activate the routes even if no database is selected the module should be loaded right at the server start. This can be done by editing the config file or passing a load parameter to the start script.

Parameter: `--load=web,muk_rest`

## API Documentation

**Authentication**
----

Generates the API token based on the given login informations.

* **URL**

  _/api/authenticate_

* **Method:**
  
  `POST`
  
* **Data Params**

  **Required:**
 
   `db=[alphanumeric]`
   
   `login=[alphanumeric]`
   
   `password=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{token: "dbULH4OKKEp.......Kby-KE4OKEpK2M"}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "invalid_db"}`
    
  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{"error": "rest_api_not_supported"}`
    
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"error": "invalid_login"}`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "POST",
  url: "/api/authenticate",
  data: {
    db: "rest",
    login: "admin",
    password: "admin",
  },
  success: success,
});
```

* **Sample Response:**

```
{token: "dbULH4OKKEp.......Kby-KE4OKEpK2M"}
```

**Life**
----

Returns the remaining lifetime to a given token.

* **URL**

  _/api/life_
  
  _/api/life/<string:token>_

* **Method:**
  
  `GET`
  
* **URL Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `db=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `3559`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "GET",
  url: "/api/life",
  data: {
    token: "...",
  },
  success: success,
});
  ```
* **Sample Response:**

```
3559
```

**Refresh**
----

Refreshes the token lifetime.

* **URL**

  _/api/refresh_

* **Method:**
  
  `POST`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `db=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `True`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "POST",
  url: "/api/refresh",
  data: {
    token: "...",
  },
  success: success,
});
```

* **Sample Response:**

```
True
```

**Close**
----

Closes the API connection.

* **URL**

  _/api/close_

* **Method:**
  
  `POST`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `db=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `True`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "POST",
  url: "/api/close",
  data: {
    token: "...",
  },
  success: success,
});
```

* **Sample Response:**

```
True
```

**Search**
----

Returns the search result.

* **URL**

  _/api/search_

  _/api/search/<string:model>_

  _/api/search/<string:model>/<int:id>_

  _/api/search/<string:model>/<int:id>/<int:limit>_

  _/api/search/<string:model>/<int:id>/<int:limit>/<int:offset>_

* **Method:**
  
  `GET`
  
* **URL Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `db=[alphanumeric]`
   
   `id=[integer]`
   
   `model=[alphanumeric]`
   
   `domain=[json]`
   
   `context=[json]`
   
   `count=[bool]`
   
   `limit=[integer]`
   
   `offset=[integer]`
   
   `order=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{...}`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "GET",
  url: "/api/search",
  data: {
    token: "...",
    model: "res.partner",
    domain: '[["id", "=", 1]]',
  },
  success: success,
});
  ```
  
* **Sample Response:**

```
[
    {
        "__last_update": "2017-12-31 03:13:29",
        "active": true,
        "bank_ids": [],
        "barcode": false,
        "category_id": [],
        "child_ids": [],
        "city": "",
        "color": 0,
        "comment": false,
        "commercial_company_name": "My Company",
        "commercial_partner_country_id": [],
        "commercial_partner_id": [
            1,
            "My Company"
        ],
        "company_id": [
            1,
            "My Company"
        ],
        "company_name": false,
        "company_type": "company",
        "contact_address": "My Company\n\n\n  \n",
        "country_id": [],
        "create_date": false,
        "create_uid": [],
        "credit_limit": 0.0,
        "customer": false,
        "date": false,
        "display_name": "My Company",
        "email": "info@yourcompany.com",
        "email_formatted": "My Company <info@yourcompany.com>",
        "employee": false,
        "function": false,
        "id": 1,
        "image": false,
        "image_medium": false,
        "image_small": false,
        "industry_id": [],
        "is_company": true,
        "lang": "en_US",
        "mobile": false,
        "name": "My Company",
        "parent_id": [],
        "parent_name": false,
        "partner_share": true,
        "phone": "",
        "ref": false,
        "self": [
            1,
            "My Company"
        ],
        "state_id": [],
        "street": "",
        "street2": false,
        "supplier": false,
        "title": [],
        "type": "contact",
        "tz": false,
        "tz_offset": "+0000",
        "user_id": [],
        "user_ids": [],
        "vat": false,
        "website": "http://www.yourcompany.com",
        "write_date": "2017-12-31 03:13:29",
        "write_uid": [
            1,
            "Administrator"
        ],
        "zip": ""
    }
]
```

**Read**
----

Returns the search result of the given fields.

* **URL**

  _/api/read_

  _/api/read/<string:model>_

  _/api/read/<string:model>/<int:id>_

  _/api/read/<string:model>/<int:id>/<int:limit>_

  _/api/read/<string:model>/<int:id>/<int:limit>/<int:offset>_

* **Method:**
  
  `GET`
  
* **URL Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `db=[alphanumeric]`
   
   `id=[integer]`
   
   `fields=[json]`
   
   `model=[alphanumeric]`
   
   `domain=[json]`
   
   `context=[json]`
   
   `count=[bool]`
   
   `limit=[integer]`
   
   `offset=[integer]`
   
   `order=[alphanumeric]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{...}`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "GET",
  url: "/api/read",
  data: {
    token: "...",
    model: "res.partner",
    domain: '[["id", "=", 1]]',
    fields: '["name"]',
  },
  success: success,
});
  ```
  
* **Sample Response:**

```
[
    {
        "id": 1,
        "name": "My Company"
    }
]
```

**Create**
----

Creates a new record.

* **URL**

  _/api/create_

* **Method:**
  
  `POST`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
  **Optional:**
 
   `model=[alphanumeric]`
   
   `values=[json]`
   
   `context=[json]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{...}`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "POST",
  url: "/api/create",
  data: {
    token: "...",
    values: '{"name": "MuK IT"}',
  },
  success: success,
});
```

* **Sample Response:**

```
[
    {
        "__last_update": "2017-12-31 12:08:58",
        "active": true,
        "bank_ids": [],
        "barcode": false,
        "category_id": [],
        "child_ids": [],
        "city": false,
        "color": 0,
        "comment": false,
        "commercial_company_name": false,
        "commercial_partner_country_id": [],
        "commercial_partner_id": [
            6,
            "MuK IT"
        ],
        "company_id": [
            1,
            "My Company"
        ],
        "company_name": false,
        "company_type": "person",
        "contact_address": "\n\n  \n",
        "country_id": [],
        "create_date": "2017-12-31 12:08:58",
        "create_uid": [
            1,
            "Administrator"
        ],
        "credit_limit": 0.0,
        "customer": true,
        "date": false,
        "display_name": "MuK IT",
        "email": false,
        "email_formatted": "MuK IT <False>",
        "employee": false,
        "function": false,
        "id": 6,
        "image": "...",
        "image_medium": "...",
        "image_small": "...",
        "industry_id": [],
        "is_company": false,
        "lang": "en_US",
        "mobile": false,
        "name": "MuK IT",
        "parent_id": [],
        "parent_name": false,
        "partner_share": true,
        "phone": false,
        "ref": false,
        "self": [
            6,
            "MuK IT"
        ],
        "state_id": [],
        "street": false,
        "street2": false,
        "supplier": false,
        "title": [],
        "type": "contact",
        "tz": false,
        "tz_offset": "+0000",
        "user_id": [],
        "user_ids": [],
        "vat": false,
        "website": false,
        "write_date": "2017-12-31 12:08:58",
        "write_uid": [
            1,
            "Administrator"
        ],
        "zip": false
    }
]
```

**Write**
----

Updates an existing record.

* **URL**

  _/api/write_

* **Method:**
  
  `PUT`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
   `ids=[json]`
   
  **Optional:**
 
   `model=[alphanumeric]`
   
   `values=[json]`
   
   `context=[json]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `True`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "PUT",
  url: "/api/write",
  data: {
    token: "...",
    values: '{"name": "MuK IT"}',
    ids: "[1]",
  },
  success: success,
});
```

* **Sample Response:**

```
True
```

**Unlink**
----

Deletes an existing record.

* **URL**

  _/api/delete_

* **Method:**
  
  `DELETE`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
   `ids=[json]`
   
  **Optional:**
 
   `model=[alphanumeric]`
   
   `context=[json]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `True`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "DELETE",
  url: "/api/unlink",
  data: {
    token: "...",
    ids: "[1]",
  },
  success: success,
});
```

* **Sample Response:**

```
True
```

**Call**
----

Generic method call.

* **URL**

  _/api/call_

* **Method:**
  
  `POST`
  
* **Data Params**

  **Required:**
 
   `token=[alphanumeric]`
   
   `method=[alphanumeric]`
   
  **Optional:**
 
   `ids=[json]`
   
   `context=[json]`
   
   `args=[json]`
   
   `kwargs=[json]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{...}`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `"error": "token_invalid"`
    
  * **Code:** 400 BAD REQUEST  <br />
    **Content:** `{'error': "arguments_missing ..."}`

* **Sample Call:**

```javascript
$.ajax({
  type: "POST",
  url: "/api/call",
  data: {
    token: "...",
    method: "copy",
    ids: "[1]",
  },
  success: success,
});
```

* **Sample Response:**

```
[
    {
        "__last_update": "2017-12-31 12:19:00",
        "active": true,
        "bank_ids": [],
        "barcode": false,
        "category_id": [],
        "child_ids": [],
        "city": "",
        "color": 0,
        "comment": false,
        "commercial_company_name": "My Company (copy)",
        "commercial_partner_country_id": [],
        "commercial_partner_id": [
            7,
            "My Company (copy)"
        ],
        "company_id": [
            1,
            "My Company"
        ],
        "company_name": false,
        "company_type": "company",
        "contact_address": "My Company (copy)\n\n\n  \n",
        "country_id": [],
        "create_date": "2017-12-31 12:19:00",
        "create_uid": [
            1,
            "Administrator"
        ],
        "credit_limit": 0.0,
        "customer": false,
        "date": false,
        "display_name": "My Company (copy)",
        "email": "info@yourcompany.com",
        "email_formatted": "\"My Company (copy)\" <info@yourcompany.com>",
        "employee": false,
        "function": false,
        "id": 7,
        "image": "...",
        "image_medium": "...",
        "industry_id": [],
        "is_company": true,
        "lang": "en_US",
        "mobile": false,
        "name": "My Company (copy)",
        "parent_id": [],
        "parent_name": false,
        "partner_share": true,
        "phone": "",
        "ref": false,
        "self": [
            7,
            "My Company (copy)"
        ],
        "state_id": [],
        "street": "",
        "street2": false,
        "supplier": false,
        "title": [],
        "type": "contact",
        "tz": false,
        "tz_offset": "+0000",
        "user_id": [],
        "user_ids": [],
        "vat": false,
        "website": "http://www.yourcompany.com",
        "write_date": "2017-12-31 12:19:00",
        "write_uid": [
            1,
            "Administrator"
        ],
        "zip": ""
    }
]
```

## Notes and Credits

The app icon is based on an icon made by [Prosymbols](https://www.flaticon.com/packs/web-design-and-development-12) from [www.flaticon.com](www.flaticon.com)
