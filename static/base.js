//----THE VIEWPROFILE JS----
const profileImageContainers = document.querySelectorAll(
  ".profile-image-container"
);
profileImageContainers.forEach((profileImageContainer) => {
  profileImageContainer.addEventListener("click", function () {
    const url = this.dataset.location;
    window.location.href = url;
  });
});


//-----CLOSE BUTTON JS-----
const closeButtons = document.querySelectorAll(".close-friends-now");
closeButtons.forEach(closeButton => {
  closeButton.addEventListener("click", () => {
    window.location.href = "/profile";
  });
});

// ------MESSAGEBOX------
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('message-input').focus();
  document.getElementById('form').addEventListener('submit', function (event) {
    document.getElementById('message-input').focus();
  });
});


//------NOTIFICATION------
function checkNotifications() {
  $.ajax({
    url: '/check_notification/',
    type: 'GET',
    success: function (response) {
      if (response.notifications.length === 0) {
        $('#notifications-container').hide();
      } else {
        $('#notifications-container').show();
        $('#notifications-container').empty();
        response.notifications.forEach(function (notification) {
          var notificationElement = '<div class="notification">' +
            '<img src="' + notification.sender_avatar_url + '" alt="Avatar">' +
            '<div class="notification-info">' +
            '<p>' + notification.sender + '</p>' +
            '<em>' + notification.message + '</em>' +
            '<span>' + notification.created_at + '</span>' +
            '</div>' +
            '<button class="close-button" data-notification-id="' + notification.id + '"><span>&times;</span></button>' +
            '</div>';
          $('#notifications-container').append(notificationElement);
        });
      }

      $('.close-button').click(function () {
        var notificationId = $(this).data('notification-id');
        $.ajax({
          url: '/update_notification_status/',
          type: 'POST',
          data: {
            notification_id: notificationId
          },
          beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          },
          success: function (response) {
            if (response.success) {
              alert('Notification removed successfully');
              location.reload();
            } else {
              alert('Error deleting notification :', response.error);
            }
          },
          error: function (xhr, status, error) {
            console.error('AJAX error:', error);
          }
        });
      });
    },
    error: function (xhr, status, error) {
      console.error('Error fetching notifications:', error);
    }
  });
}

checkNotifications();
setInterval(checkNotifications, 20000);


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

