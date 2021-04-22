if (document.querySelector('body').clientWidth > 1200) {
    days = 30;
    document.getElementById("options").innerHTML = `
        <option value="7">1 Week</option>
        <option value="30" selected>1 Month</option>
    `
} else {
    days = 7;
    document.getElementById("options").innerHTML = `
        <option value="7" selected>1 Week</option>
    `
}


const drawAxis = (svg, width, height, data) => {
    const today = new Date();
    const before = new Date(today.getTime() - days * 24 * 60 * 60 * 1000);

    let x = d3.scaleTime()
        .domain(data.length ? [before, today] : [])
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickFormat(e => `${e.getDate()}/${e.getMonth() + 1}`).ticks(days))
        .attr('id', 'x-axis')
        .attr('class', 'axis')
        .attr("stroke", "whitesmoke")
        .append('text')
        .attr('class', 'axis-label label-x')
        .attr("text-anchor", "end")
        .attr("x", width - 10)
        .attr("y", -10)
        .text('Date');

    let y = d3.scaleLinear()
        .domain([0, d3.max(data, function (d) {
            return d.value;
        })])
        .range([height, 0]);

    svg.append("g")
        .call(d3.axisLeft(y))
        .attr('id', 'y-axis')
        .attr('class', 'axis')
        .attr("stroke", "whitesmoke")
        .append('text')
        .attr('class', 'axis-label label-y')
        .attr("y", 8)
        .attr("dy", ".85em")
        .attr("transform", "rotate(-90)")
        .text(option);

    return [x, y];

}

const drawGrid = (svg, x, y, height, width) => {
    svg.append("g")
        .attr("class", "grid x-grid-lines")
        .attr("transform", "translate(0," + height + ")")
        .transition()
        .duration(500)
        .call(d3.axisBottom(x)
            .tickSize(-height, 0, 0)
            .tickFormat("")
        );

    svg.append("g")
        .attr("class", "grid y-grid-lines")
        .transition()
        .duration(500)
        .call(d3.axisLeft(y)
            .tickSize(-width, 0, 0)
            .tickFormat("")
        );
}

const buildGradient = (svg) => {
    const defs = svg.append("defs");
    const grad = defs
        .append('linearGradient')
        .attr('id', 'grad')
        .attr('x1', '0%')
        .attr('x2', '0%')
        .attr('y1', '0%')
        .attr('y2', '100%')
        .attr("gradientTransform", "rotate(-45)");

    const colors = [['rgb(69,128,179)', '1'], ['rgb(96,158,215)', '0']];

    grad.selectAll('stop')
        .data(colors)
        .enter()
        .append('stop')
        .style('stop-color', function (d) {
            return d[0];
        })
        .style('stop-opacity', function (d) {
            return d[1];
        })
        .attr('offset', function (d, i) {
            return 100 * (i / (colors.length - 1)) + '%';
        });
}

const drawGradient = (svg, x, y, height, data, update = false) => {
    // if(update){
    //     svg.select("#area").datum(data)
    //     .transition()
    //     .duration(2000)
    //     .attr("d", d3.area()
    //         .curve(d3.curveCatmullRom)
    //         .x(function (d) {
    //             return x(d.date);
    //         })
    //         .y0(height)
    //         .y1(function (d) {
    //             return y(d.value);
    //         })
    //     );
    //     return;
    // }
    // const area = svg.append("path");
    // area.datum(data)
    //     .transition()
    //     .duration(1000)
    //     .attr('id', 'area')
    //     .attr("fill", "url(#grad)")
    //     .attr("fill-opacity", .3)
    //     .attr("d", d3.area()
    //         .curve(d3.curveCatmullRom)
    //         .x(function (d) {
    //             return x(d.date)
    //         })
    //         .y0(height)
    //         .y1(function (d) {
    //             return y(d.value)
    //         })
    //     );
}

const drawLine = (svg, x, y, data, update = false) => {
    if (update) {
        svg.select("#line").datum(data)
            .transition()
            .duration(1500)
            .attr("d", d3.line()
                .curve(d3.curveCatmullRom)
                .x(function (d) {
                    return x(d.date);
                })
                .y(function (d) {
                    return y(d.value);
                })
            );
        return;
    }
    svg.append("path")
        .datum(data)
        .transition()
        .duration(1000)
        .attr('id', 'line')
        .attr("fill", "None")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .curve(d3.curveCatmullRom)
            .x(function (d) {
                return x(d.date)
            })
            .y(function (d) {
                return y(d.value)
            })
        );
}

const drawPoints = (svg, x, y, data) => {
    let div = d3.select("#chart").append('div')
        .attr("class", "tool-tip")
        .style("opacity", 0);

    svg.selectAll('.dots')
        .data(data)
        .enter()
        .append("circle")
        .attr('class', 'dots')
        .attr("fill", "#09e1f8")
        .attr("stroke", "none")
        .on('mouseover', (i, d) => {
            let [px, py] = d3.pointer(i);

            div.transition()
                .duration(300)
                .style('opacity', 1)

            div.text(`${option}s: ${d.value}`)
                .style('top', (py + 100) + "px")
                .style('left', (px) + "px")
        })
        .on('mouseout', (d) => {
            div.transition()
                .duration(300)
                .style('opacity', 0)

        })
        .transition()
        .duration(1000)
        .attr("cx", function (d) {
            return x(d.date)
        })
        .attr("cy", function (d) {
            return y(d.value)
        })
        .attr("r", 4)
}

const updateGraph = (svg, x, y, width, height, data) => {
    const today = new Date();
    const before = new Date(today.getTime() - days * 24 * 60 * 60 * 1000);

    svg.selectAll('.dots').remove();

    x.domain(data.length ? [before, today] : []).range([0, width]);
    svg.select("#x-axis")
        .transition()
        .duration(1200)
        .call(d3.axisBottom(x).tickFormat(e => `${e.getDate()}-${e.getMonth() + 1}`).ticks(days))

    y.domain([0, d3.max(data, function (d) {
        return d.value;
    })]);
    svg.select("#y-axis")
        .transition()
        .duration(1200)
        .call(d3.axisLeft(y));

    if (!data) {
        d3.select("#no-data").text("No Data");
        return;
    }

    svg.selectAll('.x-grid-lines')
        .transition()
        .duration(500)
        .call(d3.axisBottom(x)
            .tickSize(-height, 0, 0)
            .tickFormat("")
        );

    svg.selectAll('.y-grid-lines')
        .transition()
        .duration(500)
        .call(d3.axisLeft(y)
            .tickSize(-width, 0, 0)
            .tickFormat("")
        );

    drawGradient(svg, x, y, height, data, true);
    drawLine(svg, x, y, data, true);

    drawPoints(svg, x, y, data);
}

const constructGraph = (data) => {

    const margin = {top: 10, right: 40, bottom: 40, left: 40};

    let width = document.querySelector('body').clientWidth - document.getElementById('sidebar').clientWidth - 50;
    width -= margin.left + margin.right;
    const height = 500;

    let svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


    let [x, y] = drawAxis(svg, width, height, data);

    d3.select("svg")
        .append("g")
        .attr("transform", "translate(" + (width + margin.left + margin.right) / 2 + "," + height / 2 + ")")
        .append("text")
        .attr("text-anchor", "middle")
        .attr("id", "no-data");

    if (!data.length) {
        d3.select("#no-data").text("No Data");
        return;
    }

    drawGrid(svg, x, y, height, width);

    buildGradient(svg);
    drawGradient(svg, x, y, height, data);

    drawLine(svg, x, y, data);

    drawPoints(svg, x, y, data);

    document.getElementById("options").addEventListener('change', () => {
        days = +document.getElementById("options").value;
        fetchData()
            .then(data => {
                data.forEach(item => {
                    item.date = d3.timeParse("%Y-%m-%d")(item.date);
                    item.value = Number(item.value);
                })
                updateGraph(svg, x, y, width, height, data);
            })
            .catch(err => {
                console.log(err);
            });
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    fetchData()
        .then(data => {
            data.forEach(item => {
                item.date = d3.timeParse("%Y-%m-%d")(item.date);
                item.value = Number(item.value);
            })
            constructGraph(data);
        })
        .catch(err => {
            console.log(err);
        });
});

