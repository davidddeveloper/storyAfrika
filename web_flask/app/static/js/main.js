$(function(){
    let get_current_user = () => {
        let $current_user_id = $('body').data('current_user_id')
        return $.get(`http://127.0.0.1:4000/api/v1/users/${$current_user_id}/`)
            .done(function (response, statusText, jqXHR) {
                if (statusText === 'success') return response;
            })
            .fail(function (jqXHR, statusText, error) {
                console.log("Error fetching user", statusText, error)
            })
    }


    // delete temporary story
    // function to delete a story
    const delete_story = () => {
        if (localStorage.getItem('status') == 'updating') {
            localStorage.removeItem('story_id')
            localStorage.removeItem('status')
            return Promise.resolve()
        }
        const story_id = localStorage.getItem('story_id')
        return $.ajax({
            type: 'DELETE',
            url: `http://127.0.0.1:4000/api/v1/stories/${story_id}/`,
            success: function (response) {
                localStorage.removeItem('story_id')
            }
        })
    }

    // creating the carousel
    const slider = $('.slider');
    const sliderItems = $('.slider-item');
    const itemWidth = sliderItems.outerWidth(true); // includes margin
    const totalItems = sliderItems.length;
    let startX = 0;
    let isDragging = false;

    function updateSliderPosition($current_slider) {
        $current_slider.css('transform', `translateX(${-$current_slider.data('current_index') * itemWidth}px)`); 
    }

    function currentIndex ($current_slider) {
        return Number($($current_slider).data('current_index'))
    }

    function incrementCurrentIndex ($current_slider) {
        $($current_slider).data('current_index', $($current_slider).data('current_index') + 1);
    }

    function decrementCurrentIndex ($current_slider) {
        $($current_slider).data('current_index', $($current_slider).data('current_index') - 1);
    }

    $('.next').on('click', function(e) {
        let $current_slider = $(this).parent().find('.slider')
        if (currentIndex($current_slider) < totalItems - 1) {
            incrementCurrentIndex($current_slider)
            updateSliderPosition($current_slider)
        }
    });

    $('.prev').on('click', function(e) {
        let $current_slider = $(this).parent().find('.slider')
        if (currentIndex($current_slider) > 0) {
            decrementCurrentIndex($current_slider)
            updateSliderPosition($current_slider)
        }
    });

    slider.on('touchstart', function (e) { 
        startX = e.originalEvent.touches[0].pageX // horizantal position of first touch in touches array of touch objects
        isDragging = true
    })

    slider.on('touchmove', function (e) {
        if (isDragging) {
            const currentX = e.originalEvent.touches[0].pageX
            const diff = startX - currentX

            if (diff > 50) { //swips left
                if (currentIndex($(this)) < totalItems - 1) {
                    incrementCurrentIndex($(this)) // increment current index
                    updateSliderPosition($(this))
                }
                isDragging = false
            } else if (diff < -50) { // swips right
                if (currentIndex($(this)) > 0) {
                    decrementCurrentIndex($(this)) // decrement current index
                    updateSliderPosition($(this))
                }
                isDragging = false
            }
        }
    })

    slider.on('touchend', function() {
        isDragging = false;
    });

    slider.on('mousedown', function(e) {
        startX = e.pageX
        isDragging = true
    })

    slider.on('mousemove', function(e) {
        if (isDragging) {
            const currentX = e.pageX
            const diff = startX - currentX
            slider.css({'user-select': 'none'})

            if (diff > 50) { // drag left
                if (currentIndex($(this)) < totalItems - 1) {
                    incrementCurrentIndex($(this))
                    updateSliderPosition($(this))
                }
                isDragging = false
            } else if (diff < -50) { // drag right
                if (currentIndex($(this)) > 0) {
                    decrementCurrentIndex($(this))
                    updateSliderPosition($(this))
                }
                isDragging = false
            }
        }
    })

    slider.on('mouseup', function () {
        isDragging = false; slider.removeClass('dragging')
    })

    slider.on('mouseleave', function () {
        isDragging = false; slider.removeClass('dragging')
    })

    // load the state of a story text
    let $story_text_container = $('.story-story-text')
    const $story_id = $story_text_container.data('story_id')
    
    $.get(`http://127.0.0.1:4000/api/v1/stories/${$story_id}`, function (response, status) {
        if (status == 'success') {
            let content = ''
            console.log('asdf4134', JSON.parse(response.text))
            JSON.parse(response.text).forEach(block => {
                console.log(block.content)
                try {
                    let temp = $(block.content).removeAttr('contenteditable')
                    content = content + temp[0].outerHTML;
                }
                catch {
                    content = block.content;
                }
            })
            let $jcontent = $(`<div>${content}</div>`.replaceAll("⇅", "")).html();
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
    const getImage = (image, other_uri) => {
        if (!image) return image
        if (image.includes('fastly.picsum.photos')) return image
        return image
    }
    let $stories_container = $('.stories-container')
    let $story = (story) => {
        return (`
        <article class="shrink-0 story-card fade-in max-h-[350px] relative" data-story_id="${story.id}">
            <div class="flex w-[300px] items-center">
            <div class="profile flex items-center">
                <img class=" w-[40px] h-[40px] object-cover border-2 rounded-full" src="/uploads/${story.writer.avatar}/${story.writer.id}" alt="">
                <h2 class="ml-5 text-sm">${story.writer.username}</h2>
            </div>
            <div class="w-[10px] h-3 border-lightgray border-l ml-[14px] mr-[8px]"></div>
            <div class="time text-xs">
                ${
                    moment !== undefined ? moment(story.created_at).fromNow() : story.created_at
                }
            </div>
            </div>
            <div class="flex justify-between gap-[25px]">
                <div class="mt-3 flex flex-col w-3/4">
                    <h3 class="font-medium text-lg home-story-title shrink-0" data-story_id="${story.id}"><a href="/story/${story.id}">${story.title}</a></h3>
                    <p class="shrink-0 mt-[10px] w-full max-w-[400px] overflow-x-hidden whitespace-normal overflow-ellipsis line-clamp-2 sm:w-[250px] md:w-[400px]">${loadTextFormat(story.text)}</p>
                </div>
                <div class="story-image self-center w-1/4">
                    <img class='w-full h-3/4 object-cover max-h-[130px]' src="${getImage(story.image, story.writer.id)}" alt="" srcset="">
                </div>
            </div>
            <div class="px-3 mt-[15px] flex items-center justify-between">
                <div class="flex items-center">
                    <div class="flex items-center">
                        <p class="mt-3 like-count">${story.likes_count}</p>
                        ${console.log(story.liked),
                            story.liked === true 
                              ? '<button class="like-btn liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""/></button>' 
                              : '<button class="like-btn like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>'
                          }
                          
                        </div>
                    <div class="inline-block ml-5">
                        <p class="text-xs">${story.read_time} min read</p>
                    </div>
                </div>
                <div class="flex flex-row gap-2 justify-between items-center">
                <div class="bookmark">
                ${console.log(story.bookmarked),
                    story.bookmarked == true
                    ? `<button class="bookmark-btn unbookmark-btn"><img class='bookmark-img' src="/static/icons/bookmarked.svg" alt="" srcset=""></button>`
                    : `<button class="bookmark-btn"><img class='bookmark-img' src="/static/icons/bookmark.svg" alt="" srcset=""></button>`
                }
                </div>
                <div class="more-tools-main-container">
                    <button class="show-more-tools-btn">
                        <img class="" src="/static/icons/more.svg" alt=""/>
                    </button>
                    <div class="is-hidden more-tools overflow-hidden flex flex-col h-0 w-0 bg-offwhite rounded-xl shadow-xl transition-all absolute right-0 bottom-10 before:block before:absolute before:bg-offwhite before:w-[20px] before:h-[20px] before:-bottom-2 before:shadow-xl before:right-[10%] before:rotate-45">
                        <div class="p-3 pt-4">
                            ${
                                $current_user_id != story.writer.id
                                ? `<div class="flex gap-[15px] follow-card" data-user_id=${story.writer.id}>
                                        ${
                                            story.user_is_following_writer == true
                                            ? `<button class="follow flex items-center text-lightblue unfollow"><img src="/static/icons/correct.svg" alt="">Following</button>`
                                            : `<button class="follow flex items-center text-lightblue"><img src="/static/icons/plus.svg" alt="">Follow author</button>`
                                        }
                                    </div>`
                                : ''
                            }
                            <button class="text-lightgray block cursor-pointer hover:underline"><a href="/immersive_read/${story.id}" target="_blank">Read in immersive mode</a></button>
                        </div>
                        <hr class="border-black"/>
                        <div class="p-3 pt-4 login-user-actions-container">
                            <! -- append actions if user is login -->
                            ${
                                $current_user_id == story.writer.id
                                ? `<button class="update-story-btn block text-lightblue cursor-pointer hover:underline">Update story</button>
                                    <button class="delete-story-btn block text-red-500 cursor-pointer hover:underline">Delete story</button>`
                                : ''
                            }
                        </div>
                        }
                        
                    </div>
                </div>
                </div>
            </div>
        </article>
        <hr class="border-black">
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
    const perPage = 5;
    let loading = false;

    function fetchStories(url, status) {
        if (loading) return
        loading = true
        let $url = `http://127.0.0.1:4000/api/v1/topics/${$current_user_id}/foryou_stories?page=${page}&per_page=${perPage}`
        if (url) {
            $url = url
        }
        $.get($url, function ($response, $status, $error) {
            console.log($response)
            if ($status == 'success') {
                if (status == 'topic') $stories_container.empty()
                $response.stories.forEach($story_data => {
                    $stories_container.append($story($story_data))
                })
                if ($response.stories.length === 0) {
                    $stories_container.html('<h1>Try following some people to see their post here</h1>')
                    if (status == 'topic') $stories_container.html("<h1>There aren't any story yet for this topic</h1>")
                }
                if (page < $response.total_pages) {
                    page++;
                    loading = false
                } else {
                    $('.stories-container').off('scroll', handleScroll);
                }

                showMoreTools()
            }
            else {
                $stories_container.html('<h1>Failed to load data</h1>')
                loading = false;
            }
        })
    }

    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            if (localStorage.getItem('story_id')) delete_story()
            if (window.location.pathname === '/') fetchStories();  // only on home
        }
    }

    $('.stories-container').scroll(handleScroll);
    if (window.location.pathname === '/') {
        if (localStorage.getItem('story_id')) delete_story().then(() => fetchStories());  // only on home
        else fetchStories()
    }

    // get stories for a particular topic
    $('.topic-btn').on('click', function () {
        let topic_id = $(this).data('topic_id')
        console.log(topic_id)

        $('.topic-btn, .for-you, .following').removeClass('rounded-sm text-white bg-mediumpurple')
        $(this).addClass('rounded-sm text-white bg-mediumpurple')
        loading = false;
        fetchStories(`http://127.0.0.1:4000/api/v1/topics/${topic_id}/${$current_user_id}/stories?page=${page}&per_page=${perPage}`, 'topic')
    })

    $('.following').on('click', function () {
        page = 1 // reset page
    
        loading = false;
        $('.topic-btn, .for-you').removeClass('rounded-sm text-white bg-mediumpurple')
        $stories_container.empty()
        $(this).addClass('rounded-sm text-white bg-mediumpurple')
        fetchStories(`http://127.0.0.1:4000/api/v1/users/${$current_user_id}/following_stories?page=${page}&per_page=${perPage}`)
    })

    $('.for-you').on('click', function () {
        page = 1 // reset page

        loading = false;
        $('.topic-btn, .following').removeClass('rounded-sm text-white bg-mediumpurple')
        $stories_container.empty()
        $(this).addClass('rounded-sm text-white bg-mediumpurple')
        fetchStories()
    })

    const replaceButton = ($target, $value) => {
        if (window.location.pathname.includes('/story') === true) {
            $target.replaceWith($value)
        }
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
        $.get(`/stories/${$story_id}/like/`, function (response, status) {
            if (status == 'success') {
                // update like count and btn
                let $like_count = $story.find('.like-count')
                let likedBtn = '<button class="like-btn liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""></button>'
                let likeBtn = '<button class="like-btn like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>'

                $target = $target.closest('button')
                $like_count.text(response.likes_count)  // update like count

                // update btn
                if ($target.hasClass('like-btn-trans')) {
                    $target.replaceWith('<button class="like-btn liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""></button>')
                    replaceButton($('.like-btn'), likedBtn)
                } else {
                    $target.replaceWith('<button class="like-btn like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>')
                    replaceButton($('.like-btn'), likeBtn)
                }


            }
        })
    })

    //follow user or unfollow user
    $('body').delegate('.follow', 'click', function () {
        let $target = $(this)
        let user_id = $target.closest('.follow-card').data('user_id')
        $.get(`/users/${user_id}/follow/`, function (response, status) {
            if (status == 'success') {
                console.log(response)
                if ($target.hasClass('unfollow')) $target.html('<img src="/static/icons/plus.svg" alt="">Follow').removeClass('unfollow')
                else $target.html('<img src="/static/icons/correct.svg" alt="">Following').addClass('unfollow')
            }
        })
    })

    // bookmark a story

    $('body').on('click', '.bookmark-btn', function () {
        let $target = $(this)
        let story_id = $target.closest('.story-card').data('story_id')
        $.get(`/stories/${story_id}/bookmark/`, function (response, status) {
            if (status == 'success') {
                let bookmarkBtn = `<button class="bookmark-btn"><img class='bookmark-img' src="/static/icons/bookmark.svg" alt="" srcset=""></button>`
                let bookmarkedBtn = `<button class="bookmark-btn unbookmark-btn"><img class='bookmark-img' src="/static/icons/bookmarked.svg" alt="" srcset=""></button>`

                console.log($target)
                if ($target.hasClass('unbookmark-btn')) {
                    $target.html(`<img class='bookmark-img' src="/static/icons/bookmark.svg" alt="" srcset="">`).removeClass('unbookmark-btn')
                    replaceButton($('.bookmark-btn'), bookmarkBtn)
                }
                else {
                    $target.html(`<img class='bookmark-img' src="/static/icons/bookmarked.svg" alt="" srcset="">`).addClass('unbookmark-btn')
                    replaceButton($('.bookmark-btn'), bookmarkedBtn)
                }
            }
        })
    })

    // search stories in bookmark
    let bookmarkSearchInput = $('.search-bookmarks-input')
    let bookmarksContainer = $('.bookmarks-container')
    $('.show-all-bookmarks').on('click', function () {
        bookmarkSearchInput.focus()
    })

    let bookmarkCard = (story, idx) => {
        return `
            <article class="comment-card rounded-lg p-4 ${idx % 2 == 0 ? 'bg-mediumpurple text-white' : 'bg-white text-lightgray' }" data-story_id=${story.id}>
                <div class="profile container mx-auto px-5 sm:px-2 ">
                    <div class="mt-[2px] flex gap-[5px] items-center">
                        <p class="text-xs mb-2">posted ${ moment(story.created_at).fromNow()} by</p>
                    </div>
                    <div class="flex items-center">
                        ${ story.writer.avatar
                            ? `<img class="rounded-full h-[40px] w-[40px] object-cover" src="/uploads/${story.writer.avatar}/{{story.writer.id}}/" alt="">`
                            : `<img class="rounded-full h-[40px] w-[40px] object-cover" src="https://picsum.photos/200/700" alt="">`
                        }

                        <div class="ml-[15px]">
                            <div class="flex gap-[5px] follow-card" data-user_id="${story.writer.id}">
                                <h3 class="">${story.writer.username}</h3>
                                ${ story.user_is_following_writer == true 
                                    ? `<button class="follow flex items-center text-lightblue unfollow"><img src="/static/icons/correct.svg" alt="">Following</button>`
                                    : `<button class="follow flex items-center text-lightblue"><img src="/static/icons/plus.svg" alt="">Follow</button>`
                                }
                            </div>
                        </div>
                    </div>
                </div>
                <div class="">
                    <h3 class="comment-text text-base mt-[5px] ml-[50px] h-10"><a href="/story/${story.id}">${story.title}</a></h3>
                </div>
            </article>
        `
    }

    $('.search-bookmark-form').on('submit', function (e) {
        e.preventDefault()
        let searchData = bookmarkSearchInput.val()

        $.get(`/search_bookmarked_stories/${searchData}`, function (response, status) {
            if (status == 'success') {
                console.log(response)
                bookmarksContainer.empty()
                response.forEach((story, idx) => {
                    bookmarksContainer.append(bookmarkCard(story, idx))
                })

                if (response.length == 0) {
                    bookmarksContainer.append(`<article class="rounded-lg p-4 bg-mediumpurple text-white">Oh oh, looks like you haven\'t bookmarked that yet.</article>`)
                }
            }
        })
    })


    //login user profile card functionality - change avatar/image
    // also used by text-editor
    let $profile_image_container = $('.change-img-button-container');
    $profile_image_container.on('mouseenter', () => {
        $(this).find('.image-btn-change').show(100)
        $(this).find('.generate-random-image').show()
    }).on('mouseleave', () => {
        $(this).find('.image-btn-change').hide()
        $(this).find('.generate-random-image').hide()
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
            form_data.append('csrf_token', $('#csrfToken').val())

            $.ajax({
                url: '',
                type: 'POST',
                data: form_data,
                contentType: false,
                processData: false,
                success: function(response) {
                    if (window.location.pathname == '/story/write/' ||
                        window.location.pathname == '/story/write'
                    ) {
                        $('#story-image').attr('src', `/uploads/${file.name.replaceAll(" ", "_")}/${$current_user_id}`)

                    } else if (window.location.pathname == '/') {
                        $('.profile-image').attr('src', `/uploads/${file.name.replaceAll(" ", "_")}/${$current_user_id}`)
                        //$('.home-profile-img').attr('src', `/uploads/${file.name.replaceAll(" ", "_")}`)

                    }
                    if (!response.includes('/story/write/')) window.location.reload()
                },
                error: function(error) {
                    console.error('Error:', error);
                    //window.location.reload()
                }
            })
        }
    })


    // show profile card on profile-image click
    $('.home-profile-img').on('click', function () {
        $('.profile-card-shadow').show()
        $('.profile-card').removeClass('-top-[100%] hidden').addClass('flex flex-col-reverse md:flex-row top-[10%] sm:top-[20%]')
    })

    $('.profile-card-shadow').on('click', function () {
        $('.profile-card-shadow').hide()
        $('.profile-card').addClass('-top-[100%] hidden').removeClass('sm:top-[20%]').removeClass('top-[10%]')
    })

    // show more tools
    const showMoreTools = () => {

        const showTool = (target) => {
            // hide all tool except the selected one
            $('.more-tools').addClass('h-0 w-0 is-hiddden overflow-hidden') 
            target.removeClass('h-0 w-0 is-hidden overflow-hidden') 
        }
        const hideTool = (target) => {
            target.addClass('h-0 w-0 is-hidden overflow-hidden');
        }

        let moreToolBtn = $('.show-more-tools-btn')
        moreToolBtn.on('click', function (e) {
            console.log('yeah!')
            let parent = $(e.target).parent().parent();
            let moreTool = parent.find('.more-tools');

            if (moreTool.hasClass('is-hidden')) {
                showTool(moreTool)
            }
            else {
                hideTool(moreTool)
            }
        })

        // handle deleting story
        let card = $('.confirm-story-deletion')
        let divider = $('.home-divider')
        let story_id = ''
        $('.delete-story-btn').on('click', function () {
            story_id = $(this).closest('.story-card').data('story_id')

            if (card.hasClass('is-hidden')) {
                card.addClass('top-0 sm:top-2/4').removeClass('is-hidden')
                divider.show()
            } else {
                card.removeClass('top-0 sm:top-2/4').addClass('is-hidden')
                divider.hide()
            }
        })

        // hide divider and card when divider is clicked
        divider.on('click', function () {
            divider.hide()
            card.removeClass('top-0 sm:top-2/4').addClass('is-hidden')
        })

        // hide divider and card when cancel is cicked
        $('.confirm-delete-cancel').on('click', function () {
            divider.hide()
            card.removeClass('top-0 sm:top-2/4').addClass('is-hidden')
        })

        // delete story with yes
        $('.confirm-delete-yes').on('click', function () {
            localStorage.setItem('story_id', story_id) // add story_id to localstorage so delete_story would work
            // get the id of story previously added to localstorage
            if (localStorage.getItem('story_id')) delete_story().then(response => {
                localStorage.removeItem('story_id')
                if (response.status === 'Deleted') window.location.replace('/');
            });
        })

        //handle update story
        $('body').delegate('.update-story-btn', 'click', function () {
            story_id = $(this).closest('.story-card').data('story_id') // get story id
            localStorage.setItem('story_id', story_id)
            localStorage.setItem('status', 'updating')
            // if story_id was added successfully to localstorage redirect to update page
            if (localStorage.getItem('story_id')) window.location.assign('/story/write/');
        })

    }

    //story view
    if (window.location.pathname.includes('/story/')) showMoreTools()

    // a divider is a nice bg that separates fixed or absolute card from the body
    const showDivider = () => {
        
    }

    let viewImages = $('.view-image');
    viewImages.each((idx, img) => {
        let image = $(img);
        image.on('click', () => {
            image.addClass('block container mx-auto top-0 absolute h-screen')
        })
    })
})


