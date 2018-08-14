
function onEdit(item){
  let reference = document.getElementById(item.id);
  let popper = document.querySelector('.popper');
  popper.style.display = "block";
  let anotherPopper = new Popper(reference, popper, {
      placement: 'top',
      arrow: {
        classNames: [ 'MY-popper-arrow' ]
      },
      modifiers: {
        flip: {
            behavior: ['left', 'bottom', 'top']
        },
      },
      onCreate: function(item) {
        console.info("create popup");
        let content = item.instance.reference.value;
        let popup = item.instance.popper;
        let textarea = popup.querySelector(".content");
        console.info(textarea)
        textarea.value = "Ваш комментарий " + content;
      },
      onUpdate: function() {
        console.info("update popup");
      }

  });

}

document.addEventListener("DOMContentLoaded", function() {


});
