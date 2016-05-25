$(document).ready(function(){
    $(function () { $(".tooltip-options").tooltip({html : true });});
    $("div.progress").hide();
    $(".state").hide();
    $("#myVMs-data-table").DataTable();
    $("tbody tr").each(function(){
        var items = findItems($(this));
        if (items[2].text() == " Online"){
            items[2].addClass("fa-check-circle");
            items[4].addClass("disabled");
            items[7].addClass("disabled");
        }
        else if ($(this).find(".state-td i").text() == " Offline"){
            $(this).find(".state-td i").addClass("fa-times-circle");
            items[5].addClass("disabled");
            items[6].addClass("disabled");
        }
        else {
            $(this).find(".state-td i").addClass("fa-hdd-o");
            items[7].addClass("disabled");
            items[6].addClass("disabled");
        }
    });

    $(".start-button").bind("click", function(){
        var items = findItems($(this).parents("tr"));
        items[4].addClass("disabled");
        items[7].addClass("disabled");
        items[2].removeClass("fa-times-circle fa-hdd-o").text("Waiting for response...");
        var vm_name = items[0].text();
        var uuid = items[1].text();
        start_vm(vm_name, uuid, items);
    });
    $(".shutdown-button").bind("click", function(){
        var items = findItems($(this).parents("tr"));
        items[5].addClass("disabled");
        items[6].addClass("disabled");
        items[2].removeClass("fa-check-circle").addClass("fa-spinner fa-pulse fa-2x").text("");
        $.post('/control_vm/', {'uuid': items[1].text(), 'vm-name': items[0].text(), 'request_type': 'shutdown'}, function(response){
            var response_json = eval('(' + response + ')');
            if (response_json.request_result === 'success'){
                items[4].removeClass("disabled");
                items[7].removeClass("disabled");
                items[2].removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-times-circle").text(" Offline");
            }
        }); 
    });
    $(".hibernate-button").bind("click", function(){
        var items = findItems($(this).parents("tr"));
        items[6].addClass("disabled");
        items[5].addClass("disabled");
        items[2].removeClass("fa-times-circle").addClass("fa-spinner fa-pulse fa-2x").text("");
        $.post('/control_vm/', {'uuid': items[1].text(), 'vm-name': items[0].text(), 'request_type': 'savestate'}, function(response){
            var response_json = eval('(' + response + ')');
            if (response_json.request_result === 'success'){
                item[4].removeClass("disabled");
                item[7].removeClass("disabled");
                item[2].removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-hdd-o").text(" Hibernating");
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


function start_vm(vm_name, uuid, items){
    $.post('/start_vm/', {'uuid': uuid, 'vm-name': vm_name, 'request_type': 'start'}, function(data){
        var response_json = eval('(' + data + ')');
        if (response_json.request_result === 'success'){
            items[2].hide();
            $("#"+ uuid + "-start-progress-1").width("0%");
            $("#"+ uuid + "-start-progress-2").width("0%");
            $("#"+ uuid + "-start-progress-3").width("0%");
            items[9].text(" ");
            items[10].text("0");
            $("#"+uuid+"-progress-div").show();
            $(".state").show();
            var update = updateProcess(vm_name, uuid, items);
            var process_id = setInterval(update, 50);
            $('<div/>', { id: uuid, class: "hiding"}).html(process_id).appendTo('body');
        }
    });
}


function findItems(row){
    var name = row.children("td.vm-name");
    var uuid = row.children("td.vm-uuid");
    var state = row.find(".state-td i");
    var bar = $("#"+uuid.text()+"-progress-div");
    var start_button = row.find(".start-button");
    var shutdown_button = row.find(".shutdown-button");
    var hibernate_button = row.find(".hibernate-button");
    var delete_button = row.find(".delete-button");
    var vm_state = row.find(".vm-state");
    var vm_stage = row.find(".vm-stage");
    var boot_time = row.find(".time");
    return [name, uuid, state, bar, start_button, shutdown_button, hibernate_button, delete_button, vm_state, vm_stage, boot_time];
}

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

function updateProcess(vm_name, uuid, items){
    return function(){
        $.post('/start_monitor/', {'uuid': uuid, 'vm-name': vm_name, 'request_type': 'query'}, function(response){
            var response_json = eval('(' + response + ')');
            if(response_json.result == 'success'){
                var c = parseFloat(items[10].text());
                c = (c + 0.05).toFixed(2);
                items[10].text(c);
                if (response_json.state == 'pre_kernel'){
                    if (c < 3){
                        $("#"+ uuid + "-start-progress-1").css("width", (c*4).toString() + "%");
                        items[9].text("BIOS");
                    }
                    else{
                        $("#"+ uuid + "-start-progress-2").css("width", ((c-3)*4).toString() + "%");
                        items[9].text("Grub");
                    }
                }
                else{
                    items[9].text("Starting Kernel");
                    items[8].text(response_json.info);
                    var current_width = $("#"+ uuid + "-start-progress-1").width() + $("#"+ uuid + "-start-progress-2").width();
                    var total_width = $('#'+uuid+'-progress-div').width();
                    var remain = 98 - current_width/total_width*100;
                    if (parseInt(response_json.rate) <= 348){
                        var progress = parseInt(response_json.rate) / 384 * remain;
                        $("#"+ uuid + "-start-progress-3").css("width", progress.toString() + "%");
                    }
                    else{
                        $("#"+ uuid + "-start-progress-3").css("width", remain+"%");
                    }
                    //console.log(response_json.info)
                }
                return true;
            }
            else{
                $(".state").hide();
                $("#"+uuid+"-progress-div").hide();
                items[2].show();
                items[2].addClass("fa-check-circle").text(" Online");
                items[4].addClass("disabled");
                items[7].addClass("disabled");
                items[5].removeClass("disabled");
                items[6].removeClass("disabled");
                var process_element = $("#"+uuid);
                process_id = process_element.text();
                process_element.remove();
                window.clearInterval(process_id);
                return false;
            }

        });
        /*
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
        } */
    }
};

