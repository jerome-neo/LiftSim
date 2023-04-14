---
layout: page
title: User Guide
---

LiftSim is a data science project aimed at improving elevator efficiency and reducing wait times in multi-floor 
buildings, particularly, S16 building at the National University of Singapore (NUS). By utilizing statistical modeling 
techniques and simulation software, LiftSim provides valuable insights into elevator performance and management. 

## Quick start

1. Ensure you have Python `3.9` or above installed in your Computer.

2. Download the latest `____`(Coming soon!)

--------------------------------------------------------------------------------------------------------------------

## How to run our web application using Docker container

**1. Install Docker Desktop** 
- Mac Installation (https://docs.docker.com/desktop/install/mac-install/)
- Windows Installation (https://docs.docker.com/desktop/install/windows-install/)
- Linux Installation (https://docs.docker.com/desktop/install/linux-install/)

**2. Please run the following code to run our docker image in your localhost:**

```linux 
yating
```

Take note that you can change the name 'lift123' to any text that you want (without space).

**3. Open your Docker Desktop, and check whether the docker container is running**

image

**4. How to use our web application**

- Open (https:yating) to visit our simulation page
- Functions of the web application

1. Generate Lift System Simulation

   a. With manual input:
   Users can input manually with 'Add Request' button. For each request, the user needs to have three inputs: Timestamp (HH:MM, for e.g., 21:56), Source floor (for
   e.g., 1), and Destination floor (for e.g., 3). Users could have multiple requests for one run, and the request will be deleted with the 'Remove' button on the
   right. The simulation process will be triggered by pressing 'Submit' below the requests chunk.

   b. Without manual input/Randomized input:
   If there is no request submitted, by pressing the 'Start' button above the simulation block, output with randomized input will be passed to the application and
   displayed on the simulated lift system. Users can pause the process by pressing 'Pause/Resume' button and resume the process by pressing that button again.
   Lastly, the process will end when pressing the 'End' button.

2. Show Summary:
   This application also enables users to monitor the overall crowdedness within a new page. By pressing 'Show the Summary Tab' at the bottom, users are directed
   into a HTML file which includes a plot illustrating the number of tasks during a day and a table showing the summary of number of tasks and waiting time for each
   floor. The selector at top left is incorpated to select different time periods while the selector at top right is included to switch between different models for
   comparison.
