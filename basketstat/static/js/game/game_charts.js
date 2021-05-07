$(function(){


  const id = JSON.parse(document.getElementById('id').textContent).toString();;

  console.log("Game id is: ", id);


  console.log("loading game_charts.js file");
  var linechart_endpoint = "/game/quarter-scores/".concat(id);
  var piechart_endpoint = "/game/shot-selection/".concat(id);

  // line chart ajax
  $.ajax({
    url: linechart_endpoint,
    success: function(data){
      drawLineGraph(data, 'line-chart');  // call function
      console.log("Drawing line chart..");
    },
    error: function(error_data){
      console.log("Error: ",error_data);
    }
  })

  // pie chart ajax
  $.ajax({
    url: piechart_endpoint,
    success: function(data){
      drawPieChart(data, 'pie-chart');  // call function
      console.log("Drawing pie chart..");
    },
    error: function(error_data){
      console.log("Error: ",error_data);
    }
  })



  // draw piechart using team statistics
  function drawPieChart(data, id) {
    var teamStats = data.data;
    console.log(teamStats);
    
    let ctx = document.getElementById(id).getContext('2d');   //ctx
    var chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'pie',
      // The data for our dataset
      data: {
        labels: ['Two Point shots', 'Three point shots'],
        datasets: [{
          data: [teamStats.total2P, teamStats.total3P],
          borderColor:[
            "#3cba9f",
            "#ffa500",
          ],
          backgroundColor: [
            "rgb(60,186,159,0.1)",
            "rgb(255,165,0,0.1)",
          ],
          borderWidth:2,
          hoverOffset: 4,
        }]
      },

      // Configuration options go here
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
   }




  // draw the scores line graph
  function drawLineGraph(data, id) {
    var title = data.title;
    var chartlabels = data.labels;
    var data_home = data.data[0];
    var data_opponent = data.data[1];
    console.log(chartlabels, data_home, data_opponent);

    
    let ctx = document.getElementById(id).getContext('2d');   //ctx
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
          borderColor: "#3cba9f", /*borderColor: "rgb(196,88,80)",*/
          backgroundColor: "#71d1bd",
          fill: false,
        },
        ]
      },

      // Configuration options go here
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            display: true,
          },
          y: {
            display: true,
            beginAtZero: true,
            }
        }
        
      }







    });
  }








});