'use strict';

function getForceLayoutElement(nodes, links, width, height) {
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height]);

    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 3)
        .attr("fill", "cadetblue")
        .call(drag(simulation));

    const labels = node.append("text")
        .text(d => d.id)
        .attr('x', 6)
        .attr('y', 3);  

    node.append("title")
        .text(d => d.id);

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });

    // invalidation.then(() => simulation.stop());

    return svg.node();
}

function drag(simulation) {
  
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }
    
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
    
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

window.addEventListener('load', function() {
    const width  = 400,
          height = 200;
    const G = {"directed": true, "multigraph": false, "graph": {}, "nodes": [{"id": "ICD9"}, {"id": "Diseases Of The Musculoskeletal System And Connective Tissue"}, {"id": "Diseases Of The Skin And Subcutaneous Tissue"}, {"id": "Congenital Anomalies"}, {"id": "Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders"}, {"id": "Injury And Poisoning"}, {"id": "Neoplasms"}, {"id": "Diseases Of The Genitourinary System"}, {"id": "Diseases Of The Digestive System"}, {"id": "Symptoms, Signs, And Ill-Defined Conditions"}, {"id": "Diseases Of The Nervous System And Sense Organs"}, {"id": "Supplementary Classification Of Factors Influencing Health Status And Contact With Health Services"}, {"id": "Diseases Of The Circulatory System"}], "links": [{"source": "ICD9", "target": "Diseases Of The Musculoskeletal System And Connective Tissue"}, {"source": "ICD9", "target": "Diseases Of The Skin And Subcutaneous Tissue"}, {"source": "ICD9", "target": "Congenital Anomalies"}, {"source": "ICD9", "target": "Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders"}, {"source": "ICD9", "target": "Injury And Poisoning"}, {"source": "ICD9", "target": "Neoplasms"}, {"source": "ICD9", "target": "Diseases Of The Genitourinary System"}, {"source": "ICD9", "target": "Diseases Of The Digestive System"}, {"source": "ICD9", "target": "Symptoms, Signs, And Ill-Defined Conditions"}, {"source": "ICD9", "target": "Diseases Of The Nervous System And Sense Organs"}, {"source": "ICD9", "target": "Supplementary Classification Of Factors Influencing Health Status And Contact With Health Services"}, {"source": "ICD9", "target": "Diseases Of The Circulatory System"}]};
    const svgElem = getForceLayoutElement(G.nodes, G.links, width, height);
    const svgContainer = document.getElementById("svgContainer");
    svgContainer.appendChild(svgElem);
});

