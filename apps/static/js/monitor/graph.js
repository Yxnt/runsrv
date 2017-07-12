/**
 * Created by yandou on 2017/4/24.
 */


$(function () {
    toolbar();
    window.onresize = function () {
        graph();
    };
    graph();


});


function toolbar() {
    var $client = $("#endpoint");
    $client.selectpicker({
        title: "选择客户端"
    });
    $client.on('show.bs.select', function () { // 下拉列表初始化
        $client.empty();
        var data = {name: 'celery:task:system', key: 'update_host_list'};
        ajax('/api/salt/minions/', 'get', data, function (data) {
            var clients = data['rows'];
            for (var i in clients) {
                client = clients[i]['hostname'];
                $client.append($("<option></option>").attr("value", client).text(client))
            }
            $client.selectpicker('refresh');
        });
    });

    var $counter = $("#counter");
    $counter.selectpicker({
        liveSearch: true,
        title: "选择监控项"
    });
    $counter.on("show.bs.select", function () {
        $counter.empty();
        endpoint = $client.val();
        data = {endpoint: endpoint};
        ajax('/api/falcon/endpoint_item/item/', 'get', data, function (data) {
            for (var i in data) {
                $counter.append($("<option></option>").attr("value", data[i]).text(data[i]))
            }
            $counter.selectpicker('refresh');
        });
    });

    var $time = $('#choise_time');
    var start_time, end_time;
    $time.daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        timePicker24Hour: true,
        timePickerSeconds: true,
        format: 'MM/DD/YYYY hh:mm:ss'
    });
    $time.on('apply.daterangepicker', function (ev, picker) {
        start_time = picker.startDate.format('YYYY-MM-DD H:mm:ss');
        end_time = picker.endDate.format('YYYY-MM-DD H:mm:ss');
    });


    var gr = graph();

    $("#submit").click(function () {

        if (start_time === undefined && end_time === undefined) {
            start_time = gettime(60);
            end_time = gettime();
        } else if (start_time === undefined) {
            start_time = gettime(60);
        } else if (end_time === undefined) {
            end_time = gettime();
        } else {
            start_time = gettime(0, start_time);
            end_time = gettime(0, end_time);
        }

        var counters = [];

        counters.push({
            endpoint: $client.val(),
            counter: $counter.val()
        });

        var query_data = {
            start: start_time,
            end: end_time,
            cf: "AVERAGE",
            endpoint_counters: JSON.stringify(counters)
        };

        var gr_data = [];
        var label = [];
        var labels = [];
        ajax('/api/falcon/query/graph/history', 'post', query_data, function (data) {


            for (var i in data) {
                label.push(data[i]["counter"]);
                for (var l in data[i]["Values"]) {
                    labels.push(data[i]["Values"][l]["timestamp"])
                    if (data[i]["Values"][l]['value'] !== null) {
                        gr_data.push(data[i]["Values"][l]['value']);
                    } else {
                        gr_data.push("NaN");
                    }
                }
            }

            gr.set(timestamptohour(labels, islist = 1), label, gr_data)
        });

        setInterval(function () {
            var now = gettime();
            var priv = gettime(1);
            query_data['start'] = priv;
            query_data['end'] = now;
            ajax('/api/falcon/query/graph/history', 'post', query_data, function (data) {

                for (var i in data) {

                    for (var l in data[i]["Values"]) {
                        labels.push(data[i]["Values"][l]["timestamp"])
                        if (data[i]["Values"][l]['value'] !== null) {
                            gr_data.push(data[i]["Values"][l]['value']);
                        } else {
                            gr_data.push("NaN");
                        }
                    }
                }
                gr_data.shift();
                labels.shift();
                gr.set(timestamptohour(labels, islist = 1), label, gr_data)
            });

        }, 30000)
    });


}


function graph() {
    var $graph = document.getElementById('graph');
    var mychart = echarts.init($graph);


    mychart.set = function (labels, label, data) {
        var option = {
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    xAxisIndex: [0],
                    filterMode: 'filter'
                }],
            tooltip: {
                trigger: 'none',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: label
            },
            xAxis: [
                {
                    type: 'category',
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLine: {
                        onZero: false
                    },

                    axisPointer: {
                        label: {
                            formatter: function (params) {
                                return label + params.value
                                    + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                            }
                        }
                    },
                    data: labels
                }
            ],
            yAxis: {},
            series: [{
                name: label,
                type: 'line',
                data: data
            }]

        };

        mychart.setOption(option);
    };
    return mychart;


}


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


function gettime(counter, time) {
    var date;
    if (time) {
        date = new Date(time);
    } else {
        date = new Date();
    }

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