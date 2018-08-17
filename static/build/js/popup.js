class PopUp {

    static commentSelector() { return ".popup-comment-content"; }

    static showView(envelop) {
        let isOpen = envelop.getAttribute("is-open");
        let cell = null;
        console.log(isOpen);
        if (isOpen === true ) {
            envelop.setAttribute("is-open", false);
        } else {
            console.log(envelop);

            let item = envelop.parentNode.querySelector(".general-value");
            let reference = document.getElementById(item.id);
            let popper = document.querySelector('.popper');
            popper.style.display = "block";
            let popup = new Popper(reference, popper, {
            placement: 'top',
              arrow: {
                classNames: [ 'arrow' ]
              },
              modifiers: {
                flip: {
                    behavior: ['left', 'bottom', 'top']
                },
              },
              onCreate: function(item) {
                let commentText = item.instance.reference.getAttribute("comment");
                console.log(item.instance.reference);
                cell = item.instance.reference;
                let popup = item.instance.popper;
                let textarea = popup.querySelector(".content");

                textarea.setAttribute("placeholder", "Введите замечание...");
                textarea.value = commentText;
              },

            });

            let closeButton = popper.querySelector(".close");
            closeButton.onclick = function() {
                console.log("close cell-comment popup ");
                popper.style.display = "none";
                if (cell !== null) {
                    Cell.saveComment(cell);
                }
                else {
                    console.log("cell is null");
                }

            };


            envelop.setAttribute("is-open", true);
        }

    }

    static showValidate(input) {
        let comment = $(input).siblings(PopUp.commentSelector())[0];
        let comment_input = $(comment).children()[1];

        $(comment).addClass("show");
        $(comment_input).focus();
    }

    static hideAll() {
        $(".general-value").css("background", "white");
        $(PopUp.commentSelector()).removeClass("show");
    }

    static hideOnMouseUp(event) {
        let selector = PopUp.commentSelector() + ".show";
        let active_comment = $(selector)[0];
        if (active_comment) {
            let active_input = $(active_comment).siblings(".general_value")[0];
            let hideFlag = !(
                event.target === active_input ||
                event.target === active_comment ||
                $.contains( active_comment, event.target));
            if (hideFlag) {
                PopUp.hideAll();
            }
        }
    }

}

