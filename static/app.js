function showTabs() {
  $('.input-tabs-section').show();
  $('.tabs').show();
  $('.logout').hide();
}

function showLogout() {
  $('.input-tabs-section').hide();
  $('.tabs').hide();
  $('.logout').show();
}

function onLogoutEvent() {
  $.removeCookie('mytoken');
  $('#login-id').val('');
  $('#login-pw').val('');
  showTabs();
}

function checkTokenExpiration() {
  const token = $.cookie('mytoken');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    $('.greeting').text('Welcome! ' + payload['nickname']);
    const expirationTime = payload.exp * 1000;
    if (Date.now() >= expirationTime) {
      onLogoutEvent();
      alert('Login Session Has Expired!');
    } else {
      setTimeout(checkTokenExpiration, expirationTime - Date.now());
    }
  } else {
    showTabs();
  }
}

function login() {
  $.ajax({
    type: "POST",
    url: "/api/login",
    data: { id_give: $('#login-id').val(), pw_give: $('#login-pw').val() },
    success: function (response) {
      if (response['result'] == 'success') {
        const token = response['token'];
        $.cookie('mytoken', token);

        $.ajaxSetup({
          headers: { 'Authorization': 'Bearer ' + token }
        });

        showLogout();
        $('.greeting').text('Welcome! ' + response['nickname']);
        checkTokenExpiration();
      } else {
        alert(response['msg'])
      }
    }
  })
}
function register() {
  $.ajax({
    type: "POST",
    url: "/api/register",
    data: {
      id_give: $('#reg-id').val(),
      pw_give: $('#reg-pw').val(),
      nickname_give: $('#reg-nick').val()
    },
    success: function (response) {
      if (response['result'] == 'success') {
        alert('You have been registered!')
      } else {
        alert(response['msg'])
      }
    }
  })
}

$(document).ready(function () {
  const token = $.cookie('mytoken');
  checkTokenExpiration();
  if (token) {
    showLogout();
  } else {
    showTabs();
  }

  $('.tab').eq(0).click(function () {
    $('#login-section').show();
    $('#register-section').hide();
    $('.tab').eq(0).addClass('active-tab');
    $('.tab').eq(1).removeClass('active-tab');
  });

  $('.tab').eq(1).click(function () {
    $('#register-section').show();
    $('#login-section').hide();
    $('.tab').eq(1).addClass('active-tab');
    $('.tab').eq(0).removeClass('active-tab');
  });
});


