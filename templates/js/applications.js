/**
 * Created by wcx on 15/4/28.
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
    $('#operation-tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $("operation-tab").find("span").text("0");
    });
    $('#create-applications-table').DataTable({
        "ordering": true,
        "order": [[ 5, "desc" ]]});
    $('#delete-applications-table').DataTable({
        "ordering": true,
        "order": [[ 3, "desc" ]]});
    $('#nat-applications-table').DataTable({
        "ordering": true,
        "order": [[ 6, "desc" ]]});
    $('#historical-operations-table').DataTable({
        "ordering": true,
        "order": [[ 0, "desc" ]]});
});