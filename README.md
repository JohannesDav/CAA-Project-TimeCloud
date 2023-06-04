# Time Cloud - CAA 2023 Projet - Team Google

### Link to the video: 
### Link to the live dashboard: https://dashboard-3zkskaydnq-oa.a.run.app/

<!---
![Charlie Chaplin Modern Times - Time Clock Scene](modern-times-time-clock.jpg width="100" height="100")
-->
<img src="modern-times-time-clock.jpg" width="40%">


## Project structure

#### M5Stack Micropython

#### Google Cloud Functions

#### Google Cloud Run - Flask server

#### Google BigQuery Tables
Schema of the BigQuery Tables generated with ``` bq show --schema --format=prettyjson [Table]``` in the cloud console.

##### Users
```
[
  {
    "mode": "REQUIRED",
    "name": "id",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "name",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "workHours",
    "type": "FLOAT"
  }
]
```

##### Projects
```
[
  {
    "mode": "REQUIRED",
    "name": "id",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "name",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "projectHours",
    "type": "FLOAT"
  }
]
```

##### ProjectUsers: defines the many-to-many relationship between Users and Projects
```
[
  {
    "mode": "REQUIRED",
    "name": "userId",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "projectId",
    "type": "STRING"
  }
]
```

##### Events: An event in written every time a user clocks in or out from a work session
```
[
  {
    "mode": "REQUIRED",
    "name": "userId",
    "type": "STRING"
  },
  {
    "mode": "REQUIRED",
    "name": "logTime",
    "type": "TIMESTAMP"
  },
  {
    "mode": "NULLABLE",
    "name": "projectId",
    "type": "STRING"
  }
]
```
