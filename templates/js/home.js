var refreshInterval = 0;
var clockId = -1;

$(document).ready(function() {
    $('#host-data-table').DataTable({
        dom: 'R<"row"<"#host-count.col-sm-6"<"#host-count-label">><"col-sm-6"f>>rt<"row"<"col-sm-6"l><"col-sm-6"p>>',
        ajax: '/refreshSimplePageHost/',
		columns: [
			{'data': 'ip'},
			{'data': 'os'},
			{'data': 'CPU'},
			{'data': 'Memory'},
			{'data': 'Disk'},
		],
		responsive: {
			details: {
				renderer: function(api, rowIndex) {
					// 响应式插件中child单元格的渲染函数
					var html = api.cells(rowIndex, ':hidden').eq(0).map(function(cell) {
						var header = $(api.column(cell.column).header());

						var title = '<span class="dtr-title">' + header.text() + ':' + '</span>';
						var data = '<span class="dtr-data">' + api.cell(cell).data() + '</span>';

						return '<li data-dtr-index="' + cell.column + '">' + title + data + '</li>';
					}).toArray().join('');

					var row = api.row(rowIndex).node();
					var id = $(row).attr('data-id');

					var ulElement = $('<ul data-dtr-index="0"></ul>').append(html);
					return $('<div class="responsive-child" data-id="' + id + '"></div>').append(ulElement);
				}
			}
		},
		initComplete: function() {
			console.log('init complete');
			// 添加刷新按钮组
			$('#host-count').prepend($('#refresh-button-group1'));
		},
		drawCallback: function() {
			console.log('draw complete');
			var hostCount = this.api().data().length;
			// 显示在线虚拟机数量
			$('#host-count-label').html('<label><strong> ' + hostCount + ' </strong> physical servers available.</label>');

			if (hostCount != 0) {
				// 单击单元格跳转到详细信息
				$('#host-data-table tbody').on('click', 'tr', function() {
					console.log($(this).attr('data-id'));
					$(location).attr('href', '/detail/' + $(this).attr('data-id') + '/');
				});
				// 单击响应式插件生成的child单元格跳转到详细信息
				$('#host-data-table tbody').on('click', 'div.responsive-child', function(e) {
					console.log($(this).attr('data-id'));
					$(location).attr('href', '/detail/' + $(this).attr('data-id') + '/');
					e.stopPropagation();
				});
			}
		},
		createdRow: function(row, data) {
			// 为每一行赋予一个虚拟机id
			$(row).attr('data-id', data.info_id);
		},
		rowCallback: function(row, data) {
			// 修改占用率为进度条样式
			function getProgressBarClass(str) {
				var p = Number(str.substring(0, str.length - 1));
				if (p <= 20) {
					return ' progress-bar-success';
				} else if (p <= 50) {
					return '';
				} else if (p <= 80) {
					return ' progress-bar-warning';
				} else {
					return ' progress-bar-danger';
				}
			}
            var ip_wan_ip = data.ip + ' / ' + data.wan_ip;
			var memPercent = data.Memory;
			var memHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(memPercent) + '" role="progressbar" style="min-width: 2em; width: ' + memPercent + ';">' + memPercent + '</div></div>';
            var cpuPencent = data.CPU;
            var cpuHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(cpuPencent) + '" role="progressbar" style="min-width: 2em; width: ' + cpuPencent + ';">' + cpuPencent + '</div></div>';
            var diskPercent = data.Disk;
			var diskHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(diskPercent) + '" role="progressbar" style="min-width: 2em; width: ' + diskPercent + ';">' + diskPercent + '</div></div>';
			$('td:eq(0)', row).html(ip_wan_ip);
            $('td:eq(4)', row).html(diskHtml);
            $('td:eq(3)', row).html(memHtml);
            $('td:eq(2)', row).html(cpuHtml);
            if(data.state==='offline'){
                $(row).addClass('danger');
            }
		}
	});

	// 数据表插件初始化
	$('#main-data-table').DataTable({
		dom: 'R<"row"<"#vm-count.col-sm-6"<"#vm-count-label">><"col-sm-6"f>>rt<"row"<"col-sm-6"l><"col-sm-6"p>>',
		ajax: '/refreshSimplePage/',
		columns: [
			{'data': 'vm_name'},
            {'data': 'wan_ip'},
			{'data': 'ip'},
			{'data': 'os'},
			{'data': 'CPU'},
			{'data': 'Memory'},
			{'data': 'Disk'}
		],
		responsive: {
			details: {
				renderer: function(api, rowIndex) {
					// 响应式插件中child单元格的渲染函数
					var html = api.cells(rowIndex, ':hidden').eq(0).map(function(cell) {
						var header = $(api.column(cell.column).header());

						var title = '<span class="dtr-title">' + header.text() + ':' + '</span>';
						var data = '<span class="dtr-data">' + api.cell(cell).data() + '</span>';

						return '<li data-dtr-index="' + cell.column + '">' + title + data + '</li>';
					}).toArray().join('');

					var row = api.row(rowIndex).node();
					var id = $(row).attr('data-id');

					var ulElement = $('<ul data-dtr-index="0"></ul>').append(html);
					return $('<div class="responsive-child" data-id="' + id + '"></div>').append(ulElement);
				}
			}
		},
		initComplete: function() {
			console.log('init complete');
			// 添加刷新按钮组
			$('#vm-count').prepend($('#refresh-button-group'));
		},
		drawCallback: function() {
			console.log('draw complete');
			var vmCount = this.api().data().length;
			// 显示在线虚拟机数量
			$('#vm-count-label').html('<label><strong> ' + vmCount + ' </strong> virtual machines available.</label>');
			if (vmCount != 0) {
				// 单击单元格跳转到详细信息
				$('#main-data-table tbody').on('click', 'tr', function() {
					console.log($(this).attr('data-id'));
					$(location).attr('href', '/detail/' + $(this).attr('data-id') + '/');
				});
				// 单击响应式插件生成的child单元格跳转到详细信息
				$('#main-data-table tbody').on('click', 'div.responsive-child', function(e) {
					console.log($(this).attr('data-id'));
					$(location).attr('href', '/detail/' + $(this).attr('data-id') + '/');
					e.stopPropagation();
				});
			}
		},
		createdRow: function(row, data) {
			// 为每一行赋予一个虚拟机id
			$(row).attr('data-id', data.info_id);
		},
		rowCallback: function(row, data) {
			// 修改占用率为进度条样式
			function getProgressBarClass(str) {
				var p = Number(str.substring(0, str.length - 1));
				if (p <= 20) {
					return ' progress-bar-success';
				} else if (p <= 50) {
					return '';
				} else if (p <= 80) {
					return ' progress-bar-warning';
				} else {
					return ' progress-bar-danger';
				}
			}
            var ip_wan_ip = data.wan_ip + ' : ' + data.port;
			var memPercent = data.Memory;
			var memHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(memPercent) + '" role="progressbar" style="min-width: 2em; width: ' + memPercent + ';">' + memPercent + '</div></div>';
            var cpuPencent = data.CPU;
            var cpuHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(cpuPencent) + '" role="progressbar" style="min-width: 2em; width: ' + cpuPencent + ';">' + cpuPencent + '</div></div>';
			var diskPercent = data.Disk;
			var diskHtml = '<div class="progress" style="margin-bottom: 0px;"><div class="progress-bar' + getProgressBarClass(diskPercent) + '" role="progressbar" style="min-width: 2em; width: ' + diskPercent + ';">' + diskPercent + '</div></div>';
			$('td:eq(1)', row).html(ip_wan_ip);
            $('td:eq(6)', row).html(diskHtml);
            $('td:eq(5)', row).html(memHtml);
            $('td:eq(4)', row).html(cpuHtml);
            if(data.state==='offline'){
                $(row).addClass('danger');
            }
		}
	});

	// 为datatable插件应用bootstrap样式
	$('#main-data-table').removeClass('display').addClass('table table-striped table-bordered table-hover');
	$('#host-data-table').removeClass('display').addClass('table table-striped table-bordered table-hover');
	// // DataTable插件的FixedHeader扩展，响应式表现较差，暂不使用
	// new $.fn.dataTable.FixedHeader($('#main-data-table').DataTable());

	// 刷新表格数据按钮
	$('#refresh-button').click(refreshData);
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
 * 刷新DataTable数据
 */
function refreshData() {
	console.log('reload start');
	$('#main-data-table').DataTable().ajax.reload(function() {
		console.log('reload complete');
	}, false);
}
