/**
 * Created by yandou on 2017/4/14.
 */
$(function () {
    $.ajax({
        url: '/api/salt/minions',
        type: 'get',
        data: {name: 'celery:task:system', key: 'update_host_list'},
        accepts: 'application/json',
        success: function (data) {
            $("#client_number").text(data['client_number']);
            clients = data['clients'];
            var label = [];
            for (var i = 0; i < clients.length; i++) {
                label.push(clients[i]['osinfo']);
            }
            new_label = Array.from(new Set(label));

            var ctx = $("#canvas");
            var view_data = {
                labels: new_label,
                datasets: [
                    {
                        data: doughnut_data(label, new_label),
                        backgroundColor: [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ],
                        hoverBackgroundColor: [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ]
                    }]
            };
            var myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: view_data
            });
        }

    })
    ajax('/api/user/info/','get',function (data) {
        $("#user_len").text(data['data']['counter']);
    })

});


function doughnut_data(osinfo_list, set) {
    var result = {};
    var n = 0;

    for (var i = 0; i < set.length; i++) {
        result[set[i]] = n
    }

    for (var i = 0; i < osinfo_list.length; i++) {
        for (var l = 0; l < set.length; l++) {
            if (osinfo_list[i] == set[l]) {
                result[set[l]]++;
            }
        }
    }
    var data = [];
    for (var i in set) {
        data.push(result[set[i]]);
    }
    return data
}

function ajax(url,type,success_func,error_func){
    $.ajax({
        url:url,
        type:type,
        accepts:"application/json",
        success: success_func,
        error:error_func
    })
}