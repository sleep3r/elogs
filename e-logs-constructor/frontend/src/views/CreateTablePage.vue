<template>
    <div class="create-table">
        <h2 class="title">Создание секции</h2>
        <form class="form" @submit.prevent="onHandleContinue">
            <div class="form-group">
                <input type="text" class="form-control" v-model="title" placeholder="Заголовок" @input="onHandleChange">
            </div>
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="repeatableRow" v-model="repeatableRow" @change="onHandleChange">
                <label class="form-check-label" for="repeatableRow">Повторяющиеся строки</label>
            </div>
            <div v-show="error" class="error">
                Введите заголовок
            </div>
        </form>
        <div class="wysiwyg">
            <h3 class="title">Создание структуры таблицы</h3>
            <div id="summernote"></div>
            <div class="btns">
                <button class="btn btn-secondary" @click="onHandleBack" style="margin-right: 14px">Назад</button>
                <button class="btn btn-success" @click="onFormatHtml" style="margin-right: 14px">Formate html</button>
                <button class="btn btn-primary" @click.prevent="onHandleContinue" type="submit">Продолжить</button>
            </div>
        </div>
    </div>
</template>

<script>
// import 'jquery'
// import 'bootstrap3/dist/js/npm';
// import 'bootstrap3/dist/js/bootstrap';
// import 'summernote/dist/summernote.css'
// import 'summernote/dist/summernote'

import toggleHeaderInit from '../wysiwyg_modules/toggle-header'
import mergeCellsInit from '../wysiwyg_modules/merge-cells'
import splitH from '../wysiwyg_modules/split-horizontally'
import splitV from '../wysiwyg_modules/split-vertically'
import addCol from '../wysiwyg_modules/add-column'
import addRow from '../wysiwyg_modules/add-row'
import removeCol from '../wysiwyg_modules/remove-column'
import removeRow from '../wysiwyg_modules/remove-row'
import formatFactory from '../utils/formatFactory.js'
import slugify from 'slugify'
export default {
    name: "CreateTablePage",
    data () {
        return {
            title: '',
            repeatableRow: false,
            redips: {},
            repeatableRowDefaultHTML:
                `<table class="table table-bordered">
                <tbody>
                    <tr>
                        <th></th>
                        <th></th>
                        <th></th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tr>
                    <tr>
                        <td>
                            <br>
                        </td>
                        <td>
                            <br>
                        </td>
                        <td>
                            <br>
                        </td>
                        <td>
                            <br>
                        </td>
                        <td>
                            <br>
                        </td>
                        <td>
                            <br>
                        </td>
                    </tr>
                </tbody>
            </table>`,
            error: ''
        }
    },
    watch: {
        repeatableRow (value) {
            if (value) {
                $('#summernote').summernote('code', this.repeatableRowDefaultHTML)
            }
            else {
                $('#summernote').summernote('code', '')
            }
        }
    },
    methods: {
        onHandleBack () {
            this.$router.back()
        },
        onHandleChange (data) {
           data.target.value ? this.error = '' : this.error = true
        },
        onHandleContinue () {
            $('.note-popover').css({display: 'none'})
            $('.note-editable td').removeAttr('style')
            if (this.title && this.$store.getters['journalState/getJournalName']) {
                this.$store.commit('journalState/addTable',
                    {
                        title: this.title,
                        name: slugify(this.title, '_'),
                        fields: [],
                        html: $('#summernote').summernote('code'),
                        repeatable_row: this.repeatableRow
                    }
                )
                this.$router.push(`/journal/${this.$route.params.journalName}/table/${slugify(this.title, '_')}/edit_data`)
            }
            else if (!this.$store.getters['journalState/getJournalName']) {
                this.$router.push('/')
            }
            else this.error = true
        },
        onFormatHtml () {
            if (this.repeatableRow) {
                let code = $('#repeatableSummernote').summernote('code');
                let formattedCode = formatFactory(code);
                $('#repeatableSummernote').summernote('code', formattedCode);
            }
            else {
                let code = $('#summernote').summernote('code');
                let formattedCode = formatFactory(code);
                $('#summernote').summernote('code', formattedCode);
            }
        },
        redipsInit () {
            let _this = this
            _this.redips.init = function () {
                let rt = REDIPS.table;
                rt.onmousedown('redipsTable', true);

                rt.color.cell = '#9BB3DA';

                _this.redips.merge = function () {
                    REDIPS.table.merge('h', false);
                    REDIPS.table.merge('v');
                };

                _this.redips.split = function (mode) {
                    REDIPS.table.split(mode);
                };

                _this.redips.row = function (type) {
                    REDIPS.table.row('redipsTable', type);
                };

                _this.redips.column = function (type) {
                    REDIPS.table.column('redipsTable', type);
                };
            };
            window.redips = _this.redips
        },
        summernoteInit () {
            let _this = this
            $(document).ready(function() {
                $('#summernote').summernote({
                    height: 300,
                    minHeight: null,
                    maxHeight: null,
                    focus: true,
                    toolbar: [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        ['insert', ['table', 'link', 'hr']],
                        ['misk', ['undo', 'redo']],
                        ['view', ['fullscreen', 'codeview']]
                    ],
                    popover: {
                        table: [
                            ['add', ['addColumnPlugin', 'addRowPlugin']],
                            ['delete', ['removeColumnPlugin', 'removeRowPlugin']],
                            ['split', ['splitH', 'splitV']],
                            ['custom', ['cellHeader', 'mergeCells']]
                        ],
                    },
                });
                $('#summernote').on('summernote.change', function (we, contents, $editable) {
                    console.log('summernote\'s content is changed.');

                    let table = $('.note-editable table:first')
                    if (table.length) {
                        table.attr('id', 'redipsTable')
                        _this.redips.init()
                    }

                    // remove '<p><br></p>' inside tables
                    // (summernote creates them when nesting table in table)
                    var uselessParagraphs = document.querySelectorAll('table p'), i;
                    for (i = 0; i < uselessParagraphs.length; ++i) {
                        let p = uselessParagraphs[i];
                        p.parentNode.removeChild(p);
                    }
                });
            })
        }
    },
    mounted () {
        this.redipsInit()
        if ($.summernote) {
            toggleHeaderInit();
            mergeCellsInit();
            splitH()
            splitV()
            addCol()
            addRow()
            removeCol()
            removeRow()
            this.summernoteInit()
        }
    }
}
</script>

<style scoped>
.create-table {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}
.create-table > h2.title{
    margin-top: 0;
    margin-bottom: 20px;
}
.error {
    display: flex;
    align-items: center;
    background-color: rgb(245, 108, 108);
    color: rgb(255, 255, 255);
    height: 40px;
    border-radius: 6px;
    padding: 0px 15px;
    margin-bottom: 20px;
}
.form {
    width: 300px;
    margin-bottom: 10px;
}
.form-check label {
    font-weight: normal;
    margin-left: 10px;
}
.wysiwyg {
    height: 100%;
    width: 100%;
    box-sizing: border-box;
}
.wysiwyg .modal-dialog {
    width: 300px;
}
.wysiwyg .title{
    margin-top: 0;
    margin-bottom: 20px;
}
.btns {
  display: flex;
  justify-content: flex-end;
  margin-top: 0;
}
</style>