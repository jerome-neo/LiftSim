const data = [];
for (let i = 0; i < 100; i++) {
  const curr = Math.floor(Math.random() * 9) + 1;
  let dest = Math.floor(Math.random() * 9) + 1;
  while (dest === curr) {
    dest = Math.floor(Math.random() * 9) + 1;
  }
  let arrival = Math.floor(Math.random() * 57600) + 21600; // Random time between 6am and 10pm
  let endtime = Math.floor(Math.random() * 57600) + 21600;
  if (arrival >= endtime) {
    // swap the arrivalTime and endTime values
    const temp = arrival;
    arrival = endtime;
    endtime = temp;
  }
  const wait = endtime - arrival;
  data.push({
    curr,
    dest,
    arrival_time: arrival,
    end_time: endtime,
    wait_time: wait,
  });
}
  
  const TIME_BLOCK_SIZE = 3600; // 1 hour block size

  const dataByHour = {};
  for (let i = 6; i < 22; i++) {
	dataByHour[i] = 0;
  }
  
  data.forEach(({ arrival_time, end_time }) => {
	const startBlock = Math.floor(arrival_time / TIME_BLOCK_SIZE);
	const endBlock = Math.ceil(end_time / TIME_BLOCK_SIZE);
	for (let i = startBlock; i < endBlock; i++) {
	  dataByHour[Math.floor(i)]++;
	}
  });
  
  const dataPoints = [];
  for (let i = 6; i < 22; i++) {
	const hour = i < 10 ? `0${i}:00` : `${i}:00`;
	const busyLevel = dataByHour[i];
	dataPoints.push({ x: hour, y: busyLevel });
  }
  
  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dataPoints.map(({ x }) => x),
      datasets: [
        {
          label: 'Busy Level',
          data: dataPoints.map(({ y }) => y),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        zoom: {
          pan: {
            enabled: true,
            mode: 'x',
            speed: 10,
            threshold: 10,
          },
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true,
            },
            mode: 'x',
            speed: 0.1,
            threshold: 2,
          },
        },
      },
      scales: {
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Time'
          },
          ticks: {
            minRotation: 0,
            maxRotation: 90
          },
        }],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: 'Number of Tasks'
            },
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });

  console.log(myChart.data.datasets[0].data)
  console.log(dataPoints)
  let origin_data=dataPoints;
  const timeSelector = document.getElementById('time-selector');

  timeSelector.addEventListener('change', () => {
    updateChart(timeSelector);
  });
  function updateChart(timeSelector) {

    const selectedTime = timeSelector.value;
    let startTime = 0;
    let endTime = origin_data.length;
    
    switch (selectedTime) {
      case 'morning':
        startTime = 0;
        endTime = origin_data.findIndex(({ x }) => parseInt(x.split(':')[0]) === 12);
        break;
      case 'afternoon':
        startTime = origin_data.findIndex(({ x }) => parseInt(x.split(':')[0]) === 12);
        endTime = origin_data.findIndex(({ x }) => parseInt(x.split(':')[0]) === 18);
        break;
      case 'evening':
        startTime = origin_data.findIndex(({ x }) => parseInt(x.split(':')[0]) === 18);
        endTime = origin_data.length;
        break;
      default:
        break;
    }
  
    const newData = origin_data.slice(startTime, endTime);
    myChart.data.datasets[0].data = newData;
    myChart.update();
  }