$(document).ready(function() {
	$('#search-btn').on('click', function(){
		var search_query = $('#search-input').val()
		$.ajax({
			url: '/',
			type: 'POST',
			data: {'search_query': search_query},
			success: function(data) {
		        var content = $(data).filter('#content');
		        $('#content').html(content);
		    },
		    error: function(data) {
		    	// error
		    }
		});
		return false;
	});
});