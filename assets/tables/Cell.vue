<template>
  <input :class="classes"
         :name="fieldName"
         :row-index="rowIndex"
         v-model="value"
         @keypress="filterInput"
         @keydown="changeFocus"
         @change="onChanged"
         @input="onInput"
         :placeholder="placeholder"
         :style="{ color: activeColor }"
         :type="type"
  />
</template>

<script>
import axios from 'axios'

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
        value: '',
        minValue: null,
        maxValue: null,
        type: null,
        placeholder: '',
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
      if ((this.minValue && (this.value < this.minValue)) ||
          (this.maxValue && (this.value > this.maxValue))) {
        return true;
      }
      else {
        return false;
      }
    }
  },
  methods: {
      send() {
        axios
          .post('/common/save_cell/', {
            'cell_location': {
              'group_id': this.$store.state.journalInfo.id,
              'table_name': this.tableName,
              'field_name': this.fieldName,
              'index': this.rowIndex
            },
            'value': this.value
          })
          .then(response => {
            if (response.data.status !== 1) {
              console.log('didn`t save cell on server status:', response.data.status);
            }
          })
      },
      onInput(e) {
        this.$store.commit('SAVE_CELL_VALUE', {
          tableName: this.tableName,
          fieldName: this.fieldName,
          index: this.rowIndex,
          value: this.value
        })
        this.$parent.$emit('addNewLine', { editedRowIndex: this.rowIndex });
      },
      onChanged() {
        this.send();
      },
      filterInput(e) {
        if (this.type === 'number') {
          let keycode = e.which
          console.log('code')
          console.log(keycode)
          // if non number character was pressed
          if (!(e.shiftKey == false && ((keycode == 45 && this.value == '') || keycode == 46
            || keycode == 8 || keycode == 37 || keycode == 39 || (keycode >= 48 && keycode <= 57)))) {
            console.log('it is a number field')
            event.preventDefault();
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
              getTd(prevTr.children, rowIndex).children[0].focus();
            }
            break;
          case 'ArrowDown':
            let nextTr = tr.nextElementSibling;
            if (nextTr) {
              getTd(nextTr.children, rowIndex).children[0].focus();
            }
            break;
          case 'ArrowLeft':
            let prev = focusedTd.previousElementSibling;
            if (prev) {
              prev.children[0].focus();
            }
            break;
          case 'ArrowRight':
            let next = focusedTd.nextElementSibling;
            if (next) {
              next.children[0].focus();
            }
            break;
        }
      }
  },
  mounted() {
    // initializing data
    this.value = this.$store.getters.cellValue(this.tableName, this.fieldName, this.rowIndex);
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
