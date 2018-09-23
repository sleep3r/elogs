
document.addEventListener("DOMContentLoaded", function(event) {
   Toggle.bind(".header .user-name", ".user-menu", "visible");
});


class Toggle {

    static bind(selector, toggleSelector, className) {
        let el = document.querySelector(selector);
        if (el) {
            el.onclick = function() {
                let element = document.querySelector(toggleSelector);
                element.classList.toggle(className);
            }
        }
    }

    static class(toggleSelector, className) {
        let element = document.querySelector(toggleSelector);
        element.classList.toggle(className);
    }
}

window.Toggle = Toggle;
export {Toggle}
