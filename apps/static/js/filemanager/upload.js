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
    file();
});


function select() {
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

function file() {

    var $upload = $("#upload");

    var footerTemplate =
        '<div class="file-thumbnail-footer" style ="height:94px">\n' +
        '   <div style="margin:5px 0">\n' +
        '       {caption}\n' +
        '       <input id="path" class="kv-input kv-init form-control input-sm text-center " placeholder="目标路径">\n' +
        '   </div>\n' +
        '   {size}\n {progress}\n {actions}\n' +
        '</div>';

    $upload.fileinput({
        'previewFileType': 'any',
        'uploadUrl': '/api/salt/file/',
        'maxFilePreviewSize': 1024,
        'enctype': 'multipart/form-data',
        'showUploadedThumbs': true,
        'uploadExtraData': function () {
            var ajaxdata = {};
            var $group = $("#group");
            var $host = $('#host');
            var $path = $("#path");
            ajaxdata['groups'] = $group.val();
            ajaxdata['minions'] = $host.val();
            ajaxdata['opt'] = $path.val();
            return ajaxdata;
        },
        layoutTemplates: {footer: footerTemplate}
    });
    
}