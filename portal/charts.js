var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        labels: new Array(120).fill(" "),
        datasets: [{
            label: 'Temperature',
            borderColor: 'rgb(0,123,255)',
            lineTension: 0,
            fill: false,
            data: new Array(120).fill(0),
            yAxisID: 'y-axis-1',
        }, {
            label: 'servo_setpoint_history',
            // borderColor: 'rgb(0,123,255)',
            lineTension: 0,
            fill: false,
            data: new Array(120).fill(0),
            yAxisID: 'y-axis-2',
        }, {
            label: 'servo_actual_history',
            // borderColor: 'rgb(0,123,255)',
            lineTension: 0,
            fill: false,
            data: new Array(120).fill(0),
            yAxisID: 'y-axis-3',
        }]
    },
    // Configuration options go here
    options: {
        animation: {
            duration: 0
        },
        scales: {
            yAxes: [{
                id: 'y-axis-1',
                type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                display: true,
                position: 'right',
                scaleLabel: {
                    display: true,
                    labelString: 'Temperature [C]',
                    fontSize: 18,
                    fontFamily: "'Roboto', sans-serif",
                    fontColor: '#007bff'
                },
                ticks: {
                    min: 0,
                    // max: 250,
                    fontColor: '#007bff',
                    fontSize: 18,
                },
            }, {
                id: 'y-axis-2',
                type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                display: true,
                position: 'left',
                ticks: {
                    min: 0,
                    max: 100,
                    fontColor: '#6C757D',
                    fontSize: 18,
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Hob power [%]',
                    fontSize: 18,
                    fontFamily: "'Roboto', sans-serif",
                    fontColor: '#6C757D',
                },
                // grid line settings
                gridLines: {
                    drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
            }, {
                id: 'y-axis-3',
                type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                display: false,
                position: 'right',
                ticks: {
                    min: 0,
                    max: 100,
                },
                // grid line settings
                gridLines: {
                    drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
            }],
            xAxes: [{
                ticks: {
                    min: 0,
                    max: 250,
                },
                display: false
            }]
        },
        legend: {
            display: false
        },
        elements: {
            point: {
                radius: 0
            }
        },
    }
});