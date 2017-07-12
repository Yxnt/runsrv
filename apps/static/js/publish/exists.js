$(function () {
    $("#group_check").click(function () {
        var $group = $("#group");
        if ($("#group_check")[0]["checked"] === true) {
            $group.prop("disabled", false);
            $group.selectpicker('refresh');
        } else {
            $group.empty();
            $group.prop("disabled", true);
            $group.selectpicker('refresh');

        }
    });
    $("#host_check").click(function () {
        if ($("#group_check")[0]["checked"] === true) {
            return alert("已选择组")
        }
        var $host = $("#host");
        if ($("#host_check")[0]["checked"] === true) {
            $host.prop("disabled", false);
            $host.selectpicker('refresh');
        } else {
            $host.empty();
            $host.prop("disabled", true);
            $host.selectpicker('refresh');
        }
    });

    select();
    submit();
});

function select() {
    var $project = $("#project");
    $project.selectpicker({
        liveSearch: true,
        title: "选择项目"
    });
    $project.on('show.bs.select', function () { // 下拉列表初始化
        $project.empty();
        var data = {all: 1};
        ajax('/api/publish/gitinfo/', 'get', data, function (data) {

            for (var i in data) {
                $project.append($("<option></option>").attr("value", data[i]).text(data[i]))
            }
            $project.selectpicker('refresh');
        });
    });


    var $group = $("#group");
    $group.on('show.bs.select', function () { // 下拉列表初始化
        $group.empty();
        var data = {all: 1};
        ajax('/api/assets/group/', 'get', data, function (data) {
            for (var i in data) {

                $group.append($("<option></option>").attr("value", data[i]).text(data[i]))
            }
            $group.selectpicker('refresh');
        });
    });


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

function submit() {
    var $project = $("#project");
    var $submit = $("#submit");
    var $method = $("#method");
    var $group = $("#group");
    var $host = $("#host");
    var $tag = $("#tag");
    var $tag_s = $("#tag_s");
    $method.on('show.bs.select', function (e) {
        $method.empty();
        $method.append($("<option></option>").attr("value", "tag").text("标签更新（线上更新）"));
        $method.append($("<option></option>").attr("value", "master").text("获取最新版本（预发布或者DotNetCore代码更新）"));
        $method.selectpicker('refresh');
        $tag.attr("hidden", true)
    });
    var module = undefined;
    $method.on('changed.bs.select', function (e) {
        if (e["currentTarget"]['value'] === "tag") {
            $tag.attr("hidden", false);
            module='fetch';

        } else {
            $tag.attr("hidden", true);
            module="pull";
        }
    });


    $tag_s.on('show.bs.select', function (e) {
        $tag_s.empty();
        data = {reponame: $project.val()};
        ajax('/api/publish/gittag/', 'get', data, function (data) {
            for (var i in data) {
                $tag_s.append($("<option></option>").attr("value", data[i]).text(data[i]))
            }
            $tag_s.selectpicker('refresh');
        });

    });


    $submit.click(function () {
        if ($project.val() === '') {
            return layer.msg("未选中项目")
        }

        if ($group.val() === '' && $host.val() === '') {
            return layer.msg("未选择组或主机")
        }

        console.log($tag_s.val());
        data = {
            groups: $group.val(),
            reponame: $project.val(),
            minions: $host.val(),
            tag:$tag_s.val(),
            module:module
        };
        var load = layer.load(10000000, {
            shade: [0.1, '#fff'] //0.1透明度的白色背景
        });
        ajax('/api/publish/update/', 'post', data, function (data) {
            jid = data['return'][0]['jid'];
            taskjob(jid, load);
        })
    })
}

function taskjob(jid, loading) {
    var $result = $("#status");
    html = "";
    var refresh = setInterval(function () {
        data = {jid: jid};

        ajax('/api/salt/jid/', 'get', data, function (data) {
            updatepath = data['info'][0]['Arguments'][0];
            operator = data['info'][0]['Function'];
            minions = data['info'][0]['Minions'];
            ret = data['return'];
            for (var i in minions) {
                if (ret[0][minions[i]] !== true) {
                    html += "<p><span class='text-success'>" + minions[i] + "</span>" + "：" + "执行成功" + "</p>";
                    html += "<p>更新结果：" + JSON.stringify(ret[0][minions[i]]) + "</p>";
                }
            }
            layer.close(loading);
            $result.html(html);
            return clearInterval(refresh);
        });
    }, 5000)
}