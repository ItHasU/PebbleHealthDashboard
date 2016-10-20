/*
$(function () {
    $('#chart-week').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Steps this week'
        },
        xAxis: {
            categories: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Steps count'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            type: 'column',
            name: 'Steps per day this week',
            data: [1500, 1400, 1550, 1350, 0, 1434, 4343]
        }, {
            type: 'line',
            name: 'Average steps per day',
            data: [1500, 1400, 1550, 1350, 0, 1434, 4343]
        }]
    });
});

$(function () {
    $('#chart-week').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Steps this week'
        },
        xAxis: {
            categories: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Steps count'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            type: 'column',
            name: 'Steps per day this week',
            data: [1500, 1400, 1550, 1350, 0, 1434, 4343]
        }, {
            type: 'line',
            name: 'Average steps per day',
            data: [1500, 1400, 1550, 1350, 0, 1434, 4343]
        }]
    });
});

*/









$(function () {
    // Create the chart
    $('#chart-average-day').highcharts({
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Average steps per day'
        },
        subtitle: {
            text: "Over the full period"
        },
        yAxis: {
            title: {
                text: 'Steps count'
            }
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },
        tooltip: {
            valueSuffix: ' steps'
        },
        series: [{
            name: 'Average step count per day',
            data: [{
                name: "Mon",
                y: 1500
            }, {
                name: "Tue",
                y: 1450
            }, {
                name: "Wed",
                y: 1450
            }, {
                name: "Thu",
                y: 1450
            }, {
                name: "Fri",
                y: 1450
            }, {
                name: "Sat",
                y: 1450
            }, {
                name: "Sun",
                y: 2500
            }],
            size: '80%',
            innerSize: '60%'
        }]
    });
});


$(function () {
    $.getJSON("/api/data", function(raw_data) {
        $('#chart-full-day').highcharts({
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Steps per day - Full history'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Steps per day'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: 'area',
                name: 'Steps per day',
                data: raw_data.steps
            }]
        });
    });
});