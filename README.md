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

## Server: `app.py`

  - running on `port=5000`

responsible for backend management


### Admin Pages

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

## API: `API.py`

  - running on `port=5100`

Set of API access points the backend server has to communicate with the microservices.

## Microservices

Set of independent services that provide several information to the main backend server.

### Rooms: `rooms.py`

  - running on `port=5400`
  - API interaction to Fenix
  - API interaction to server (Read)

### Secretariats: `secretariats.py`

  - running on `port=5200`
  - API interaction to server (R/Write)

### Canteen: `canteen.py`

  - running on `port=5300`
  - API interaction to Fenix
  - API interaction to server (R)

## Mobile application: `mobile.py`

  - running on `port=5000` (should be changed to 5500, for example)
