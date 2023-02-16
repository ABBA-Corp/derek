$('#product_ctg_select').on('change', (e) => {
    let id = $(e.target).val()
    let url = '/admin/get_ctg_atributs'

    $.ajax({
        url: url,
        type: 'GET',
        data: {'id': id},
        success: (data) => {
            console.log(data)
            for(let item in data) {
                console.log(item)
                $('.atributs_wrap').html(
                    `
                        <select name="color[1]" id="color">
                            {% for color in colors %}
                            <option value="{{ color.id }}">{{ color.name|get_item:lang.code }}</option>
                            {% endfor %}
                        </select>
                    `
                )
            }
        }
    })
})