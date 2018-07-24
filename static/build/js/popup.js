class PopUp {


    static commentSelector() { return ".popup-comment-content"; }

    static showViewPopup(icon) {
        let input = $(icon).siblings(".general-value")[0];
        let comment = $(icon).siblings(PopUp.commentSelector())[0];

        $(input).css(
            "background",
            "radial-gradient(white 80%, #24A48A)"
        );
        $(comment).addClass("show");
    }


    static showValidatePopup(input) {
        let comment = $(input).siblings(PopUp.commentSelector())[0];
        let comment_input = $(comment).children()[1];

        $(input).css(
            "background",
            "radial-gradient(white 80%, #24A48A)"
        );
        $(comment).addClass("show");
        $(comment_input).focus();
    }

    static hidePopups() {
        $(".general-value").css(
            "background",
            "white"
        );
        $(".popup-comment-content").removeClass("show");
    }

    static hidePopusOnMouseUp(event) {

        let active_comment = $(PopUp.commentSelector() + ".show")[0];
        if (active_comment) {
            let active_input = $(active_comment).siblings(".general_value")[0];
            let hideFlag = !(
                event.target === active_input ||
                event.target === active_comment ||
                $.contains( active_comment, event.target));
            if (hideFlag) {
                PopUp.hidePopups();
            }
        }
    }

}

