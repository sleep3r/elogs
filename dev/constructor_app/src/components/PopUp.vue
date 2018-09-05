<template>
    <div class="pop-up" v-bind:style="{display: display, left: x + 'px', top: y + 'px'}">
        <form-input
                    @change="(value) => onHandleChange('fieldName', value)"
                    :value="fieldName"
                    :label="'Имя'"
                    :placeholder="''"
                    class="cell-input"
        />
    </div>
</template>

<script>
    export default {
        name: "PopUp",
        props: ['display', 'x', 'y', 'cell'],
        data () {
            return {
                fieldName: ''
            }
        },
        watch: {
          cell (value) { //обработка значения инпута не работает
              if (value) {
                  this.fieldName = $(this.cell).attr('field-name')
                  // console.log($('.cell-input').val())
              }
              else {
                  this.fieldName = ''
                  // console.log($('.cell-input').val())
              }
              console.log($('.cell-input').val())
          }
        },
        methods: {
            onHandleChange (data, value) {
                this[data] = value
                $(this.cell).attr('field-name', value)
                this.$store.commit('journalState/setField', {name: this.$route.params.tableName, field: {field_name: value}})
            }
        }
    }
</script>

<style scoped>
.pop-up {
    display: none;
    position: absolute;
    width: 200px;
    border: 1px solid rgba(0,0,0,0.4);
    padding: 10px;
    border-radius: 4px;
    background-color: #fff;
}
</style>