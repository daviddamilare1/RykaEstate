$(document).ready(function(){
    
    // Add to selection
    $('.add-to-selection').on('click', function(){
        let button = $(this)
        // <button class="button border add-to-selection" data-index="{{r.id}}"><i class="fas fa-shopping-cart"></i> Add To Selection</button>
        let id  = button.attr('data-index')
        
        let hotel_id = $('#id').val();
        // warp the class element ".room_id_${id" in a bactic "``"
        let room_id = $(`.room_id_${id}`).val();
        let room_number = $(`.room_number_${id}`).val();

        let hotel_name = $('#hotel_name').val();
        let room_name = $('#room_name').val();
        let room_price = $('#room_price').val();
        let number_of_beds = $('#number_of_beds').val();
        let room_type = $('#room_type').val();
        let checkin = $('#checkin').val();
        let checkout = $('#checkout').val();
        let adult = $('#adult').val();
        let kids = $('#kids').val();






        console.log(room_id);
        console.log(room_number);
        console.log(hotel_name);
        console.log(room_name);
        console.log(room_price);
        console.log(number_of_beds);
        console.log(room_type);
        console.log(checkin);
        console.log(checkout);
        console.log(adult);
        console.log(kids);

        $.ajax({
            url: '/bookings/add_to_selection/',
            data: {
                'id': id,
                'hotel_id': hotel_id,
                'hotel_name': hotel_name,
                'room_name': room_name,
                'room_price': room_price,
                'number_of_beds': number_of_beds,
                'room_number': room_number,
                'room_type': room_type,
                'room_id': room_id,
                'checkout': checkout,
                'checkin': checkin,
                'adult': adult,
                'kids': kids,

            },
            dataType: 'json',
            beforeSend: function(){
                console.log('Sending data to server...');
                button.html('<i class="fas fa-spinner fa-spin"></i>')

            },
            success:
            function(res){
                console.log(res);
                $('.room-count').text(res.total_selected_items)
                button.html('<i class="fas fa-check"></i>Added To Selection')
            }

        })

        
    })

    
    // Delete Items from Cart
    $(document).on('click', '.delete-item', function(){
        let id = $(this).attr('data-item');
        let button = $(this)

        Swal.fire({
            title: 'Are you sure you want to delete this room?',
            text: "You won't be able to revert this action",
            icon: 'warning',
            showCancelButton:true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#dd3333',
            confirmButtonText: 'Yes, delete it!'

        }).then((result) => {
            if (result.isConfirmed){
                $.ajax({
                    url: '/bookings/delete_selection/',
                    data: {
                        'id':id
                    },
                    dataType:'json',
                    beforeSend:function(){
                        button.html('<i class="fas fa-spinner fa-spin"></i>')
                    },
                    success:function(res){
                        $('.room-count').text(res.total_selected_item)
                        $('.selection-list').html(res.data)
                    },
                });
            }
        });
        
    });



    // Update room status every 3 secs
    function makeAjaxCall() {
        
        $.ajax({
            url: "/update_room_status/",
            type: "GET",
            success: function(data){
                console.log('Checked Rooms');
                
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error:', errorThrown);
            }

        });
    }


    setInterval(makeAjaxCall, 60000);

    //  End

    // $(document).on('click', "#add-to-bookmark", function(){
    //     let button = $(this)
    //     let id = button.attr('data-hotel');
    //     console.log(id);

    //     $.ajax({
    //         url: '/dashboard/add_to_bookmark/',
    //         beforeSend: function() {
    //             console.log('Add to bookmark...');
                
    //         },
    //         data: {
    //             'id': id
    //         },
    //         success: function(res){
    //             console.log(res);
                
    //         }
    //     })

       
        
    // })


    // Add Review
    $(document).on('click', '#review-btn', function(){
        let button = $(this);
        let id = button.attr('data-hotel');
        let review = $('#review-input').val();
        let rating = $('#rating-input').val();

        console.log('ID ===',id);
        console.log('Review ===',review);
        console.log('Rating ===',rating);

        $.ajax({
            url: '/dashboard/add_review/',
            beforeSend: function(){
                console.log('Adding Review');
                
            },
            data:{
                'id':id,
                'review':review,
                'rating':rating,
            },
            success: function(res){
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                });

                Toast.fire({
                    icon: res.icon,
                    title: res.data
                });
                $('#add-review-button').hide()
                $('#review_div').html('Thank you for your feedback')
                
            }
        })
        
    })



    // Function to save form data to localStorage (Show form booking data even after reload)
    function saveFormData() {
        const form = document.getElementById('booking-form');
        const inputs = form.querySelectorAll('input, select');
        const formData = {};

        inputs.forEach(input => {
            if (input.name) {
                formData[input.name] = input.value;
            }
        });

        localStorage.setItem('bookingFormData', JSON.stringify(formData));
    }

    // Function to restore form data from localStorage
    function restoreFormData() {
        const savedData = localStorage.getItem('bookingFormData');
        if (savedData) {
            const formData = JSON.parse(savedData);
            const form = document.getElementById('booking-form');
            const inputs = form.querySelectorAll('input, select');

            inputs.forEach(input => {
                if (formData[input.name]) {
                    input.value = formData[input.name];
                }
            });

            // Update qtyTotal display if needed
            const adults = formData['adults'] || 0;
            const kids = formData['kids'] || 0;
            const qtyTotal = parseInt(adults) + parseInt(kids);
            document.querySelector('.qtyTotal').textContent = qtyTotal || 1;
        }
    }

    // Event listeners for input changes
    document.getElementById('booking-form').addEventListener('input', saveFormData);
    document.getElementById('booking-form').addEventListener('change', saveFormData);

    // Restore form data on page load
    document.addEventListener('DOMContentLoaded', restoreFormData);

    // Optional: Clear localStorage after successful submission
    document.getElementById('booking-form').addEventListener('submit', function() {
        // Optionally clear localStorage after submission
        // localStorage.removeItem('bookingFormData'); // Uncomment to clear after submission
    });






    
})


