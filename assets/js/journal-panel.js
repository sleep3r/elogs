
class JournalPanel {
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
