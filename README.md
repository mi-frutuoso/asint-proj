# ASInt project

ASInt project - 1st semester 2019/2020

The goal of this project is to develop a web application that makes use of the resources of IST, via FenixEdu API, using custom services that store important resources, accessible by WEB and REST interfaces. It was developed under the course `Internet Based Systems Architecture` (ASInt).

## Authors

This project was developed by the students:

- [81305 - Pedro Direita]

- [84303 - Maria Frutuoso]

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

## Entities  

### Server: `app.py`

  - running on `port=5000`

responsible for backend management


#### Admin Pages

TODO: admin authentication

Check all existing secretariats (with link to edit and delete a specific one):

````
http://127.0.0.1:5000/frontend/listSecretariats
````

  - associated templates: `secretariats.html`, `edit.html`

Add a new secretariat:

````
http://127.0.0.1:5000/frontend/addSecretariat
````

  - associated template: `add.html`

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
  - API interaction to server (R/Write)

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

  - running on `port=5000` (should be changed to 5500, for example)

Main page that redirects to a custom FenixEdu application webpage that asks the user its authorization to use their account (personal information) in that application:

````
http://127.0.0.1:5000/
````

If the user authorizes, they will be redirected to a homepage that displays its username and photo. From now on, the previous link will redirect to this homepage.