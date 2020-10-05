'use strict';

function getForceLayoutElement(nodes, links, width, height) {
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height]);

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody().strength(-350))
        .force("center", d3.forceCenter(width / 4, height / 2));

    const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line");

    const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter().append("g")

    const circles = node.append("circle")
        .attr("r", 3)
        .attr("fill", "cadetblue")
        .attr("stroke", "white")
        .attr("stroke-width", "1")
        .call(d3.drag()
            .on("start", function dragstarted(d) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on("drag", function dragged(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            })
            .on("end", function dragended(d) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
        }));
    
    const labels = node.append("text")
        .text(function(d) {
            return d.id;
        })
        .attr('x', 6)
        .attr('y', 3)
        .attr("class", "node-text");
    
    node.append("title")
        .text(function(d) { return d.id; });
    
    simulation
        .nodes(nodes)
        .on("tick", () => {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        
            node.attr("transform", function(d) {
                  return "translate(" + d.x + "," + d.y + ")";
                })
          });

    simulation.force("link").links(links);

    return svg.node();
}
  


window.addEventListener('load', function() {
    const width  = 400,
          height = 200;
    const G = {"directed":true,"multigraph":false,"graph":{},"nodes":[{"id":"ICD-10-CM"},{"id":"Certain infectious and parasitic diseases"},{"id":"Neoplasms"},{"id":"Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism"},{"id":"Endocrine, nutritional and metabolic diseases"},{"id":"Mental, Behavioral and Neurodevelopmental disorders"},{"id":"Diseases of the nervous system"},{"id":"Diseases of the eye and adnexa"},{"id":"Diseases of the ear and mastoid process"},{"id":"Diseases of the circulatory system"},{"id":"Diseases of the respiratory system"},{"id":"Diseases of the digestive system"},{"id":"Diseases of the skin and subcutaneous tissue"},{"id":"Diseases of the musculoskeletal system and connective tissue"},{"id":"Diseases of the genitourinary system"},{"id":"Pregnancy, childbirth and the puerperium"},{"id":"Certain conditions originating in the perinatal period"},{"id":"Congenital malformations, deformations and chromosomal abnormalities"},{"id":"Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"},{"id":"Injury, poisoning and certain other consequences of external causes"},{"id":"External causes of morbidity"},{"id":"Factors influencing health status and contact with health services"}],"links":[{"source":"ICD-10-CM","target":"Certain infectious and parasitic diseases"},{"source":"ICD-10-CM","target":"Neoplasms"},{"source":"ICD-10-CM","target":"Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism"},{"source":"ICD-10-CM","target":"Endocrine, nutritional and metabolic diseases"},{"source":"ICD-10-CM","target":"Mental, Behavioral and Neurodevelopmental disorders"},{"source":"ICD-10-CM","target":"Diseases of the nervous system"},{"source":"ICD-10-CM","target":"Diseases of the eye and adnexa"},{"source":"ICD-10-CM","target":"Diseases of the ear and mastoid process"},{"source":"ICD-10-CM","target":"Diseases of the circulatory system"},{"source":"ICD-10-CM","target":"Diseases of the respiratory system"},{"source":"ICD-10-CM","target":"Diseases of the digestive system"},{"source":"ICD-10-CM","target":"Diseases of the skin and subcutaneous tissue"},{"source":"ICD-10-CM","target":"Diseases of the musculoskeletal system and connective tissue"},{"source":"ICD-10-CM","target":"Diseases of the genitourinary system"},{"source":"ICD-10-CM","target":"Pregnancy, childbirth and the puerperium"},{"source":"ICD-10-CM","target":"Certain conditions originating in the perinatal period"},{"source":"ICD-10-CM","target":"Congenital malformations, deformations and chromosomal abnormalities"},{"source":"ICD-10-CM","target":"Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"},{"source":"ICD-10-CM","target":"Injury, poisoning and certain other consequences of external causes"},{"source":"ICD-10-CM","target":"External causes of morbidity"},{"source":"ICD-10-CM","target":"Factors influencing health status and contact with health services"}]};
    const svgElem = getForceLayoutElement(G.nodes, G.links, width, height);
    const svgContainer = document.getElementById("svgContainer");
    svgContainer.appendChild(svgElem);
});

