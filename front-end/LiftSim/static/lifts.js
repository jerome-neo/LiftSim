//const data = JSON.parse(receivedJSON);
//keys is the sorted timestamps, keys[0] is the first timestamp
//const keys1 = Object.keys(data1).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received
//const keys2 = Object.keys(data2).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received

let stopSimulationFlag = false;
let pauseSimulationFlag = false;

//use closure to solve the issue of setTimeout function => use setInterval to solve the problem caused by setTimeout
function updateFloors(model,key,data,time) {
  let i = 0;
  let interval = setInterval(fn, time);
  function fn() {
    //document.getElementById("loop-counter").textContent = "Loop Counter: " + key[i];
    if (stopSimulationFlag) { // If the flag is true, then exit the loop
      clearInterval(interval);
      return;
    }
    if (pauseSimulationFlag) {
      return;
    }
    const value = data[key[i]];
    const lift1info = value[0]["1"];
    const lift2info = value[1]["2"];
    const lift3info = value[2]["3"];
    const lift1type = lift1info["elevator_type"];
    const lift2type = lift2info["elevator_type"];
    const lift3type = lift3info["elevator_type"];
    const lift1floor = lift1info["floor"];
    const lift2floor = lift2info["floor"];
    const lift3floor = lift3info["floor"];
    const lift1people = lift1info["num_passengers"];
    const lift2people = lift2info["num_passengers"];
    const lift3people = lift3info["num_passengers"];


    updateEachFloor(model, 1, lift1type, lift1floor, lift1people);
    updateEachFloor(model, 2, lift2type, lift2floor, lift2people);
    updateEachFloor(model, 3, lift3type, lift3floor, lift3people);
    i++;
    time = refreshTime;
    clearInterval(interval);
    interval = setInterval(fn, time);
    if (i >= key.length) {
      clearInterval(interval);
    }
    console.log(time);
  }
}



function stopSimulation(model) {
  stopSimulationFlag = true;
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 9; j++) {
        const liftElement = document.getElementById(`m${model}e${i + 1}`);
        const floorElement = document.getElementById(`m${model}e${i + 1}f${i + 1}`);
        const numPeopleElement = floorElement.querySelector('.numPeople');
        const elevatorTypeElement = liftElement.querySelector('.elevatorType');
        numPeopleElement.innerHTML = "0";
        elevatorTypeElement.innerHTML = "NIL";
        updateEachFloor(model, i + 1, 0, {}, 0);
    }
  }
}

function updateEachFloor(model, lift, typeStatus, floorStatus, peopleStatus) {
    for (let i = 0; i < 9; i++) {
      const liftElement = document.getElementById(`m${model}e${lift}`);
      const floorElement = document.getElementById(`m${model}e${lift}f${i + 1}`);
      const numPeopleElement = floorElement.querySelector('.numPeople');
      const elevatorTypeElement = liftElement.querySelector('.elevatorType');
      // Clear the Lift status
      liftElement.classList.remove('on');
      liftElement.classList.remove('target');
      if (typeStatus === 1) {
          elevatorTypeElement.innerHTML = "UP";
      } else if (typeStatus === -1) {
          elevatorTypeElement.innerHTML = "DOWN";
      } else {
          elevatorTypeElement.innerHTML = "NIL";
      }
      if (floorStatus[String(i+1)] === 1) {
        floorElement.classList.add('on');
        numPeopleElement.innerHTML = peopleStatus;
      } else if (floorStatus[String(i+1)] === 2) {
        floorElement.classList.add('target');
      } else {
        floorElement.classList.remove('on');
        floorElement.classList.remove('target');
        numPeopleElement.innerHTML = "0";
      }
    }
}
