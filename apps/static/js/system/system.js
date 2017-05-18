/**
 * Created by yandou on 2017/4/14.
 */
$(function () {
   $("#update_host").click(function () {
       $.ajax({
           url:'/api/salt/minions/',
           type:'post',
           success: function () {
               alert("1")
           }
       })
   })
});