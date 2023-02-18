$(document).on('click', '.new_options_delete', (e) => {
    $(e.target).parent().parent().parent().remove()
    $('input[name="options_count"]').val(Number($('input[name="options_count').val()) - 1)
})