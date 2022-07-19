var jwt = null
function secure_get_with_token(endpoint, on_success_callback, on_fail_callback){
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt  = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}



function secure_post_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback){
        xhr = new XMLHttpRequest();
        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
        }
        function get_and_set_new_jwt(data){
                jwt  = data.token
                on_success_callback(data)
        }
        $.ajax({
                url: endpoint,
                type: 'POST',
                datatype: 'json',
		data: data_to_send,
                success: on_success_callback,
                error: on_fail_callback,
                beforeSend: setHeader
        });
}

function file_upload(endpoint, data_to_send, on_success_callback, on_fail_callback)
{
    console.log(data_to_send)
	xhr = new XMLHttpRequest();
	$.ajax({
		//actual post
       		url: endpoint,
        	type: "POST",
            xhr: function () {
 	       		var myXhr = $.ajaxSettings.xhr();
        		if (myXhr.upload) {
				myXhr.upload.addEventListener('progress', function(event){
                     			var percent = 0;
                     			var position = event.loaded || event.position;
                     			var total = event.total;
                    			if (event.lengthComputable) {
                        			percent = Math.ceil(position / total * 100);
							if(percent == 100)
							{

							}
                    			}
            			}, false);
            		}
            	return myXhr;
        	},
        contentType: 'application/json',
        dataType : 'json',
		timeout: 60000,
        data: JSON.stringify(data_to_send),
        success: on_success_callback,
		error: on_fail_callback,


 });
}

