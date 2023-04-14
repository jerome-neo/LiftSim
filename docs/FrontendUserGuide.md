---
layout: page
title: Front End User Guide
---

LiftSim is a web application designed for the building management officer to simulate the movement processes and monitor the overall crowdedness and waiting time of three lifts at S16

## Quick start

1. Ensure you have Python `3.9` or above installed in your Computer.

2. Download the zip file or clone the whole repository.

3. Open the terminal and change directory to this folder.

--------------------------------------------------------------------------------------------------------------------

## How to run our web application using Docker container

**1. Install Docker Desktop** 
- Mac Installation (https://docs.docker.com/desktop/install/mac-install/)
- Windows Installation (https://docs.docker.com/desktop/install/windows-install/)
- Linux Installation (https://docs.docker.com/desktop/install/linux-install/)

**2. Please run the following code to run our docker image in your localhost:**

```linux 
docker compose up
```

**3. Open your Docker Desktop, and check whether the docker container is running**

<p align="center">
    <img src="https://github.com/jerome-neo/DSA3101-07-S16/blob/front-end/docs/images/Submit.jpg">
</p>

**4. How to use our web application**

- Open http://localhost:9000/simulation to visit our simulation page
- Functions of the web application

1. Generate Lift System Simulation

   a. With manual input:
   
   Users can input manually with 'Add Request' button. For each request, the user needs to have three inputs: Timestamp (HH:MM, for e.g., 10:03), Source floor (for
   e.g., 1), and Destination floor (for e.g., 3). Users could have multiple requests for one run, simply by clicking 'Add Request' button repeatedly and adding
   inputs. Request will be deleted with the 'Remove Request Set' button on the right. The simulation process will be triggered by pressing 'Submit' below the
   requests chunk. The 'Refresh Speed' slider is for adjusting the speed of the simulation process.
   ![image](https://drive.google.com/file/d/1e2oX4eD7IHrrfcF7TQp8cXGNifmC0REA/view?usp=share_link).jpg
   ![image](https://drive.google.com/file/d/1bdcE3GlMHcbfRrqNQhAmpI_1jlFJgaIL/view?usp=share_link)

   b. Without manual input/Randomized input:
   
   If there is no request submitted, by pressing the 'Start' button above the simulation block, output with randomized input will be passed to the application and
   displayed on the simulated lift system. Users can pause the process by pressing 'Pause/Resume' button and resume the process by pressing that button again.
   Lastly, the process will end when pressing the 'End' button. Similarly, the 'Refresh Speed' slider is for adjusting the speed of the simulation process.
   ![image](https://drive.google.com/file/d/1WoWdj0c4r6e1q088tFNc-xw-rPgrTOzT/view?usp=share_link)

2. Show Summary:
   
   This application also enables users to monitor the overall crowdedness within a new page. By pressing 'Show the Summary Tab' at the bottom, users are directed
   into a HTML file which includes a plot illustrating the number of tasks during a day and a table showing the summary of number of tasks and waiting time for each
   floor. The selector at top left is incorpated to select different time periods while the selector at top right is included to switch between different models for
   comparison.
   ![image](https://drive.google.com/file/d/1bnwvUu_fWB4wIGNAIryDPYgXdKsUQpYU/view?usp=share_link)
