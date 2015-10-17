/**
 * Created by wcx on 15/4/27.
 */
$(document).ready(function(){
    $('#create-tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $("create-tab a span").text("0");
    });
    $('#delete-tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $("delete-tab").find("span").text("0");
    });
    $('#nat-tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $("nat-tab").find("span").text("0");
    });
    $('#create-applications-table').DataTable({
        "ordering": true,
        "order": [[ 5, "desc" ]]});
    $('#delete-applications-table').DataTable({
        "ordering": true,
        "order": [[ 4, "desc" ]]});
    $('#nat-applications-table').DataTable({
        "ordering": true,
        "order": [[ 7, "desc" ]]});
    $("#create-applications-table .approve-button").bind("click", function(){
        var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/approve_single_creation/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-check-square-o"> Approved</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#create-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });
    $("#create-applications-table .refuse-button").bind("click", function(){
       var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/refuse_single_creation/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-ban"> Rejected</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#create-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });
    $("#delete-applications-table .approve-button").bind("click", function(){
        var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/approve_single_delete/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-check-square-o"> Approved</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#delete-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });
    $("#delete-applications-table .refuse-button").bind("click", function(){
       var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/refuse_single_delete/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-ban"> Rejected</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#delete-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });
    $("#nat-applications-table .approve-button").bind("click", function(){
        var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/approve_single_nat/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-check-square-o"> Approved</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#nat-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });
    $("#nat-applications-table .refuse-button").bind("click", function(){
       var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $.post("/refuse_single_nat/", { id: application_id})
            .done(function(){
                $(id_selector).find(".approve-button,.refuse-button").hide();
                $(id_selector).find("div").prepend('<i class="fa fa-ban"> Rejected</i>');
                $(id_selector).find(".remove-button").show();
                var create_count = $("#nat-tab").find("span");
                var count = parseInt(create_count.text()) - 1;
                create_count.text(count.toString());
            });
    });

    $(".remove-button").bind("click", function(){
        var application_id = $(this).parents("td").siblings(".application-id").text();
        var id_selector = "#application-" + application_id;
        $(id_selector).remove();
    });
});