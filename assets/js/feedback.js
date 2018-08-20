import $ from 'jquery'

class FeedBack {

    static send() {
        console.log("SendMessageToDevelopers");
        let $theme = $("#devs-message-theme");
        let $text = $("#devs-message-text");

        let theme = $theme.val();
        let text = $text.val();
        let plant = document.URL.split("?")[0].split("/")[3];
        let journal = document.URL.split("?")[0].split("/")[4];
        let data = {
            "theme": theme, "text": text,
            "user": backend.user.username, "email": backend.user.email,
            "plant": plant, "journal": journal,
        };
        if (text && theme && text.length < 1000 && theme.length < 200) {
            $("#MessageToDevelopersModal").modal("hide");
            $.ajax({
                type: 'POST',
                url: "/feedback/send-message",
                data: data,
                success: console.log,
                dataType: "json"
            });
            $("#message-modal-alert").css("display", "none");
            $theme.val("");
            $text.val("");

        }
        else {
            $("#message-modal-alert").css("display", "block");
        }
    }
}

$(document).ready(() => {
   window.FeedBack = FeedBack;
});

export {FeedBack}
