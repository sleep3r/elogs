<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

    import Vue from 'vue/dist/vue.esm.js'
    import axios from 'axios'
    import cell from './Cell.vue'
    import tableComment from './TableComment.vue'
    import ToggleButton from 'vue-js-toggle-button'
    import store from '../store/store';

    Vue.use(ToggleButton);
    Vue.component('cell', cell);
    Vue.component('Cell', cell);
    Vue.component('table-comment', tableComment);

    export default {
        name: 'TableCommon',
        props: {
            name: String,
        },
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
                return createElement('div', 'Loading...');
            } else {
                return createElement({template: "<div class=\"journal-table\" id=\"table_id_" + this.name + "\">" + $(this.template)[0].outerHTML +
                        "<div style='overflow-x: auto; margin-bottom: 20px;'>" + $(this.template)[2].outerHTML + "</div>" + "<table-comment table-name=\"" + this.name + "\"></table-comment></div>",
                    name: 'table-' + this.name,
                    data: () => { return {
                        data: this.$data,
                        props: this.$props
                    }},
                    computed: {
                        rowsCount: function () {
                            return this.$store.getters['journalState/maxRowIndex'](this.props.name) + 1;
                        }
                    },
                    components: { 'cell': cell, 'table-comment': tableComment },
                    mounted() {

                    }
                })
            }
        },
        mounted() {
            let self = this;
            let templateUrl = 'http://localhost:8000/templates/tables/' + this.$store.getters['journalState/plantName'] + '/' + this.$store.getters['journalState/journalName'] + '/' + this.name;
            axios.get(templateUrl)
                .then(function (response) {
                    self.template = response.data;
                })
                .catch(function (error) {
                    console.log('error: ', error);
                })
        },
    }
</script>
