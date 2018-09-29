<template>
    <div>
        <div class="menu__panel">
            <div class="menu__title">Список цехов</div>
            <i class="menu__toggle fas fa-bars"></i>
        </div>
        <div class="menu__logo"><i class="fas fa-sitemap"></i></div>
        <ul class="menu menu--left">
            <li class="menu__item" v-for="plant in getPlants" :key="plant.name" @click="onMenuItemClick">
                <a href="#" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">{{plant.verbose_name}}</span>
                    <b class="arrow fa fa-angle-down"></b>
                </a>
                <ul class="sub-menu">
                    <!--{% for journal_path, journal_verbose in menu_data.furnace.items %}-->
                    <li class="menu__item" v-for="journal in plant.journals" :key="journal.name">
                        <a href="" :data-plant-name="plant.name" :data-journal-name="journal.name" :data-shift-id="journal.current_shift_id" class="menu-item__link">{{journal.verbose_name}}</a>
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
    import axios from 'axios'

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
            this.$store.dispatch('journalState/loadPlants')
                .then(() => {
                    setTimeout(() => this.setListeners(), 0)
                    setTimeout(() => this.setActiveItem(), 0)
                })
        },
        methods: {
            onMenuItemClick () {
                const selectorMenuItem = "li.menu__item";
                const selectorLink = "a.menu-item__link";
                event.preventDefault();
                const listItem = event.target.closest(selectorMenuItem);
                const linkNode = listItem.querySelector(selectorLink);
                const plantName = linkNode.getAttribute("data-plant-name")
                const journalName = linkNode.getAttribute("data-journal-name")

                if (plantName && journalName) {
                    this.setActiveItem()
                    this.$store.dispatch('journalState/loadJournal', {
                      'plantName': plantName,
                      'journalName': journalName,
                      'id': ''
                    })
                    // let id = this.$store.getters['journalState/journalInfo']['id']
                    // this.$router.push('/' + plantName + '/' + journalName + '/' + id + '/')
                    this.$router.push('/' + plantName + '/' + journalName + '/')
                } else {
                    listItem.classList.toggle("open");
                }
            },
            setListeners () {
                let menu = $(".column-left");
                let lastScrollTop = 0;
                let menuHeaderHeight = $('.menu__panel').outerHeight() + $('.menu__logo').outerHeight()
                let headerHeight = $('.header').outerHeight()

                $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`})

                $(window).scroll(function (event) {
                    let st = $(this).scrollTop();
                    if (st < 100) {
                        menu.css({top: '50px'})
                    }
                    if ((lastScrollTop - st > 2) && (st > 100)) {
                        menu.css({top: '50px'})
                        $('.menu--left').css({height: `calc(100vh - ${menuHeaderHeight + headerHeight + 16}px)`})
                    } else if ((st - lastScrollTop > 10) && (st > 100)) {
                        menu.css({top: '0px'})
                        $('.menu--left').css({height: `calc(100vh - (${menuHeaderHeight + 16}px))`})
                    }
                    lastScrollTop = st;
                });
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
                    `.menu__item a[data-journal-name="${this.$route.params.journal}"]`)
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
