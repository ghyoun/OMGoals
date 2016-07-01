$(function() {
  $( "#tabs" ).tabs();
  $( "#accordion" ).accordion();
});

$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
});

