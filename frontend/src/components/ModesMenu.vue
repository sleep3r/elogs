<template>
    <div>
        <div class="menu__panel menu__panel--modes">
            <div class="menu__title">Список режимов</div>
            <i class="menu__toggle fas fa-bars" @click="toggleMenu"></i>
        </div>
        <div class="menu__sub-title">
            <button class="btn" data-toggle="modal" data-target="#addModeModal">Добавить режим</button>
        </div>
        <ul class="menu menu--left menu--modes">
            <li v-for="item in getModes" :id='item.id' class="menu__item" @click="onMenuItemClick(item.id)" style="padding-bottom: 10px;">
                <span>{{item.message}}</span>
                <i :style="{color: item.is_active ? '#9FBF47' : '#FF734C'}" class="fas fa-circle is-active-icon"></i>
            </li>
        </ul>
    </div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "ModesMenu",
        data() {
            return {
                menuSelector: ".menu--left"
            }
        },
        computed: {
            getModes () {
                return this.$store.getters['modesState/modes']
            }
        },
        mounted() {
            this.$store.dispatch('modesState/getModes')
                .then(() => {
                    setTimeout(() => this.setListeners(), 0);
                    setTimeout(() => this.setActiveItem(), 0)
                })
        },
        methods: {
            toggleMenu () {
                $('.column-left').toggleClass('menu__hidden');
                $('.column-content').toggleClass('menu__hidden')
            },
            onMenuItemClick (modeId) {
                event.preventDefault();

                this.$router.push('/modes?modeId=' + modeId);
                this.setActiveItem();
                this.$store.commit('modesState/SET_CURRENT_MODE', modeId);

                if ($('#app').outerWidth() < 768) {
                    this.toggleMenu()
                }
            },
            setListeners () {
                // let menu = $(".column-left");
                // let lastScrollTop = 0;
                // let menuHeaderHeight = $('.menu__panel').outerHeight() + $('.menu__sub-title').outerHeight();
                // let headerHeight = $('.header').outerHeight();

                // $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`});

                // $(window).scroll(function (event) {
                //     let st = $(this).scrollTop();
                //     if (st < 100) {
                //         menu.css({top: '50px'})
                //     }
                //     if ((lastScrollTop - st > 2) && (st > 100)) {
                //         menu.css({top: '50px'});
                //         $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`})
                //     } else if ((st - lastScrollTop > 10) && (st > 100)) {
                //         menu.css({top: '0px'});
                //         $('.menu--left').css({height: `calc(100vh - (${menuHeaderHeight + 16}px))`})
                //     }
                //     lastScrollTop = st;
                // });
            },
            setActiveItem() {
                this.closeAllItems();
                let currentModeId = this.getURLParameter('modeId');
                let currentMode = document.getElementById(currentModeId);
                currentMode ? currentMode.classList.add("open") : null
            },
            closeAllItems() {
                let allItems = document.querySelectorAll(".menu--left .menu__item");
                for (let key in allItems) {
                    let menuItem = allItems[key];
                    if (typeof(menuItem) === 'object') {
                        menuItem.classList.remove("open");
                    }
                }
            },
            getURLParameter (paramName) {
                let url = window.location.search.substring(1);
                let urlParams = url.split('&');
                for (let i = 0; i < urlParams.length; i++) {
                    let parameterName = urlParams[i].split('=');
                    if (parameterName[0] === paramName) {
                        return parameterName[1];
                    }
                }
                return "";
            }
        }
    }
</script>
