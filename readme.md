# Client Project API

## Installing Packages
```bash
pip install -r requirement.txt
```
## To Switch Into Project Folder
```bash
cd client_project
```
## Run Project 
```bash
python manage.py runserver
```
## APIs
1. To Login 
```bash
POST /login

Body:
{
   "username" : "devil",
   "password" : "2606"
}
```
2. To logout
```bash
GET /logout
```
3. All Clients
```bash
GET /clients
```
4. Create New Client
```bash
POST /clients

Body:
{
   "client_name" : "company A"
}
```
5. Retrieve info of a client
```bash
GET /clients?id=1
```
6. Update info of a client
```bash
PUT-PATCH /clients?id=2

Body:
{
    "client_name" : "company B"
}
```

7. Delete Client
```bash
DELETE /clients?id=3
```

8. Create Project
```bash
POST /clients/projects?id=1

Body:
{
    "project_name" : "Project A",
    "users" : [
        {
            "id" : 1,
            "name" : "devil"
        }
    ]
}
```
9. Listing all Projects Assigned to logged in user
```bash
GET /projects
```