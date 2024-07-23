$(function(){

    // creating the carousel
    const slider = $('.slider');
    const sliderItems = $('.slider-item');
    const itemWidth = sliderItems.outerWidth(true); // includes margin
    const totalItems = sliderItems.length;
    let currentIndex = 0;

    function updateSliderPosition() {
        slider.css('transform', `translateX(${-currentIndex * itemWidth}px)`);
    }

    $('.next').on('click', function() {
        if (currentIndex < totalItems - 1) {
            currentIndex++;
            updateSliderPosition();
        }
    });

    $('.prev').on('click', function() {
        if (currentIndex > 0) {
            currentIndex--;
            updateSliderPosition();
        }
    });

    // load the state of a story text
    let $story_text_container = $('.story-story-text')
    const $story_id = $story_text_container.data('story_id')
    
    $.get(`http://127.0.0.1:4000/api/v1/stories/${$story_id}`, function (response, status) {
        if (status == 'success') {
            $story_text_container.html(`${response.text}`)
        }
    })

    //login user profile card functionality
    let $profile_image_container = $('.change-img-button-container');
    $profile_image_container.on('mouseenter', () => {
        $(this).find('.profile-image-btn-change').show(300)
    }).on('mouseleave', () => {
        $(this).find('.profile-image-btn-change').hide(300)
    })

    let $change_profile_image_btn = $('.profile-image-btn-change')
    $change_profile_image_btn.on('click', () => {
        $(this).find('#file-input-field').click()

    })

    $('#file-input-field').change(function () {
        let file = this.files[0]
        if (file) {
            let form_data = new FormData()
            form_data.append('file', file)
            //form_data.append('csrf_token', $('#csrfToken').val())

            $.ajax({
                url: '',
                type: 'POST',
                data: form_data,
                contentType: false,
                processData: false,
                success: function(response) {
                    console.log('Success:', response);
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            })
        }
    })


    // show profile card on profile-image click
    $('.home-profile-img').on('click', function () {
        $('.profile-card-shadow').show(200)
        $('.profile-card').css({'display': 'flex', 'top': '30%'}).slideDown(200)
    })

    $('.profile-card-shadow').on('click', function () {
        $('.profile-card-shadow').hide(200)
        $('.profile-card').css({'display': 'hidden', 'top': '-50%'}).slideUp(200)
    })
})