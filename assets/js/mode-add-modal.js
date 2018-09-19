import shortid from 'shortid'
import axios from "axios";
let fieldsLength = 0
let currentMode = {}

$(document).ready(function () {
    $('button[data-target="mode-cell-add"]').click(function (e) {
        e.preventDefault()
        addFieldItem()
    })
    $('button[data-target="mode-add"]').click(function (e) {
        e.preventDefault()
        currentMode.message = $('#message').val()
        currentMode.plant = $('#plantName').val()
        currentMode.journal = $('#journalName').val()
        currentMode.fields = []
        $('#fields').find('.field-item').each(function () {
            currentMode.fields.push({
                table_name: $(this).find('input[data-field-name="table_name"]').val(),
                name: $(this).find('input[data-field-name="name"]').val(),
                min_normal: $(this).find('input[data-field-name="min_normal"]').val(),
                max_normal: $(this).find('input[data-field-name="max_normal"]').val()
            })
        })
        addMode(currentMode)
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

function addMode(mode) {
    axios.post('/bl/modes-api/', mode)
        .then(response => {
            console.log('res', response)
        })
        .catch(e => {
            console.log(e)
        });
    location.reload()
}