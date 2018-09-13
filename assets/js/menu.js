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

  let menu = new Menu(".menu--left");

});


class Menu {

   constructor(menuSelector) {
     let menuNode = document.querySelector(menuSelector);
     this.menuNode = menuNode;
     this.menuSelector = menuSelector;

     this.closeAllItems();
     this.setActiveItem();
   }

   setActiveItem() {
      function firstMatchedParent(node, selector) {
       if (node.classList.contains(selector)) { return node; }
       return firstMatchedParent(node.parentNode, selector);
      }

      let link =  this.menuNode.querySelector(".menu__item a[data-url='"+ location.pathname +"']");
      if (link === null ) return;

      let currentItem = link.parentNode;
      currentItem.classList.add("open");

      // set .open parentNode also
      let parentItem = firstMatchedParent(currentItem.parentNode, "menu__item");
      parentItem.classList.add("open");
   }

   closeAllItems() {
     let allItems = document.querySelectorAll(".menu--left .menu__item");
     for (let key in allItems) {
       let menuItem = allItems[key];
       if (typeof(menuItem) === 'object') {
         menuItem.classList.remove("open");
       }
     }
   }

}