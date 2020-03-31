$('.multi-menu .title').click(function () {
    $(this).next().removeClass('hidden').parent().siblings().find('.body').addClass('hidden')
})
