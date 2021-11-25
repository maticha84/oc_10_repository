![logo](https://github.com/maticha84/oc_10_repository/blob/master/img/logo.png)

# README for SoftDesK_API
___
## Description
___
This API is made for create an issue tracking system on 3 plateformS (WEB, ANDROID, iOS).
all of the enpoints of this API are comment in the Postman documentation bellow : 

Endpoints documentation is here < [Click](https://documenter.getpostman.com/view/16915168/UVC9g4uB) >
(_Made with Postman_)

## Installation
___
At first, you have to install python3 (I use the 3.9.6 version). You can find on the official site Python your version for Windows /Linux/ Mac.

Then you need to install a new environment for running the application, containing the packages included in the file requirement.txt .To do this, please follow the instructions below:

Create a virtual environment at the root of the project, using the command python -m venv env. Then, activate this environment :

---
    Windows: venv\Scripts\activate.bat
---
    Linux & Mac: source venv/Scripts/activate
---
After that, install the requirement.txt with using this command : `pip install -r requirements.txt`

Then, go to the root project folder, and run the following command: 

---
    ../> py manage.py runserver
---

It will be start the server to this address : [127.0.0.1:8000](http://127.0.0.1:8080)


If you want to run the application without using the database provided in the project, you can. 

First, you have to migrate the project using the command bellow to create a new database : 

---
    ../> py manage.py migrate
---

When the server is started, you can use the enpoints of the API, above using the documentation provided earlier
___
___
## List of endpoints (URI): 
___
### Authentication
___
__/singup/__ 

    --> POST: to create an account

__/login/__  
    
    --> POST: to reciept a token acces and a token refresh when you use a correct account
    'ACCESS_TOKEN_LIFETIME': 5 minutes
    'REFRESH_TOKEN_LIFETIME': 1 days

__/login/refresh/___

    --> POST: to reciept a new access token using the refresh token.

### Projects - only authenticated users 
___
__/projects/__
    
    - All project's contributor: 
    --> GET: Recieve all project concerned by the authenticated user
    --> POST: Create a new project - the author will be the login user. 

__/projects/{id}/__

    - All project's contributor: 
    --> GET: Recieve information concerned the selectionned project.

    - Project's authors only: 
    --> PUT: Update of the project. 
    fields : title, description, type 
    --> DELETE: Delete one project. 

### Contributors - only authenticated users 
___

__/projects/{id}/contibutors/__
    
    - All project's contributor: 
    --> GET: Recieve all contributor concerned by the project
    
    - Project's authors only: 
    --> POST: add a new contributor

__/projects/{id}/contibutors/{id}__

    - Project's authors only: 
    --> DELETE: Delete a project's contributor.

### Issues _ only authenticated users
___

__/projects/{id}/issues/__

    - All project's contributor: 
    --> GET: Recieve all issues concerned by the project
    --> POST : create an issue for the project. The author of this issue will be automatically the login user.
    fields : title, desc, tag, priority, status, assignee_user

__/projects/{id}/issues/{id}/__
    
    - Issue's author only:
    --> PUT: Update the issue.
    fields : title, desc, tag, priority, status, assignee_user
    --> DELETE: delete the comment

### Comments _ only authenticated users
___

__/projects/{id}/issues/{id}/comments/__
    
    - All project's contributor: 
    --> GET: Recieve all comments concerned by the issue
    --> POST : create a comment for the project. The author of this comment will be automatically the login user.
    fields : description

__/projects/{id}/issues/{id}/comments/{id}/__
    
    - All project's contributor: 
    --> GET: Recieve comment using his id

    - Comment's author only:
    --> PUT: update the description filed of a comment
    --> DELETE: Delete a comment.

### Warning - DELETE PROJECT

When a project is deleted by a project's author, every contributors, issues and comments objects
concerned by the project will be destroy to.

### Examples and documentation : 

A documentation with examples made with Postman is published [Here](https://documenter.getpostman.com/view/16915168/UVC9g4uB)
    