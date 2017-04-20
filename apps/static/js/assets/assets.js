/**
 * Created by yandou on 2017/4/13.
 */

$(function () {
    var path = window.location.pathname;
    if (path === '/dashboard/host') {
        var host = new hostTable();
        host.Init();
    } else if (path === '/dashboard/group') {

        var group = new groupTable();
        group.Init();
        // group.ajax();

        var tool = new toolbar();
        tool.Init();

    }
});

var hostTable = function () {
    var tableInit = new Object();
    tableInit.Init = function () {
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
                {data: "osinfo"},
                {data: 'status'}
            ],
            columnDefs: [
                {
                    "targets": [2],
                    "data": "所属组",
                    "render": function (data, type, full) {
                        if (data === "") {
                            return "暂无信息"
                        }
                    }
                },
                {
                    "targets": [3],
                    "data": "地区",
                    "render": function (data, type, full) {
                        if (data === "") {
                            return "暂无信息"
                        } else {
                            return data
                        }
                    }
                },
                {
                    "targets": [5],
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
                    "targets": [6],
                    "data": "操作",
                    "render": function (data, type, full) {
                        return '<button class="btn btn-info btn-sm" id="more">详细信息</button><button class="btn btn-primary btn-sm">监控信息</button><button class="btn btn-danger btn-sm">删除</button>'
                    }
                }
            ]
        });
    };
    return tableInit;
};

var groupTable = function () {
    var tableInit = new Object();
    var table = $("#groupTable");

    tableInit.Init = function () {
        table.bootstrapTable("hideLoading"); // 不显示加载内容
        table.bootstrapTable({
            classes: "table table-hover table-bordered table-condensed", // 表格样式
            url: "/api/assets/group/",
            contentType: "",
            cache: false,
            pagination: true, // 分页
            paginationLoop: "true",
            smartDisplay: "false",
            sidePagination: "server", // 服务端分页
            pageSize:10,
            pageList: [5, 10, 15, 50, 100, 200], //分页条数

            search: true, // 搜索
            searchOnEnterKey: true, //回车触发搜索
            searchAlign: "right", //搜索框位置，right or left

            iconsPrefix: "fa", // icon 来源 glyphicon or fa(FontAwesome)
            icons: { // icon 图标设置
                refresh: "fa fa-refresh"
            },

            responseHandler: function (res) {
                return {
                    "rows": res.rows,
                    "total": res.total
                }
            },


            showRefresh: true, // 显示刷新按钮
            toolbarAlign: "left", // 工具栏位置 right or left
            toolbar: "#toolbar", // 自定义工具栏
            clickToSelect: true, // 当点击时多选或单选
            selectItemName: "select", // 多选框名称

            columns: [{ // thead
                checkbox: true
                // field: "check"
            }, {
                field: "groupname",
                title: "组名"
            }, {
                field: "groupdesc",
                title: "组描述"
            }, {
                field: "clientnumber",
                title: "客户端数量"
            }, {
                field: "operator",
                title: "操作",
                formatter: function (value, row, index) {
                    html = "";
                    html += "<button class='btn btn-info btn-sm'>详细信息</button>";
                    return html
                }

            }]

        });
    };

    return tableInit;
};


var toolbar = function () {
    var tool = new Object();
    tool.Init = function () {
        var new_button = $("#new");
        new_button.click(function () {

            // 弹出页面内容
            html = '<div>' +
                '<div class="form-horizontal">' +
                '<div class="form-group">' +
                '<label for="groupname" class="col-sm-2 control-label">组名</label>' +
                '<div class="col-sm-10">' +
                '<input id="groupname" type="text" class="form-control">' +
                '</div></div>' +
                '<div class="form-group">' +
                '<label for="groupdesc" class="col-sm-2 control-label">组描述</label>' +
                '<div class="col-sm-10">' +
                '<input id="groupdesc" type="text" class="form-control">' +
                '</div></div>' +
                '<div class="form-group">' +
                '<label for="clients" class="col-sm-2 control-label">客户端</label>' +
                '<div class="col-sm-10">' +
                '<select id="clients" class="selectpicker" multiple>' +
                '</select>' +
                '</div></div>' +
                '</div></div>';

            layer.open({
                type: 1,
                skin: 'layui-layer-rim', //加上边框
                area: ['500px', '400px'], //宽高
                title: "添加组", // 标题
                content: html, // 弹出窗口内容
                shadeClose: true, // 点击其他位置关闭
                btn: ['提交'], // 提交按钮
                btn1: function (index, layero) { // 点击提交按钮执行方法
                    var select = $('.selectpicker');
                    var groupname = $("input#groupname").val();
                    var groupdesc = $("input#groupdesc").val();
                    var clients = select.val();

                    if (clients !== null) {
                        if (groupname !== "") {
                            var data = {name: groupname, description: groupdesc, client: clients};

                            ajax('/api/assets/group/', 'post', data, function (data) {
                                layer.close(index)
                            })
                        }
                    }

                },
                resize: true, // 可调整弹出窗大小
                success: function (layero, index) { // 弹出页面成功弹出后的动作
                    var select = $('.selectpicker');
                    select.selectpicker({ // bootstrap-selected 方法
                        actionsBox: true // 增加select all 或 delete all 功能
                    });
                    select.on('show.bs.select', function () { // 下拉列表初始化
                        select.empty();
                        var data = {name: 'celery:task:system', key: 'update_host_list'};
                        ajax('/api/salt/minions/', 'get', data, function (data) {
                            var clients = data['clients'];
                            for (var i in clients) {
                                client = clients[i]['hostname'];
                                select.append($("<option></option>").attr("value", client).text(client))
                            }
                            select.selectpicker('refresh');
                        });
                    });
                },
                end: function () {
                    $("button[name=refresh]").click();
                }
            });
        });
    };
    return tool;
};


function ajax(url, type, data, success_fun, error_fun) {
    var ajax = $.ajax({
        url: url,
        type: type,
        data: data,
        dataType: 'json',
        accepts: 'application/json',
        success: success_fun,
        error: error_fun,
        traditional: true
    });
    return ajax

}