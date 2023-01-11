# Coin Glass API and MongoDB
This project is built in order to pull data from ***Coin Glass API*** and store required into collections in ***MongoDB***. Then, collect data stored in db and save in local as json files.

## Requirements
Python version > 3.8
Modules:
```
pip install "pymongo[srv]"
or
python -m  pip install "pymongo[srv]"

pip install requests
pip install json
```

## Setup
Set your parameters in ***io_params.json*** file for which segments to get from Coin Glass API and store into database in MongoDB.

### MongoDB Setup
Create a cluster and a database in that cluster.

In **_DatabaseManager.py_**, edit `self.connection_string`. Set this variable to the connection string of your database:
```
"mongodb+srv://<user>:<pw>@<clustername.clusterid>.mongodb.net/?retryWrites=true&w=majority"
```
> user and pw are credentials to connect to your cluster.

![Connection](/assets/clusterConnection.jpg)


Then set `self.db_name` to your database name where collections will be stored in.
![DB Name](/assets/clusterDB.jpg)


### API to DataBase

(Optional) In **_Main.py_**, define these variables:
```
self.disabled = [""]  # segment name from io_params.json to not take into account.

self.time_interval = 5  # seconds to wait for the next run.
```

### DataBase to Local

This handles everything itself.


## Use
### API to DataBase
To store data in database from Coin Glass API, you can simply run ***Main.py***. It will collect data and store in given time interval defined in **_Setup_** section.
***Main.py*** utilizes ***coinglassApi.py***, ***DatabaseManager.py*** and ***io_params.json***

> Time interval between each run can depend on the time it takes to get and store data.

### DataBase to Local
Simply run ***LocalJsonSaver.py***. This script utilizes ***DatabaseManager.py*** and ***io_params.json***.
