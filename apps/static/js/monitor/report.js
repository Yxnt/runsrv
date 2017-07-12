/**
 * Created by yandou on 2017/4/27.
 */


$(function () {
    var table = report();
    table.Init();
});

function report() {
    var tableInit = new Object();
    var table = $("table");
    tableInit.Init = function () {
        table.bootstrapTable("hideLoading"); // 不显示加载内容
        table.bootstrapTable({
            classes: "table table-hover table-bordered table-condensed", // 表格样式
            url: "/api/monitor/report",


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
            }, {
                field: "hostname",
                title: "主机"
            }, {
                field: "message",
                title: "异常信息"
            }, {
                field: "level",
                title: "错误等级"
            }, {
                field: "type",
                title: "类型"
            }, {
                field: "time",
                title: "发生时间"
            }, {
                field: "status",
                title: "状态",
                formatter: function (value, row, index) {
                    if (value === true) {
                        return "未处理，已发邮件"
                    } else{
                        return "已处理"
                    }
                }
            }, {
                field: "operator",
                title: "操作",
                formatter: function (value, row, index) {
                    html = "";
                    html += "<button class='btn btn-info btn-sm' id='commit'>状态修改</button>";
                    return html
                }

            }]

        });
    };
    return tableInit
}