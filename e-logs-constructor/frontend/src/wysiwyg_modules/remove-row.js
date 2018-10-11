export default function () {
    $.extend($.summernote.plugins, {

        'removeRow': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.removeRowPlugin', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Row -<b>',
                        tooltip:  'Remove row',
                        click:function (e) {
                            self.removeRow();
                        }
                    }),
                ]).render();
            });

            this.removeRow = function () {
                if (redips) redips.row('delete')
            };
        }
    });
};
