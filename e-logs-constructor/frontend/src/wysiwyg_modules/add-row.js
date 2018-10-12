export default function () {
    $.extend($.summernote.plugins, {

        'addRow': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.addRowPlugin', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Row +<b>',
                        tooltip:  'Add row',
                        click:function (e) {
                            self.addRow();
                        }
                    }),
                ]).render();
            });

            this.addRow = function () {
                if (redips) redips.row('insert')
            };
        }
    });
};
