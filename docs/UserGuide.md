---
layout: page
title: User Guide
---

LiftSim is a data science project aimed at improving elevator efficiency and reducing wait times in multi-floor 
buildings, particularly, S16 building at the National University of Singapore (NUS). By utilizing statistical modeling 
techniques and simulation software, LiftSim provides valuable insights into elevator performance and management. 

* Table of Contents
{:toc}

--------------------------------------------------------------------------------------------------------------------

## Quick start

1. Ensure you have Python `3.9` or above installed in your Computer.

2. Download the latest `____`(Coming soon!)


--------------------------------------------------------------------------------------------------------------------

## How to run our simulation model API using Docker container

**1. Install Docker Desktop** 
- Mac Installation (https://docs.docker.com/desktop/install/mac-install/)
- Windows Installation (https://docs.docker.com/desktop/install/windows-install/)
- Linux Installation (https://docs.docker.com/desktop/install/linux-install/)

**2. Please run the following code to run our docker image in your localhost:**

```linux 
docker run --name lift123 -p 9001:5000 -d kevinchs0808/liftsim
```

Take note that you can change the name 'lift123' to any text that you want (without space).

**3. Open your Docker Desktop, and check whether the docker container is running**

![image](https://user-images.githubusercontent.com/62506934/230116962-c54e4c71-4d1d-4280-8efe-1c8ecf378069.png)
  
**4. How to make a request?**

```code python 
**PYTHON**
# Manual Input from User
test = requests.get('http://127.0.0.1:9001/manual', json=json_data)
result = test.json()

# Random Dataset Generator
test = requests.get('http://127.0.0.1:9001/random')
result = test.json()
```
```code javascript 
**JAVASCRIPT**
# Manual Input from User
fetch('http://127.0.0.1:9001/manual', {
    method: 'POST',
    body: inputJson,
    headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    }
  })
      .then(response => response.json())

# Random Dataset Generator
fetch('http://localhost:9001/random')
    .then(response => response.json())
```

**5. What is the expected manual user input?**

A string format of json data with the following format:

```python
json_data = '''
[
    {
        "Time":"16:04", 
        "Source":"2", 
        "Destination":"8"
    },
    {
        "Time":"16:32", 
        "Source":"3", 
        "Destination":"1"
    },
    {
        "Time":"17:54", 
        "Source":"1", 
        "Destination":"3"
    }
]'''
```

**6. What will the API return for both manual and random requests?**

```python
data = {
    'Otis':{
      'Elevators': elevators_data_otis, 
      'Persons': persons_data_otis
    }, 
          
    'ModernEGCS':{
      'Elevators': elevators_data_egcs, 
      'Persons': persons_data_egcs
    }
}
```
Note that elevators_data_otis is not a file name, it’s the JSON data inside the file

## Features



### Viewing help : `help`

Description

Format:

Example:



### Adjusting arrival rate : "???"

Description

Format:

Example:



