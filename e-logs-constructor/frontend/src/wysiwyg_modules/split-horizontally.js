export default function () {
    $.extend($.summernote.plugins, {

        'splitH': function (context) {
            let self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.splitH', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Split H<b>',
                        tooltip:  'Split horizontally',
                        click:function (e) {
                            self.splitH();
                        }
                    }),
                ]).render();
            });

            this.splitH = function () {
                if (redips) redips.split('h')
            };
        }
    });
};
