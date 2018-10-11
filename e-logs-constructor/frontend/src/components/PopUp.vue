<template>
    <div class="pop-up" v-bind:style="{display: display, left: x + 'px', top: y + 'px'}">
        <div class="form-group">
            <input type="text" id="name" class="form-control" v-model="fieldName" placeholder="Имя" @input="(value) => onHandleChange('fieldName', value)">
        </div>
        <template v-if="cellTag === 'td'">
            <div class="form-group">
                <input type="text" id="minValue" class="form-control" v-model="minValue" placeholder="Минимальное значение" @input="(value) => onHandleChange('minValue', value)">
            </div>
            <div class="form-group">
                <input type="text" id="maxValue" class="form-control" v-model="maxValue" placeholder="Максимальное значение" @input="(value) => onHandleChange('maxValue', value)">
            </div>
            <div class="form-group">
                <select required id="type" class="form-control" v-model="type" @change="(value) => onHandleChange('type', value)">
                    <option value="" selected disabled>Тип ячейки</option>
                    <option value="text">Текст</option>
                    <option value="number">Число</option>
                    <option value="datalist">Список</option>
                    <option value="date">Дата</option>
                    <option value="time">Время</option>
                    <option value="datetime">Дата со временем</option>
                </select>
            </div>
            <div class="form-group">
                <input type="text" id="units" class="form-control" v-model="units" placeholder="Единицы измерения" @input="(value) => onHandleChange('units', value)">
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        name: "PopUp",
        props: ['display', 'x', 'y', 'cell', 'cellTag', 'selectedCells'],
        data () {
            return {
                fieldName: '',
                minValue: '',
                maxValue: '',
                type: '',
                units: ''
            }
        },
        watch: {
          cell (value) {
              if (value && this.cellTag === 'td' && this.selectedCells.length === 1) {
                  this.fieldName = $(`#${this.cell}`).attr('field-name')
                  this.minValue = this.$store.getters['journalState/getCellMinValue'](this.$route.params.tableName, this.cell)
                  this.maxValue = this.$store.getters['journalState/getCellMaxValue'](this.$route.params.tableName, this.cell)
                  this.type = this.$store.getters['journalState/getCellType'](this.$route.params.tableName, this.cell)
                  this.units = this.$store.getters['journalState/getCellUnits'](this.$route.params.tableName, this.cell)
              }
              else if (value && this.cellTag === 'th') {
                  this.fieldName = $(`#${this.cell}`).text()
                  this.minValue = ''
                  this.maxValue = ''
                  this.type = ''
                  this.units = ''
              }
              else {
                  this.fieldName = ''
                  this.minValue = ''
                  this.maxValue = ''
                  this.type = ''
                  this.units = ''
              }

              $('#name input').val(this.fieldName)
              $('#minValue input').val(this.minValue)
              $('#maxValue input').val(this.maxValue)
              $('#type input').val(this.type)
              $('#units input').val(this.units)
          }
        },
        methods: {
            onHandleChange (data, input) {
                if (data === 'fieldName') {
                    this.selectedCells.map(item => {
                        $(item).attr('field-name', input.target.value)
                    })
                    if (this.cellTag === 'th') {
                        $(`#${this.cell}`).text(input.target.value)
                    }
                    else {
                        this.selectedCells.map(item => {
                            $(item).text(input.target.value)
                        })
                    }
                }

                if (this.cellTag === 'td') {
                    this.$store.commit('journalState/setFields',
                        {
                            name: this.$route.params.tableName,
                            fields: {
                                field_name: this.fieldName,
                                cells: this.selectedCells,
                                min_value: this.minValue,
                                max_value: this.maxValue,
                                type: this.type,
                                units: this.units
                            }
                        }
                    )
                }
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
.form-group {
    margin-bottom: 15px;
}
.form-group select:invalid {
    color: #999;
}
.form-group:last-child {
    margin-bottom: 0;
}
.form-group select option:first-child{
    display: none;
}
</style>