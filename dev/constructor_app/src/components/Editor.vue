<template>
    <div class="editor-container" >
       <div class="editor-header">
           <!--<btn :onClick="onAddRow">Добавить строку</btn>-->
       </div>
        <div id="editor-content" class="editor-body" v-html="table">

        </div>
        <pop-up :display="display" :x="x" :y="y" :cell="currentCell"/>
    </div>
</template>

<script>
    import Cell from './Cell'
    import PopUp from './PopUp'
    export default {
        name: "Editor",
        components: {Cell, PopUp},
        data () {
          return {
              currentCell: null,
              display: 'none',
              x: '0',
              y: '0',
              table: '<table style="width: 100%;">\n' +
                  '                <thead>\n' +
                  '                    <tr>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                        <th>\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </th>\n' +
                  '                    </tr>\n' +
                  '                </thead>\n' +
                  '                <tbody>\n' +
                  '                    <tr>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n' +
                  '                    </tr>\n' +
                  '                </tbody>\n' +
                  '            </table>',
              colsLength: 10,
              rowsLength: 1
          }
        },
        methods: {
            onAddRow () {
                this.rowsLength ++
                let table = $(this.table)
                let thead = table.find('thead')
                let tbody = table.find('tbody')
                let newRowData = ''
                thead.find('th').each(function () {
                    newRowData = newRowData + '                        <td style="width: 10.0000%;">\n' +
                  '                            <div class="cell" field-name="" row-index="0"></div>\n' +
                  '                        </td>\n'
                })
                tbody.append(newRowData)
                this.table = '<table>' + table.html() + '</table>'
            }
        },
        mounted () {
            let _this = this
            let cells = []
            $('.cell').click(function(e) {
                e.stopPropagation()
                _this.display = 'block'
                if (e.clientX + $('.pop-up').outerWidth() >= $('#app').outerWidth()) {
                    _this.x = e.clientX - $('.pop-up').outerWidth()
                }
                else _this.x = e.clientX
                _this.y = e.clientY
                _this.currentCell = this
            })
            $('.pop-up').click(function(e) {
                e.stopPropagation()
                _this.display = 'block'
            })
            $('#app').click(function(e) {
                _this.display = 'none'
                _this.currentCell = null
            })
            $('.cell').each(function () {
                cells.push({cell: this})
            })
            this.$store.commit('journalState/setTable',
                {
                    tableName: this.$route.params.tableName,
                    fields: cells
                }
            )
        }
    }
</script>

<style lang="scss">
.editor-container {

}
.editor-header {
    padding: 10px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12),0 1px 1px 1px rgba(0,0,0,0.16);
}
.editor-body {
    height: auto;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12),0 1px 1px 1px rgba(0,0,0,0.16);
}
.editor-body table input {
    width: 100%;
    box-sizing: border-box;
    padding: 6px;
    border: none;
    outline: none;
}
.editor-body table th input {
    background-color: #eaeaea;
}
.editor-body table td input {
    background-color: #ffffff;
}
table {
    width: 100%;
    border-collapse: collapse;
}
.cell {
    width: 100%;
    height: 28px;
    transition: 0.2s;

    &:hover {
        cursor: pointer;
    }
}
table td {
    padding: 0;
    border: 1px solid #a9a9a9;

    .cell:hover {
        width: 100%;
        height: 28px;
        background-color: #f9f9f9;
    }
}
table th {
    padding: 0;
    border: 1px solid #a9a9a9;
    background-color: #eaeaea;

    .cell:hover {
        width: 100%;
        height: 28px;
        background-color: #e3e3e3;
    }
}
</style>
