// ajax function

$(function () {

  $("#test").click(function(){
    console.log("P tag was clicked!")
  })


// {% block javascript %}
//   <script src="{% static 'js/player/player.js'%}"></script>
// {% endblock %} 



  /*
      On submiting the form, send the POST ajax
      request to server and after successfull submission
      display the object.
  */
  $("#player-form").submit(function (e) {
      console.log("Fired up player form");
      // preventing from page reload and default actions
      e.preventDefault();
      // serialize the data for sending the form data.
      var serializedData = $(this).serialize();
      // make POST ajax call
      $.ajax({
          type: 'POST',
          url: "post_player/",
          data: serializedData,
          success: function (response) {
              // on successfull creating object
              // 1. clear the form.
              $("#player-form").trigger('reset');

              // display the new player to table.
              var instance = JSON.parse(response["instance"]);
              var fields = instance[0]["fields"];
              $("#player-table tbody").prepend(
                  `<tr>
                  <td>${fields["number"]||""}</td>
                  <td>${fields["name"]||""}</td>
                  </tr>`
              )
          },
          error: function (response) {
              // alert the error if any error occured
              alert(response["responseJSON"]["error"]);
          }
      })
  })




});