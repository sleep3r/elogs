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
                menuSelector: ".menu--left",
            }
        },
        computed: {
            getPlants () {
                return this.$store.getters['journalState/plants']
            }
        },
        mounted() {
            EventBus.$on("set-menu-journal-item", (payload) => {
                this.pushJournalPage(payload.plantName, payload.journalName)
            })
            EventBus.$on("set-menu-dashboard-item", () => {
                this.onDashboardClick()
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
                $('.journal_title_container').toggleClass('menu__hidden')
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
                    this.pushJournalPage(plantName, journalName)
                } else {
                    listItem.classList.toggle("open");
                }
            },
            pushJournalPage(plantName, journalName) {
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
                let menu = $('.menu.menu--left');
                let lastScrollTop = 0;

                $(window).scroll(function (event) {
                    if (lastScrollTop >= $(this).scrollTop()) {
                        menu.scrollTop(menu.scrollTop() - lastScrollTop + $(this).scrollTop())
                    }
                    else {
                        menu.scrollTop(menu.scrollTop() + $(this).scrollTop() - lastScrollTop)
                    }
                    lastScrollTop = $(this).scrollTop()
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
