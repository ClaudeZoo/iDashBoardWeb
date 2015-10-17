
$(document).ready(function(){
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
        var vm_state = $(this).parents("tr").find(".state-td i")
        var start_button = $(this).parents("tr").find(".start-button");
        var shutdown_button = $(this).parents("tr").find(".shutdown-button");
        var hibernate_button = $(this).parents("tr").find(".hibernate-button");
        var delete_button = $(this).parents("tr").find(".delete-button");
        start_button.addClass("disabled");
        delete_button.addClass("disabled");
        vm_state.removeClass("fa-times-circle fa-hdd-o").addClass("fa-spinner fa-pulse fa-2x").text("")
        $.post('/control_vm/', {'uuid': vm_uuid, 'vm-name': vm_name, 'request_type': 'start'}, function(response){
            var response_json = eval('(' + response + ')');
            if (response_json.request_result === 'success'){
                hibernate_button.removeClass("disabled");
                shutdown_button.removeClass("disabled");
                vm_state.removeClass("fa-spinner fa-pulse fa-2x").addClass("fa-check-circle").text(" Online");
            }
        }); 
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