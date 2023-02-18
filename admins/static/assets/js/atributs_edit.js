$(document).on('click', '.new_options_delete', (e) => {
    $(e.target).parent().parent().parent().remove()
    $('.options_count').val(Number($('.options_count').val() - 1))
})