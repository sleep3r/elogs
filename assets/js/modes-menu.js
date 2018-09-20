import axios from 'axios'

let modes
let currentMode

$(document).ready(function () {
    getModes()
})

function setData() {
    modes.map(item => $('.menu--modes').append(`<li id=${item.id} class="menu__item">${item.message}</li>`))
    setListeners()
}

function setListeners() {
    $('.menu--modes .menu__item').click(function () {
        $('.menu--modes .menu__item').removeClass('selected')
        $(this).addClass('selected')

        $('.mode-content__body tbody').html('')
        currentMode = getCurrentMode(+$(this).attr('id'))

        $('#modeTitle').text(currentMode.message)
        currentMode.fields.map(item =>
            $('.mode-content__body tbody').append(`<tr>
                                                        <td data-target="table_name">${item.table_name}</td>
                                                        <td data-target="name">${item.name}</td>
                                                        <td data-target="min_normal">${item.min_normal}</td>
                                                        <td data-target="max_normal">${item.max_normal}</td>
                                                   </tr>`)
        )
        $('.mode-content__title__mode-btns').css({display: 'block'})
        $('button[data-target="mode-on-off"]').text(currentMode.is_active ? 'Выключить' : 'Включить')
        $('.mode-content__body').css({display: 'block'})
    })

    $('button[data-target="mode-on-off"]').click(function () {

    })

    $('button[data-target="mode-edit"]').click(function () {
        $('.mode-content__body td').each(function () {
            $(this).html($(`<input type="text" class="form-control" value="${$(this).text()}">`))
        })
        $('.mode-content__title__mode-btns').css({display: 'none'})
        $('.mode-content__title__mode-edit-btns').css({display: 'block'})
    })

    $('button[data-target="mode-save"]').click(function () {
        $('.mode-content__body tbody tr').each(function () {
            let _this = this
            $(this).children('td').each(function () {
                if (!$(this).find('input').val()) {
                    $(_this).remove()
                }
            })
        })
        $('.mode-content__body td').each(function () {
            $(this).html(`${$(this).find('input').val()}`)
        })
        $('.mode-content__title__mode-edit-btns').css({display: 'none'})
        $('.mode-content__title__mode-btns').css({display: 'block'})

        updateFieldItems()
        console.log(currentMode)
    })

    $('button[data-target="mode-add-row"]').click(function () {
        $('.mode-content__body tbody').append(`<tr>
                                                    <td data-target="table_name"><input type="text" class="form-control" value=""></td>
                                                    <td data-target="name"><input type="text" class="form-control" value=""></td>
                                                    <td data-target="min_normal"><input type="text" class="form-control" value=""></td>
                                                    <td data-target="max_normal"><input type="text" class="form-control" value=""></td>
                                               </tr>`)
    })

    $('button[data-target="mode-delete"]').click(function () {

    })
}

function getModes() {
    return axios.get('/bl/modes_api/')
        .then(response => {
            modes = response.data
            setData()
        })
        .catch(e => {
            console.log(e)
        });
}

function updateFieldItems() {
    // $('.mode-content__body tbody tr').each(function () {
    //     let currentField = currentMode.fields.filter(item => item.name === $(this).children('td[data-target="name"]').text())[0]
    //     if (!currentField) {
    //         currentField = {
    //             name: $(this).children('td[data-target="name"]').text()
    //         }
    //     }
    //     currentField.table_name = $(this).children('td[data-target="table_name"]').text()
    //     currentField.name = $(this).children('td[data-target="name"]').text()
    //     currentField.min_normal = $(this).children('td[data-target="min_normal"]').text()
    //     currentField.max_normal = $(this).children('td[data-target="max_normal"]').text()
    //
    //     currentMode.fields.map(item => item.name === currentField.name ? item = currentField : currentMode.fields.push(currentField))
    // })
}

function updateMode() {
    return axios.put('/bl/modes_api/', currentMode)
        .then(response => {
            location.reload()
        })
        .catch(e => {
            console.log(e)
        });
}

function getCurrentMode(id) {
    return modes.filter(item => item.id === id)[0]
}