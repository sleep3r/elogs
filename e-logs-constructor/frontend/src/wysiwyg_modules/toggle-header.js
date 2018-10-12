export default function () {
    $.extend($.summernote.plugins, {

        'cellHeader': function (context) {
            var self = this,
                ui = $.summernote.ui,
                options = context.options,
                $editor   = context.layoutInfo.editor,
                $editable = context.layoutInfo.editable;

            context.memo('button.cellHeader', function () {
                return ui.buttonGroup([
                    ui.button({
                        contents: '<b>Header<b>',
                        tooltip:  'Toggle header',
                        click:function (e) {
                            self.toggleCellHeader();
                        }
                    }),
                ]).render();
            });

            this.toggleCellHeader = function () {
                const rng = context.invoke('createRange', $editable);
                const dom = $.summernote.dom;
                if (rng.isCollapsed() && rng.isOnCell()) {
                    context.invoke('beforeCommand');
                    var cell = dom.ancestor(rng.commonAncestor(), dom.isCell)
                    var $cell = $(cell)
                    if ($cell.is('td')) {
                        self.replaceTags($cell, 'th')
                    }
                    else if ($cell.is('th')) {
                        self.replaceTags($cell, 'td')
                    }
                    context.invoke('afterCommand');
                }
            };

            this.replaceTags = function($nodes, newTag) {
                $nodes.replaceWith(function() {
                    return $("<" + newTag + " />", {html: $(this).html(), colspan: $(this).attr('colspan'), rowspan: $(this).attr('rowspan')});
                });
            }

        }
    });
};
