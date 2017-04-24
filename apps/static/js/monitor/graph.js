/**
 * Created by yandou on 2017/4/24.
 */


$(function () {
    toolbar();
    graph();
});


function toolbar() {
    var client = $("#endpoint");
    client.selectpicker({
        actionsBox: true,
        title: "选择客户端"
    });

    var counter = $("#counter");
    counter.selectpicker({
        actionsBox: true,
        title: "选择监控项"
    });


    $('#choise_time').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        timePickerSeconds: true,
        format: 'MM/DD/YYYY h:mm A'
    });


}


function graph() {
    var $graph = $("#graph");
    var char = new Chart($graph, {
        type: 'line',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                // data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
            }]
        },
        options:{
            reverse:true
        }

    });
    char.update();

}