//let data1Person;
//let data2Person;
// Function to create a set of three input fields
function createInputSet() {

  const inputSet = document.createElement("div");
  inputSet.className = "input-container";

  // Create three input fields
  const timeInput = document.createElement("input");
  timeInput.type = "text";
  timeInput.name = "Time";
  timeInput.placeholder = "Arrival Time";
  inputSet.appendChild(timeInput);

  const srcInput = document.createElement("input");
  srcInput.type = "text";
  srcInput.name = "Source";
  srcInput.placeholder = "Source";
  inputSet.appendChild(srcInput);

  const destInput = document.createElement("input");
  destInput.type = "text";
  destInput.name = "Destination";
  destInput.placeholder = "Destination";
  inputSet.appendChild(destInput);

  // Create the remove button
  const removeBtn = document.createElement("button");
  removeBtn.className = "remove-btn";
  removeBtn.innerHTML = "Remove Request Set";

  // Add event listener to remove button
  removeBtn.addEventListener("click", () => {
    inputSet.remove();
    //console.clear();
    //inputs = [];
  });

  // Append remove button to input set
  inputSet.appendChild(removeBtn);

  // Append input set to container
  const formContainer = document.getElementById("form-container");
  formContainer.appendChild(inputSet);

}

let slider;
let refreshTime;
    document.addEventListener("DOMContentLoaded", function() {
      slider = document.getElementById("speed-slider");
      refreshTime = slider.value;

      slider.addEventListener("change", function() {
        refreshTime = slider.value;
        console.log(refreshTime);
      });
});
/*
const slider = document.getElementById("speed-slider");
let refreshTime = 2000;
slider.addEventListener("change", function() {
  refreshTime = slider.value;
});*/

// Add event listener to submit button
const submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", (event) => {
  event.preventDefault();
  let inputs = [];
    // Loop through each input field and add its value to the inputs array
  for (let i = 0; i < document.getElementsByName("Time").length; i++) {
    const inputTime = document.getElementsByName("Time")[i].value;
    //const [hours, minutes] = inputTime.split(":");
    //const input1 = (parseInt(hours) - 6) * 3600 + parseInt(minutes) * 60;
    const input2 = parseInt(document.getElementsByName("Source")[i].value);
    const input3 = parseInt(document.getElementsByName("Destination")[i].value);

    inputs.push({
      "Time": String(inputTime),
      "Source": String(input2),
      "Destination": String(input3)
    });
  }

  // Convert the inputs received to a json.file
  const inputJson = JSON.stringify(inputs);


  // Send JSON to backend using fetch API
  fetch('http://127.0.0.1:9001/manual', {
    method: 'POST',
    body: inputJson,
    headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    }
  })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        const manualData1 = data['Otis']['Elevators'];
        const manualData2 = data['ModernEGCS']['Elevators'];
        const manualKeys1 = Object.keys(manualData1).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received
        const manualKeys2 = Object.keys(manualData2).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received
        stopSimulationFlag = false;
        pauseSimulationFlag = false;
        updateFloors(1,manualKeys1,manualData1,refreshTime);
        updateFloors(2,manualKeys2,manualData2,refreshTime);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
});



// Add event listener to start button
const startBtn = document.getElementById("start-btn");
startBtn.addEventListener("click", () => {
    fetch('http://localhost:9001/random')
    .then(response => response.json())
    .then(data => {
      // Process data from server
      console.log('Success:', data);
      const data1 = data['Otis']['Elevators'];
      const data2 = data['ModernEGCS']['Elevators'];
      window.data1Person = data['Otis']['Persons'];
      window.data2Person = data['ModernEGCS']['Persons'];
      const keys1 = Object.keys(data1).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received
      const keys2 = Object.keys(data2).sort((a, b) => parseInt(a) - parseInt(b)); //sort the json we received
      stopSimulationFlag = false;
      pauseSimulationFlag = false;
      updateFloors(1,keys1,data1,refreshTime);
      updateFloors(2,keys2,data2,refreshTime);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});


// Add event listener to end button
const endBtn = document.getElementById("end-btn");
endBtn.addEventListener("click", () => {
  stopSimulationFlag = true;
  stopSimulation(1);
  stopSimulation(2);
});

// Add event listener to pause button
const pauseBtn = document.getElementById("pause-btn");
pauseBtn.addEventListener("click", () => {
  pauseSimulationFlag = !pauseSimulationFlag;
});


document.addEventListener('DOMContentLoaded', function() {
  const showPageButton = document.getElementById('show-page-btn');
  showPageButton.addEventListener("click", () => {
    showPage();
  });
});

function showPage() {
  // Show the summary page
  window.location.href = "summary";
}


/*const showPageButton = document.getElementById('show-page-btn');
showPageButton.addEventListener("click", () => {
  showPage();
});

function showPage() {
  // Show the summary page
  window.location.href = "summary.html";
}
*/
/*function displayInputs() {

  // Loop through each input field and add its value to the inputs array
  for (let i = 0; i < document.getElementsByName("Arrival Time").length; i++) {
    const inputTime = document.getElementsByName("Arrival Time")[i].value;
    const [hours, minutes] = inputTime.split(":");
    const input1 = hours * 3600 + minutes * 60;
    const input2 = parseInt(document.getElementsByName("Source")[i].value);
    const input3 = parseInt(document.getElementsByName("Destination")[i].value);

    inputs.push({
      "time": input1,
      "src": input2,
      "dest": input3
    });
  }
  console.log(inputs)
}

// Convert array to JSON string
const inputJson = JSON.stringify(inputs);

// Send JSON to backend using fetch API
fetch('http://localhost:5000/manual', {
  method: 'POST',
  body: inputJson,
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
*/

/*function createInputSet() {
*/
/*
  // Create the submit button
  const submitBtn = document.createElement("button");
  submitBtn.type = "submit";
  submitBtn.innerHTML = "Submit";

  // Add event listener to submit button
  submitBtn.addEventListener("click", (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the input values
    const input1Value = timeInput.value;
    const input2Value = srcInput.value;
    const input3Value = destInput.value;

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
  const formContainer = document.getElementById("form-container");
  formContainer.appendChild(inputSet);
  //const container = document.getElementById("input-container");
  //container.appendChild(inputSet);


}
 */