/**
 * Created by yandou on 2017/4/6.
 */

function ajax(username, password, remeber) {
    $.ajax({
        url: '/api/user/login',
        type: 'post',
        dataType: 'json',
        accepts: 'application/json',
        data: {username: username, password: password, remeber: remeber},
        success: function (data) {
            url = data['data']['next'];
            $(location).attr("href", url);
        }
    })
}