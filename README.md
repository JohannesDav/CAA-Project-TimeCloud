# Time Cloud - CAA 2023 Projet - Team Google

<img src="time-cloud.png" style="width:300px"/>

Time Cloud is a cloud-based time logging system designed to automate the tracking of project work hours. It utilizes an IOT device with touchscreen interaction and NFC identification, in conjunction with Google Cloud components, to record work sessions, assign hours to projects, facilitate multi-user collaboration, and generate progress reports.

### Link to the video: https://youtu.be/zGE4gNw6h68
### Link to the live dashboard: https://dashboard-3zkskaydnq-oa.a.run.app/

## Project structure

#### M5Stack Code
The MicroPython code for the M5Stack Core 2 is in the [main.py file](M5Stack/main.py). It can be uploaded to the device, for example, using [the web-based UIFlow IDE](https://flow.m5stack.com/).

#### Google Cloud Functions
[getUserInfo](CloudFunctions/getInfo.py): This Google Cloud Function retrieves user details, their active work status, and associated project information from the BigQuery database using the provided user ID.

[logEvent](CloudFunctions/logEvent.py): This Google Cloud Function logs a timestamped event related to a user and a specific project into the BigQuery database, thereby tracking the user's activity on the project.

#### Google Cloud Run - Flask dashboard server

[main.py](CloudRun/main.py): Flask web application interfacing with Google BigQuery for user and project management. It defines API endpoints for getting user status, user progress, project progress, user and project lists, as well as for adding users, adding projects, and assigning users to projects.

[dashboard.html](CloudRun/templates/dashboard.html): HTML file constructing the user interface of the project management dashboard.

[dashboard.js](CloudRun/static/js/dashboard.js): JavaScript file managing the interaction between the server and the user interface.

[requirements.txt](CloudRun/requirements.txt): Text file listing the Python library dependencies for the application.

[Dockerfile](CloudRun/Dockerfile): Script containing instructions to create a Docker image of the application for deployment on Google Cloud Run. The flask server can be deployed using ```gcloud run deploy```.

#### Google BigQuery Tables
Schema of the BigQuery Tables generated with ```bq show --schema --format=prettyjson [Table]``` in the cloud console.

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

## Hardware Used

[M5Stack Core 2](https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit-for-aws-iot-edukit)

[Adafruit PN532 breakout board](https://www.adafruit.com/product/364)

The jumpers on the PN532 board should be set to SPI mode. The reader is connected to the [M5Stack's SPI port](https://static-cdn.m5stack.com/resource/docs/products/core/core2/core2_mbus_01.webp) and 3.3v power. The SSEL (chip select) can be connected to any free GPIO pin, for example, GPIO27.

<br />
<br />

#### Time Cloud: Helping you punch time right on the nose!
<img src="modern-times-time-clock.jpg" width="400px">

