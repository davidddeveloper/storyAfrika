$(function () {
    let showCommentViewBtn = $('.show-comment-view')
    let commentView = $('.comments-view')

    const checkElementOverflowing = (el) => {

    }

    $('body').on('click', '.show-comment-view', () => {
        if (commentView.hasClass('is-hidden')) {
            commentView.removeClass('md:-right-[100%] is-hidden -bottom-[100%]').addClass('-bottom-[20%] md:right-0')

        } else {
            commentView.removeClass('md:right-0').addClass('md:-right-[100%] is-hidden')
        }
    })

    $('.comment-textarea').on('input', function () {
        if ($(this).val().length > 8) $('.share-comment').removeAttr('disabled').removeClass('opacity-0')
        else $('.share-comment').addClass('opacity-0').attr('disabled')
    })

    $('.view-more').on('click', function () {
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


})