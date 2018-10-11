export default function () {
    $.extend($.summernote.plugins, {

        'addColumn': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.addColumnPlugin', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Col +<b>',
                        tooltip:  'Add column',
                        click:function (e) {
                            self.addColumn();
                        }
                    }),
                ]).render();
            });

            this.addColumn = function () {
                if (redips) redips.column('insert')
            };
        }
    });
};
