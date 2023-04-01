// Define variables
let passengers = [];

// Define functions
function addPassenger() {
  const numOfPeople = parseInt(document.getElementById("numOfPeople").value);
  const sourceFloor = parseInt(document.getElementById("sourceFloor").value);
  const destinationFloor = parseInt(document.getElementById("destinationFloor").value);
  
  // Validate input
  if (numOfPeople <= 0 || sourceFloor < 1 || sourceFloor > 10 || destinationFloor < 1 || destinationFloor > 10) {
    alert("Please enter valid input.");
    return;
  }
  
  // Add passenger to list
  passengers.push({
    numOfPeople: numOfPeople,
    sourceFloor: sourceFloor,
    destinationFloor: destinationFloor
  });
  
  // Add passenger to lift queue
  addPassengerToQueue(numOfPeople, sourceFloor, destinationFloor);
  
  // Clear input fields
  document.getElementById("numOfPeople").value = "";
  document.getElementById("sourceFloor").value = "";
  document.getElementById("destinationFloor").value = "";
}

function addPassengerToQueue(numOfPeople, sourceFloor, destinationFloor) {
  // Calculate which lift to add the passenger to
  let liftNumber = 1;
  let minDistance = getDistance(1, sourceFloor);
  for (let i = 2; i <= 3; i++) {
    const distance = getDistance(i, sourceFloor);
    if (distance < minDistance) {
      liftNumber = i;
      minDistance = distance;
    }
  }
  
  // Add passenger to lift queue
  const liftQueue = document.getElementById("lift" + liftNumber);
  const listItem = document.createElement("li");
  listItem.textContent = numOfPeople + " person(s) from floor " + sourceFloor + " to floor " + destinationFloor;
  liftQueue.appendChild(listItem);
}

function getDistance(liftNumber, floorNumber) {
  // Calculate distance between lift and floor
  const liftPosition = (liftNumber - 1) * 3 + 2;
}

const elevatorStatus = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0], // Elevator 1
  [0, 0, 0, 0, 0, 0, 0, 0, 0], // Elevator 2
  [0, 0, 0, 0, 0, 0, 0, 0, 0]  // Elevator 3
];

// Set a certain elevator to the target floor
function setTargetFloor(elevatorNumber, floorNumber) {
  elevatorStatus[elevatorNumber - 1][floorNumber - 1] = 1;
  // Get the corresponding DOM element of the floor
  const floorElement = document.getElementById(`e${elevatorNumber}f${floorNumber}`);
  // Modify the style of the DOM element
  floorElement.classList.add('target');
}

function rmTargetFloor(elevatorNumber, floorNumber) {
  elevatorStatus[elevatorNumber - 1][floorNumber - 1] = 1;
  // Get the corresponding DOM element of the floor
  const floorElement = document.getElementById(`e${elevatorNumber}f${floorNumber}`);
  // Modify the style of the DOM element
  floorElement.classList.remove('target');
}

// Turn On the light of a certain floor in a certain elevator
function turnOnLight(elevatorNumber, floorNumber) {
  elevatorStatus[elevatorNumber - 1][floorNumber - 1] = 1;
  // Get the corresponding DOM element of the floor
  const floorElement = document.getElementById(`e${elevatorNumber}f${floorNumber}`);
  // Modify the style of the DOM element
  floorElement.classList.add('on');
}

// Turn off the light of a certain floor in a certain elevator
function turnOffLight(elevatorNumber, floorNumber) {
  elevatorStatus[elevatorNumber - 1][floorNumber - 1] = 0;
  // Get the corresponding DOM element of the floor
  const floorElement = document.getElementById(`e${elevatorNumber}f${floorNumber}`);
  // Modify the style of the DOM element
  floorElement.classList.remove('on');
}

//setTargetFloor(1, 9)
//turnOnLight(2, 5)

data={
    "0": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "27": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "40": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 1,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 2
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "49": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 2
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 1,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "66": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "92": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 1,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "99": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "126": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "131": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 1,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "135": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 1,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "139": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 1,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "144": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 1,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "149": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 1
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "159": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "163": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 1,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "167": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 1,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "184": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 1,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "192": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ],
    "197": [
        {
            "1": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 1
                },
                "num_passengers": 0
            }
        },
        {
            "2": {
                "elevator_type": 1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 1
            }
        },
        {
            "3": {
                "elevator_type": -1,
                "floor": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 1,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0
                },
                "num_passengers": 0
            }
        }
    ]
}


//const data = JSON.parse(receivedJSON);
//keys is the sorted timestamps, keys[0] is the first timestamp
const keys = Object.keys(data).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received

//use closure to solve the issue of setTimeout function
function updateFloors() {
  for (let i = 0; i < keys.length; i++) {
    setTimeout((function(i) {
      return function() {
        const value = data[keys[i]];
        const lift1info = value[0]["1"];
        const lift2info = value[1]["2"];
        const lift3info = value[2]["3"];
        const lift1floor = lift1info["floor"];
        const lift2floor = lift2info["floor"];
        const lift3floor = lift3info["floor"];
        turnOffAllLight();
        updateEachFloor(1, lift1floor);
        updateEachFloor(2, lift2floor);
        updateEachFloor(3, lift3floor);
      }
    })(i), i * 2000);
  }
}

updateFloors();


/*async function main() {
  //const data = JSON.parse(receivedJSON);
  const keys = Object.keys(data).sort((a, b) => parseInt(a) - parseInt(b));

  await updateFloors(keys);
}

main().catch(error => console.error(error));
async function updateFloors(keys) {
  for (const key of keys) {
    const value = data[key];
    const lift1info = value[0]["1"];
    const lift2info = value[1]["2"];
    const lift3info = value[2]["3"];
    const lift1floor = lift1info["floor"];
    const lift2floor = lift2info["floor"];
    const lift3floor = lift3info["floor"];

    await new Promise(resolve => setTimeout(resolve, 2000)); // 等待两秒钟

    updateEachFloor(1, lift1floor);
    updateEachFloor(2, lift2floor);
    updateEachFloor(3, lift3floor);
  }
}*/

/*keys.forEach(key => {
  const value = data[key]; //lift "1","2","3"
  const lift1info = value[0]["1"];
  const lift2info = value[1]["2"];
  const lift3info = value[2]["3"];
  const lift1floor = lift1info["floor"];
  const lift2floor = lift2info["floor"];
  const lift3floor = lift3info["floor"];
  const updateFloors = () => {
    updateEachFloor(1, lift1floor);
    updateEachFloor(2, lift2floor);
    updateEachFloor(3, lift3floor);
  };
  setTimeout(updateFloors, 2000);
});

function updateFloors() {
    for (let i = 0; i < keys.length; i++) {
        setTimeout(() => {
        const value = data[keys[i]];
        const lift1info = value[0]["1"];
        const lift2info = value[1]["2"];
        const lift3info = value[2]["3"];
        const lift1floor = lift1info["floor"];
        const lift2floor = lift2info["floor"];
        const lift3floor = lift3info["floor"];
        //turnOffAllLight();
        updateEachFloor(1, lift1floor);
        updateEachFloor(2, lift2floor);
        updateEachFloor(3, lift3floor);
        }, 2000);
    }
}
updateFloors();

const data = JSON.parse(receivedJSON);
const keys = Object.keys(data).sort((a, b) => parseInt(a) - parseInt(b));

//recursive version
function updateFloors(index) {
  if (index >= keys.length) {
    return;
  }

  const value = data[keys[index]];
  const lift1info = value[0]["1"];
  const lift2info = value[1]["2"];
  const lift3info = value[2]["3"];
  const lift1floor = lift1info["floor"];
  const lift2floor = lift2info["floor"];
  const lift3floor = lift3info["floor"];

  updateEachFloor(1, lift1floor);
  updateEachFloor(2, lift2floor);
  updateEachFloor(3, lift3floor);

  setTimeout(() => {
    updateFloors(index + 1);
  }, 2000);
}

updateFloors(0);*/

function turnOffAllLight() {
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 9; j++) {
      const floorElement = document.getElementById(`e${i + 1}f${j + 1}`);
      floorElement.classList.remove('on');
      floorElement.classList.remove('target');
    }
  }
}


function updateEachFloor(lift, floorStatus) {
    for (let i = 0; i < 9; i++) {
      const floorElement = document.getElementById(`e${lift}f${i + 1}`);
      if (floorStatus[String(i+1)] === 1) {
        floorElement.classList.add('on');
      } else if (floorStatus[String(i+1)] === 2) {
        floorElement.classList.add('target');
      } else {
        floorElement.classList.remove('on');
        floorElement.classList.remove('target');
      }
    }
}

//updateEachFloor(1, {"1": 0, "2": 0, "3": 1, "4": 0, "5": 0, "6": 0, "7": 2, "8": 0, "9": 0})
//updateEachFloor(2, {"1": 0, "2": 0, "3": 0, "4": 0, "5": 1, "6": 0, "7": 0, "8": 0, "9": 2})
//updateEachFloor(3, {"1": 0, "2": 1, "3": 0, "4": 2, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0})
//floorStatus = {"1": 1, "2": 0, "3": 1, "4": 0, "5": 0, "6": 0, "7": 2, "8": 0, "9": 0}

/*function updateElevatorStatus(elevatorStatus) {
  for (let i = 0; i < elevatorStatus.length; i++) {
    for (let j = 0; j < elevatorStatus[i].length; j++) {
      const floorElement = document.getElementById(`e${i + 1}f${j + 1}`);
      if (elevatorStatus[i][j] === 1) {
        floorElement.classList.add('on');
      } else if (elevatorStatus[i][j] === 2) {
        floorElement.classList.add('target');
      } else {
        floorElement.classList.remove('on');
        floorElement.classList.remove('target');
      }
    }
  }
}


const currentStatus = [
  [0, 0, 0, 1, 0, 0, 2, 0, 0], // Elevator 1
  [0, 0, 1, 0, 0, 0, 0, 2, 0], // Elevator 2
  [0, 0, 0, 0, 1, 0, 2, 0, 0]  // Elevator 3
];
updateElevatorStatus(currentStatus)*/