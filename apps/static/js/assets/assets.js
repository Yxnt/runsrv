/**
 * Created by yandou on 2017/4/13.
 */

$(function () {
    $("#more").on("click", function () {
        layer.open({
            type: 1,
            area: ['600px', '360px'],
            shadeClose: true, //点击遮罩关闭
            title:"主机详细信息",
            content: '<a href="abc">fwaef</a>'
        });
    })
});
