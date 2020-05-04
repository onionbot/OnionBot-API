var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        labels: new Array(120).fill(" "),
        datasets: [{
            label: 'My First dataset',
            borderColor: 'rgb(0,123,255)',
            data: new Array(120).fill(0),
            lineTension: 0,
            fill: false,
        }]
    },
    // Configuration options go here
    options: {
        animation: {
            duration: 0
        },
        scales: {
            yAxes: [{
                ticks: {
                    min: 0, 
                    // max: 250,
                }
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
            point:{
                radius: 0
            }
        },
    }
});

