var nowSort = "tier";

d3.selectAll(".dropdown-item").on("click", function () {
    var rank = d3.select(this).text().replace(/(\r\n|\n|\r|\s)/gm, "");
    var dropdown = d3.select("#dropdownSelect");
    dropdown.html(""); // 清空內容
    if (rank != "All") {
        dropdown.append("img")
            .attr("src", "../images/rank/Rank=" + rank + ".png")
            .attr("alt", "Rank")
            .attr("width", "25")
            .attr("height", "25")
            .attr("class", "me-1");
    }
    dropdown.append("span").text(rank);
    var position = d3.select(".nav-link.active").text().replace(/(\r\n|\n|\r|\s)/gm, "").toUpperCase();
    displayAllInfo(position, rank.toLowerCase(), nowSort);
});

d3.selectAll("#positionTab .nav-item").on("click", function () {
    var rank = d3.select("#dropdownSelect").text().replace(/(\r\n|\n|\r|\s)/gm, "").toLowerCase();
    var position = d3.select(this).text().replace(/(\r\n|\n|\r|\s)/gm, "").toUpperCase();
    displayAllInfo(position, rank, nowSort);
});

function displayChampions(position, rank, sortWith) {
    d3.selectAll("tbody").html(""); // 清空內容

    d3.csv("../data/champions/" + rank + ".csv").then(function (data) {
        if (position !== "ALL") {
            if (position === "MIDDLE") {
                position = "MID";
            } else if (position === "BOTTOM") {
                position = "ADC";
            }

            data = data.filter(function (d) {
                return d.position === position;
            });
        }

        if (sortWith === "winRate") {
            data.sort(function (a, b) {
                return b.winRate - a.winRate;
            });
        } else if (sortWith === "pickRate") {
            data.sort(function (a, b) {
                return b.pickRate - a.pickRate;
            });
        } else if (sortWith === "banRate") {
            data.sort(function (a, b) {
                return b.banRate - a.banRate;
            });
        } else {
            data.sort(function (a, b) {
                return a.tier - b.tier;
            });
        }

        var table = d3.select("#champions-table");
        var tbody = table.append("tbody");
        var rows = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr");

        var cells = rows.selectAll("td")
            .data(function (row, i) {
                return Object.values(row).slice(1).map(function (value, j) {
                    return { value: value, row: i, column: j };
                });
            })
            .enter()
            .append("td")
            .html(function (d) {
                if (d.column === 0) {
                    return d.row + 1;
                } else if (d.column === 1) {
                    // 如果是第二個 column，則插入圖片
                    var cleanedValue = d.value.replace(/[\s.'"]/g, "");
                    switch (cleanedValue) {
                        case ("RenataGlasc"): cleanedValue = "Renekton";
                        case ("Nunu&Willump"): cleanedValue = "Nunu";
                        case ("Wukong"): cleanedValue = "MonkeyKing";
                    }

                    return '<img src="../images/champion/' + cleanedValue + '.png" class="me-2" alt="' + d.value + '" width="30" height="30">' + d.value;
                } else if (d.column === 2) {
                    if (d.value === "0") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#E84057" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M6.666 15l-1.274-1.274V6.614L6.666 5.34h3.598l1.274 1.274v7.112L10.264 15H6.666zm1.12-1.54H9.13l.462-.462V7.342L9.13 6.88H7.786l-.462.462v5.656l.462.462zM12.854 15V5.34h4.802l1.26 1.274v3.654l-1.26 1.274H14.8V15h-1.946zm1.946-4.914h1.75l.42-.434V7.23l-.42-.434H14.8v3.29z"/></g></svg>'
                    } else if (d.value === "1") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#0093FF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.148 15L10.148 13.446 11.632 13.446 11.632 6.894 10.148 6.894 10.148 5.34 13.564 5.34 13.564 13.446 15.02 13.446 15.02 15z"/></g></svg>'
                    } else if (d.value === "2") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#00BBA3" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M9.165 15L9.165 10.702 10.229 9.638 12.707 9.638 13.015 9.33 13.015 7.188 12.693 6.88 11.447 6.88 11.125 7.188 11.125 8.238 9.193 8.238 9.193 6.572 10.411 5.34 13.715 5.34 14.961 6.586 14.961 10.226 13.897 11.29 11.419 11.29 11.111 11.598 11.111 13.376 14.947 13.376 14.947 15z"/></g></svg>'
                    } else if (d.value === "3") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#FFB900" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.124 15L8.892 13.768 8.892 12.046 10.838 12.046 10.838 13.11 11.244 13.516 12.644 13.516 13.05 13.11 13.05 11.318 12.588 10.842 10.068 10.842 10.068 9.288 12.588 9.288 13.05 8.826 13.05 7.258 12.644 6.852 11.244 6.852 10.838 7.258 10.838 8.28 8.892 8.28 8.892 6.572 10.124 5.34 13.764 5.34 14.996 6.558 14.996 9.036 13.988 10.044 14.996 11.066 14.996 13.782 13.778 15z"/></g></svg>'
                    } else if (d.value === "4") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#9AA4AF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M12.672 15L12.672 12.452 8.64 12.452 8.64 11.192 9.998 5.34 11.72 5.34 10.628 10.842 12.672 10.842 12.672 5.34 14.604 5.34 14.604 10.842 15.318 10.842 15.318 12.452 14.604 12.452 14.604 15z"/></g></svg>'
                    } else if (d.value === "5") {
                        return '<svg width="24" height="24"><g fill="none"><path fill="#A88A67" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.327 15L9.095 13.768 9.095 12.06 11.041 12.06 11.041 13.082 11.433 13.474 12.651 13.474 13.057 13.068 13.057 10.422 12.749 10.1 11.517 10.1 10.901 10.716 9.095 10.716 9.095 5.34 14.877 5.34 14.877 6.95 11.041 6.95 11.041 9.26 11.727 8.574 13.855 8.574 15.003 9.722 15.003 13.754 13.757 15z"/></g></svg>'
                    }
                } else if (d.column === 3) {
                    return '<img src="../images/position/' + d.value.toLowerCase() + '.svg" class="me-2" alt="' + d.value + '" width="25" height="25">';
                } else if (d.column === 4 || d.column === 5 || d.column === 6) {
                    return d.value + " %";
                }
                else {
                    return d.value;
                }
            });
    });
}

function displayBubbleChart(position, rank, sortWith) {
    d3.select("#bubble-chart-container").html("");
    d3.csv("../data/champions/" + rank + ".csv").then(function (data) {
        data = data.map(function (d) {
            d[sortWith] = +d[sortWith];
            return d;
        });
        if (position !== "ALL") {
            if (position === "MIDDLE") {
                position = "MID";
            } else if (position === "BOTTOM") {
                position = "ADC";
            }

            data = data.filter(function (d) {
                return d.position === position;
            });
        }

        var width = d3.select("#bubble-chart-container").node().getBoundingClientRect().width;
        var height = width;
        var minRadius, maxRadius;

        switch (sortWith) {
            case "tier":
                minRadius = 5;
                maxRadius = 35;
                break;
            case "winRate":
                minRadius = 10;
                maxRadius = 20;
                break;
            case "pickRate":
                minRadius = 5;
                maxRadius = 35;
                break;
            case "banRate":
                minRadius = 5;
                maxRadius = 35;
                break;
        }

        const tooltip = d3.select(".tooltip");

        const radiusScale = d3.scalePow()
            .exponent(0.68) // Controls the curvature of the scale
            .domain((sortWith == "tier") ? [d3.max(data, d => d[sortWith]), d3.min(data, d => d[sortWith])] : [d3.min(data, d => d[sortWith]), d3.max(data, d => d[sortWith])]) //0: OP, 5: Bad
            .range([minRadius, maxRadius]);

        console.log(radiusScale.domain());

        const svg = d3.select("#bubble-chart-container").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("id", "bubble-chart-svg");

        const defs = svg.append('defs');
        data.forEach((d, i) => {
            var cleannedName = d.name.replace(/[\s.'"]/g, "");
            switch (cleannedName) {
                case ("RenataGlasc"): cleannedName = "Renekton";
                case ("Nunu&Willump"): cleannedName = "Nunu";
                case ("Wukong"): cleannedName = "MonkeyKing";
            }

            defs.append('pattern')
                .attr('id', 'hero-image-' + cleannedName + '-' + i)
                .attr('patternUnits', 'objectBoundingBox')
                .attr('width', 1)
                .attr('height', 1)
                .append('image')
                .attr('xlink:href', '../images/champion/' + cleannedName + '.png')
                .attr('width', radiusScale(d[sortWith]) * 2)
                .attr('height', radiusScale(d[sortWith]) * 2)
                .attr('preserveAspectRatio', 'xMidYMid slice');
        });

        const simulation = d3.forceSimulation(data)
            .force("charge", d3.forceManyBody().strength(20 / Math.sqrt(data.length)))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => radiusScale(d[sortWith])))
            .on("tick", ticked);

        simulation.on("tick", () => {
            ticked();
            //boundingBoxForce();
        });

        function ticked() {
            const minShowRadius = 6;
            const bubbles = svg.selectAll(".bubble")
                .data(data)
                .join("circle")
                .attr("class", "bubble")
                .attr("r", d => radiusScale(d[sortWith]))
                .attr("cx", d => {
                    const radius = radiusScale(d[sortWith]);
                    return Math.max(radius, Math.min(width - radius, d.x));
                })
                .attr("cy", d => {
                    const radius = radiusScale(d[sortWith]);
                    return Math.max(radius, Math.min(height - radius, d.y));
                })
                .style("fill", function (d, i) {
                    var cleannedName = d.name.replace(/[\s.'"]/g, "");
                    switch (cleannedName) {
                        case ("RenataGlasc"): cleannedName = "Renekton";
                        case ("Nunu&Willump"): cleannedName = "Nunu";
                        case ("Wukong"): cleannedName = "MonkeyKing";
                    }

                    return "url(#hero-image-" + cleannedName + "-" + i + ")";
                })
                .style("display", d => (position == "ALL" && radiusScale(d[sortWith]) < minShowRadius) ? "none" : "block")
                .on("mouseover", (event, d) => {
                    tooltip.style("opacity", 1)
                        .html(d.name + "<br>" + sortWith + ": " + d[sortWith].toLocaleString() + (sortWith == "tier" ? "" : "%"))
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", () => tooltip.style("opacity", 0))
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
        }


        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            simulation.alphaTarget(0.1).restart();
            // Calculate the bubble's radius for the current data point
            const radius = radiusScale(event.subject[sortWith]);

            // Keep the dragged position within the bounds, accounting for the radius to prevent overlap with the border
            const newX = Math.max(radius, Math.min(width - radius, event.x));
            const newY = Math.max(radius, Math.min(height - radius, event.y));

            // Update the position for the current data point
            event.subject.fx = newX;
            event.subject.fy = newY;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

    });
}

d3.selectAll("#champions-table .hoverable").on("click", function () {
    var rank = d3.select("#dropdownSelect").text().replace(/(\r\n|\n|\r|\s)/gm, "").toLowerCase();
    var position = d3.select(".nav-link.active").text().replace(/(\r\n|\n|\r|\s)/gm, "").toUpperCase();
    if (d3.select(this).attr("id") === "tier-th") {
        nowSort = "tier";
        displayAllInfo(position, rank, "tier");
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    } else if (d3.select(this).attr("id") === "wr-th") {
        nowSort = "winRate";
        displayAllInfo(position, rank, "tier");
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    } else if (d3.select(this).attr("id") === "pr-th") {
        nowSort = "pickRate";
        displayAllInfo(position, rank, "tier");
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    } else if (d3.select(this).attr("id") === "br-th") {
        nowSort = "banRate";
        displayAllInfo(position, rank, "tier");
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    }
});

function displayAllInfo(position, rank, sortWith) {
    displayChampions(position, rank, sortWith);
    displayBubbleChart(position, rank, sortWith);
}

displayAllInfo("ALL", "all", "tier");