import shortid from 'shortid'
let fieldsLength = 0

$(document).ready(function () {
    $('button[data-target="mode-cell-add"]').click(function (e) {
        e.preventDefault()
        addFieldItem()
    })
    $('#plantName').change(function () {
        $('#journal').css({display: 'block'})
    })
    $('#journalName').change(function () {
        $('#fields').css({display: 'block'})
        $('button[data-target="mode-cell-add"]').css({display: 'block'})
    })
})

function addFieldItem() {
    $('.no-fields-text').css({display: 'none'})
    let currentFieldItemId = shortid.generate()
    let fieldItem = $(`<div class="row field-item" id="${currentFieldItemId}">
                            <div class="col">
                                <input type="text" class="form-control" data-field-name="table_name" placeholder="Таблица">
                            </div>
                            <div class="col">
                                <input type="text" class="form-control" data-field-name="name" placeholder="Ячейка">
                            </div>
                            <div class="col">
                                <input type="text" class="form-control" data-field-name="min_normal" placeholder="Мин. значение">
                            </div>
                            <div class="col">
                                <input type="text" class="form-control" data-field-name="max_normal" placeholder="Макс. значение">
                            </div>
                            <div class="delete-icon" data-target="${currentFieldItemId}"><i class="fas fa-minus"></i></div>
                        </div>`)

    fieldItem.find('.delete-icon').click(function () {
        deleteFieldItem(currentFieldItemId)
    })

    $('#addModeModal .fields-container').append(fieldItem)
    fieldsLength++
}

function deleteFieldItem(id) {
    $(`#${id}`).remove()

    fieldsLength--
    if (fieldsLength === 0) {
        $('.no-fields-text').css({display: 'block'})
    }
}