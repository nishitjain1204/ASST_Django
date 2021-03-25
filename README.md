# ASST
 Django-Firebase app for improving Security Systems in housing societies using Face Recognition and IOT 
 <br>
 
<p align='center'><img src="https://github.com/coldkillerr/ASST_Django/blob/master/ASST.png" alt="ASST" height="300" border="0"></p>

## How to use the app :

1) Get your society registered with the application . Once the society is registered you have the permission to assign one account to every flat in the society as the admin of that house.

2) Now the admin has the powers to register his house members. These members will be verified by the secretary before registration.

3) Once the registrations are done , every admin will be able to keep a watch on the people who have come to visit him and he has the power to permit them inside or reject them.

4) Now the admin will have to also register a watchman who will recieve live notifications whom to permit and whom to reject.





## Starting the Django Server :

### Setting up firebase credentials :
1) Create a project [here](https://console.firebase.google.com/u/0/)
2) Download the credentials.json from  [firebase project settings](https://console.firebase.google.com). Paste the path to credentials 
[here](https://github.com/coldkillerr/ASST_Django/blob/baa2bb5b0f069a424a07a277542d26ce5acb4aa0/ASST/config.py#L9)
3) Get the firebase SDK snippet from  [firebase project settings](https://console.firebase.google.com). Paste it [here](https://github.com/coldkillerr/ASST_Django/blob/baa2bb5b0f069a424a07a277542d26ce5acb4aa0/ASST/config.py#L13) and [here](https://github.com/coldkillerr/ASST_Django/blob/baa2bb5b0f069a424a07a277542d26ce5acb4aa0/templates/firebase_config.js#L5)

### Setting up the virtualenv
1) Create a virtual environment with
``` 
python3 -m virtualenv yourenv
```
2) Navigate to the project directory and install the requirements with 
```
pip3 install -r requirements.txt
```
3) Make migrations with
```
python3 manage.py migrate
```
4) Run server with 
```
python3 manage.py runserver
```
## 


 
