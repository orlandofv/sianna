// Submit maintenance on submit
$('#maintenance-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    console.log($('#id_schedule_name').val())
};