<template>
    <div>
        <div class="menu__panel">
            <i class="menu__toggle fas fa-bars" @click="toggleMenu"></i>
        </div>
        <ul class="menu menu--left">
            <li class="menu__item" @click="onDashboardClick" style="padding-bottom: 10px">
                <span data-url="/dashboard" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">Панель аналитики</span>
                </span>
            </li>
            <li class="menu__item" v-for="plant in getPlants" :key="plant.name" @click="onMenuItemClick">
                <a href="#" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">{{plant.verbose_name}}</span>
                    <b class="arrow fa fa-angle-down"></b>
                </a>
                <ul class="sub-menu">
                    <!--{% for journal_path, journal_verbose in menu_data.furnace.items %}-->
                    <li class="menu__item" v-for="journal in plant.journals" :key="journal.name">
                        <a href="" :data-plant-name="plant.name" :data-journal-name="journal.name" class="menu-item__link">{{journal.verbose_name}}</a>
                    </li>
                    <!--{% endfor %}-->

                    <!--{% if user|in_group:"Big boss" or user.is_superuser or user.name == 'makagonov-s-n' %}-->
                    <!--<li class="menu__item">-->
                    <!--<a href="" data-url="/furnace/report_income_outcome_schieht" class="menu-item__link"><b>{% trans "Поступление, расходы и остатки Zn концентратов"%}</b></a>-->
                    <!--</li>-->
                    <!--<li class="menu__item">-->
                    <!--<a href="" data-url="/furnace/metals_compute" class="menu-item__link"><b>{% trans "Рассчёт металлов" %}</b></a>-->
                    <!--</li>-->
                    <!--{% endif %}-->
                </ul>
            </li>
        </ul>
    </div>
</template>

<script>
    import $ from 'jquery'
    import EventBus from '../EventBus'

    export default {
        name: "Menu",
        data() {
            return {
                menuSelector: ".menu--left"
            }
        },
        computed: {
            getPlants () {
                return this.$store.getters['journalState/plants']
            }
        },
        mounted() {
            EventBus.$on("set-menu-item", () => {
                this.setActiveItem()
            })


            this.$store.dispatch('journalState/loadPlants')
                .then(() => {
                    setTimeout(() => this.setListeners(), 0)
                    if (location.pathname !== '/dashboard') {
                        setTimeout(() => this.setActiveItem(), 0)
                    }
                    else {
                        setTimeout(() => this.onDashboardClick(), 0)
                    }
                })
        },
        methods: {
            toggleMenu () {
                $('.column-left').toggleClass('menu__hidden')
                $('.column-content').toggleClass('menu__hidden')
            },
            onMenuItemClick () {
                const selectorMenuItem = "li.menu__item";
                const selectorLink = "a.menu-item__link";
                event.preventDefault();
                const listItem = event.target.closest(selectorMenuItem);
                const linkNode = listItem.querySelector(selectorLink);
                const plantName = linkNode.getAttribute("data-plant-name")
                const journalName = linkNode.getAttribute("data-journal-name")

                let $menu = $('.menu.menu--left')

                let url = ''

                if (plantName && journalName) {
                    url = '/' + plantName + '/' + journalName;
                }

                if (url !== null && url !== "" && url !== "#") {
                    if (this.$store.getters['journalState/isSynchronized']) {
                        this.$store.dispatch('journalState/loadJournal', {
                          'plantName': plantName,
                          'journalName': journalName
                        })
                            .then((id) => {
                                this.$router.push('/' + plantName + '/' + journalName + '/' + id)
                                this.setActiveItem()

                                if ($('#app').outerWidth() < 768) {
                                    this.toggleMenu()
                                }
                            })
                    }
                } else {
                    listItem.classList.toggle("open");
                }
            },
            onDashboardClick () {
                const selectorMenuItem = 'li.menu__item';
                const selectorLink = 'span.menu-item__link[data-url="/dashboard"]';
                // event.preventDefault();
                const listItem = document.querySelector(selectorLink).closest(selectorMenuItem);

                this.closeAllItems()
                listItem.classList.toggle("open")
                this.$router.push('/dashboard')

            },
            setListeners () {
                // let menu = $(".column-left");
                // let menuLogo = $('.menu__logo');
                // let lastScrollTop = 0;
                // let menuHeaderHeight = $('.menu__panel').outerHeight() + menuLogo.outerHeight()
                // let headerHeight = $('.header').outerHeight()

                // $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`})

                // $(window).scroll(function (event) {
                //     let st = $(this).scrollTop();
                //     if (st < 100) {
                //         menu.css({top: '50px'})
                //     }
                //     if ((lastScrollTop - st > 2) && (st > 100)) {
                //         menu.css({top: '50px'})
                //         $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`})
                //     } else if ((st - lastScrollTop > 10) && (st > 100)) {
                //         menu.css({top: '0px'})
                //         $('.menu--left').css({height: `calc(100vh - (${menuHeaderHeight + 16}px))`})
                //     }
                //     lastScrollTop = st;
                // });
            },
            setActiveItem() {
                this.closeAllItems()
                function firstMatchedParent(node, selector) {
                    if (node.classList.contains(selector)) {
                        return node;
                    }
                    return firstMatchedParent(node.parentNode, selector);
                }

                let link = document.querySelector(
                    `.menu__item a[data-plant-name="${this.$route.params.plant}"][data-journal-name="${this.$route.params.journal}"]`)
                if (!link) return;

                let currentItem = link.parentNode;
                currentItem.classList.add("open");

                // set .open parentNode also
                let parentItem = firstMatchedParent(currentItem.parentNode, "menu__item");
                parentItem.classList.add("open");
            },
            closeAllItems() {
                let allItems = document.querySelectorAll(".menu--left .menu__item");
                for (let key in allItems) {
                    let menuItem = allItems[key];
                    if (typeof(menuItem) === 'object') {
                        menuItem.classList.remove("open");
                    }
                }
            }
        }
    }
</script>

<style scoped>

</style>
