$(function () {
    let $body = $('body')
    let $currentBlock = $('.block').first()

    // create a temporary story in database
    if (!localStorage.getItem('story_id')) {
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:4000/api/v1/stories/',
            data: JSON.stringify({"title": " ", "text": '[{"content":"xyz"}]', "user_id": $body.data('current_user_id')}),
            dataType: 'json',
            contentType: 'application/json',
            success: function (response) {
                localStorage.setItem('story_id', response.id)
            }
        })
    }

    // save state of block
    const saveBlocks = () => {
        const blocks = [];
        let $story = {}
        $('.block').each(function() {
          blocks.push({ content: $(this).html() });
        });

        //localStorage.setItem('blocks', JSON.stringify(blocks));
        let $story_id = localStorage.getItem('story_id')
        // get the story
        $.get(`http://127.0.0.1:4000/api/v1/stories/${$story_id}/`, function (response, status) {
            if (status == 'success') {
                $story = response

                // update the story
                $story.text = JSON.stringify(blocks)
                $.ajax({
                    type: "PUT",
                    url: `http://127.0.0.1:4000/api/v1/stories/${$story_id}`,
                    data: JSON.stringify($story),
                    dataType: "json",
                    contentType: "application/json",
                    success: function (response) {
                        console.log('saved to db')
                    }
                });
            }
        })
    };

    // Load blocks from local storage
    const loadBlocks = () => {
        let $story_id = localStorage.getItem('story_id')

        // get the story state
        $.get(`http://127.0.0.1:4000/api/v1/stories/${$story_id}/`, function (response, status) {
            if (status == 'success') {
                console.log(response)
                const blocks = JSON.parse(response.text) || [];
                console.log(blocks, 'asdf')
                const $container = $('#blocks-container');

                $container.empty();
                blocks.forEach(block => {
                    const $block = $(`<div class="block" contenteditable="true"><span class="handle">⇅</span>${block.content}</div>`);
                    $block.html(block.content);
                    $container.append($block);
                    console.log(block.content)
                });
            }
        })
        
        makeBlocksSortable();
    };

    //inserts a new block or delete a block
    $(document).on('keydown', '.block', function (e) {
        $(this).focus()
        //inserts a new block on enter key
        if (e.key === 'Enter') {
            e.preventDefault()
            let $newBlock = $('<div contenteditable=true class="block"><span class="handle">⇅</span></div>')
            $(this).after($newBlock)
            $newBlock.focus()
            saveBlocks()
            $currentBlock = $newBlock
        }

        // change focus on arrowup
        else if (e.key === 'ArrowUp' && $(this).prev('.block').length) {
            $(this).prev('.block').focus()
        }

        // change focus on arrowdown
        else if (e.key === 'ArrowDown' && $(this).next('.block').length) {
            $(this).next('.block').focus()
        }

       
        else if (e.key === '/' && $(this).text().replace("⇅", "").length === 0 ) {
            let $position = $(this).offset()
            
            $("#toolbar").css({
                top: $position.top - window.screenY - $(this).outerHeight() - 80,
                left: $position.left
            }).show()
        }

        //delete a block on enter key
        if (e.key === 'Backspace' && $(this).text().trim() === "") {
            if ($(this).prev('.block').length) {
                $(this).prev('.block').focus()
                $(this).remove()

                $currentBlock = $(this).prev('.block')
            }
            else if ($(this).next('.block').length) {
                $(this).next().focus()
                $(this).remove()

                $currentBlock = $(this).next('.block')
            }
        }

        // hide toolbar when typing
        if (e.key !== '/')
        {
            $("#toolbar").hide()
        }

        // hide handlers
        $(this).find('.handle').hide()
    })

    //show toolbar on select
    $(document).on("mouseup", '.block', function (e) {
        $(this).find('.handle').hide() // hide the handlers
        $('#toolbar').hide()
        $(this).focus()
        let $toolbar = $("#toolbar")
        let $selection = window.getSelection()
        let $range = $selection.getRangeAt(0)
        let $rect = $range.getBoundingClientRect()
       
        let $selectedText = $selection.toString()
        if ($selectedText) {
            $toolbar.css({
                top: window.scrollY + $rect.top - $toolbar.outerHeight() - 80,
                left: $rect.left
            }).show()
        } else {
            console.log('xzy')
            $toolbar.hide()
        }

        $currentBlock = $($selection.anchorNode).closest('.block');
    })

    //focus on block
    $(document).on("click", '.block', function (e) {
        $(this).focus()
    })

    // add the formating using execCommand
    $.each($("#formatting button"), function (key, button) {
        button.addEventListener("click", function (e) {
            document.execCommand($(this).data('format'))
        })
    })

   //show block type
   $("#type button.type-btn").on('click', function () {
    $('.types').toggle()
    
   })

    // create block type
   $(document).delegate('#types button', 'click', function (e) {
    
    switch ($(this).data('format')) {
        case "h1":
            constructBlock('h1', $currentBlock)
            break;
        
        case "h2":
            constructBlock('h2', $currentBlock)
            break;
        
        case "text":
            constructBlock('p', $currentBlock)
            break;
        
        case "p":
            constructBlock('p', $currentBlock, $css={'text-indent': '20px'})
            break;
        
        default:
            break;
    }

    // helper function
    function constructBlock ($tag, $block, $css=null) {
        $block = $(`<${$tag} contenteditable=true class="block"><span class="handle" contenteditable="false">⇅</span>${$block.text() !== '/' ? $block.text().replace("⇅", "") : ''}</${$tag}>`)

        if ($css) $block.css($css);

        $currentBlock.replaceWith($block)

        $currentBlock = $block
        $currentBlock.focus()
        if ($tag == 'p') {
            $currentBlock.find('.handle').css({
                "left": "-35px"
            })
        }
    }

    //hide types tools
    console.log($(this).closest('.types'))
    $(this).closest('.types').hide()
   })

    // make block draggable
    // Initialize sortable for the editor container
    const makeBlocksSortable = () => {
        $('#blocks-container').sortable({
            handle: '.handle',
            axis: 'y',
            containment: '#blocks-container',
            update: saveBlocks
        }
        // axis: 'y' only on x if not specified draggable everywhere
        );
    }
    makeBlocksSortable()

    // show handle on block hover
    $(document).on('mouseenter', '.block', function () {
        $(this).find('.handle').show()
    })

    $(document).on('mouseleave', '.block', function (event) {
        let target = event.relatedTarget
        let $handle = $(this).find('.handle').hide();
        /*if ($handle.is(":hover")) {
            // pass
        } else {
            $handle.hide()
        }
        $handle.mouseenter(function () { 
            //do noting
        }).mouseleave(function() {
            $handle.hide()
        })*/
    })

    $(document).on('mouseenter', '.handle', function (event) {
        $(this).show()
    })

    // save state of block when save is clicked
    $('.save-state').on('click', function () {
        saveBlocks()
    })

    // load blocks
    if (localStorage.getItem('story_id')) {
        loadBlocks()
    }

   // miscellaneous - hide all popups
   $("#toolbar").hide()
   $(".types").hide()
   $(".handle").hide()
   
   $(document).on('click', function () {
       let $selection = window.getSelection()
       let $block = $(":focus")
       if ($selection.toString() === "" && $block.text().length === 0) {

           $("#toolbar").hide()
           $('.types').hide()
       }
   })
})