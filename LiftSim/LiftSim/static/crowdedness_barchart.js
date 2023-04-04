var data=window.data1Person;
var selectedAlog="Otis";
var selectedTime="The Whole Day";
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
          backgroundColor: 'rgba(245, 166, 35, 0.8)',
          borderColor: 'rgba(245, 166, 35, 1)',
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
            maxRotation: 0,
            autoSkip: false,
            callback: function (value, index, values) {
              if (index % 2 === 1) {
                return `${value}    `.padEnd(20, ' '); // pad the label with spaces to move it to the right by 50 pixels
              } else {
                return '';
              }
              
            }
          },
          gridLines: {
            drawOnChartArea: false
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
  

  let origin_xaxis=myChart.data.labels;
  const timeSelector = document.getElementById('time-selector');
  const elevatorAlgorithmSelector = document.getElementById('elevator-algorithm-selector');
  timeSelector.addEventListener('change', () => {
    selectedTime= timeSelector.value
    updateChart(selectedTime,selectedAlog);
  });

  elevatorAlgorithmSelector.addEventListener('change', () => {
    selectedAlog= elevatorAlgorithmSelector.value;
    updateChart(selectedTime,selectedAlog);
  });
  

  function updateChart(selectedTime,selectedAlog) {
    
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

    let startTime = 0;
    let endTime = dataPoints.length;
    const myHeading = document.querySelector('#my-heading');
    myHeading.textContent = "Number of Task During "+selectedTime+" with "+selectedAlog+" Alogrithm";
    switch (selectedTime) {
      case 'Morning':
        startTime = 0;
        endTime = dataPoints.findIndex(({ x }) => parseInt(x.split(':')[0]) === 12);
        break;
      case 'Afternoon':
        startTime = dataPoints.findIndex(({ x }) => parseInt(x.split(':')[0]) === 12);
        endTime = dataPoints.findIndex(({ x }) => parseInt(x.split(':')[0]) === 18);
        break;
      case 'Evening':
        startTime = dataPoints.findIndex(({ x }) => parseInt(x.split(':')[0]) === 18);
        endTime = dataPoints.length;
        break;
      default:
        break;
    }
  
    const newData = dataPoints.slice(startTime, endTime);
    const newLabels = origin_xaxis.slice(startTime, endTime);
    myChart.data.datasets[0].data = newData;
    myChart.data.labels = newLabels;
    myChart.update();
  }