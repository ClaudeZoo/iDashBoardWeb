$(document).ready(function () {
    var node_subnets, nodes, links, selected_vm_info_id, selected_subnet, available_vms;
    var svg = d3.select("svg"),
        width = +svg.property("clientWidth"),
        height = +svg.property("clientHeight");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var node_menu = function (d) {

        if (d.size == 70 || node_subnets[d.id] == undefined) {
            return [{
                title: 'Show Details',
                action: function (elm, d) {
                    window.open("/detail/" + d.id + "/");
                }
            }];
        } else {
            return [{
                title: 'Delete it from a subnet',
                action: function (elm, d) {
                    console.log('Delete it from a subnet!');
                    console.log(elm);
                    console.log('The data for this circle is: ' + d.size);
                    console.log(node_subnets[d.id]);
                    if ($('[type=checkbox]')) {
                        $('[type=checkbox]').remove();
                    }

                    var subnets = node_subnets[d.id];
                    $("#subnets").empty();
                    $("#subnets").append("<label>Subnets</label>");
                    for (var i = 0; i <= subnets.length - 1; i++) {
                        console.log(subnets[i]);
                        var network_name = subnets[i]['name'];
                        var network_id = subnets[i]['id'];
                        if (subnets[i] != "") {
                            $('#subnets').append($('<br><input type="checkbox" name="checkbox-' + network_id + '"> ' + network_name + '</input>'));
                        }
                    }
                    selected_vm_info_id = d.id;
                    $('#DeleteVMSubnetModal').modal();
                }
            }, {
                title: 'Show Details',
                action: function (elm, d) {
                    window.open("/detail/" + d.id + "/");
                }
            },
                {
                    title: 'Shutdown',
                    action: function (elm, d) {
                        $.post('/control_vm/', {
                            'uuid': d.uuid,
                            'vm-name': d.name,
                            'request_type': 'shutdown'
                        }, function (response) {
                            var response_json = eval('(' + response + ')');
                            if (response_json.request_result === 'success') {
                                alert("Shutdown Success!");
                                location.reload();
                            }
                        })
                    }
                }
            ];
        }
        ;
    };

    var link_menu = function (d) {
        if (d.group == 0 || d.group == 3) {
            return [
                /*
                 title: 'Show Details',
                 action: function(elm, d) {
                 window.open("/detail/" + d.id + "/");
                 }*/
            ];
        } else {
            return [{
                title: 'Add a vm to this subnet',
                action: function () {
                    var vms_in_subnet = new Set();
                    var current_host;
                    selected_subnet = d.group;
                    for (var i = 0; i < links.length; i++) {
                        if (links[i].group == d.group) {
                            if (!vms_in_subnet.has(links[i].source.id)) {
                                vms_in_subnet.add(links[i].source.id);
                                current_host = links[i].source.group;
                            }
                            if (!vms_in_subnet.has(links[i].target.id)) {
                                vms_in_subnet.add(links[i].target.id);
                                current_host = links[i].target.group;
                            }
                        }
                    }

                    console.log(vms_in_subnet);
                    available_vms = [];

                    for (var i = 0; i < nodes.length; i++) {
                        if (nodes[i]['uuid'] != undefined && !(vms_in_subnet.has(nodes[i].id)) && nodes[i]['group'] == current_host) {
                            available_vms.push(nodes[i])
                        }
                    }
                    console.log(available_vms);
                    $("#vms").empty();
                    $("#vms").append("<label>Virtual Machines</label>");

                    $("#addVM-btn").attr("disabled", false);
                    if (available_vms.length == 0) {
                        $("#vms").append("<br><h4>No available virtual machines could be added in this subnet</h4>");
                        $("#addVM-btn").attr("disabled", true);
                    } else {
                        for (var i = 0; i < available_vms.length; i++) {
                            $('#vms').append(
                                $(
                                    '<br><input type="checkbox" name="checkbox-' +
                                    available_vms[i].id + '"> ' + available_vms[i].name + '</input>'
                                )
                            );
                        }

                    }
                    $('#AddVMModal').modal();
                }
            }, {
                title: 'Delete this subnet',
                action: function () {
                    selected_subnet = d.group;
                    $('#DeleteNetModal').modal();
                }
            }]
        }
    };

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }).strength(0.1))
        .force("collision", d3.forceCollide().radius(function (d) {
            return d.size + 15;
        }))
        .force("charge", d3.forceManyBody().strength(-600))
        .force("center", d3.forceCenter(width / 2, height / 2));

    var draw = function (error, graph) {
        if (error) throw error;

        node_subnets = graph.node_subnets;

        nodes = graph.nodes;

        links = graph.links;

        var circles = [];
        graph.links.forEach(function (link) {
            circles.push({
                source: graph.nodes[link.source],
                target: graph.nodes[link.target]
            });
        });
        //sort links by source, target, then group
        graph.links.sort(function (a, b) {
            if (a.source > b.source) {
                return 1;
            } else if (a.source < b.source) {
                return -1;
            } else {
                if (a.target > b.target) {
                    return 1;
                }
                if (a.target < b.target) {
                    return -1;
                } else {
                    if (a.group > b.group) {
                        return 1;
                    } else if (a.group < b.group) {
                        return -1;
                    } else {
                        return 0;
                    }
                }
            }
        });

        var linkNum = {};
        //any links with duplicate source and target get an incremented 'linknum'
        for (var i = 0; i < graph.links.length; i++) {
            if (i != 0 &&
                graph.links[i].source == graph.links[i - 1].source &&
                graph.links[i].target == graph.links[i - 1].target) {
                graph.links[i].linkindex = graph.links[i - 1].linkindex + 1;
            } else {
                graph.links[i].linkindex = 1;
            }
            // save the total number of links between two nodes
            if (linkNum[graph.links[i].target + "," + graph.links[i].source] !== undefined) {
                linkNum[graph.links[i].target + "," + graph.links[i].source] = graph.links[i].linkindex;
            } else {
                linkNum[graph.links[i].source + "," + graph.links[i].target] = graph.links[i].linkindex;
            }
        }


        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // Add a circle element to the previously added g element.
        var circle = node.append("circle")
            .attr("class", "node")
            .attr("r", function (d) {
                return d.size
            })
            .attr("fill", function (d) {
                return color(d.group)
            })
            .on("dblclick", function (d) {
                window.open("/detail/" + d.id + "/");
            })
            .on('contextmenu', d3.contextMenu(node_menu));

        var trans = d3.transition().duration(2000);
        d3.interval(function () {
            circle.transition(trans)
                .attr("r", function (d) {
                    return d.size + 5;
                })
                .transition(trans)
                .attr("r", function (d) {
                    return d.size - 5;
                });

        }, 4000, d3.now());


        var label = node.append("text")
            .attr("dy", ".35em")
            .attr("dx", "-28px")
            .text(function (d) {
                return d.name;
            });
        node.append("title")
            .text(function (d) {
                return "VM Name: " + d.name + "\nMemory: " + d.memory + "\nuuid: " + d.uuid;
            });

        var path = svg.selectAll("path")
            .data(graph.links)
            .enter().insert('g', '.node')
            .append("path")
            .style("stroke", function (d) {
                return color(d.group);
            })
            .attr("stroke-width", function (d) {
                return d.value;
            })
            .attr("group_id", function (d) {
                return d.group;

            })
            .on('mouseover', function (d) {
                d3.selectAll('[group_id="' + d.group + '"]').style('stroke', "#666");
            })
            .on('mouseout', function (d) {
                d3.selectAll('[group_id="' + d.group + '"]').style('stroke', color(d.group));

            })
            .on('contextmenu', d3.contextMenu(link_menu));

        simulation
            .on("tick", ticked)
            .nodes(graph.nodes);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            circle
                .attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                });

            label
                .attr("x", function (d) {
                    return d.x
                })
                .attr("y", function (d) {
                    return d.y;
                });
            path
                .attr("d", function (d) {
                    var curve = 2;
                    var homogeneous = 3.2;
                    var dx = (d.target.x - d.source.x),
                        dy = (d.target.y - d.source.y),
                        dr = Math.sqrt(dx * dx + dy * dy);

                    var totalLinkNum = linkNum[d.source.id + "," + d.target.id] || linkNum[d.target.id + "," + d.source.id];
                    if (totalLinkNum > 1) {
                        dr = dr / (1 + (1 / totalLinkNum) * (d.linkindex - 1));
                    }

                    return "M" + d.source.x + "," + d.source.y +
                        "A" + dr + "," + dr + " 0 0 1," + d.target.x + "," + d.target.y +
                        "A" + dr + "," + dr + " 0 0 0," + d.source.x + "," + d.source.y;
                })
        }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    };
    d3.json("/topology_data", draw);
    /*
     var update = function () {
     d3.json("/topology_data", draw);
     };
     d3.interval(update, 2000, d3.now());
     */
});


function rm_vm_from_networks() {
    var selected_subnets = $('#subnets :checked');
    if (selected_subnets != []) {
        var network_ids = [];
        for (var i = 0; i < selected_subnets.length; i++) {
            network_ids.push(selected_subnets[i].name.substring(9));
        }
        console.log(network_ids);
        $.post('/rm_vm_from_networks/', {
            'network_ids': network_ids.join(','),
            'info_id': selected_vm_info_id,
        }, function (response) {
            if (response == 'Offline') {
                alert('Be sure to start this vm, if you want to remove it from any subnet!');
            } else if (response == 'Failed') {
                alert('Failed to remove this vm from a subnet.');
            } else {
                alert('Succeed!');
                location.reload();
            }

        })
    } else {
        alert("Please choose a subnet at least!");
    }
}

function confirmDeleteNet() {
    $.post('/del_network/', {
        'network_id': selected_subnet
    }, function (response) {
        if (response == 'Offline') {
            alert('Be sure to start all relevant virtual machines, ' +
                'if you want to delete this subnet!');
        } else if (response == 'Failed') {
            alert('Failed to delete this subnet.');
        } else {
            alert('Succeed!');
            location.reload();
        }
    })
}

function confirmAddVM() {
    var selected_vms = $('#vms :checked');
    if (selected_vms != []) {
        $.post('/add_vm_in_network/', {
            'network_id': selected_subnet,
            'vm_info_ids': available_vms.map(function (x) {
                return x.id;
            }).join(',')
        }, function (response) {
            if (response.offline_vms_name != undefined) {
                var failed_vms_name_str =
                    alert('Failed to add offline virtual machine(s) into this subnet: \n' +
                        response.offline_vms_name.join(',') + '\n' +
                        'Please start them(it)!');
            } else if (response == 'Failed') {
                alert('Failed to add this vm into this subnet.');
            } else {
                alert('Succeed!');
                location.reload();
            }
        });
    } else {
        alert("Please choose a virtual machine at least!");
    }
}
