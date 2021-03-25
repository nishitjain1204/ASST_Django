# ASST
 Django-Firebase app for improving Security Systems in housing societies using Face Recognition and IOT 
 <br>
 
<p align='center'><img src="https://github.com/coldkillerr/ASST_Django/blob/master/ASST.png" alt="ASST" height="300" border="0"></p>

## Starting the Django Server

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



 
