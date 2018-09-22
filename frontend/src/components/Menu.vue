<template>
    <div>
        <div class="menu__panel">
            <div class="menu__title">Список цехов</div>
            <i class="menu__toggle fas fa-bars"></i>
        </div>
        <div class="menu__logo"><i class="fas fa-sitemap"></i></div>
        <ul class="menu menu--left">
            <li class="menu__item open">
                <a href="#" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">Обжиг</span>
                    <b class="arrow fa fa-angle-down"></b>
                </a>
                <ul class="sub-menu">
                    <!--{% for journal_path, journal_verbose in menu_data.furnace.items %}-->
                    <li class="menu__item">
                        <a href="" data-url='??journal_path??' class="menu-item__link">?? journal_verbose ??</a>
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
            <li class="menu__item">
                <a href="#" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">Выщелачивание</span>
                    <b class="arrow fa fa-angle-down"></b></a>
                <ul class="sub-menu">
                    <!--{% for journal_path, journal_verbose in menu_data.leaching.items %}-->
                    <li class="menu__item">
                        <a href="" data-url='?? journal_path ??' class="menu-item__link">?? journal_verbose ??</a>
                    </li>
                    <!--{% endfor %}-->
                </ul>
            </li>
            <li class="menu__item">
                <a href="#" class="menu-item__link">
                    <i class="menu-item__icon fa fa-book"></i>
                    <span class="menu-item__title">Электролиз</span>
                    <b class="arrow fa fa-angle-down"></b>
                </a>
                <ul class="sub-menu">
                    <!--{% for journal_path, journal_verbose in menu_data.electrolysis.items %}-->
                    <li class="menu__item">
                        <a href="" data-url='??  journal_path  ??' class="menu-item__link">?? journal_verbose ??</a>
                    </li>
                    <!--{% endfor %}-->
                </ul>
            </li>
        </ul>
    </div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Menu",
        data() {
            return {
                menuSelector: ".menu--left"
            }
        },
        mounted () {
            const selectorMenuItemTopLevel = ".menu > li.menu__item";
            const selectorMenuItem = "li.menu__item";
            const selectorLink = "a.menu-item__link";
            let items = document.querySelectorAll(selectorMenuItemTopLevel);
            [].forEach.call(items, (item) => {
                item.addEventListener('click', function (event) {
                    event.preventDefault();
                    const listItem = event.target.closest(selectorMenuItem);
                    const linkNode = listItem.querySelector(selectorLink);
                    const url = linkNode.getAttribute("data-url");

                    if (url !== null && url !== "" && url !== "#") {
                        location.href = url;
                    } else {
                        listItem.classList.toggle("open");
                    }

                }, false);
            });

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

            this.closeAllItems();
            this.setActiveItem();
        },
        methods: {
            setActiveItem () {
                function firstMatchedParent(node, selector) {
                    if (node.classList.contains(selector)) {
                        return node;
                    }
                    return firstMatchedParent(node.parentNode, selector);
                }

                let link = document.querySelector(this.menuSelector).querySelector(".menu__item a[data-url='" + location.search + "']");
                if (!link) return;

                let currentItem = link.parentNode;
                currentItem.classList.add("open");

                // set .open parentNode also
                let parentItem = firstMatchedParent(currentItem.parentNode, "menu__item");
                parentItem.classList.add("open");
            },
            closeAllItems () {
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