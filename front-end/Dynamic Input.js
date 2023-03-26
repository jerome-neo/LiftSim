// Function to create a set of three input fields
function createInputSet() {
  const inputSet = document.createElement("div");
  inputSet.className = "input-container";

  // Create three input fields
  for (let i = 1; i <= 3; i++) {
    const input = document.createElement("input");
    input.type = "text";
    input.name = "request-" + i;
    input.placeholder = "Request " + i;
    inputSet.appendChild(input);
  }

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





var clock = new Vue({
  el: '#clock',
  data: {
      time: '',
      date: ''
  }
});

var week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
var timerID = setInterval(updateTime, 1000);
updateTime();
function updateTime() {
  var cd = new Date();
  clock.time = zeroPadding(cd.getHours(), 2) + ':' + zeroPadding(cd.getMinutes(), 2) + ':' + zeroPadding(cd.getSeconds(), 2);
  clock.date = zeroPadding(cd.getFullYear(), 4) + '-' + zeroPadding(cd.getMonth()+1, 2) + '-' + zeroPadding(cd.getDate(), 2) + ' ' + week[cd.getDay()];
};

function zeroPadding(num, digit) {
  var zero = '';
  for(var i = 0; i < digit; i++) {
      zero += '0';
  }
  return (zero + num).slice(-digit);
}
