```{raw} html

    <div id="vizContainer">
        <style>
        circle { fill: cadetblue; }
        line { stroke: #ccc; }
        </style>
        <div id="content">
            <svg width="400" height="300">
                <g class="links"></g>
                <g class="nodes"></g>
            </svg>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.2.2/d3.min.js"></script>
        <script>
        var width = 400, height = 300

        var G = {"directed": true, "multigraph": false, "graph": {}, "nodes": [{"id": "ICD9"}, {"id": "Diseases Of The Musculoskeletal System And Connective Tissue"}, {"id": "Diseases Of The Skin And Subcutaneous Tissue"}, {"id": "Congenital Anomalies"}, {"id": "Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders"}, {"id": "Injury And Poisoning"}, {"id": "Neoplasms"}, {"id": "Diseases Of The Genitourinary System"}, {"id": "Diseases Of The Digestive System"}, {"id": "Symptoms, Signs, And Ill-Defined Conditions"}, {"id": "Diseases Of The Nervous System And Sense Organs"}, {"id": "Supplementary Classification Of Factors Influencing Health Status And Contact With Health Services"}, {"id": "Diseases Of The Circulatory System"}], "links": [{"source": "ICD9", "target": "Diseases Of The Musculoskeletal System And Connective Tissue"}, {"source": "ICD9", "target": "Diseases Of The Skin And Subcutaneous Tissue"}, {"source": "ICD9", "target": "Congenital Anomalies"}, {"source": "ICD9", "target": "Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders"}, {"source": "ICD9", "target": "Injury And Poisoning"}, {"source": "ICD9", "target": "Neoplasms"}, {"source": "ICD9", "target": "Diseases Of The Genitourinary System"}, {"source": "ICD9", "target": "Diseases Of The Digestive System"}, {"source": "ICD9", "target": "Symptoms, Signs, And Ill-Defined Conditions"}, {"source": "ICD9", "target": "Diseases Of The Nervous System And Sense Organs"}, {"source": "ICD9", "target": "Supplementary Classification Of Factors Influencing Health Status And Contact With Health Services"}, {"source": "ICD9", "target": "Diseases Of The Circulatory System"}]};
        var nodesIdxs = Object.keys(G.nodes).map(key => G.nodes[key].id);
        var nodes = nodesIdxs.map(x => ({name: x}));
        var links = G.links.map(link => ({
            source: nodesIdxs.indexOf(link.source),
            target: nodesIdxs.indexOf(link.target)
        }));

        var simulation = d3.forceSimulation(nodes)
            .force('charge', d3.forceManyBody().strength(-100))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('link', d3.forceLink().links(links))
            .on('tick', ticked);

        function updateLinks() {
            var u = d3.select('.links')
                .selectAll('line')
                .data(links)

            u.enter()
                .append('line')
                .merge(u)
                .attr('x1', function(d) {
                    return d.source.x
                })
                .attr('y1', function(d) {
                    return d.source.y
                })
                .attr('x2', function(d) {
                    return d.target.x
                })
                .attr('y2', function(d) {
                    return d.target.y
                })

                u.exit().remove()
        }

        function updateNodes() {
            u = d3.select('.nodes')
                .selectAll('text')
                .data(nodes)

            u.enter()
                .append('text')
                .text(function(d) {
                    return d.name
                })
                .append('circle')
                .attr('r', 5)
                .merge(u)
                .attr('x', function(d) {
                    return d.x
                })
                .attr('y', function(d) {
                    return d.y
                })
                .attr('dy', function(d) {
                    return 5
                })

            u.exit().remove()
        }

        function ticked() {
            updateLinks()
            updateNodes()
        }
    </script>
    </div>
```