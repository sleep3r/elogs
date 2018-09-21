<template>
  <input :class="classes"
         :name="fieldName"
         :row-index="rowIndex"
         :value="value"
         @keypress="filterInput"
         @keydown="changeFocus"
         @change="onChanged"
         @input="onInput"
         :placeholder="placeholder"
         :style="{ color: activeColor }"
         :type="type"
         v-tooltip="{content: 'Введите число', show: showCellTypeTooltip, trigger: 'manual'}"
         @blur="showCellTypeTooltip=false"
  />
</template>

<script>
import axios from 'axios'
import { VTooltip, VPopover, VClosePopover } from 'v-tooltip'

Vue.directive('tooltip', VTooltip)
Vue.directive('close-popover', VClosePopover)
Vue.component('v-popover', VPopover)

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
    }
  },
  computed: {
    tableName: function () {
        if (typeof this.$parent.props !== 'undefined') {
          return this.$parent.props.name;
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
        return this.$store.getters.cellValue(this.tableName, this.fieldName, this.rowIndex);
      },
      set: function (val) {
        this.$store.commit('SAVE_CELL_VALUE', {
          tableName: this.tableName,
          fieldName: this.fieldName,
          index: this.rowIndex,
          value: val
        });
      }
    }
  },
  methods: {
      send() {
        this.$socket.sendObj({
          'cell_location': {
            'group_id': this.$store.state.journalInfo.id,
            'table_name': this.tableName,
            'field_name': this.fieldName,
            'index': this.rowIndex
          },
          'value': this.value
        });
      },
      onInput(e) {
        this.$parent.$emit('addNewLine', { editedRowIndex: this.rowIndex });
        this.value = e.target.value;
        this.send();
      },
      onChanged() {

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

        switch(e.key) {
          case 'ArrowUp':
            let prevTr = tr.previousElementSibling;
            if (prevTr) {
              getTd(prevTr.children, rowIndex).children[0].select();
            }
            break;
          case 'ArrowDown':
            let nextTr = tr.nextElementSibling;
            if (nextTr) {
              getTd(nextTr.children, rowIndex).children[0].select();
            }
            break;
          case 'ArrowLeft':
            let prevTd = focusedTd.previousElementSibling;
            if (prevTd) {
              prevTd.children[0].select();
            }
            break;
          case 'ArrowRight':
            let nextTd = focusedTd.nextElementSibling;
            if (nextTd) {
              nextTd.children[0].select();
            }
            break;
        }
      }
  },
  mounted() {
    // initializing data
    let desc = this.$store.getters.fieldDescription(this.tableName, this.fieldName);
    this.placeholder = desc['units'] || ''
    this.minValue = desc['min_normal'] || null
    this.maxValue = desc['max_normal'] || null
    this.type = desc['type'] || 'text'

    if (this.linked) {
      // auto fill cell
      this.value = this.$store.getters[this.linked];
      this.send();
    }
  }
}
</script>
