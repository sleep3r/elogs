document.addEventListener("DOMContentLoaded", function(event) {
  let element = document.querySelector(".header");
  window.addEventListener('scroll', function() {
      let scrollPos = window.pageYOffset;
      if (scrollPos > 0) {
            element.classList.add("sticky");
      } else {
            element.classList.remove("sticky");
      }
  });
});
