$(function () {

    let showCommentViewBtn = $('.show-comment-view')
    let commentView = $('.comments-view')

    const checkElementOverflowing = (el) => {

    }

    $('body').on('click', '.show-comment-view', () => {
        if (commentView.hasClass('is-hidden')) {
            $('.divider').show()
            commentView.removeClass('md:-right-[100%] is-hidden -bottom-[100%]').addClass('-bottom-[20%] md:right-0')
            $('textarea').focus()

        } else {
            commentView.removeClass('md:right-0').addClass('md:-right-[100%] md:-bottom-[100%] is-hidden')
        }
    })

    $('.divider').on('click', function () {
        commentView.removeClass('md:right-0 -bottom-[20%]').addClass('md:-right-[100%] md:-bottom-[100%] -bottom-[100%] is-hidden')
        $('.divider').hide()
    })

    $('.comment-textarea').on('input', function () {
        if ($(this).val().length > 8) $('.share-comment').removeAttr('disabled').removeClass('opacity-0')
        else $('.share-comment').addClass('opacity-0').attr('disabled')
    })

    $('body').delegate('.view-more', 'click', function () {
        let $commentText = $($(this).parent()).find('.comment-text')
        const scrollHeight = $commentText.prop('scrollHeight')
        let commentHeight = $commentText.prop('clientHeight')

        console.log(scrollHeight)
        console.log(commentHeight)

        // double the height when view more is clicked
        if (commentHeight < scrollHeight) {
            $commentText.height(commentHeight + commentHeight);
        }
        // but ensuring that the height is equal the content height
        if (commentHeight >= scrollHeight) {
            $commentText.height(scrollHeight)
            $(this).hide()
        }
    })

    // function to replace button
    const replaceButton = ($target, $value) => {
        if (window.location.pathname.includes('/story') === true) {
            $target.replaceWith($value)
        }
    }

    // like comment
    $('body').on('click', '.comment-like-btn', (e) => {
        let $target = $(e.target)
        let $comment = $(e.target.closest('.comment-card'))
        const $comment_id = $comment.data('comment_id')

        // like the comment
        $.get(`/comments/${$comment_id}/like/`, function (response, status) {
            console.log(response)
            if (status == 'success') {
                // update like count and btn
                let $like_count = $comment.find('.comment-like-count')
                let likedBtn = '<button class="comment-like-btn comment-liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""></button>'
                let likeBtn = '<button class="comment-like-btn comment-like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>'

                $target = $target.closest('button')
                $like_count.text(response.likes_count)  // update like count

                // update btn
                if ($target.hasClass('comment-like-btn-trans')) {
                    $target.replaceWith('<button class="comment-like-btn comment-liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""></button>')
                    replaceButton($target.siblings('.comment-like-btn'), likedBtn)
                } else {
                    $target.replaceWith('<button class="comment-like-btn comment-like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>')
                    replaceButton($target.siblings('.comment-like-btn'), likeBtn)
                }
            }
        })
    })

    // share comment
    let $current_user_id = $('body').data('current_user_id')
    let $story_id = $('.story-card').data('story_id')
    let $comment_container = $('.comments-container')
    let $share_comment_btn = $('.share-comment')
    

    const $comment_form = $('.share-comment-form')
    $comment_form.on('submit', function (e) {
        e.preventDefault()

        console.log($comment_form.find('#comment-textarea'))

        comment_json = JSON.stringify({"comment": $comment_form.find('#comment-textarea').val()})

        $.ajax({
            type: "POST",
            url: `/api/v1/stories/${$story_id}/${$current_user_id}/comments/`,
            data: comment_json,
            dataType: 'json',
            contentType: 'application/json',
            success: function (response) {
                console.log('xyz', response)
            }
        });
    })
    
    // load comments
    let $comment = (comment, idx) => {
        return ( `
        <article class="comment-card rounded-lg p-4 ${idx % 2 == 0 ? 'bg-mediumpurple text-white' : 'bg-white text-lightgray' }" data-comment_id="${ comment.id }">
            <div class="profile container mx-auto px-5 sm:px-2 ">
            <div class="flex items-center">
                ${ 
                    comment.commenter.avatar == null
                    ? `<img class="rounded-full h-[40px] w-[40px] object-cover" src="/uploads/${comment.commenter.avatar}" alt="">`
                    : `<img class="rounded-full h-[40px] w-[40px] object-cover" src="https://picsum.photos/200/700" alt="">`
 
                }
                <div class="ml-[15px]">
                    <div class="flex gap-[5px] follow-card" data-user_id=${comment.commenter.id}}>
                        <h3 class="">${comment.commenter.username}</h3>
                        <button class="follow flex items-center text-lightblue"><img src="/static/icons/plus.svg" alt="">Follow</button>
                    </div>
                    <div class="mt-[2px] flex gap-[5px] items-center">
                        <p class="text-xs">posted ${ moment(comment.created_at).fromNow()}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="relative isolate comment-text-container">
            <p class="comment-text text-sm mt-[10px] ml-[50px] h-10 overflow-hidden">${comment.comment}</p>
            <span class="span block text-white text-sm absolute bottom-0 right-0 z-10 px-1 rounded-md bg-lightblue cursor-pointer view-more">view more</span>
        </div>
        <div class="flex items-center ml-[50px]">
            <p class="mt-3 text-sm comment-like-count">${comment.likes_count }</p>
            ${
                comment.is_liked_by == true
                ? `<button class="comment-like-btn comment-liked-btn"><img class="block active:bg-lightblue" src="/static/icons/liked.svg" alt=""/></button>`
                : `<button class="comment-like-btn comment-like-btn-trans"><img class="block active:bg-lightblue" src="/static/icons/like.svg" alt=""/></button>`
            }
        </div>
    </article>
    `)}

    $.get(`/api/v1/stories/${$story_id}/${$current_user_id}/comments/`, function (response, status) {
        if (status == 'success') {
            console.log(response)
            response.forEach((comment, idx) => {
                if (idx <= 6) {
                    $comment_container.append($comment(comment, idx))

                }

            })
        }
    })



    // fetch comments based on sort-type (newest, relevant)
    let $sort_comment_by_select = $('#sort-comment-by')

    $sort_comment_by_select.on('change', function () {
        let value = $sort_comment_by_select.val()
        let $response = {}

        if (value == 'relevants') {
            
            $.get(`/api/v1/stories/${$story_id}/${$current_user_id}/comments/relevant/`, function (response, status) {
                if (status == 'success') {
                    console.log(response)
                    $comment_container.empty()
                    response.forEach((comment, idx) => {
                        if (idx <= 5) {
                            $comment_container.append($comment(comment, idx))
                        }

                    })
                }
            })
        }

        if (value == 'newests') {
            
            $.get(`/api/v1/stories/${$story_id}/${$current_user_id}/comments/newest/`, function (response, status) {
                if (status == 'success') {
                    $response = {}
                    $comment_container.empty()
                    response.forEach((comment, idx) => {
                        if (idx <= 5) {
                            $comment_container.append($comment(comment, idx))

                        }

                    })
                }
            })
        }
        
    })
})
