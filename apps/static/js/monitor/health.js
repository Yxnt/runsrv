/**
 * Created by yandou on 2017/4/26.
 */

$(function () {
    var health = health_table();
    health.Init();
});


function health_table() {
    var table = new Object();
    var $health = $("#health");
    table.Init = function () {
        $health.bootstrapTable("hideLoading"); // 不显示加载内容
        $health.bootstrapTable({
            classes: "table table-hover table-bordered table-condensed", // 表格样式
            url: "",
            queryParams: function () {
                data = {
                    name: 'celery:task:system',
                    key: 'update_host_list',
                    limit: 10,
                    offset: 0,
                    order: 'asc'
                };
                return data
            },
            cache: false,
            pagination: true, // 分页
            paginationLoop: "true",
            smartDisplay: "false",
            sidePagination: "server", // 服务端分页
            pageSize: 10,
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
                field: "hostname",
                title: "主机名"
            }, {
                field: "ip",
                title: "IP"
            }, {
                field: "cpu",
                title: "cpu可用性"
            }, {
                field: "memory",
                title: "内存可用性"
            }, {
                field: "network",
                title: "网络连通性",
                formatter: function (value, rows, index) {
                    if (value === "UP") {
                        return "<span class=\"label label-success\">" + value + "</span>"
                    } else {
                        return "<span class=\"label label-danger\">" + value + "</span>"
                    }
                }
            }, {
                field: "operator",
                title: "操作",
                formatter: function (value, row, index) {
                    html = "";
                    html += '<button class="btn btn-sm btn-default" id="Monitor" data-toggle="control-sidebar">监控信息</button>';
                    html += '<button class="btn btn-sm btn-info" id="More">更多信息</button>';
                    return html
                },
                events: operatorevenv
            }]


        });
    };
    return table;
}