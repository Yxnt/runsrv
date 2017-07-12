$(function () {
    repotable();
});


function repotable() {
    columns = [{
        field: "reponame",
        title: "项目名"
    }, {
        field: "repoid",
        title: "项目ID"
    }, {
        field: "repodesc",
        title: "项目描述"
    }, {
        field: "repoaddr",
        title: "项目地址"
    }, {
        field: "repopubpath",
        title: "项目发布路径",
        editable: {
            type: "text",
            mode: "line"
        }
    }];
    var $t = table("#repotable", '/api/publish/gitinfo', columns, 'editable-save.bs.table', function (e, field, row, old, $el) {
        var wait = layer.load(1, {time: 5 * 1000});
        id = row['repoid'];
        path = row['repopubpath'];
        data = {
            repoid: id,
            repopubpath: path
        };

        ajax('/api/publish/gitinfo/', 'post', data, function () {
            layer.close(wait);
        }, function () {
            layer.msg('更新失败页面数据为浏览器缓存');
        })
    });
    return $t.Init();
}



