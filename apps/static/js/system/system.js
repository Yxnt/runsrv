/**
 * Created by yandou on 2017/4/14.
 */
$(function () {
    $("#update_host").click(function () {
        $.ajax({
            url: '/api/salt/minions/',
            type: 'post',
            success: function () {
                alert("1")
            }
        })
    });
    $("#update_git").click(function () {
        $.ajax({
            url: '/api/publish/gitinfo/',
            type: 'post',
            data: {updategit: 1},
            success: function (data) {
                alert(data)
            }
        })
    })
});