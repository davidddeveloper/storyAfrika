$(function () {
    $('.profile-nav button, .topic-nav button').on('click', (e) => {
        const target = $(e.target);

        $('.profile-nav button, .topic-nav button').removeClass('border-b-2 border-lightgray')
        target.addClass('border-b-2 border-lightgray')

        
        $('.topic-about-container').hide(500)
        $('.topic-stories-container').show(500)
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