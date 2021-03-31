
// ajax example
// ajax
// go to url /user/create/  -- urls.py
// $.ajax({
// 	type: 'POST',
// 	url:'/user/create/',
// 	data:{
// 		name: $('#name').val(),
// 		email: $('#email').val(),
// 		name: $('name').val(),
// 		password: $('#password').val(),
// 	},
// 	success:function(){}
// });



// Submit post on submit
// $('#leave-comment').on('submit', function(event){
//     event.preventDefault();   // prevents default browser behaviour on form submission
//     console.log("form submitted!")
//     $.ajax({
//     	type:'POST',
//     	url:'/game/'



//     })
// });

// works
$("#hide").click(function(){
	$("#hide").hide();
});



