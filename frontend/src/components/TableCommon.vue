<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

    import Vue from 'vue/dist/vue.esm.js'
    import axios from 'axios'
    import cell from './Cell.vue'
    import tableComment from './TableComment.vue'
    import ToggleButton from 'vue-js-toggle-button'
    import store from '../store/store';
    import tab from './Tabs/tab.vue';
    import tabs from './Tabs/tabs.vue';

    Vue.use(ToggleButton);
    Vue.component('cell', cell);
    Vue.component('Cell', cell);
    Vue.component('table-comment', tableComment);

    export default {
        name: 'TableCommon',
        props: [
            'name',
            'index'
        ],
        data: function () {
            return {
                fact: false,
                template: null,
                rowsCount: 1,
                months: {
                    'January': 'Январь',
                    'February': 'Февраль',
                    'March': 'Март',
                    'April': 'Апрель',
                    'May': 'Май',
                    'June': 'Июнь',
                    'July': 'Июль',
                    'August': 'Август',
                    'September': 'Сентябрь',
                    'October': 'Октябрь',
                    'November': 'Ноябрь',
                    'December': 'Декабрь'
                },
            }
        },
        render: function (createElement) {
            if (!this.template) {
                return createElement({template: '<div class="spinner-container"><i class="spinner"></i></div>'});
            } else {
                return createElement({template: "<div class=\"journal-table\" id=\"table_id_" + this.name + "\">" +
                        this.template + "<table-comment table-name=\"" + this.name + "\"></table-comment></div>",
                    name: 'table-' + this.name,
                    data: () => { return {
                        data: this.$data,
                        props: this.$props
                    }},
                    watch: {
                        rowsCount (value) {
                            setTimeout(() => {
                                $('.elog-journal-table td').each(function () {
                                    $(this).height($(this).height())
                                })
                            }, 0)
                        }
                    },
                    computed: {
                        shiftOrder: function() {
                            return this.$store.getters['journalState/shiftOrder'];
                        },
                        rowsCount: function () {
                            return this.$store.getters['journalState/maxRowIndex'](this.props.name) + 1;
                        }
                    },
                    components: { 'cell': cell, 'table-comment': tableComment, tab, tabs },
                    mounted() {
                        setTimeout(() => {
                            $('.elog-journal-table td').each(function () {
                                $(this).height($(this).height())
                            })
                        }, 0)
                    }
                })
            }
        },
        mounted() {
            let self = this;

            let templateUrl = window.HOSTNAME+'/templates/tables/' + this.$store.getters['journalState/plantName'] + '/' + this.$store.getters['journalState/journalName'] + '/' + this.name + '/';
            axios.get(templateUrl)
                .then(function (response) {
                    let $mainElement = $("<div />").append(($(response.data).clone()))
                    $mainElement.find('table').each(function () {
                        if ($(this).parent().is('div')) {
                            $(this).wrap("<div style='overflow-x: auto; margin-bottom: 20px;'></div>")
                        }
                    })
                    self.template = $mainElement[0].outerHTML

                })
                .catch(function (error) {
                    console.log('error: ', error);
                })
        },
    }
</script>
