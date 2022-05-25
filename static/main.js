function createDoughnutChart(labels, data, text, label, element_id){
    const m_chart = new Chart(document.getElementById(element_id), {
        type: 'doughnut',
        data: {
        labels: labels,
        datasets: [
            {
            label: label,
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9"],
            data: data
            }
        ]
        },
        options: {
        title: {
            display: true,
            text: text
        }
        }
    });
}

var random_number = Math.floor(100000000 + Math.random() * 900000000);
// Delete view
// Get table tr elements 

function DeleteItems(element_id, delete_url, redirect_url){
    
    var selected_rows=[];
    var array_rows=[];
    
    $(element_id).find('tr').each(function(){
        var row=$(this);
        console.log(row.find('input[type="checkbox"]').is(':checked'));
        if (row.find('input[type="checkbox"]').is(':checked')) {
            // console.log(row.attr('data-id'));
            selected_rows.push(row.attr('data-id'));
            array_rows = selected_rows;

        };
    });

    var selected_rows = JSON.stringify(selected_rows);
   
    $.ajax({
        url: delete_url,
        type: 'POST',
        data: {'check_box_item_ids': selected_rows,
        'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()},
        success: function () {
            
            // Refreh element
            $(element_id).load(location.href + " " + element_id);

            console.log('Item apagado');
            // window.location.href = redirect_url;
            
            if (array_rows.length > 0){
                $( "<div class='alert alert-warning p-0 m-0' id='alerta" + random_number + "' role='alert'>" + 
                    " <button type='button' class='btn close' style='vertical-align: center;" + 
                    "horizontal-align: right;' data-dismiss='alert' aria-label='Close' " +
                    "<span aria-hidden='True' onclick='Hide(alerta" + random_number + ")'>&times;</span>" +
                    "</button> Item(s) deleted successfully</div>" ).insertBefore( ".page-breadcrumb" );
            };

            $("#alerta" + random_number).delay(3200).hide(300);
            random_number = Math.floor(100000000 + Math.random() * 900000000);
        },
    })
};

$(document).ready(function() {
    
    console.log("document ready.")

    var random_number = Math.floor(100000000 + Math.random() * 900000000);
    if ($('#id_component_no').val() == ""){ 
        $('#id_component_no').val(random_number);
    }
    
    if ($('#id_allocation_no').val() == ""){
        $('#id_allocation_no').val(random_number);
    }

    if ($('#id_order').val() == ""){
        $('#id_order').val(random_number);
    }

    $('#checkall').click(function () {
        $('.rowcheckbox').prop('checked', this.checked);
    });

    $('.rowcheckbox').click(function () {
        if ($('#checkall').prop('checked', true)) {
            $('#checkall').prop('checked', false)
        }

    });
   
     // Use DataTables to display table
     $('#sortTableExtraLarger').DataTable({
        columnDefs: [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 7 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });

    // Use DataTables to display table
    $('#sortTableExtraLarge').DataTable({
        columnDefs: [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 6 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });

    // Use DataTables to display table
    $('#sortTableLarge').DataTable({
        columnDefs: [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 5 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });

     // Use DataTables to display table
     $('#sortTableMedium').DataTable({
        stateSave: true,
        "bFilter" : true,
        "responsive" : true,
        "iDisplayLength": 10,
        columnDefs: [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 4 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });

     // Use DataTables to display table
     $('#sortTableSmall').DataTable({
        columnDefs: [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 3 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });

     // Use DataTables to display table
     $('#sortTableSmaller').DataTable({
        columnDefs: [
            { orderable: false, targets: 0 },
            { "width": "1%", "targets": 0 }
        ],
        order: [[1, 'asc']]
    });    
});




