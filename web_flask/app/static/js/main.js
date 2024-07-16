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
})