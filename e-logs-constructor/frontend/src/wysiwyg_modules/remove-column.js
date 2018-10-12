export default function () {
    $.extend($.summernote.plugins, {

        'removeColumn': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.removeColumnPlugin', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Col -<b>',
                        tooltip:  'Remove column',
                        click:function (e) {
                            self.removeColumn();
                        }
                    }),
                ]).render();
            });

            this.removeColumn = function () {
                if (redips) redips.column('delete')
            };
        }
    });
};
