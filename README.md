# ASInt project

ASInt project - 1st semester 2019/2020

The goal of this project is to develop a web application that makes use of the resources of IST, via FenixEdu API, using custom services that store important resources, accessible by WEB and REST interfaces. It was developed under the course `Internet Based Systems Architecture` (ASInt).


## Authors

This project was developed by the students:

````
81305 - Pedro Direita (MEEC)

84303 - Maria Frutuoso (MEEC)
````

## Content

This README file helps to understand each component present in this web application system, and their interfaces made available for resource query and exchange. Each component is stored in a different folder inside the parent directory in order to simulate modular division and interconectivity of systems.

- [Server](#server-apppy)
    - [Admin Pages](#admin-pages)
- [API](#api-apipy)
- [Microservices](#microservices)
    - [Rooms](#rooms-roomspy)
    - [Secretariats](#secretariats-secretariatspy)
    - [Canteen](#canteen-canteenpy)
- [Mobile application](#mobile-application-mobilepy)

## Package dependencies

This project uses the following packages:

  - `flask`;
  - `requests`;
  - `flask-login`;

## Entities  

In this project, you may find each entity inside a different folder, organized as follows:

````
.
├── API
│   ├── API.py
│   └── ...
├── microservices
│   ├── canteen                          
│   │   └── canteen.py
│   ├── rooms                             
│   │   └── rooms.py
│   ├── secretariats
│   │   ├── src
│   │   │   ├── __init__.py
│   │   │   └── utils.py
│   │   ├── templates
│   │   │   └── index.html            # not useful
│   │   └── secretariats.py
├── mobile
│   ├── templates                          
│   │   └── main_menu.html
│   ├── mobile.py                             
│   └── users.py
└── server
    ├── src                          
    │   └── utils.py                  # not useful
    ├── templates                          
    │   ├── add.html
    │   ├── admin.html
    │   ├── admin_login.html
    │   ├── admin_logout.html
    │   ├── edit.html
    │   └── secretariats.html
    └── app.py
````


### Server: `app.py`

  - running on `port=5500`

responsible for backend management


#### Admin Pages

The main Admin page is available at

````
http://127.0.0.1:5500/admin
````

and a message will be displayed if the admin is not logged in.
Admin authentication is performed at:

````
http://127.0.0.1:5500/admin/login
````

When the credentials are accepted (`username: admin; password: admin`), the page will redirect to the main Admin page, but more features will be then displayed.

##### Check all existing secretariats (with link to edit and delete a specific one):

````
http://127.0.0.1:5500/frontend/listSecretariats
````

  - associated templates: `secretariats.html`, `edit.html`

##### Add a new secretariat:

````
http://127.0.0.1:5500/frontend/addSecretariat
````

  - associated template: `add.html`

Admin logout is performed at:

````
http://127.0.0.1:5500/admin/logout
````


### API: `API.py`

  - running on `port=5100`

Independent application that works as a set of API access points the backend server has to communicate with the microservices.

#### Rooms' access points

Find the location (building and campus) of a specific room given its `id`, by accessing the `Rooms` service:

````
http://127.0.0.1:5100/location/<ID>
````

Retrieve the schedule of a specific room given its `id`, by accessing the `Rooms` service:

````
http://127.0.0.1:5100/timetable/<ID>
````

#### Secretariats' access points

Get all existing secretariats, by accessing the `Secretariat` service:

````
http://127.0.0.1:5100/secretariats
````

View the details of a specific secretariat with `id=ID`, by accessing the `Secretariat` service:

````
http://127.0.0.1:5100/secretariats/<ID>
````

#### Canteen's access points

Retrieve the menu of the IST canteen, by accessing the `Canteen` service:

````
http://127.0.0.1:5100/menus
````


### Microservices

Set of independent application services that provide several information to the main backend server.

#### Rooms: `rooms.py`

  - running on `port=5400`
  - API interaction to Fenix
  - API interaction to server (Read)

AP that retrieves the location (building and campus) of a specific room given its `id`:

````
http://127.0.0.1:5400/location/<ID>
````

AP that retrieves the schedule of a specific room given its `id`:

````
http://127.0.0.1:5400/timetable/<ID>
````

#### Secretariats: `secretariats.py`

  - running on `port=5200`

  - displays API endpoints (R/W) so that the admin of the backend server can interact with the data
  
  - offers data persistance (the current state of the list of secretariats is continuously saved)

API that retrieves all existing secretariats:

````
http://127.0.0.1:5200/listAll
````

API that retrieves the details of a specific secretariat with `id=ID`:

````
http://127.0.0.1:5200/getSecretariat/<ID>
````

#### Canteen: `canteen.py`

  - running on `port=5300`
  - API interaction to Fenix
  - API interaction to server (R)

AP that retrieves the menu of the IST canteen:

````
http://127.0.0.1:5300/menus
````

### Mobile application: `mobile.py`

  - running on `port=5000`

Main page that redirects to a custom FenixEdu application webpage that asks the user its authorization to use their account (personal information) in that application:

````
http://127.0.0.1:5000/
````

If the user authorizes, they will be redirected to a homepage that displays its username and photo. From now on, the previous link will redirect to this homepage.