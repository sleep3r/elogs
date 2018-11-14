<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

    import Vue from 'vue/dist/vue.esm.js'
    import ajax from '../axios.config'
    import cell from './Cell.vue'
    import tableComment from './TableComment.vue'
    import ToggleButton from 'vue-js-toggle-button'
    import store from '../store/store';
    import tab from './Tabs/tab.vue';
    import tabs from './Tabs/tabs.vue';

    Vue.use(ToggleButton);
    Vue.component('cell', cell);
    Vue.component(  'Cell', cell);
    Vue.component('table-comment', tableComment);

    export default {
        name: 'TableCommon',
        props: [
            'name',
            'index'
        ],
        data: function () {
            return {
                title: '',
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
                                                    '<div class="table__title">' +
                                                        '<span class="table__title__text">' + this.title + '</span>' +
                                                        // '<button v-if="userIsBoss || $store.getters[`userState/isSuperuser`]" class="btn btn-outline" @click="openConstructor">' + 'Открыть в конструкторе' + '</button>' +
                                                    '</div>' +
                                                    this.template +
                                                    "<table-comment table-name=\"" + this.name + "\"></table-comment>" +
                                                "</div>",
                    name: 'table-' + this.name,
                    data: () => { return {
                        data: this.$data,
                        props: this.$props
                    }},
                    methods: {
                        openConstructor () {
                            window.open(`${window.location.hostname === 'localhost' ?
                                'http://127.0.0.1:8085'
                                : window.FRONT_CONSTRUCTOR_HOSTNAME}/journal/${this.$route.params.journal}/table/create?plant=${this.$route.params.plant}&table=${this.props.name}&imported=true`,
                            '_blank')
                        }
                    },
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
                        userIsBoss: function () {
                            return this.$store.getters['userState/isBoss']
                        },
                        shiftOrder: function() {
                            return this.$store.getters['journalState/shiftOrder'];
                        },
                        rowsCount: function () {
                            let maxRowIndex = this.$store.getters['journalState/maxRowIndex'](this.props.name)
                            let isForPrint = this.$store.getters['journalState/isForPrint']

                            if (this.$store.getters['journalState/journalInfo'].mode === 'edit') {
                                return maxRowIndex + 1 + (isForPrint ? 10 : 0);
                            }
                            else {
                                return maxRowIndex + 1 + (isForPrint ? 10 : 0) || 1 + (isForPrint ? 10 : 0)
                            }
                        }
                    },
                    components: { 'cell': cell, 'table-comment': tableComment, tab, tabs },
                    mounted() {
                        setTimeout(() => {
                            $('.elog-journal-table td').each(function () {
                                $(this).height($(this).height())
                            })
                        }, 0)
                        setTimeout(() => {
                            $('.elog-journal-table .changing-header').each(function () {
                                $(this).height($(this).height())
                            })
                        }, 0)
                    }
                })
            }
        },
        mounted() {
            let self = this;

            let currentTable = {
                plant: self.$store.getters['journalState/plantName'],
                journal: self.$store.getters['journalState/journalName'],
                table: self.name
            }
            self.title = self.$store.getters['journalState/tableVerboseName'](currentTable.table)
            self.template = self.$store.getters['journalState/tableHTML'](currentTable)

            let templateUrl = window.HOSTNAME+'/api/templates/tables/' + this.$store.getters['journalState/plantName'] + '/' + this.$store.getters['journalState/journalName'] + '/' + this.name + '/';
            ajax.get(templateUrl)
                .then(function (response) {
                    let $mainElement = $("<div />").append(($(response.data).clone()))
                    $mainElement.find('table').each(function () {
                        if ($(this).parent().is('div')) {
                            $(this).wrap("<div style='overflow-x: auto; overflow-y: hidden; margin-bottom: 20px;'></div>")
                        }
                    })
                    self.template = $mainElement[0].outerHTML

                    if (!self.$store.getters['journalState/tableHTML'](currentTable)) {
                        self.$store.commit('journalState/ADD_TABLE_HTML', {...currentTable, html: self.template})
                    }
                    else {
                        self.$store.commit('journalState/UPDATE_TABLE_HTML', {...currentTable, html: self.template})
                    }
                })
                .catch(function (error) {
                    console.log('error: ', error);
                })
        },
    }
</script>
