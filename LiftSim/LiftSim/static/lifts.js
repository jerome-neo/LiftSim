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

setTargetFloor(1, 9)
turnOnLight(2, 5)
