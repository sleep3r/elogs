<template>
    <div v-if="mode!=='edit_constraints'" :style="{ 'height': height + 'px'}" :class="cssClass">
      <!-- Regular cell -->
        <template>
            <span v-if="hasFormula" class="formula-marker" style="margin-top: 10px;"><b><i>F</i></b></span>
        </template>
        <component
            :is="tag"
            :class="['general-value', 'number-cell', 'form-control',
                    mode === 'edit' ? 'form-control__edit' : '',
                    hasFormula ? 'formula-cell' : '',
                    mode === 'view' ? 'no-shadow' : '',
                    ]"
            :name="fieldName"
            :row-index="rowIndex"
            :value="value"
            :type="type == 'number' ? '' : type"
            :readonly="mode !== 'edit' || hasFormula"
            :placeholder="placeholder"
            :style="[{ color: activeColor, fontWeight: fontWeight, outline: outline }]"
            @keypress="filterInput"
            @keydown="changeFocus"
            @change="onChanged"
            @input="onInput"
            @click="(e) => showPopover(e, {onlyChat: false})"
            @blur="showTooltip=false"
            @contextmenu.prevent="$refs.menu.open"
            v-tooltip="{content: tooltipContent, show: showTooltip,
                trigger: 'manual', placement: 'top', boundariesElement: getBody}"
            :list="fieldName"
        >{{ tag == 'textarea' ? value : '' }}</component>
        <div class="widthCell">
        </div>
        <template>
            <datalist>
                <option v-for="person in personsList" :value="person" :key="person"></option>
            </datalist>
        </template>
        <datalist :id="fieldName" v-if="options">
            <option v-for="option in options" :value="option" :key="option">{{option}}</option>
        </datalist>
        <i
            @click="(e) => showPopover(e, {onlyChat: true})"
            v-if="(cellComments.length) && (userCommentsCounter > 0)"
            class="far fa-envelope comment-notification"
        >
            <!--<span v-if="hasUnreaded" class="unreaded"></span>-->
        </i>
        <vue-context ref="menu">
            <ul>
                <li @click="deleteRow()">Удалить строку</li>
                <li @click="addRow()">Добавить строку</li>
                <li @click="flushRow()">Очистить строку</li>
            </ul>
        </vue-context>
    </div>

    <div v-else-if="type=='number'">
        <label style="width: 10%">от</label>
        <input class="number-cell general-value"
               style="width: 40%; border: none"
               :value="minValue"
               @input="onMinConstraintInput"
        >
        <label style="width: 10%">до</label>
        <input class="number-cell general-value"
               style="width: 40%; border: none"
               :value="maxValue"
               @input="onMaxConstraintInput"
        >
    </div>
</template>

<script>
    import Vue from 'vue/dist/vue.esm.js'
    import ajax from '../axios.config'
    import shortid from 'shortid'
    import {VTooltip, VPopover, VClosePopover} from 'v-tooltip'
    import CellComment from './CellComment.vue'
    import ClockPicker from './ClockPicker.vue'
    import { VueContext } from 'vue-context';
    import EventBus from '../EventBus';

    Vue.directive('tooltip', VTooltip);
    Vue.directive('close-popover', VClosePopover);
    Vue.component('v-popover', VPopover);
    Vue.component('vue-context', VueContext);
    Vue.component('CellComment', CellComment);
    Vue.component('clock-picker', ClockPicker);
    Vue.directive('tooltip', VTooltip.VTooltip);
    Vue.directive('close-popover', VTooltip.VClosePopover);
    Vue.component('v-popover', VTooltip.VPopover);


    export default {
        name: 'Cell',
        props: [
            'fieldName',
            'rowIndex',
            'linked',
            'cssClass',
            'options'

        ],
        data() {
            return {
                isShowPopover: false,
                coordX: 0,
                coordY: 0,
                classes: 'general-value number-cell form-control',
                type: null,
                placeholder: '',
                showTooltip: false,
                personsList: [],
                tooltipContent: '',
                fontWeight: 'lighter',
                minWidth: 0,
                height: null,
                highlight: false,
                backgroundColor: null,
            }
        },
        watch: {
            mode (value) {
                setTimeout(() => this.setPickersListeners(), 1)
            },
            value: function (val) {
                if (this.responsible) {
                    if (!(this.$store.getters['userState/username'] in this.responsible)) {
                        // this.$root.$emit('addTypingUser', this.responsible)
                        this.fontWeight = 'bold'
                        this.tooltipContent = Object.values(this.responsible)[0] + ' печатает...'
                        this.showTooltip = true;
                        var self = this
                        setTimeout(function() {
                            self.showTooltip = false;
                            self.fontWeight = 'lighter'
                        }, 1500);
                    }
                }
            }
        },
        computed: {
            getBody () {
                return $('body').get()
            },
            tag () {
                return this.height < 40 ? 'input' : 'textarea'
            },
            shiftId () {
                return this.$store.getters['journalState/journalInfo'].id
            },
            userCommentsCounter () {
                return this.cellComments.filter((item, index) => item.type === 'user_comment').length
            },
            cellComments () {
                return this.$store.getters['journalState/cellComments'](this.tableName, this.fieldName, this.rowIndex)
            },
            journalName () {
                return this.$store.getters['journalState/journalInfo'].journal.name
            },
            hasUnreaded () {
              // получить все сообщения
              // и автор не я
              let unreadedComments = this.cellComments.filter(v => !(this.userName in v.user));
              return (unreadedComments.length > 0);
            },
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
            outline: function () {
                return this.highlight ? '2px solid #666666' : ''
            },
            critical: function () {
                return (this.minValue && (parseInt(this.value) < parseInt(this.minValue))) ||
                    (this.maxValue && (parseInt(this.value) > parseInt(this.maxValue)));
            },
            responsibles() {
                return this.$store.getters['journalState/journalInfo'].responsibles
            },
            userIsResponsible() {
                let responsibles = this.responsibles;
                for (let i in responsibles) {
                    if (typeof responsibles[i][this.userName] !== 'undefined') {
                        return true
                    }
                }
                return false
            },
            userName() {
                return this.$store.getters['userState/username']
            },
            responsible: function () {
                return this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['responsible'];
            },
            value: {
                cache: false,
                get: function () {
                    let cell = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)
                    return typeof cell === "undefined" ? '' : cell['value']
                },
                set: function (val) {
                    // console.log('set')
                    this.$store.commit('journalState/SET_SYNCHRONIZED', navigator.onLine)
                    this.$store.commit('journalState/SAVE_CELLS', {'cells': [{
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        index: this.rowIndex,
                        value: val,
                        responsible: {[this.$store.getters['userState/username']]: this.$store.getters['userState/fullname']},
                        notSynchronized: !navigator.onLine
                    }]});
                    if (this.type === 'time' || this.type === 'date') {
                        this.onChanged()
                    }
                }
            },
            fieldConstraints: function() {
                if (this.mode == "edit_constraints") {
                    var currentMode = this.$store.getters['journalState/currentConstraintsModeId']
                    // return constraints for particular constraints mode
                    return this.$store.getters['journalState/fieldConstraints'](this.tableName, this.fieldName, currentMode)
                }
                else {
                    // return active constraints that exist for this field
                    return this.$store.getters['journalState/fieldConstraints'](this.tableName, this.fieldName, null)
                }
            },
            minValue: {
                get: function () {
                    return this.fieldConstraints['min_normal']
                },
                set: function (val) {
                    var currentMode = this.$store.getters['journalState/currentConstraintsModeId']
                    this.$store.commit('journalState/SET_CONSTRAINT', {
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        constraintType: 'min_normal',
                        constraintValue: val,
                        mode: this.$store.getters['journalState/currentConstraintsModeId']
                    })
                    var payload = {
                        fields: [{
                            name: this.fieldName,
                            table_name: this.tableName,
                            min_normal: val,
                            max_normal: this.maxValue
                        }],
                        id: currentMode,
                    }
                    ajax.put(window.HOSTNAME+`/api/bl/modes_api/`, payload, {
                        withCredentials: true
                    })
                        .catch(e => {
                            console.log(e)
                        });
                }
            },
            maxValue: {
                get: function () {
                    return this.fieldConstraints['max_normal']
                },
                set: function (val) {
                    let currentMode = this.$store.getters['journalState/currentConstraintsModeId']
                    this.$store.commit('journalState/SET_CONSTRAINT', {
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        constraintType: 'max_normal',
                        constraintValue: val,
                        mode: currentMode
                    })
                    let payload = {
                        fields: [{
                            name: this.fieldName,
                            table_name: this.tableName,
                            min_normal: this.minValue,
                            max_normal: val
                        }],
                        id: currentMode,
                    }
                    ajax.put(window.HOSTNAME+`/api/bl/modes_api/`, payload, {
                        withCredentials: true
                    })
                        .catch(e => {
                            console.log(e)
                        });
                }
            },
            hasFormula: function() {
                return Boolean(
                    this.$store.getters['journalState/fieldFormula'](
                        this.tableName, this.fieldName,
                    )
                )
            },
            mode() {
                return this.$store.getters['journalState/journalInfo'].mode;
            },
        },
        methods: {
            showPopover (e, options) {
                let x = e.clientX;
                let y = e.clientY;

                // kostyl'
                if (this.mode === 'validate') {
                    EventBus.$emit('preshow-cell-comment', {
                        show: true,
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        rowIndex: this.rowIndex,
                        onlyChat: false,
                        isNumber: this.type === 'number',
                        preshow: true
                    })
                }
                else if (this.mode !== 'validate' && options.onlyChat) {
                    EventBus.$emit('preshow-cell-comment', {
                        show: true,
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        rowIndex: this.rowIndex,
                        onlyChat: true,
                        isNumber: this.type === 'number',
                        preshow: true
                    })
                }

                let currentElement = $(e.srcElement).is('input') || $(e.srcElement).is('textarea') ? $(e.srcElement) : $(e.srcElement).siblings('input')

                let inputOffset = 4;

                setTimeout(() => {
                    let popUpWidth = $('.cell-popup').outerWidth() ? $('.cell-popup').outerWidth() : 280;
                    let appWidth = $('#app').outerWidth()
                    let popUpHeight = $('.cell-popup').outerHeight() ? $('.cell-popup').outerHeight() : 424;
                    let appHeight = $('#app').outerHeight()

                    if (e.clientX + popUpWidth >= appWidth) {
                        x = e.clientX - e.offsetX - popUpWidth + currentElement.outerWidth()
                    } else {
                        x = e.clientX  - e.offsetX
                    }

                    if (e.clientY - e.offsetY + popUpHeight + currentElement.outerHeight() >= appHeight) {
                        y = e.clientY - popUpHeight - e.offsetY - inputOffset
                    } else {
                        y = e.clientY - e.offsetY + inputOffset + currentElement.outerHeight()
                    }

                    if (this.mode === 'validate') {
                        EventBus.$emit('show-cell-comment', {
                            coordX: x,
                            coordY: y,
                            show: true,
                            tableName: this.tableName,
                            fieldName: this.fieldName,
                            rowIndex: this.rowIndex,
                            onlyChat: false,
                            isNumber: this.type === 'number',
                            preshow: false
                        })
                    }
                    else if (this.mode !== 'validate' && options.onlyChat) {
                        EventBus.$emit('show-cell-comment', {
                            coordX: x,
                            coordY: y,
                            show: true,
                            tableName: this.tableName,
                            fieldName: this.fieldName,
                            rowIndex: this.rowIndex,
                            onlyChat: true,
                            isNumber: this.type === 'number',
                            preshow: false
                        })
                    }
                }, 0)

                if (this.mode === 'edit' && this.type === 'time' && $(e.srcElement).is('input')) {
                    this.showClock(e)
                }
            },
            showClock (e) {
                EventBus.$emit('show-clock-picker', {
                    event: e,
                    tableName: this.tableName,
                    fieldName: this.fieldName,
                    rowIndex: this.rowIndex,
                })
            },
            deleteRow() {
                this.$store.commit('journalState/DELETE_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$store.dispatch('journalState/sendJournalData');
            },
            addRow() {
                this.$store.commit('journalState/INSERT_EMPTY_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$store.dispatch('journalState/sendJournalData');
            },
            flushRow() {
                this.$store.commit('journalState/FLUSH_TABLE_ROW', {tableName: this.tableName, index: this.rowIndex, maxRowIndex: this.$store.getters['journalState/maxRowIndex'](this.tableName)});
                this.$store.dispatch('journalState/sendJournalData');
            },
            setPickersListeners () {
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
            getPersons(name, plantName) {
                return ajax.get(window.HOSTNAME + `/api/bl/dicts/autocomplete/?name=${name}&plant=${plantName}`, {
                    withCredentials: true
                })  .then((response) => {
                        // console.log(response);
                        this.personsList = response.data
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            send(final=false) {
                // console.log('socket')
                this.$socket.sendObj({
                    'type': 'shift_data',
                    'final':final,
                    'cells': [{
                        'cell_location': {
                            'group_id': this.$store.getters['journalState/journalInfo'].id,
                            'table_name': this.tableName,
                            'field_name': this.fieldName,
                            'index': this.rowIndex
                        },
                        'value': this.value
                    }]
                });
            },
            onInput(e) {
                $(this.$el).find('.widthCell').text(e.target.value)
                $(this.$el).find('input').css({'min-width': $(this.$el).find('.widthCell').outerWidth()})

                this.value = e.target.value;

                // console.log('oninput')
                if ($(this.$el).find('input').attr('placeholder') === 'Фамилия И.О.') {
                    let plantName = this.$store.getters['journalState/plantName'];
                    this.getPersons(e.target.value, plantName)
                }

                this.send();
            },
            onMinConstraintInput(e) {
                this.minValue = e.target.value
            },
            onMaxConstraintInput(e) {
                this.maxValue = e.target.value
            },
            onChanged(e) {
                // console.log(this.value)
                e ? e.preventDefault() : null
                if (this.critical) {
                  console.log('critical message sent')
                    this.$socket.sendObj({
                    'type': 'messages',
                    'cell': {
                        'field_name': this.fieldName,
                        'table_name': this.tableName,
                        'group_id': this.$store.getters['journalState/journalInfo'].id,
                        'index': this.rowIndex
                    },
                    'crud': "add",
                    'message': {
                        'text': this.value,
                        'link': 'lalala',
                        'type': 'critical_value'
                    },
                });
                } else {
                  console.log('non critical message sent')
                    this.$socket.sendObj({
                        'type': 'messages',
                        'cell': {
                            'field_name': this.fieldName,
                            'table_name': this.tableName,
                            'group_id': this.$store.getters['journalState/journalInfo'].id,
                            'index': this.rowIndex
                        },
                        "crud":"update",
                    });
                }
                // setTimeout(this._updateCells(), 0)
                this.send(true)
            },
            filterInput(e) {
                if (this.type === 'number') {
                    let keycode = e.which
                    // if non number character was pressed
                    if (!(e.shiftKey == false && ((keycode == 45 && this.value == '') || keycode == 46
                        || keycode == 8 || keycode == 37 || keycode == 39 || (keycode >= 48 && keycode <= 57)))) {
                        if (keycode !== 47) {
                            this.tooltipContent = 'Введите число'
                            this.showTooltip = true;
                            event.preventDefault();
                        }
                    }
                    else {
                        this.showTooltip = false;
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
                        if (td.tagName === 'TD') {
                            index += (parseInt(td.getAttribute('colspan'), 10) || 1);
                        }
                    }
                    return index;
                }

                function getTd(tds, index) {
                    let nextRowIndex = 0
                    for (let i = 0; i < tds.length; i++) {
                        let td = tds[i];
                        if ((nextRowIndex === index)&&(td.tagName === 'TD')) {
                            return td;
                        }
                        if (td.tagName === 'TD') {
                            nextRowIndex += (parseInt(td.getAttribute('colspan'), 10) || 1);
                        }
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
                            getTd(prevTr.children, rowIndex).children[0].children[0].select();
                        }
                        break;
                    case 'ArrowDown':
                        event.preventDefault();
                        let nextTr = tr.nextElementSibling;
                        if (nextTr) {
                            getTd(nextTr.children, rowIndex).children[0].children[0].select();
                        }
                        break;
                    case 'ArrowLeft':
                        event.preventDefault();
                        let prevTd = focusedTd.previousElementSibling;
                        if (prevTd) {
                            prevTd.children[0].children[0].select();
                        }
                        break;
                    case 'ArrowRight':
                        event.preventDefault();
                        let nextTd = focusedTd.nextElementSibling;
                        if (nextTd) {
                            nextTd.children[0].children[0].select();
                        }
                        break;
                }
            },
            _updateCells() {
                // console.log("updating cells")
                let journalComponent = this.$parent.$parent.$parent
                for (let commonTableComponentIndex in journalComponent.$children) {
                    let journalComponentChildren = journalComponent.$children[commonTableComponentIndex]
                    if (journalComponentChildren.$options.name === "TableCommon") {
                        let tableComponent = journalComponentChildren.$children[0]
                        for (let cellComponentIndex in tableComponent.$children) {
                            let cellComponent = tableComponent.$children[cellComponentIndex]
                            cellComponent.$forceUpdate()
                        }
                    }
                }
            }
        },
        mounted() {
            this.height = this.$el.parentElement.clientHeight;
            // initializing data
            let desc = this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName);
            // console.log(this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName))
            this.placeholder = desc['units'] || '';
            this.type = desc['type'] || 'text';

            // this.$root.$on('send', () => {
            //     this.send();
            // })

            if (this.linked) {
                // auto fill cell
                // this.value = this.$store.getters['journalState/' + this.linked];
                // this.send();
            }

            setTimeout(() => $(this.$el).find('input').css({'min-width': $(this.$el).find('.widthCell').text(this.value).outerWidth() + 'px'}), 0)

            setTimeout(() => this.setPickersListeners(), 1)

            EventBus.$on('time-value-changed', (data) => {
                if (this.tableName === data.tableName && this.fieldName === data.fieldName && this.rowIndex === data.rowIndex) {
                    this.value = data.value
                }
            })

            EventBus.$on('highlight' + this.shiftId + this.journalName + this.tableName + this.fieldName + this.rowIndex, () => {
                this.$el.scrollIntoView({block: "center"})
                this.highlight = true
                var self = this
                setTimeout(function() {
                    self.highlight = false
                }, 4500);
            })

        }
    }
</script>

<style lang="scss">
    .on-year {
        display: inline-block;
        input {
            width: 60px;
        }
    }

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
                padding: 0;
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
            transition: opacity .50s, visibility .15s;
        }

        &[aria-hidden='false'] {
            visibility: visible;
            opacity: 1;
            transition: opacity .50s;
        }
    }

    .no-shadow.no-shadow {
        box-shadow: none;
    }

    .v-popover > span.trigger {
        height: 100%;
    }

    .unreaded {
        font-size: 0;
        border: 5px solid red;
        border-radius: 5px;
        background-color: red;

        position: absolute;
        left: -5px;
        top: -2px;
    }
</style>
