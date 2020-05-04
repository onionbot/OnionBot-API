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
                position: 'left',
                ticks: {
                    min: 0,
                    // max: 250,
                },
            }, {
                id: 'y-axis-2',
                type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                display: true,
                position: 'right',
                ticks: {
                    min: 0,
                    max: 100,
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


var lineChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'My First dataset',
        borderColor: window.chartColors.red,
        backgroundColor: window.chartColors.red,
        fill: false,
        data: [
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor()
        ],
        yAxisID: 'y-axis-1',
    }, {
        label: 'My Second dataset',
        borderColor: window.chartColors.blue,
        backgroundColor: window.chartColors.blue,
        fill: false,
        data: [
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor()
        ],
        yAxisID: 'y-axis-2'
    }]
};

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = Chart.Line(ctx, {
        data: lineChartData,
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: true,
                text: 'Chart.js Line Chart - Multi Axis'
            },
            scales: {
                yAxes: [{
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }, {
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            }
        }
    });
};