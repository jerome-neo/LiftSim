
  console.log(data)
  const summaryData = {};
  data.forEach((row) => {
	const { curr, wait_time } = row;
	if (!summaryData[curr]) {
	  summaryData[curr] = {
		tasks: 0,
		totalWaitTime: 0
	  };
	}
	summaryData[curr].tasks++;
	summaryData[curr].totalWaitTime += wait_time;
  });

  const tableBody = document.getElementById('table-body');
  for (let i = 1; i <= 9; i++) {
	const rowData = summaryData[i];
	const tasks = rowData ? rowData.tasks : 0;
	const totalWaitTime = rowData ? rowData.totalWaitTime : 0;
	const avgWaitTime = tasks > 0 ? totalWaitTime / tasks : 0;
	
	const tr = document.createElement('tr');
	
	const tdFloor = document.createElement('td');
	tdFloor.innerText = i;
	tr.appendChild(tdFloor);
	
	const tdTasks = document.createElement('td');
	tdTasks.innerText = tasks;
	tr.appendChild(tdTasks);
	
	const tdTotalWaitTime = document.createElement('td');
	tdTotalWaitTime.innerText = totalWaitTime.toFixed(2);
	tr.appendChild(tdTotalWaitTime);
	
	const tdAvgWaitTime = document.createElement('td');
	tdAvgWaitTime.innerText = avgWaitTime.toFixed(2);
	tr.appendChild(tdAvgWaitTime);
	
	tableBody.appendChild(tr);
  }


  elevatorAlgorithmSelector.addEventListener('change', () => {
    selectedAlog= elevatorAlgorithmSelector.value;
    updateTable(selectedAlog);
  });
function updateTable(selectedAlog){
	switch (selectedAlog) {
		case "Otis":
		  data=window.data1Person;
		  console.log(data);
		  break;
		case "ModernEGCS":
		  data=window.data2Person;
		  console.log(data);
		  break;
		default:
		  break;
	  }
	console.log(data)
  const summaryData = {};
  data.forEach((row) => {
	const { curr, wait_time } = row;
	if (!summaryData[curr]) {
	  summaryData[curr] = {
		tasks: 0,
		totalWaitTime: 0
	  };
	}
	summaryData[curr].tasks++;
	summaryData[curr].totalWaitTime += wait_time;
  });
  
  const tableBody = document.getElementById('table-body');
  while (tableBody.firstChild) {
	tableBody.removeChild(tableBody.firstChild);
  }
  for (let i = 1; i <= 9; i++) {
	const rowData = summaryData[i];
	const tasks = rowData ? rowData.tasks : 0;
	const totalWaitTime = rowData ? rowData.totalWaitTime : 0;
	const avgWaitTime = tasks > 0 ? totalWaitTime / tasks : 0;
	
	const tr = document.createElement('tr');
	
	const tdFloor = document.createElement('td');
	tdFloor.innerText = i;
	tr.appendChild(tdFloor);
	
	const tdTasks = document.createElement('td');
	tdTasks.innerText = tasks;
	tr.appendChild(tdTasks);
	
	const tdTotalWaitTime = document.createElement('td');
	tdTotalWaitTime.innerText = totalWaitTime.toFixed(2);
	tr.appendChild(tdTotalWaitTime);
	
	const tdAvgWaitTime = document.createElement('td');
	tdAvgWaitTime.innerText = avgWaitTime.toFixed(2);
	tr.appendChild(tdAvgWaitTime);
	
	tableBody.appendChild(tr);
  }
}