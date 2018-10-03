<template>
    <v-popover
            offset="16"
            :disabled="mode !== 'validate'">
        <input
                :class="classes"
                :name="fieldName"
                :row-index="rowIndex"
                :value="value"
                @keypress="filterInput"
                @keydown="changeFocus"
                @change="onChanged"
                @input="onInput"
                @blur="showCellTypeTooltip=false"
                :readonly="mode !== 'edit'"
                :placeholder="placeholder"
                :style="{ color: activeColor }"
                :type="type"
                v-tooltip="{content: 'Введите число', show: showCellTypeTooltip, trigger: 'manual'}"
                @contextmenu.prevent="$refs.menu.open"
        >
        <template>
            <datalist>
                <option v-for="item in personsList" :value="item"></option>
            </datalist>
        </template>
        <i
                v-if="$store.getters['journalState/cellComment'](tableName, fieldName, rowIndex)"
                class="far fa-envelope comment-notification"></i>
        <template slot="popover">
            <CellComment
                    :table-name="tableName"
                    :field-name="fieldName"
                    :row-index="rowIndex"/>
        </template>

        <!-- Menu to create, delete and flush a row -->
        <vue-context ref="menu">
            <ul>
                <li @click="deleteRow()">Удалить строку</li>
                <li @click="addRow()">Добавить строку</li>
                <li @click="flushRow()">Очистить строку</li>
            </ul>
        </vue-context>
    </v-popover>
</template>

<script>
    import Vue from 'vue/dist/vue.esm.js'
    import axios from 'axios'
    import shortid from 'shortid'
    import {VTooltip, VPopover, VClosePopover} from 'v-tooltip'
    import CellComment from './CellComment.vue'
    import { VueContext } from 'vue-context';
    import 'clockpicker/dist/bootstrap-clockpicker.min'

    Vue.directive('tooltip', VTooltip);
    Vue.directive('close-popover', VClosePopover);
    Vue.component('v-popover', VPopover);
    Vue.component('vue-context', VueContext);
    Vue.component('CellComment', CellComment);


    export default {
        name: 'Cell',
        props: [
            'fieldName',
            'rowIndex',
            'linked'
        ],
        data() {
            return {
                classes: 'general-value number-cell form-control',
                minValue: null,
                maxValue: null,
                type: null,
                placeholder: '',
                showCellTypeTooltip: false,
                personsList: null,
            }
        },
        watch: {
            mode (value) {
                this.setPickersListeners()
            }
        },
        computed: {
            tableName: function () {
                if (typeof this.$parent.props !== 'undefined') {
                    return this.$parent.props.name;
                }
                else {
                    return ''
                }
            },
            activeColor: function () {
                return this.critical ? 'red' : '';
            },
            critical: function () {
                return (this.minValue && (this.value < this.minValue)) ||
                    (this.maxValue && (this.value > this.maxValue));
            },
            value: {
                get: function () {
                    return this.$store.getters['journalState/cellValue'](this.tableName, this.fieldName, this.rowIndex);
                },
                set: function (val) {
                    this.$store.commit('journalState/SET_SYNCHRONIZED', navigator.onLine)
                    this.$store.commit('journalState/SAVE_CELL_VALUE', {
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        index: this.rowIndex,
                        value: val,
                        notSynchronized: !navigator.onLine
                    });
                }
            },
            mode() {
                return this.$store.getters['journalState/journalInfo'].mode;
            },
        },
        methods: {
            deleteRow() {
                console.log('delete row')
                this.$store.commit('journalState/DELETE_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$root.$emit('send');
            },
            addRow() {
                this.$store.commit('journalState/INSERT_EMPTY_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$root.$emit('send');
            },
            flushRow() {
                this.$store.commit('journalState/FLUSH_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$root.$emit('send');
            },
            setPickersListeners () {
                if (this.type === 'time') {
                    if (this.mode === 'edit') {
                        $(this.$el).find('input').clockpicker({
                            autoclose: true,
                            'default': 'now',
                            donetext: false,
                            afterDone: () => {
                                this.value = $(this.$el).find('input').val();
                            }
                        })
                    }
                    else {
                        $(this.$el).find('input').clockpicker('remove')
                    }
                }
                if (this.type === 'date') {
                    if (this.mode === 'edit') {
                        $(this.$el).find('input').datepicker({
                            format: 'yyyy-mm-dd',
                            autoclose: true,
                            endDate: '+0d'
                        }).on('changeDate', () => {
                            this.value = $(this.$el).find('input').val();
                        })
                    }
                    else {
                        $(this.$el).find('input').datepicker('destroy')
                    }
                }

                if ($(this.$el).find('input').attr('placeholder') === 'Фамилия И.О.') {
                    let currentId = shortid.generate()
                    $(this.$el).find('input').attr('list', currentId)
                    $(this.$el).find('datalist').attr('id', currentId)
                }
            },
            getPersons(name) {
                return axios.get(`http://127.0.0.1:8000/api/autocomplete/?name=${name}`, {
                    withCredentials: true
                })
                    .catch(err => {
                        console.log(err)
                    })
            },
            send() {
                this.$socket.sendObj({
                    'type': 'shift_data',
                    'cell_location': {
                        'group_id': this.$store.getters['journalState/journalInfo'].id,
                        'table_name': this.tableName,
                        'field_name': this.fieldName,
                        'index': this.rowIndex
                    },
                    'value': this.value
                });
            },
            onInput(e) {
                this.value = e.target.value;
                if ($(this.$el).find('input').attr('placeholder') === 'Фамилия И.О.') {
                    this.getPersons(e.target.value)
                        .then((resp) => {
                            this.personsList = resp.data
                        })
                }

                this.send();
            },
            onChanged(e) {
                e.preventDefault()
            },
            filterInput(e) {
                if (this.type === 'number') {
                    let keycode = e.which
                    // if non number character was pressed
                    if (!(e.shiftKey == false && ((keycode == 45 && this.value == '') || keycode == 46
                        || keycode == 8 || keycode == 37 || keycode == 39 || (keycode >= 48 && keycode <= 57)))) {
                        this.showCellTypeTooltip = true;
                        event.preventDefault();
                    }
                    else {
                        this.showCellTypeTooltip = false;
                    }
                }
            },

            changeFocus(e) {
                function getIndex(tds, focusedTd) {
                    let index = 0
                    for (let i = 0; i < tds.length; i++) {
                        let td = tds[i];
                        if (td === focusedTd) {
                            break;
                        }
                        index += (parseInt(td.getAttribute('colspan'), 10) || 1);
                    }
                    return index;
                }

                function getTd(tds, index) {
                    let nextRowIndex = 0
                    for (let i = 0; i < tds.length; i++) {
                        let td = tds[i];
                        if (nextRowIndex === index) {
                            return td;
                        }
                        nextRowIndex += (parseInt(td.getAttribute('colspan'), 10) || 1);
                    }
                }

                let focusedTd = this.$el.parentElement;
                let tr = focusedTd.parentElement;
                let rowIndex = getIndex(tr.children, focusedTd);


                switch (e.key) {
                    case 'ArrowUp':
                        event.preventDefault();
                        let prevTr = tr.previousElementSibling;
                        if (prevTr) {
                            getTd(prevTr.children, rowIndex).children[0].children[0].children[0].select();
                        }
                        break;
                    case 'ArrowDown':
                        event.preventDefault();
                        let nextTr = tr.nextElementSibling;
                        if (nextTr) {
                            getTd(nextTr.children, rowIndex).children[0].children[0].children[0].select();
                        }
                        break;
                    case 'ArrowLeft':
                        event.preventDefault();
                        let prevTd = focusedTd.previousElementSibling;
                        if (prevTd) {
                            prevTd.children[0].children[0].children[0].select();
                        }
                        break;
                    case 'ArrowRight':
                        event.preventDefault();
                        let nextTd = focusedTd.nextElementSibling;
                        if (nextTd) {
                            nextTd.children[0].children[0].children[0].select();
                        }
                        break;
                }
            }
        },
        mounted() {
            // initializing data
            let desc = this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName);
            this.placeholder = desc['units'] || '';
            this.minValue = desc['min_normal'] || null;
            this.maxValue = desc['max_normal'] || null;
            this.type = desc['type'] || 'text';

            this.$root.$on('send', () => {
                this.send();
            })

            if (this.linked) {
                // auto fill cell
                this.value = this.$store.getters['journalState/' + this.linked];
                this.send();
            }

            this.setPickersListeners()
        }
    }
</script>

<style lang="scss">
    .tooltip {
        display: block !important;
        z-index: 10000;

        .tooltip-inner {
            max-width: 450px;
            background: black;
            color: white;
            border-radius: 16px;
            padding: 5px 10px 4px;
        }

        .tooltip-arrow {
            width: 0;
            height: 0;
            border-style: solid;
            position: absolute;
            margin: 5px;
            border-color: black;
            z-index: 1;
        }

        &[x-placement^="top"] {
            margin-bottom: 5px;

            .tooltip-arrow {
                border-width: 5px 5px 0 5px;
                border-left-color: transparent !important;
                border-right-color: transparent !important;
                border-bottom-color: transparent !important;
                bottom: -5px;
                left: calc(50% - 5px);
                margin-top: 0;
                margin-bottom: 0;
            }
        }

        &[x-placement^="bottom"] {
            margin-top: 5px;

            .tooltip-arrow {
                border-width: 0 5px 5px 5px;
                border-left-color: transparent !important;
                border-right-color: transparent !important;
                border-top-color: transparent !important;
                top: -5px;
                left: calc(50% - 5px);
                margin-top: 0;
                margin-bottom: 0;
            }
        }

        &[x-placement^="right"] {
            margin-left: 5px;

            .tooltip-arrow {
                border-width: 5px 5px 5px 0;
                border-left-color: transparent !important;
                border-top-color: transparent !important;
                border-bottom-color: transparent !important;
                left: -5px;
                top: calc(50% - 5px);
                margin-left: 0;
                margin-right: 0;
            }
        }

        &[x-placement^="left"] {
            margin-right: 5px;

            .tooltip-arrow {
                border-width: 5px 0 5px 5px;
                border-top-color: transparent !important;
                border-right-color: transparent !important;
                border-bottom-color: transparent !important;
                right: -5px;
                top: calc(50% - 5px);
                margin-left: 0;
                margin-right: 0;
            }
        }

        &.popover {
            $color: #f9f9f9;

            .popover-inner {
                background: $color;
                color: black;
                padding: 0px;
                border-radius: 5px;
                box-shadow: 0 5px 30px rgba(black, .1);
            }

            .popover-arrow {
                border-color: $color;
            }
        }

        &[aria-hidden='true'] {
            visibility: hidden;
            opacity: 0;
            transition: opacity .15s, visibility .15s;
        }

        &[aria-hidden='false'] {
            visibility: visible;
            opacity: 1;
            transition: opacity .15s;
        }
    }
</style>
