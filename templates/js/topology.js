

$(document).ready(function () {
    var node_subnets, selected_vm_info_id;

    var svg = d3.select("svg"),
        width = +svg.property("clientWidth"),
        height = +svg.property("clientHeight");

    var color = d3.scaleOrdinal(d3.schemeCategory20);


    var node_menu = function(d) {
        if(d.size == 70 || node_subnets[d.id] == undefined){
            return [{
                title: 'Show Details',
                action: function(elm, d) {
                    window.open("/detail/" + d.id + "/");
                }
            }];
        }else{
            return [{
                    title: 'Delete it from a subnet',
                    action: function(elm, d) {
                        console.log('Delete it from a subnet!');
                        console.log(elm);
                        console.log('The data for this circle is: ' + d.size);
                        console.log(node_subnets[d.id]);
                        if($('[type=checkbox]')){
                            $('[type=checkbox]').remove();
                        }

                        var subnets = node_subnets[d.id];
                        for(var i = 0; i <= subnets.length - 1; i++){
                            console.log(subnets[i]);
                            var network_name = subnets[i]['name'];
                            var network_id = subnets[i]['id'];
                            $("#subnets").html("");
                            if(subnets[i] != ""){
                                $('#subnets').append($('<br><input type="checkbox" name="checkbox-' + network_id + '">' + network_name + '</input>'));
                            }
                        }
                        selected_vm_info_id = d.id;
                        $('#DeleteVMSubnetModal').modal();
                    }
                }, {
                    title: 'Show Details',
                    action: function(elm, d) {
                    window.open("/detail/" + d.id + "/");
                    }
                }];
        }

    }

    var link_menu = function(d){
        if(d.group == 0 ){
            return [{
                /*
                title: 'Show Details',
                action: function(elm, d) {
                    window.open("/detail/" + d.id + "/");
                }*/
            }];
        }else{
            return [{
                title:'Delete a vm in this subnet',
                action: function(){
                    alert('Delete a vm in this subnet');
                }
            },{
                title:'Delete this subnet',
                action: function(){
                    $('#deleteNetModal').modal();
                }
            }]
        }
     }

    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }).strength(0.05))
        .force("collision", d3.forceCollide().radius(function (d) {
            return d.size + 15;
        }))
        .force("charge", d3.forceManyBody().strength(-1000))
        .force("center", d3.forceCenter(width / 2, height / 2));


    //d3.json("/js/topology.json", function (error, graph) {
    d3.json("/topology_data", function (error, graph) {
        if (error) throw error;

        node_subnets = graph.node_subnets;

        var circles = [];
        graph.links.forEach(function(link) {
            circles.push({
                source: graph.nodes[link.source],
                target: graph.nodes[link.target]
            });
        });
        //sort links by source, target, then group
        graph.links.sort(function(a,b) {
            if (a.source > b.source) {
                return 1;
            } else if (a.source < b.source) {
                return -1;
            } else {
                if (a.target > b.target) {
                    return 1;
                }if (a.target < b.target) {
                    return -1;
                } else {
                    if(a.group > b.group){
                        return 1;
                    }else if(a.group < b.group){
                        return -1;
                    }else{
                        return 0;
                    }
                }
            }
        });

        var linkNum = {};
        //any links with duplicate source and target get an incremented 'linknum'
        for (var i = 0; i < graph.links.length; i++) {
            if (i != 0 &&
                graph.links[i].source == graph.links[i-1].source &&
               graph.links[i].target == graph.links[i-1].target) {
                graph.links[i].linkindex = graph.links[i-1].linkindex + 1;
            } else {
                graph.links[i].linkindex = 1;
            }
            // save the total number of links between two nodes
            if(linkNum[graph.links[i].target + "," + graph.links[i].source] !== undefined) {
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
            .on('contextmenu',d3.contextMenu(node_menu));
        /*
         var cc = clickcancel();
         circle.call(cc);
         cc.on('click', function () {
         alert("click")
         });
         cc.on('dblclick', function () {
         alert("dbclick")
         });
         */
        // Add a text element to the previously added g element.

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
            .enter().insert('g','.node')
            .append("path")
            .style("stroke", function(d) {
                return color(d.group);
            })
            .attr("stroke-width", function (d) {
                return d.value;
            })
            .attr("group_id", function(d){
                return d.group;

            })
            .on('mouseover', function(d){
                d3.selectAll('[group_id="' + d.group + '"]').style('stroke',"#666");
            })
            .on('mouseout', function(d){
                d3.selectAll('[group_id="' + d.group + '"]').style('stroke',color(d.group));

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
            //.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

            label
                .attr("x", function (d) {
                    return d.x
                })
                .attr("y", function (d) {
                    return d.y;
                });
            path
                .attr("d", function(d){
                var curve = 2;
                var homogeneous=3.2;
                var dx = (d.target.x - d.source.x),
                    dy = (d.target.y - d.source.y),
                    dr = Math.sqrt(dx * dx + dy * dy),
                    offsetDX = (dx * d.target.size) / dr,
                    offsetDY = (dy * d.target.size) / dr;

                var totalLinkNum = linkNum[d.source.id + "," + d.target.id] || linkNum[d.target.id + "," + d.source.id];
                if(totalLinkNum > 1){
                    dr = dr/(1 + (1/totalLinkNum) * (d.linkindex - 1));
                }

                return "M" + d.source.x + "," + d.source.y +
                "A" + dr + "," + dr + " 0 0 1," + (d.target.x - offsetDX) + "," + (d.target.y - offsetDY) +
                "A" + dr + "," + dr + " 0 0 0," + d.source.x + "," + d.source.y;
            })
        }
    });
})
;

function clickcancel() {
    var event = d3.dispatch('click', 'dblclick');

    function cc(selection) {
        var down,
            tolerance = 5,
            last,
            wait = null;
        // euclidean distance
        function dist(a, b) {
            return Math.sqrt(Math.pow(a[0] - b[0], 2) + Math.pow(a[1] - b[1], 2));
        }

        selection.on('mousedown', function () {
            down = d3.mouse(document.body);
            last = +new Date();
        });
        selection.on('mouseup', function () {
            if (dist(down, d3.mouse(document.body)) > tolerance) {
                return;
            } else {
                if (wait) {
                    window.clearTimeout(wait);
                    wait = null;
                    event.call("dblclick");
                } else {
                    wait = window.setTimeout(function () {
                        event.call("click");
                        wait = null;
                    }, 300);
                }
            }
        });
    };

    // The '.on' instance method that accepts event
    // listeners. Unlike d3 v4, this cannot be simply
    // achieved via d3.rebind, which no longer exists
    cc.on = function () {
        var value = event.on.apply(event, arguments);
        return value === event ? cc : value;
    };

    return cc
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

function rm_vm_from_networks(){
    var selected_subnets = $(':checked');
    if(selected_subnets != []){
        var network_ids = [];
        for(var i = 0; i < selected_subnets.length; i++){
            network_ids.push(selected_subnets[i].name.substring(9));
        }
        console.log(network_ids);
        $.post('/rm_vm_from_networks/', {
            'network_ids':network_ids.join(','),
            'info_id':selected_vm_info_id,
        }, function(response){
            if(response == 'Offline'){
                alert('Be sure to start this vm, if you want to remove it from any subnet!');
            }else if(response == 'Failed'){
                alert('Failed to remove this vm from a subnet.');
            }else{
                alert('Succeed!');
            }


        })
    }else{
        alert("Please choose a subnet!");
    }
}

function confirmDeleteNet(){

}