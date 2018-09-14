import $ from "jquery";

class JournalPanel {

   static init() {
       let selector = ".mode-buttons .btn-" + Journal.getMode();
       let activeBtn = document.querySelector(selector);
       if (activeBtn !== null) {
           activeBtn.classList.toggle("btn--active");
       }
   }

   static changeMode(mode){
      let id = this.getUrlParam("id");

      function prepareUrl(mode) {
          let url = location.pathname.concat(mode);
              if (id !== null) {
                  url = url.concat("&id=" + id);
              }
          return url;
      }

      switch (mode) {
          case 'view':
              location.href = prepareUrl("?page_mode=view");
             break;
          case 'edit':
             location.href = prepareUrl("?page_mode=edit");
             break;
          case 'validate':
             location.href = prepareUrl("?page_mode=validate");
             break;
          default:
             console.log("change mode to Default mode!");
             break;
      }
   }

   static endShift(shift_id){
     $.confirm({
        title: 'Вы действительно хотите сдать смену?',
        content: 'После закрытия смены у вас будет 12 часов на редактирование занесенных во время прошедшей смены данных.',
        autoClose: 'cancel|60000',
        theme: 'supervan',
        buttons: {
            confirm: {
                text: "Да",
                action: function(id=shift_id) {
                    $.post("/common/end_shift/", {id:id} ,function() {location.reload()});
                }
            },
            cancel: {
                text: "Нет",
            },
        }
     });
   }

   static getUrlParam(paramName) {
       let url = window.location.search.substring(1);
       let urlParams = url.split('&');
       for (let i = 0; i < urlParams.length; i++) {
            let parameterName = urlParams[i].split('=');
            if (parameterName[0] === paramName) {
                return parameterName[1];
            }
       }

       return "";
   }
}

// $(document).ready(() => {
//     window.JournalPanel = JournalPanel;
// });

window.JournalPanel = JournalPanel;

export {JournalPanel}
