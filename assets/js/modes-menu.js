import axios from 'axios'

let modes
let currentMode

$(document).ready(function () {
    getModes()
})

function setData() {
    modes.map(item => $('.menu--modes').append(`<li id=${item.id} class="menu__item">${item.message}</li>`))

    $('.menu--modes .menu__item').click(function () {
        $('.menu--modes .menu__item').removeClass('selected')
        $(this).addClass('selected')

        $('.mode-content__body tbody').html('')
        currentMode = getCurrentMode(+$(this).attr('id'))

        $('#modeTitle').text(currentMode.message)
        currentMode.fields.map(item =>
            $('.mode-content__body tbody').append(`<tr>
                                                        <td>${item.table_name}</td>
                                                        <td>${item.name}</td>
                                                        <td>${item.min_normal}</td>
                                                        <td>${item.max_normal}</td>
                                                   </tr>`)
        )
        $('.mode-content__title__mode-btns').css({display: 'block'})
        $('button[data-target="mode-on-off"]').text(currentMode.is_active ? 'Выключить' : 'Включить')
        $('.mode-content__body').css({display: 'block'})
    })

    $('button[data-target="mode-on-off"]').click(function () {

    })
    $('button[data-target="mode-edit"]').click(function () {

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

function getCurrentMode(id) {
    return modes.filter(item => item.id === id)[0]
}