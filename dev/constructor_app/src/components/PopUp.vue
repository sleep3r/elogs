<template>
    <div class="pop-up" v-bind:style="{display: display, left: x + 'px', top: y + 'px'}">
        <form-input
                    @change="(value) => onHandleChange('fieldName', value)"
                    :value="fieldName"
                    :label="'Имя'"
                    :placeholder="''"
                    id="name"
        />
        <form-input
                    @change="(value) => onHandleChange('minValue', value)"
                    :value="minValue"
                    :label="'Минимальное значение'"
                    :placeholder="''"
                    id="minValue"
        />
        <form-input
                    @change="(value) => onHandleChange('maxValue', value)"
                    :value="maxValue"
                    :label="'Максимальное значение'"
                    :placeholder="''"
                    id="maxValue"
        />
    </div>
</template>

<script>
    export default {
        name: "PopUp",
        props: ['display', 'x', 'y', 'cell'],
        data () {
            return {
                fieldName: '',
                minValue: '',
                maxValue: ''
            }
        },
        watch: {
          cell (value) {
              if (value) {
                  this.fieldName = $(this.cell).attr('field-name')
                  $('#name input').val($(this.cell).attr('field-name'))
              }
              else {
                  this.fieldName = ''
                  $('#name input').val('')
                  $('#minValue input').val('')
                  $('#maxValue input').val('')
              }
          }
        },
        methods: {
            onHandleChange (data, value) {
                this[data] = value
                console.log(data)
                if (data === 'fieldName') {
                    $(this.cell).attr('field-name', value)
                }
                this.$store.commit('journalState/setField',
                    {
                        name: this.$route.params.tableName,
                        field: {field_name: this.fieldName, cell: this.cell, min_value: this.minValue, max_value: this.maxValue}
                    }
                )
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