$(function(){

    // creating the carousel
    let $prev_button = $('.slider-main-container #prev')
    let $next_button = $('.slider-main-container #next')
    let $carousel_items = $('.slider-main-container .carousel-items')

    let counter = 100;
    $next_button.on('click', function (e) {
        if (counter <= $carousel_items.width())
        {
            if (counter == 0)
            {
                $carousel_items.css({'transform': `translate(-${100}px)`})
                counter += 100;
            }
            else {
                $carousel_items.css({'transform': `translate(-${counter}px)`})
                counter += 100;
            }
        }
    })

    $prev_button.on('click', function (e) {
        counter += Number($carousel_items.css('transform').split(',')[4])
        $carousel_items.css({'transform': `translate(-${counter}px)`})
    })

    // load the state of a story text
    let $story_text_container = $('.story-story-text')
    const $story_id = $story_text_container.data('story_id')
    
    $.get(`http://127.0.0.1:4000/api/v1/stories/${$story_id}`, function (response, status) {
        if (status == 'success') {
            $story_text_container.html(`${response.text}`)
        }
    })
})