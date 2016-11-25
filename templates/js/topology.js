$(document).ready(function() {

    var svg = d3.select("svg"),
        width = +svg.property("clientWidth"),
        height = +svg.property("clientHeight");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }).strength(0.1))
        .force("collision", d3.forceCollide().radius(function (d) {
            return d.size + 15;
        }))
        .force("charge", d3.forceManyBody().strength(-100))
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json("/js/topology.json", function (error, graph) {
        if (error) throw error;

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function (d) {
                return Math.sqrt(d.value);
            })
            .attr("stroke", "#aaa");

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
            .attr("r", function(d) { return d.size})
            .attr("fill", function(d) { return color(d.group)});


        // Add a text element to the previously added g element.

        var label = node.append("text")
            .attr("dy", ".35em")
            .text(function(d) {
                return d.id;
            });
        node.append("title")
            .text(function(d) { return d.id + "\n" + d.id; });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            circle
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
                //.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

            label
                .attr("x", function(d) { return d.x + d.size + 4})
                .attr("y", function(d) { return d.y;});
        }
    });
});

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
