// Delete view
// Get table tr elements 
function DeleteItems(element_id, delete_url, redirect_url){
    
    console.log("entrei");

    var selected_rows=[];
    
    $(element_id).find('tr').each(function(){
        var row=$(this);
        console.log(row.find('input[type="checkbox"]').is(':checked'));
        if (row.find('input[type="checkbox"]').is(':checked')) {
            console.log(row.attr('data-id'));
            selected_rows.push(row.attr('data-id'));
            };
    });

    var selected_rows = JSON.stringify(selected_rows);
   
    $.ajax({
        url: delete_url,
        type: 'POST',
        data: {'ckeck_box_item_ids': selected_rows,
        'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()},
        success: function () {
            console.log('Item apagado');
            window.location.href = redirect_url
         }
    })
};

$("#submit-id-save_maintenance_clone").click(function(event) {
    event.preventDefault();
    save_maintenance_ajax_results();
});

$("#submit-id-save_maintenance_new").click(function(event) {
    event.preventDefault();
    save_maintenance_ajax_results();
    // $('#id_name').val('');
    $('#id_action').val('');
    $('#id_notes').val('');
    $('#id_name').focus();

});

function save_maintenance_ajax_results() {
    var random_number = Math.floor(100000000 + Math.random() * 900000000);
    var random_number2 = Math.floor(100000000 + Math.random() * 900000000);

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
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $( "<div class='alert alert-success p-0 m-0' id='alerta" + random_number + "' role='alert'>" + 
            " <button type='button' class='btn close' style='vertical-align: center;" + 
            "horizontal-align: right;' data-dismiss='alert' aria-label='Close' " +
            "<span aria-hidden='True' onclick='Hide(alerta" + random_number + ")'>&times;</span>" +
            "</button>" + $('#id_name').val() + " Data added successfully</div>" ).insertBefore( ".page-breadcrumb" );
            $("#alerta" + random_number).delay(3200).hide(300);
            
        },
        // handle a non-successful response
        error: function(xhr, status, error) {
            // Get the error messages from python Views
            var data = xhr.responseText;
            // Convert string to JavaScript Object
            var err = JSON.parse( data );
            // Extract the error messages and Parse them
            var errorMessage = JSON.parse(err.error);
            // Get the keys of the JavaScript Objects
            const keys = Object.keys(errorMessage);
            // Extract the Message using the keys

            keys.forEach(n => $( "<div class='alert alert-danger p-0 m-0' id='alerta" + n + random_number2 + 
            "' role='alert'>" + 
            " <button type='button' class='btn close' style='vertical-align: center;" + 
            "horizontal-align: right;' data-dismiss='alert' aria-label='Close' " +
            "<span aria-hidden='True' onclick='Hide(alerta" + n + random_number2 + ")'>&times;</span>" +
            "</button>" + errorMessage[n][0].message + "</div>" ).insertBefore( ".page-breadcrumb" )
            );

            $("#alerta" + n + random_number2).delay(3200).hide(300);
                    
          }
    });
};


