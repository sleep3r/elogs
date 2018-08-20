document.addEventListener("DOMContentLoaded", function(event) {
  const selectorMenuItemTopLevel = ".menu > li.menu__item";
  const selectorMenuItem = "li.menu__item";
  const selectorLink = "a.menu-item__link";
  let items = document.querySelectorAll(selectorMenuItemTopLevel);
  [].forEach.call(items, (item) => {
    item.addEventListener('click', function(event) {
      event.preventDefault();
      const listItem = event.target.closest(selectorMenuItem);
      const linkNode = listItem.querySelector(selectorLink);
      const url = linkNode.getAttribute("data-url");

      if (url !== null && url !== "" && url !== "#") {
         location.href = url;
      } else {
        listItem.classList.toggle("open");
      }

    }, false);
  });
});
