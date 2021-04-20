console.log("loading game charts.js")
$(function(){
  var endpoint = "/game/test-linechart/";
  var $lineChart = $('#line-chart');
  $.ajax({
    url: endpoint,
    success: function(data){
      drawLineGraph(data, 'line-chart');  // call function
      console.log("Drawing line chart..");
    },
    error: function(error_data){
      console.log("Error: ",error_data);
    }
  })
  // define functions to call
  function drawLineGraph(data, id) {
    var title = data.title;
    var chartlabels = data.labels;
    var data_home = data.data[0];
    var data_opponent = data.data[1];
    console.log(chartlabels, data_home, data_opponent);

    
    var ctx = document.getElementById(id).getContext('2d');   //ctx
    var chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'line',
      // The data for our dataset
      data: {
        labels: chartlabels,
        datasets: [{
          data: data_home,
          label: "Home Team",
          borderColor: "#3e95cd",
          backgroundColor: "#7bb6dd",
          fill: false,
        },{
          data: data_opponent,
          label: "Opponent",
          borderColor: "#3cba9f",
          backgroundColor: "#71d1bd",
          fill: false,

        }
        ]
      },

      // Configuration options go here
      options: {
        scales: {
          xAxes: [{
            display: true
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }

    });
  }


});