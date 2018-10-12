export default function () {
    $.extend($.summernote.plugins, {

        'mergeCells': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.mergeCells', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Merge<b>',
                        tooltip:  'Merge cells',
                        click:function (e) {
                            self.mergeCells();
                        }
                    }),
                ]).render();
            });

            this.mergeCells = function () {
                if (redips) redips.merge()
            };
        }
    });
};
