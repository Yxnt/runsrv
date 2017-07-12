$(function () {
    select();
    tree();
});

function select() {

    var $host = $('#host');
    $host.selectpicker({ // bootstrap-selected 方法
        actionsBox: true // 增加select all 或 delete all 功能
    });
    $host.on('show.bs.select', function () { // 下拉列表初始化
        $host.empty();
        var data = {name: 'celery:task:system', key: 'update_host_list'};
        ajax('/api/salt/minions/', 'get', data, function (data) {
            var clients = data['rows'];
            for (var i in clients) {
                client = clients[i]['hostname'];
                $host.append($("<option></option>").attr("value", client).text(client))
            }
            $host.selectpicker('refresh');
        });
    });
}

function tree() {

    var $get = $("#getdir");
    var $host = $("#host");

    $get.click(function () {

        var setting = {
            async: {
                enable: true,//采用异步加载
                url: "/api/salt/file/download",
                type: "post",
                dataType: "json",
                otherParam: {minion: $host.val()},
                autoParam: ["id","name"]
            },
            view: {
                showLine: true
            },
            data: {
                simpleData: {
                    enable: true
                }
            },
            callback: {
                beforeAsync:BeforeAsync,
                onClick:DownLoadClick
            }
        };

        $.fn.zTree.init($('#tree'), setting)
    });
}

function BeforeAsync(treeId, treeNode) {
    var path = "";
    if (treeNode && treeNode.getParentNode() !== null){
        path += treeNode.getParentNode()['name'];
        path += "/";
        path += treeNode['name'];
        treeNode['name'] = path;
        return treeNode;
    }

}

function DownLoadClick(event, treeId, treeNode) {
    var path = "";
    var minion = $("#host");
    if (treeNode['isParent'] !== true){
        path += treeNode.getParentNode()['name'];
        path += '/';
        path += treeNode['name'];

        url = "/api/salt/file/download?name=" + path + "&minion=" + minion.val();
        window.open(url);
    }
}