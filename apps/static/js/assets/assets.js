/**
 * Created by yandou on 2017/4/13.
 */


var interval;

$(function () {
    var path = window.location.pathname;
    if (path === '/dashboard/host') {
        var host = new hostTable();
        host.Init();

    } else if (path === '/dashboard/group') {

        var group = new groupTable();
        group.Init();

        var tool = new toolbar();
        tool.Init();

    }
});

var hostTable = function () {
    var tableInit = new Object();
    var table = $("#hostTable");
    tableInit.Init = function () {

        var operatorevenv = {
            'click #Monitor': function (e, value, row, index) {
                hostname = row["hostname"];
                content = "";
                content += "<div class='col-md-6'>";
                content += '<canvas id="CPU" height="200"></canvas><canvas id="Memory" height="200"></canvas>';
                content += "</div>";
                content += "<div class='col-md-6'>";
                content += '<canvas id="Network" height="200"></canvas><canvas id="Disk" height="200"></canvas>';
                content += "</div>";
                layer.open({
                    title: false,
                    area: ['800px', '560px'],
                    shadeClose: true,
                    content: content,
                    success: function (layero, index) {

                        monitor();

                    },
                    end: function (layero, index) {
                        stopinterval()
                    }
                })
            },
            'click #More': function (e, value, row, index) {
                hostname = row["hostname"]
            }
        };
        table.bootstrapTable("hideLoading"); // 不显示加载内容
        table.bootstrapTable({
            classes: "table table-hover table-bordered table-condensed", // 表格样式
            url: "/api/salt/minions/",
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
                field: "location",
                title: "位置"
            }, {
                field: "osinfo",
                title: "操作系统"
            }, {
                field: "status",
                title: "状态",
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


function gettime(counter) {
    var date = new Date();
    var timestamp = Date.parse(date);
    var cur_time = parseInt(timestamp.toString().substring(0, 10));
    if (counter) {
        seconds = counter * 60;
        return cur_time - seconds
    }
    return cur_time;
}

function timestamptohour(time, islist) {
    ret = [];
    if (islist === 1) {
        for (var i in time) {
            var date = new Date(time[i] * 1000);
            seconds = ("0" + date.getSeconds()).slice(-2);
            ret.push(date.getHours() + ":" + date.getMinutes() + ":" + seconds)
        }
        return ret
    } else {
        var date = new Date(time * 1000);
        seconds = ("0" + date.getSeconds()).slice(-2);
        return date.getHours() + ":" + date.getMinutes() + ":" + seconds;
    }


}

function monitor() {
    var query_addr = "/api/falcon/query/graph/";
    var history_operator = query_addr + "history";

    var start_time = gettime(4);
    var end_time = gettime();
    var query_data = {
        start: start_time,
        end: end_time,
        cf: "AVERAGE",
        endpoint_counters: JSON.stringify([
            {
                endpoint: hostname,
                counter: "cpu.idle"
            },
            {
                endpoint: hostname,
                counter: "mem.memfree.percent"
            }
        ])

    };

    var cpu_info = $("#CPU");
    var cpu = new Chart(cpu_info, {
        type: 'line'
    });


    var mem_info = $('#Memory');
    var mem = new Chart(mem_info, {
        type: 'line'
    });

    var net_info = $("#Network");
    var net = new Chart(net_info, {
        type: 'line'
    });

    var disk_info = $("#Disk");
    var disk = new Chart(disk_info, {
        type: 'line',
    });


    ajax(history_operator, 'post', query_data, function (data) {
        cpu_data = [];
        cpu_labels = [];
        var cpu_label;

        mem_data = [];
        mem_labels = [];
        var mem_label;
        for (var i in data) {
            if (data[i]["counter"].match("cpu")) {
                cpu_label = data[i]["counter"];
                for (var l in data[i]["Values"]) {
                    cpu_labels.push(data[i]["Values"][l]["timestamp"]);
                    cpu_data.push(data[i]["Values"][l]["value"]);
                }
            } else if (data[i]["counter"].match("mem")) {
                mem_label = data[i]["counter"];
                for (var l in data[i]["Values"]) {
                    mem_labels.push(data[i]["Values"][l]["timestamp"]);
                    mem_data.push(data[i]["Values"][l]["value"]);
                }
            }
        }

        cpu.data.datasets = [{
            type: 'line',
            label: cpu_label,
            data: cpu_data,
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10
        }];
        cpu.data.labels = timestamptohour(cpu_labels, islist = 1);



        mem.data.labels = timestamptohour(mem_labels, islist = 1);
        mem.data.datasets = [{
            type: "line",
            label: mem_label,
            data: mem_data,
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10
        }];

        cpu.update();
        mem.update();
    });

    interval = setInterval(function () {
        var refresh = {
            data: JSON.stringify([{
                endpoint: hostname,
                counter: "cpu.idle"
            },
                {
                    endpoint: hostname,
                    counter: "mem.memfree.percent"
                }])
        };
        var last_operator = query_addr + "last";
        ajax(last_operator, 'post', refresh, function (data) {
            cpu.data.labels.shift();
            cpu.data.datasets[0].data.shift();
            for (var i in data) {
                if (data[i]["counter"].match("cpu")) {
                    time = timestamptohour(data[i]["value"]["timestamp"]);
                    value = data[i]["value"]['value'];
                    cpu.data.labels.push(time);
                    cpu.data.datasets[0].data.push(value);
                }
            }
            cpu.update();
        })
    }, 60000);
}

function stopinterval() {
    clearInterval(interval);
}