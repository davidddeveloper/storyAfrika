$(function(){
    const get_current_user = () => {
        let $current_user_id = $('body').data('current_user_id')
        let $current_user = null
        $.get(`http://127.0.0.1:4000/api/v1/users/${$current_user_id}/`, function (response, status) {
                if (status == 'success') {
                    $current_user = response
                    console.log($current_user)
                }
            }
        );

        return $current_user
    }
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
            let content = ''
            JSON.parse(response.text).forEach(block => {
                content = content + block.content;
            })
            let $jcontent = $(`<div>${content}</div>`.replace("⇅", "").replace("⇅", "").replace("⇅⇅", "")).text();
            $story_text_container.html(`${$jcontent}`)
        }
    })

    // load stories when user scroll to the bottom
    const $current_user_id = $('body').data('current_user_id')
    const loadTextFormat = (text) => {
        try {
            let json_text = JSON.parse(text)
            let content = ''
            json_text.forEach(block => {
                content = content + block.content.replace("⇅", "")
            })
            let $jcontent = $(`<div>${content}</div>`).text()
            return $jcontent
        } catch (error) {
            let $jtext = $(`<div>${text}</div>`).text()
            return $jtext
        }
    }
    let $stories_container = $('.stories-container')
    let $story = (story) => {
        return (`
        <article class="shrink-0 story-card fade-in" data-story_id="${story.id}">
            <div class="flex w-[300px] items-center">
            <div class="profile flex items-center">
                <img class=" w-[40px] h-[40px] object-cover border-2 rounded-full" src="https://picsum.photos/200/400" alt="">
                <h2 class="ml-5 text-sm">${story.writer.username}</h2>
            </div>
            <div class="w-[10px] h-4 border-lightgray border-l ml-[15px] mr-[15px]"></div>
            <div class="time text-xs">
                ${moment(story.created_at).fromNow()}
            </div>
            </div>
            <div class="flex justify-between gap-[25px]">
                <div class="mt-3 flex flex-col w-3/4">
                    <h3 class="font-medium text-lg home-story-title shrink-0" data-story_id="${story.id}"><a href="/story/${story.id}">${story.title}</a></h3>
                    <p class="shrink-0 mt-[10px] w-full max-w-[400px] overflow-x-hidden whitespace-nowrap overflow-ellipsis sm:w-[250px] md:w-[400px]">${loadTextFormat(story.text)}</p>
                </div>
                <div class="story-image self-center w-1/4">
                    <img class='w-full h-3/4 object-cover' src="/uploads/${story.image}" alt="" srcset="">
                </div>
            </div>
            <div class="px-3 mt-[15px] flex items-center justify-between">
                <div class="flex items-center">
                    <div class="flex items-center">
                        <p class="mt-3 like-count">${story.likes_count}</p>
                        ${
                            story.liked === false 
                              ? '<button class="like-btn like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>' 
                              : '<button class="like-btn liked-btn hidden"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""/></button>'
                          }
                          <button class="like-btn liked-btn hidden"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""></button>
                        </div>
                    <div class="inline-block ml-5">
                        <p class="text-xs">${story.read_time} min read</p>
                    </div>
                </div>
                <div class="bookmark">
                    <button class="like-bookmark">
                        <img src="/static/icons/bookmark.svg" alt="" srcset="">
                        <img src="/static/icons/bookmark_click.svg" alt="" srcset="">
                    </button>
                </div>
            </div>
        </article>
    `)}

    /*$.get(`http://127.0.0.1:4000/api/v1/users/${$current_user_id}/following_stories/`, function ($response, $status) {
        if ($status == 'success') {
            $response.forEach(story_data => {
                $stories_container.append($story(story_data))
            })
            if (Object.keys($response).length === 0) {
                $response.html('<h1>Try following some people to see their post here</h1>')
            }
        }
    })*/

    // load data when the user scrolls to the bottom
    let page = 1;
    const perPage = 10;
    let loading = false;

    function fetchStories() {
        if (loading) return
        loading = true

        let $url = `http://127.0.0.1:4000/api/v1/users/${$current_user_id}/following_stories?page=${page}&per_page=${perPage}`
        $.get($url, function ($response, $status, $error) {
            if ($status == 'success') {
                $response.stories.forEach($story_data => {
                    $stories_container.append($story($story_data))
                })
                if ($response.stories.length === 0) {
                    $stories_container.html('<h1>Try following some people to see their post here</h1>')
                }
                if (page < $response.total_pages) {
                    page++;
                    loading = false
                } else {
                    $('.stories-container').off('scroll', handleScroll);
                }
            }
            else {
                $stories_container.html('<h1>Failed to load data</h1>')
                loading = false;
            }
        })
    }

    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            //if (localStorage.getItem('story_id')) delete_story()
            fetchStories();
        }
    }

    $('.stories-container').scroll(handleScroll);
    fetchStories();

    // delete temporary story
    // function to delete a story
    const delete_story = () => {
        const story_id = localStorage.getItem('story_id')
        $.ajax({
            type: 'DELETE',
            url: `http://127.0.0.1:4000/api/v1/stories/${story_id}/`,
            success: function (response) {
                console.log(response)
                localStorage.removeItem('story_id')
            }
        })
    }

    const story_and_user_id = ($story) => {
        let current_user_id = $('body').data('current_user_id')
        let story_id = $story.data('story_id')

        return [current_user_id, story_id]
    }
    // interactions - like bookmark
    $('body').on('click', '.like-btn', (e) => {
        let $target = $(e.target)
        let $story = $(e.target.closest('.story-card'))
        let [$current_user_id, $story_id] = story_and_user_id($story)

        // like the story
        $.get(`http://127.0.0.1:5000/stories/${$story_id}/like/`, function (response, status) {
            if (status == 'success') {
                // update like count and btn
                $target = $target.closest('button')
                let $like_count = $story.find('.like-count')
                console.log(response.likes_count)
                $like_count.text(response.likes_count)  // update like count

                // update btn
                if ($target.hasClass('liked-btn')) {
                    $target.hide()
                    $story.find('.like-btn-trans').show()
                } else if ($target.hasClass('like-btn-trans')) {
                    $target.hide()
                    $story.find('.liked-btn').show()
                }


            }
        })
    })
    //login user profile card functionality - change avatar/image
    let $profile_image_container = $('.change-img-button-container');
    $profile_image_container.on('mouseenter', () => {
        $(this).find('.image-btn-change').show(300)
    }).on('mouseleave', () => {
        $(this).find('.image-btn-change').hide(300)
    })

    let $change_profile_image_btn = $('.image-btn-change')
    $change_profile_image_btn.on('click', () => {
        $(this).find('#file-input-field').click()

    })

    $('#file-input-field').change(function () {
        let file = this.files[0]
        if (file) {
            let form_data = new FormData()
            form_data.append('file', file)
            if (localStorage.getItem('story_id')) form_data.append('story_id', localStorage.getItem('story_id'))
            //form_data.append('csrf_token', $('#csrfToken').val())

            $.ajax({
                url: '',
                type: 'POST',
                data: form_data,
                contentType: false,
                processData: false,
                success: function(response) {
                    //console.log('Success:', response);
                    $('#story-image').attr('src', `/uploads/${file.name}`)
                },
                error: function(error) {
                    //console.error('Error:', error);
                    window.location.reload()
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

    console.log(get_current_user())
})