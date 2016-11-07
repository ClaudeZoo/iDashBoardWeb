var refreshInterval = 0;
var clockId = -1;

$(document).ready(function() {

	$('#task-status-table').DataTable({
		paging: false,
		order: [[2, 'desc']],
		dom: 'Rt',
		responsive: true,
		columns: [
			{data: 'PID', type: 'num'},
			{data: 'USER'},
			{data: 'cpu', type: 'num'},
			{data: 'mem', type: 'num'},
			{data: 'cmd'}
		]
	});

	// 为datatable插件应用bootstrap样式
	$('#task-status-table').removeClass('display').addClass('table table-striped table-bordered table-hover');

	// 刷新表格数据按钮
	$('#refresh-button').click(refreshData);
	
	// 初始化数据
	refreshData();
});

/**
 * 设置自动刷新时间
 */
function setRefreshOption(interval, index) {
	clearInterval(clockId);
	if (interval > 0) {
		clockId = setInterval(refreshData, interval * 1000);
	}
	console.log('interval set to ' + interval);
	// 更新UI
	$('#refresh-option-menu span.glyphicon-check').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
	$('#refresh-option-menu span').eq(index).removeClass('glyphicon-unchecked').addClass('glyphicon-check');
}

/**
 * 刷新虚拟机数据
 */
function refreshData() {
	console.log('reload start');

	var url = $(location).attr('href').replace(/\/detail\//, '/get-detail/');

	$.post(url, function(json) {
		// 在这里更新表格数据
		var data = json;

		$('#td-os').text(data.uName);
		$('#td-cpu-info').text(data.cpuInfo);
		$('#td-total-mem').text(data.memory.split(" ")[0]);
		$('#td-total-swap').text(data.memory_swap.split(" ")[0]);
        var cpu = ["us: ","sy: ","ni: ","id: ","wa: ","hi: ","si: ", "st: "];
        var strs = data.cpuLoad.split(" ");
        var str = "";
        for (var i = 0; i < strs.length; i++){
            str += "<strong>"+cpu[i]+"</strong>" + strs[i] + "&emsp;";
        }
		$('#td-cpu-load').html(str);
        var mem = ["total: ","used: ","free: ","buffers: "];
        str = "";
        strs = data.memory.split(" ");
        for (var i = 0; i < strs.length; i++) {
            str += "<strong>" + mem[i] + "</strong>" + strs[i] + "&emsp;";
        }
		$('#td-mem-load').html(str);
        var swap = ["total: ","used: ","free: ","cached Mem: "];
        str = "";
        strs = data.memory_swap.split(" ");
        for (var i = 0; i < strs.length; i++){
            str += "<strong>"+swap[i]+"</strong>" + strs[i] + "&emsp;";
        }
		$('#td-swap-load').html(str);
        var task = ["total：","running：","sleeping：","stopped：", "zombie: "];
        str = ""
        strs = data.tasks.split(" ");
        for (var i = 0; i < strs.length; i++){
            str += "<strong>"+task[i]+"</strong>" + strs[i] + "&emsp;";
        }
		$('#td-task-info').html(str);
		$('#td-user').text(data.userName);
		
		$('#td-ipv4').text(data.ipv4);
		$('#td-ipv6').text(data.ipv6);
		$('#td-broadcast').text(data.broadcast);
		$('#td-mask').text(data.mask);
		$('#td-dns').text(data.dns);

		var table = $('#task-status-table').DataTable();
		table.clear();
		// 渲染表格
		table.rows.add(data.process).draw();

		// 更新完毕
		console.log('reload complete');
	}, 'json');
}
