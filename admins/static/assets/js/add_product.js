$(document).on('click', '.delete_variant_btn.no-ajax', (e) => {
    console.log($(e.target).parent().parent())
    $(e.target).parent().parent().parent().remove()
    let last_id = $('.del_btn_container').last().attr('data-item')
    $('.del_btn_container').last().html(
        `
            <span class="delete_variant_btn no-ajax" data-id="${last_id}">&#215;</span>
        `
    )
    $('input[name="variant_count"]').val(Number($('input[name="variant_count"]').val()) - 1)
})

let category_atributs;

function fill_atributs(wrap, data) {
    $(wrap).html('')
    let item_id = $(wrap).attr('data-item')
    for (let item of data) {
        console.log(item)
        wrap.insertAdjacentHTML('beforeend', `
                        <div class="input_box">
                            <label for="price">${item.name}</label>
                            <select name="option[${item_id}]" id="options_${item_id}_${item.id}" class='form-select'></select>
                        </div>
                    `)
        for (let opt of item.options) {
            $(`#options_${item_id}_${item.id}`).html(
                $(`#options_${item_id}_${item.id}`).html() +
                `
                    <option value="${opt.id}" >${opt.name}</option>
                 `
            )
        }
    }
}

$(document).on('change', '#product_ctg_select', (e) => {
    let id = $(e.target).val()
    let url = '/admin/get_ctg_atributs'

    $.ajax({
        url: url,
        type: 'GET',
        data: {'id': id},
        success: (data) => {
            category_atributs = data;
            console.log(data)
            let atr_wraps = document.querySelectorAll('.atributs_wrap')
            console.log(atr_wraps)
            for (let wrap of atr_wraps) {
                fill_atributs(wrap, data)
            }
        }
    })
})