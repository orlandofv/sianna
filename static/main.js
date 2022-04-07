$("#submit-id-save_maintenance_clone").click(function(event) {
    event.preventDefault();
    save_maintenance_ajax_results();
});

$("#submit-id-save_maintenance_new").click(function(event) {
    event.preventDefault();
    save_maintenance_ajax_results();
    $('#id_name').val('');
    $('#id_action').val('');
    $('#id_notes').val('');
    $('#id_name').focus();

});

function save_maintenance_ajax_results() {
    console.log("form submitted!"); // sanity check
    $.ajax({
        url :  "new", // the endpoint
        type : "POST", // http method
        data : {
            name: $('#id_name').val(),
            type: $('#id_type').val(),
            schedule: $('#id_schedule').val(),
            frequency: $('#id_frequency').val(),
            time_allocated: $('#id_time_allocated').val(),
            action: $('#id_action').val(),
            item_used: $('#id_item_used').val(),
            quantity: $('#id_quantity').val(),
            notes: $('#id_notes').val(),
            'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()}, // data sent with the post request
        // handle a successful response
        success : function(json) {
            // console.log(json); // log the returned json to the console
            // console.log("success"); // another sanity check
            $('#results').html("<div class='alert-box alert-success radius p-10 m-0' data-alert><span class='btn close'></span>" 
            + data.name + " saved successfully!</div>"); // add the error to the dom
        },
        // handle a non-successful response
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
          }
    });
};


