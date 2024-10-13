$(function () {
    $('.stories-btn').on('click', (e) => {
        $('.topic-nav').removeClass('before:right-0').addClass('before:left-0');
        $('.topic-about-container').hide(500)
        $('.topic-stories-container').show(500)
    })
    $('.about-btn').on('click', (e) => {
        $('.topic-nav').removeClass('before:left-0').addClass('before:right-0')
        $('.topic-about-container').show(500)
        $('.topic-stories-container').hide(500)
    })
    
    $('.topic-contributors-btn').on('click', function () {
        $(this).addClass('text-black').removeClass('text-lightgray')
        $('.topic-followers-btn').addClass('text-lightgray').removeClass('.text-black')
        $('.topic-contributors-container').show(400)
        $('.topic-followers-container').hide(400)
        
    })

    $('.topic-followers-btn').on('click', function () {
        $(this).addClass('text-black').removeClass('text-lightgray')
        $('.topic-contributors-btn').addClass('text-lightgray').removeClass('text-black')
        $('.topic-contributors-container').hide(400)
        $('.topic-followers-container').show(400)
    })

    $('.show-followers-card-btn').on('click', function () {
        $('.separator').show()
        $('.topic-follower-and-contributors-card').show()
    })
    $('.separator').on('click', function () {
        $(this).hide()
        $('.topic-follower-and-contributors-card').hide()

    })
})