import $ from 'jquery'
// import PNotify from 'pnotify';

let Notifications = {
    markAsRead_: function(ids) {
        jQuery.ajax({
            url: '/api/common/messages/read/',
            data: { ids: ids },
            method: 'POST',
            //contentType: 'application/json',
            beforeSend: function(xhr, settings) {
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     // Only send the token to relative URLs i.e. locally.
                     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }
             }
        })
    },
    readAll: function(event, button) {
        let ids = [];
        let notifications = jQuery(button).closest('li').parent().find('li.notification');
        notifications.each(function() {
            ids.push($(this).data('id'));
        });
        this.markAsRead_(ids);
        notifications.slideUp(function() {
            $(this).remove();
        });
        jQuery(button).parent().slideUp();
    },
    open: function(event, link) {
        event.stopPropagation();
        let element = jQuery(link).closest('li');
        this.markAsRead_([element.data('id')]);
        let msg = element.data('message');
        element.slideUp(function() {
            let parent = $(this).parent();
            $(this).remove();
            if (parent.find('li.notification').length === 0) {
                parent.find('li.notification-header').slideUp(function() {
                    $(this).remove();
                })
            }
        });
        (new PNotify({
          target: document.body,
            title: 'Внимание',
            text: msg,
          buttons: {
            closer: true,
            closer_hover: false,
            sticker: false,
          },
          styling: 'brighttheme',
          type: 'error',
          hide: false,
          addclass: 'notification-full'
        })).open();
        return false;
    }
};

function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         let cookies = document.cookie.split(';');
         for (let i = 0; i < cookies.length; i++) {
             let cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }


Date.prototype.decrementMonth = function () {
    return new Date(this.setMonth(this.getMonth() - 1));
};

Date.prototype.incrementMonth = function () {
    return new Date(this.setMonth(this.getMonth() + 2));
};

Date.prototype.getMonthWithYear = function() {
    return this.getFullYear() + '-' + this.getMonth();
}


/**
 * @return {string}
 */
function GetURLParameter(paramName) {
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

$(document).ready(function () {
    let cell_id = GetURLParameter("highlight");
    if (cell_id.length > 0) {
        setTimeout(() => {
            $("table #" + cell_id + "").addClass("highlight");
        }, 1000);
    }
    
    // JournalPanel.init();
});

export {Notifications, getCookie, GetURLParameter}
