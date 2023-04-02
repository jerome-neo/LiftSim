// Function to create a set of three input fields
function createInputSet() {
  const inputSet = document.createElement("div");
  inputSet.className = "input-container";
  
  // Create three input fields
  const input1 = document.createElement("input");
  input1.type = "text";
  input1.name = "No. of people taking the lift";
  input1.placeholder = "No. of people taking the lift";
  inputSet.appendChild(input1);

  const input2 = document.createElement("input");
  input2.type = "text";
  input2.name = "Source";
  input2.placeholder = "Source";
  inputSet.appendChild(input2);

  const input3 = document.createElement("input");
  input3.type = "text";
  input3.name = "Destination";
  input3.placeholder = "Destination";
  inputSet.appendChild(input3);


  // Create the submit button
  const submitBtn = document.createElement("button");
  submitBtn.type = "submit";
  submitBtn.innerHTML = "Submit";

  // Add event listener to submit button
  submitBtn.addEventListener("click", (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();
  
    // Get the input values
    const input1Value = input1.value;
    const input2Value = input2.value;
    const input3Value = input3.value;
  
    // Store the input values in an object
    const inputValues = {
      "No. of people taking the lift": input1Value,
      "Source": input2Value,
      "Destination": input3Value
    };
  
    // Do something with the input values
    console.log(inputValues);
  });

  // Create the remove button
  const removeBtn = document.createElement("button");
  removeBtn.className = "remove-btn";
  removeBtn.innerHTML = "Remove Request Set";

  // Add event listener to remove button
  removeBtn.addEventListener("click", () => {
    inputSet.remove();
  });

  // Append remove button to input set
  inputSet.appendChild(removeBtn);

  // Append input set to container
  const container = document.getElementById("input-container");
  container.appendChild(inputSet);
}


// Add event listener to "Add Request" button
const addBtn = document.getElementById("add-btn");
addBtn.addEventListener("click", () => {
  createInputSet();
});





// Add event listener to start button
const startBtn = document.getElementById("start-btn");
startBtn.addEventListener("click", () => {
  updateFloors(1,keys1,data1);
  updateFloors(2,keys2,data2);
});

// Add event listener to end button
const endBtn = document.getElementById("end-btn");
endBtn.addEventListener("click", () => {
  stopSimulationFlag = true;
  stopSimulation(1);
  stopSimulation(2);
});

// Append start button to input set
inputSet.appendChild(startBtn);

// Create the pause button
const pauseBtn = document.createElement("button");
pauseBtn.type = "button";
pauseBtn.innerHTML = "Pause";

// Add event listener to pause button
let timerId;
pauseBtn.addEventListener("click", () => {
  if (timerId) {
    // Pausing the simulation
    clearInterval(timerId);
    timerId = null;
    pauseBtn.innerHTML = "Resume";
  } else {
    // Resuming the simulation
    timerId = setInterval(updateFloors, 2000);
    pauseBtn.innerHTML = "Pause";
  }
});

// Append pause button to input set
inputSet.appendChild(pauseBtn);



// Append end button to input set
inputSet.appendChild(endBtn);



