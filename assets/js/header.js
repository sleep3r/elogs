$(document).ready( function(event) {
  let header = $(".header");
  let lastScrollTop = 0;
  $(window).scroll(function(event){
     let st = $(this).scrollTop();
     if(st < 100){
         header.removeClass("hidden").addClass("sticky")
     }
     if((lastScrollTop - st > 2) && (st > 100)) {
         header.removeClass("hidden").addClass("sticky");
     } else if((st - lastScrollTop > 10) && (st > 100)) {
         header.removeClass("sticky").addClass("hidden");
     }
     lastScrollTop = st;
  });
});
