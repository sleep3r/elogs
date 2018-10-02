import axios from 'axios'

let modes
let currentMode

$(document).ready(function () {
    getModes()
})

function setData() {
    modes.map(item =>
        $('.menu--modes').append(`<li id=${item.id} class="menu__item">
                                      <span>${item.message}</span>
                                      <i style="color: ${item.is_active ? '#9FBF47' : '#FF734C'}" class="fas fa-circle is-active-icon"></i>
                                  </li>`))
    setListeners()
}

function removeData() {
    $('.menu--modes').find('li').remove()
    removeModeData()
}

function setModeData() {
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
    let $onOfBtn = $('button[data-target="mode-on-off"]')
    $onOfBtn.text(currentMode.is_active ? 'Выключить' : 'Включить')
    $onOfBtn.attr('data-value', currentMode.is_active ? 'on' : 'off')
    $('.mode-content__body').css({display: 'block'})
}

function removeModeData() {
    $('.menu--modes .menu__item').removeClass('selected')
    $('.mode-content__body tbody').html('')
    $('#modeTitle').text('Выберите режим')
    $('.mode-content__body').css({display: 'none'})
    $('.mode-content__title__mode-btns').css({display: 'none'})
    $('.mode-content__title__mode-edit-btns').css({display: 'none'})
    $('button[data-target="mode-on-off"]').attr('data-value', 'off')
}

function setListeners() {
    $('.menu--modes .menu__item').click(function () {
        removeModeData()
        $(this).addClass('selected')
        currentMode = getCurrentMode(+$(this).attr('id'))
        setModeData()
    })

    $('button[data-target="mode-on-off"]').click(function () {
        toggleModeActive($('button[data-target="mode-on-off"]').attr('data-value') === 'on' ? 0 : 1)
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

        let updatedMode = Object.assign({}, currentMode, { fields: updateFieldItems() })
        updateMode(updatedMode)
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
        deleteMode()
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

function getCurrentMode(id) {
    return modes.filter(item => item.id === id)[0]
}

function updateFieldItems() {
    let updatedFields = []
    $('.mode-content__body tbody tr').each(function () {
        updatedFields.push({
            table_name: $(this).children('td[data-target="table_name"]').text(),
            name: $(this).children('td[data-target="name"]').text(),
            min_normal: +$(this).children('td[data-target="min_normal"]').text(),
            max_normal: +$(this).children('td[data-target="max_normal"]').text()
        })
    })
    return updatedFields
}

function updateMode(mode) {
    return axios.put('/bl/modes_api/', mode)
        .then(response => {
            location.reload()
            // removeData()
            // getModes().then(() => {
            //     $(`.menu--modes li[id="${currentMode.id}"]`).trigger('click')
            // })
        })
        .catch(e => {
            console.log(e)
        });
}

function toggleModeActive(isActive) {
    return axios.put('/bl/modes_api/', { id: currentMode.id, is_active: isActive })
        .then(response => {
            location.reload()
            // removeData()
            // getModes().then(() => {
            //     $(`.menu--modes li[id="${currentMode.id}"]`).trigger('click')
            // })
        })
        .catch(e => {
            console.log(e)
        });
}

function deleteMode() {
    return axios.delete(`/bl/modes_api/${currentMode.id}`)
        .then(response => {
            location.reload()
        })
        .catch(e => {
            console.log(e)
        });
}
