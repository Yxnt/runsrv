/**
 * Created by yandou on 2017/4/13.
 */

$(function () {
    // $.ajax({
    //     url: '/api/salt/minions',
    //     type: 'get',
    //     accepts: 'application/json',
    //     data: {name: 'celery:task:system', key: 'update_host_list'},
    //     success: function (data) {
    //         clients = data['clients'];
    //         for (var i=0;i<clients.length;i++){
    //             hostname=clients[i]['hostname'];
    //             ip=clients[i]['ip'];
    //             location = clients[i]['location'];
    //             group=clients[i]['group'];
    //             osinfo=clients[i]['osinfo'];
    //             status=clients[i]['status'];
    //         }
    //     }
    // });
    $('#hostTable').DataTable({
        "paging": false,
        "searching": false,
        ajax: {
            url: '/api/salt/minions',
            data: {name: 'celery:task:system', key: 'update_host_list'},
            dataSrc: 'clients'
        },
        columns: [
            {data: 'hostname'},
            {data: 'ip'},
            {data: 'group'},
            {data: 'location'},
            {data: 'status'}
        ],
        columnDefs: [
            {
                "targets": [2],
                "data": "所属组",
                "render": function (data, type, full) {
                    if (data === ""){
                        return "暂无信息"
                    }
                }
            },
                        {
                "targets": [3],
                "data": "地区",
                "render": function (data, type, full) {
                    if (data === ""){
                        return "暂无信息"
                    }
                }
            },
            {
                "targets": [4],
                "data": "主机状态",
                "render": function (data, type, full) {
                    if (data === "UP") {
                        return "<span class=\"label label-success\">" + data + "</span>"
                    } else {
                        return "<span class=\"label label-danger\">" + data + "</span>"
                    }
                }
            },
            {
                "targets": [5],
                "data": "操作",
                "render": function (data, type, full) {
                    return '<button class="btn btn-info btn-sm" id="more">详细信息</button><button class="btn btn-primary btn-sm">监控信息</button><button class="btn btn-danger btn-sm">删除</button>'
                }
            }
        ]
    });
    $("#more").on("click", function () {
        layer.open({
            type: 1,
            area: ['600px', '360px'],
            shadeClose: true, //点击遮罩关闭
            title: "主机详细信息",
            content: '<a href="abc">fwaef</a>'
        });
    })


});

