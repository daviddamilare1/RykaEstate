$(document).ready(function() {
    
    // UPDATE APARTMENT STATUS every 3 secs
    function makeAjaxCall() {
        $.ajax({
            url: "/update_apartment_status/",
            type: "GET",
            success: function(data) {
                console.log('Checked Apartments:', data);
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Apartment status error:', errorThrown);
            }
        });
    }

    setInterval(makeAjaxCall, 3000);
});