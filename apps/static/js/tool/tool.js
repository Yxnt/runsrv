function ajax(url, method, data, success_fun, error_fun) {
    var ajax = $.ajax({
        url: url,
        type: method,
        data: data,
        cache: false,
        dataType: 'json',
        accepts: 'application/json',
        success: success_fun,
        error: error_fun,
        traditional: true
    });
    return ajax
}

function table(tableid, apiurl, tablecolumns, event, func) {
    var $tableInit = new Object();
    var $table = $(tableid);
    $tableInit.Init = function () {
        $table.bootstrapTable("hideLoading");
        $table.bootstrapTable({
            classes: "table table-hover table-bordered table-condensed", // 表格样式
            url: apiurl,

            editable: true,
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

            columns: tablecolumns

        });
    };


    $table.on(event, func);

    return $tableInit;
}

