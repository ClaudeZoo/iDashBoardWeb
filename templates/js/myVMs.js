$(document).ready(function(){
    $(function () { $(".tooltip-options").tooltip({html : true });});
    $("div.progress").hide();
    $("#myVMs-data-table").DataTable();
    $("tbody tr").each(function(){
        var start_button = $(this).find(".start-button");
        var shutdown_button = $(this).find(".shutdown-button");
        var hibernate_button = $(this).find(".hibernate-button");
        var delete_button = $(this).find(".delete-button");
        if ($(this).find(".state-td i").text() == " Online"){
            $(this).find(".state-td i").addClass("fa-check-circle");
            start_button.addClass("disabled");
            delete_button.addClass("disabled");
        }
        else if ($(this).find(".state-td i").text() == " Offline"){
            $(this).find(".state-td i").addClass("fa-times-circle");
            shutdown_button.addClass("disabled");
            hibernate_button.addClass("disabled");
        }
        else {
            $(this).find(".state-td i").addClass("fa-hdd-o");
            shutdown_button.addClass("disabled");
            hibernate_button.addClass("disabled");
        }
    });
    $(".start-button").bind("click", function(){
        var vm_name = $(this).parents("tr").children("td.vm-name").text();
        var vm_uuid = $(this).parents("tr").children("td.vm-uuid").text();
        $("#"+vm_uuid+"-progress-div").show();
        var vm_state = $(this).parents("tr").find(".state-td i");
        var start_button = $(this).parents("tr").find(".start-button");
        var shutdown_button = $(this).parents("tr").find(".shutdown-button");
        var hibernate_button = $(this).parents("tr").find(".hibernate-button");
        var delete_button = $(this).parents("tr").find(".delete-button");
        var update = updateProcess(vm_name, vm_uuid, vm_state, hibernate_button, shutdown_button);
        start_button.addClass("disabled");
        delete_button.addClass("disabled");
        vm_state.removeClass("fa-times-circle fa-hdd-o").text("Offline")
        var process_id = setInterval(update, 3000);//时间太短会有error，500时有一半error
        $('<div/>', { id: vm_uuid, class: "hiding"}).html(process_id).appendTo('body');
    });
    $(".shutdown-button").bind("click", function(){
        var vm_name = $(this).parents("tr").children("td.vm-name").text();
        var vm_uuid = $(this).parents("tr").children("td.vm-uuid").text();
        var vm_state = $(this).parents("tr").find(".state-td i")
        var start_button = $(this).parents("tr").find(".start-button");
        var shutdown_button = $(this).parents("tr").find(".shutdown-button");
        var hibernate_button = $(this).parents("tr").find(".hibernate-button");
        var delete_button = $(this).parents("tr").find(".delete-button");
        hibernate_button.addClass("disabled");
        shutdown_button.addClass("disabled");
        vm_state.removeClass("fa-check-circle").addClass("fa-spinner fa-pulse fa-2x").text("")
        $.post('/control_vm/', {'uuid': vm_uuid, 'vm-name': vm_name, 'request_type': 'shutdown'}, function(response){
            var response_json = eval('(' + response + ')');
            if (response_json.request_result === 'success'){
                start_button.removeClass("disabled");
                delete_button.removeClass("disabled");
                vm_state.removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-times-circle").text(" Offline");
            }
        }); 
    });
    $(".hibernate-button").bind("click", function(){
        var vm_name = $(this).parents("tr").children("td.vm-name").text();
        var vm_uuid = $(this).parents("tr").children("td.vm-uuid").text();
        var vm_state = $(this).parents("tr").find(".state-td i")
        var start_button = $(this).parents("tr").find(".start-button");
        var shutdown_button = $(this).parents("tr").find(".shutdown-button");
        var hibernate_button = $(this).parents("tr").find(".hibernate-button");
        var delete_button = $(this).parents("tr").find(".delete-button");
        hibernate_button.addClass("disabled");
        shutdown_button.addClass("disabled");
        vm_state.removeClass("fa-times-circle").addClass("fa-spinner fa-pulse fa-2x").text("")
        $.post('/control_vm/', {'uuid': vm_uuid, 'vm-name': vm_name, 'request_type': 'savestate'}, function(response){
            var response_json = eval('(' + response + ')');
            if (response_json.request_result === 'success'){
                start_button.removeClass("disabled");
                delete_button.removeClass("disabled");
                vm_state.removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-hdd-o").text(" Hibernating");
            }
        }); 
    });

    $(".delete-button").bind("click", function(){
        var vm_uuid = $(this).parents("tr").children("td.vm-uuid").text();
        $("#deleteModal").attr("vm-uuid", vm_uuid);
    });
    $(".nat-button").bind("click", function(){
        var host = $(this).parents("tr").children("td.host-id").text();
        var vm_uuid = $(this).parents("tr").children("td.vm-uuid").text();
        $("#natModal").attr("vm-uuid", vm_uuid);
        $.get('/free_ports/', {'host': host}).done(function(data){
            var free_ports = JSON.parse(data);
            var i = 0;
            $(".port-select").empty();
            for(i=0; i<free_ports.length; i++){
                $(".port-select").append("<option>"+ free_ports[i] + "</option>");
            }
        });
        
    });
});

function applyNat(){
    var protocol = $(".protocol-select option:selected").text();
    var host_port = $(".port-select option:selected").text();
    var vm_port = $(".vm-port").val();
    $.post('/apply_nat/', {'uuid': $('#natModal').attr('vm-uuid'), 'protocol': protocol, 'host_port': host_port, 'vm_port': vm_port});
}


function confirmDelete(data_id){
    $.post('/delete_apply/', {'uuid': $('#deleteModal').attr('vm-uuid')}, function(data){
        }
    );
}

function updateProcess(vm_name, vm_uuid, vm_state, hibernate_button, shutdown_button){
    return function(){
        var process_id;
        var current_width = $("#"+ vm_uuid + "-start-progress-1").width() + $("#"+ vm_uuid + "-start-progress-2").width()
            + $("#"+ vm_uuid + "-start-progress-3").width() + $("#"+ vm_uuid + "-start-progress-4").width();
        var total_width = $('#'+vm_uuid+'-progress-div').width();
        var current_process = current_width/total_width*100;
        if(current_process == 0){
            $.post('/start_vm/', {'uuid': vm_uuid, 'vm-name': vm_name, 'request_type': 'start',
            'current_process':current_process}, function(response){
                var response_json = eval('(' + response + ')');
                if(response_json.request_result === 'success'){
                    vm_state.html(state_string(1));
                    $("#"+ vm_uuid + "-start-progress-1").css("width", '1%');
                }
            });
        }
        else{
            $.post('/powering_process_vm/', {'uuid': vm_uuid, 'vm-name': vm_name, 'process':current_process}, function(response){
                var response_json = eval('(' + response + ')');
                if (response_json.request_result === 'success'){
                    if(response_json.next_state == 5){
                        hibernate_button.removeClass("disabled");
                        shutdown_button.removeClass("disabled");
                        //省略掉完成状态100%状态
                        vm_state.removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-check-circle").text(" Online");
                        $("#" + vm_uuid + "-progress-div").hide();
                        $("#"+ vm_uuid + "-start-progress-1").css("width", "0%");
                        $("#"+ vm_uuid + "-start-progress-2").css("width", "0%");
                        $("#"+ vm_uuid + "-start-progress-3").css("width", "0%");
                        $("#"+ vm_uuid + "-start-progress-4").css("width", "0%");
                        current_process = 100;
                        process_id = $("#"+vm_uuid).text();
                        $("#"+vm_uuid).remove();
                        window.clearInterval(process_id);
                    }
                    else{
                        var current_state_number = state_number(vm_state.text());
                        var next_state_number;
                        var next_process;
                        var current_state_process =  $("#"+ vm_uuid + "-start-progress-" + current_state_number).width()/total_width*100;
                        if(response_json.next_state == 0){
                            //next_process = current_state_process + response_json.request_process;
                            next_state_number = current_state_number;
                            //如果iDashboard返回的process是原始百分比而不是增量，那么
                            next_process=response_json.request_process - (current_process-current_state_process)
                        }
                        else{
                            next_state_number = current_state_number + response_json.next_state;
                            //如果iDashboard返回是原始百分比而不是增量，那么
                            next_process=response_json.request_process-current_process
                            //next_process = response_json.request_process
                            if(next_state_number > 4){
                                next_state_number = 4;
                                next_process = current_state_process + response_json.request_process;
                            }
                            vm_state.html(state_string(next_state_number));
                        }
                        $("#"+ vm_uuid + "-start-progress-" + next_state_number).css("width", next_process+'%');
                    }


                }
            });
        }
    }

}

function state_string(state_number){
    if(state_number == 1){
        return "开机中"; //"BIOS自检"
    }
    else if(state_number == 2){
        return "开机中"; //"磁盘驱动"
    }
    else if(state_number == 3){
        return "开机中"; //"Linux内核解压"
    }
    else if(state_number == 4){
        return "开机中"; //"驱动程序加载"
    }
    else{
        return "Online"
    }
}

function state_number(state) {
    if(state == "Offline"){
        return 0;
    }
    else if(state == "BIOS自检"){
        return 1;
    }
    else if(state == "磁盘驱动"){
        return 2;
    }
    else if(state == "Linux内核解压"){
        return 3;
    }
    else if(state == "驱动程序加载"){
        return 4;
    }
    return 1;
}