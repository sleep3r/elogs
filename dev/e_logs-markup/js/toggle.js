class Toggle {

    static byClick(toggleSelector, className, node) {
        let scope = node.parentNode;
        let element = scope.querySelector(toggleSelector);
        element.classList.toggle(className);
    }

}