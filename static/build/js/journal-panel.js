
class JournalPanel {
   static changeMode(mode){
      switch (mode) {
          case 'view':
               location.href = location.pathname.concat("?page_mode=view&");
             break;
          case 'edit':
             location.href = location.pathname.concat("?page_mode=edit&");
             break;
          case 'validate':
             location.href = location.pathname.concat("?page_mode=validate&");
             break;
          default:
             console.log("change mode to Default mode!");
             break;
      }
   }
}
