function submitAddCourse() {
    var courseName = $('#addCourseModal .ui.form input[name="course_name"]').val();
    var middlewareToken = $('#addCourseModal .ui.form input[name="csrfmiddlewaretoken"]').val();

    $('#addCourseModal .ui.form').addClass('loading');

    $.post('/dashboard/courses/new', {
      name : courseName,
      csrfmiddlewaretoken : middlewareToken
    }, function() {
      $('#addCourseModal.ui.modal').modal('hide');
        location.reload();

    }).fail(function() {
      console.log(arguments);
    })
}

$('#addCourseModal .ui.save.button').click(function(e) {
  submitAddCourse();
})

$('#addCourseModal.ui.modal').modal(
	{
		transition:'fly down',
		duration:500,
		closable:false,
		selector:{
			approve:'.actions .save'
		},
		onShow:function(){
			$(this).find('.ui.form').removeClass('loading');
      $(this).find('input[name=course_name]').val('');
		},
		onApprove: function(){
			return false;
		}
	}
);

$('#addCourseBtn').on('click', function(){
	$('#addCourseModal.ui.modal').modal('show');
});

$('input[name=course_name]').keypress(function(e) {
  if (e.keyCode == 13) {
    e.preventDefault();
    submitAddCourse();
  }
});