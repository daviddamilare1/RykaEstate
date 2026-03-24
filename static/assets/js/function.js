(function($) {
    console.log('function.js loaded from assets/js/function.js');

    // Show SweetAlert2 toast message
    function showMessage(message, type = 'success') {
        console.log('Displaying SweetAlert2 message:', message, 'Type:', type);
        Swal.fire({
            text: message,
            icon: type,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 5000,
            timerProgressBar: true
        });
    }

    // UPDATE APARTMENT STATUS every 3 secs
    

    // ADD COMMENT AJAX
    function getCookie(name) {
        console.log('Fetching CSRF token for:', name);
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        console.log('CSRF token:', cookieValue || 'null');
        return cookieValue;
    }

    $(document).ready(function() {
        console.log('jQuery document.ready fired');

        // Target all forms with action containing "add_comment"
        const $reviewForms = $('form[action*="add_comment"]');
        console.log('Review forms found:', $reviewForms.length);

        $reviewForms.each(function() {
            const $form = $(this);
            const $reviewsContainer = $('#reviews-container');
            const $commentCount = $('#comment-count');

            console.log('Processing form:', $form.attr('action'));
            console.log('Review form:', $form.length ? 'found' : 'not found');
            console.log('Reviews container:', $reviewsContainer.length ? 'found' : 'not found');
            console.log('Comment count:', $commentCount.length ? 'found' : 'not found');

            if (!$form.length) {
                console.error('Review form not found');
                return;
            }
            if (!$reviewsContainer.length) {
                console.error('Reviews container not found');
                return;
            }
            if (!$commentCount.length) {
                console.error('Comment count element not found');
                return;
            }

            $form.on('submit', function(event) {
                event.preventDefault();
                event.stopPropagation();
                console.log('Form submission intercepted for:', $form.attr('action'));

                const formData = new FormData(this);
                const csrfToken = getCookie('csrftoken');
                // const isAgentReview = $form.attr('action').includes('agent/add_comment');

                console.log('Form data:', [...formData.entries()]);

                $.ajax({
                    url: $form.attr('action'),
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    },
                    success: function(data) {
                        console.log('Response data:', data);
                        if (data.success) {
                            const review = data.review;
                            console.log('Profile image in response:', review.profile_image || 'none');
                            const reviewHtml = `
                                <div class="comment-thread">
                                    <div class="comment-box">
                                        <div class="comment-wrapper">
                                            <div class="avatar-wrapper">
                                                <img src="${review.profile_image || '/static/assets/img/person/default.jpg'}" alt="Avatar" loading="lazy" />
                                                <span class="status-indicator"></span>
                                            </div>
                                            <div class="comment-content">
                                                <div class="comment-header">
                                                    <div class="user-info">
                                                        <h4>${review.full_name}</h4>
                                                        <span class="time-badge pt-1 pb-2">
                                                            ${Array(5).fill().map((_, i) => `<i class="fas fa-star" ${i < review.rating ? 'style="color: gold;"' : ''}></i>`).join('')}
                                                        </span>
                                                        <span class="time-badge">
                                                            <i class="bi bi-clock"></i>
                                                            ${new Date(review.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
                                                        </span>
                                                    </div>
                                                </div>
                                                <div class="comment-body">
                                                    <p>${review.review}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            $reviewsContainer.prepend(reviewHtml);
                            $form[0].reset();
                            const currentCount = parseInt($commentCount.text()) || 0;
                            $commentCount.text(currentCount + 1);
                            console.log('Review added, comment count updated to:', currentCount + 1);

                            $form.hide();
                            // const $reviewExistMessage = $('<p>').text('You have already submitted a review for this agent.');
                            // $form.parent().prepend($reviewExistMessage);
                            
                            showMessage('Thank you for your review!', 'success');

                        } else {
                            console.error('Failed to submit review:', data.error);
                            showMessage(data.error || 'Failed to submit review. Please try again.', 'error');
                        }
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        console.error('Fetch error:', errorThrown, 'Status:', xhr.status);
                        showMessage(`An error occurred while submitting the review: ${errorThrown}`, 'error');
                    }
                });
            });
            console.log('Submit event listener attached to form:', $form.attr('action'));
        });


        // Mark Notification As Seen
        $(document).on('click', '.mark-noti-as-seen', function() {
            let button = $(this);
            let id = button.attr("data-index");
            console.log("Notification ID:", id); // Debug: Confirm ID
            let targetElement = $(".noti-div-" + id);
            console.log("Target element:", targetElement); // Debug: Confirm element exists
            
            $.ajax({
                url: "/agents/close_notification/",
                method: "GET",
                data: { "id": id },
                beforeSend: function() {
                    console.log("Sending Data...");
                },
                success: function(res) {
                    if (targetElement.length > 0) {
                        targetElement.addClass("d-none"); // Hide the element
                        console.log("Added d-none to:", targetElement); // Debug
                        const Toast = Swal.mixin({
                            toast: true,
                            position: 'top-end',
                            showConfirmButton: false,
                            timer: 1000,
                            timerProgressBar: true,
                        });
                        Toast.fire({
                            icon: 'success',
                            title: 'Notification Seen!'
                        });
                    } else {
                        console.error("Element not found for selector: .noti-div-" + id);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error marking notification as seen:", xhr.responseJSON?.error || error);
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        timerProgressBar: true,
                    });
                    Toast.fire({
                        icon: 'error',
                        title: 'Failed to mark notification as seen: ' + (xhr.responseJSON?.error || 'Unknown error')
                    });
                }
            });
        });



    });


    

    
})(jQuery);