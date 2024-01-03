var nowSort = "tier";
var nowOrder = "desc";

var difficultyOrder = {
    "Severe": 1,
    "Hard": 2,
    "Average": 3,
    "Easy": 4
};

function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}

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
    displayAllInfo(position, rank.toLowerCase(), nowSort, nowOrder);
});

d3.selectAll("#positionTab .nav-item").on("click", function () {
    var rank = d3.select("#dropdownSelect").text().replace(/(\r\n|\n|\r|\s)/gm, "").toLowerCase();
    var position = d3.select(this).text().replace(/(\r\n|\n|\r|\s)/gm, "").toUpperCase();
    displayAllInfo(position, rank, nowSort, nowOrder);
});

function displayChampions(position, rank, sortWith, sortOrder) {
    d3.selectAll("tbody").html(""); // 清空內容

    Promise.all([
        d3.csv("../data/champions/" + rank + ".csv"),
        d3.csv("../data/championDifficulty.csv")  // 假設你的難度數據在這個文件中
    ]).then(function (files) {

        var data = files[0];
        var difficultyData = files[1];

        data.forEach(function (d) {
            var difficulty = difficultyData.find(function (dd) { return dd.championName === d.name; });
            if (difficulty) {
                d.difficulty = difficulty.difficulty;
            }
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

        if (sortWith === "winRate") {
            data.sort(function (a, b) {
                return sortOrder == "desc" ? b.winRate - a.winRate : a.winRate - b.winRate;
            });
        } else if (sortWith === "pickRate") {
            data.sort(function (a, b) {
                return sortOrder == "desc" ? b.pickRate - a.pickRate : a.pickRate - b.pickRate;
            });
        } else if (sortWith === "banRate") {
            data.sort(function (a, b) {
                return sortOrder == "desc" ? b.banRate - a.banRate : a.banRate - b.banRate;
            });
        } else if (sortWith === "difficulty") {
            data.sort(function (a, b) {
                return sortOrder == "desc" ? difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty] : difficultyOrder[b.difficulty] - difficultyOrder[a.difficulty];
            });
        }
        else {
            data.sort(function (a, b) {
                return sortOrder == "desc" ? a.tier - b.tier : b.tier - a.tier;
            });
        }

        var table = d3.select("#champions-table");
        var tbody = table.append("tbody");
        var rows = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr")
            .on("click", function (event, d) {
                window.open("champion.html?name=" + encodeURIComponent(d.name) + "&tier=" + encodeURIComponent(d.tier) + "&rank=" + encodeURIComponent(rank), "_self");
            });

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
                        return '<svg class="tier-banner-svg" tier="0" width="24" height="24"><g fill="none"><path fill="#E84057" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M6.666 15l-1.274-1.274V6.614L6.666 5.34h3.598l1.274 1.274v7.112L10.264 15H6.666zm1.12-1.54H9.13l.462-.462V7.342L9.13 6.88H7.786l-.462.462v5.656l.462.462zM12.854 15V5.34h4.802l1.26 1.274v3.654l-1.26 1.274H14.8V15h-1.946zm1.946-4.914h1.75l.42-.434V7.23l-.42-.434H14.8v3.29z"/></g></svg>'
                    } else if (d.value === "1") {
                        return '<svg class="tier-banner-svg" tier="1" width="24" height="24"><g fill="none"><path fill="#0093FF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.148 15L10.148 13.446 11.632 13.446 11.632 6.894 10.148 6.894 10.148 5.34 13.564 5.34 13.564 13.446 15.02 13.446 15.02 15z"/></g></svg>'
                    } else if (d.value === "2") {
                        return '<svg class="tier-banner-svg" tier="2" width="24" height="24"><g fill="none"><path fill="#00BBA3" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M9.165 15L9.165 10.702 10.229 9.638 12.707 9.638 13.015 9.33 13.015 7.188 12.693 6.88 11.447 6.88 11.125 7.188 11.125 8.238 9.193 8.238 9.193 6.572 10.411 5.34 13.715 5.34 14.961 6.586 14.961 10.226 13.897 11.29 11.419 11.29 11.111 11.598 11.111 13.376 14.947 13.376 14.947 15z"/></g></svg>'
                    } else if (d.value === "3") {
                        return '<svg class="tier-banner-svg" tier="3" width="24" height="24"><g fill="none"><path fill="#FFB900" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.124 15L8.892 13.768 8.892 12.046 10.838 12.046 10.838 13.11 11.244 13.516 12.644 13.516 13.05 13.11 13.05 11.318 12.588 10.842 10.068 10.842 10.068 9.288 12.588 9.288 13.05 8.826 13.05 7.258 12.644 6.852 11.244 6.852 10.838 7.258 10.838 8.28 8.892 8.28 8.892 6.572 10.124 5.34 13.764 5.34 14.996 6.558 14.996 9.036 13.988 10.044 14.996 11.066 14.996 13.782 13.778 15z"/></g></svg>'
                    } else if (d.value === "4") {
                        return '<svg class="tier-banner-svg" tier="4" width="24" height="24"><g fill="none"><path fill="#9AA4AF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M12.672 15L12.672 12.452 8.64 12.452 8.64 11.192 9.998 5.34 11.72 5.34 10.628 10.842 12.672 10.842 12.672 5.34 14.604 5.34 14.604 10.842 15.318 10.842 15.318 12.452 14.604 12.452 14.604 15z"/></g></svg>'
                    } else if (d.value === "5") {
                        return '<svg class="tier-banner-svg" tier="5" width="24" height="24"><g fill="none"><path fill="#A88A67" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.327 15L9.095 13.768 9.095 12.06 11.041 12.06 11.041 13.082 11.433 13.474 12.651 13.474 13.057 13.068 13.057 10.422 12.749 10.1 11.517 10.1 10.901 10.716 9.095 10.716 9.095 5.34 14.877 5.34 14.877 6.95 11.041 6.95 11.041 9.26 11.727 8.574 13.855 8.574 15.003 9.722 15.003 13.754 13.757 15z"/></g></svg>'
                    }
                } else if (d.column === 3) {
                    return '<img class="position-svg" src="../images/position/' + d.value.toLowerCase() + '.svg" class="me-2" alt="' + d.value + '" width="25" height="25">';
                } else if (d.column === 4 || d.column === 5 || d.column === 6) {
                    return d.value + " %";
                } else if (d.column === 7) {
                    if (d.value === "Severe") {
                        return '<svg class="difficulty-banner-svg" difficulty="Severe" width="24" height="24"><g fill="none"><path fill="rgb(191, 9, 13)" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M 10.327 15 L 9.095 13.768 L 9.095 12.06 L 11.041 12.06 L 11.041 13.082 L 11.433 13.474 L 12.651 13.474 L 13.057 13.068 L 13.079 12.02 L 9.103 8.959 L 9.112 6.041 L 10.369 5.004 L 13.762 4.988 L 15.097 6.041 L 15.097 8.068 L 13.071 8.068 L 13.086 6.984 L 12.694 6.607 L 11.405 6.607 L 10.997 7.031 L 11.002 8.078 L 14.98 11.052 L 14.98 14.009 L 13.757 15 z"/></g></svg>'
                    } else if (d.value === "Hard") {
                        return '<svg class="difficulty-banner-svg" difficulty="Hard" width="24" height="24"><g fill="none"><path fill="rgb(253, 114, 0)" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M 10.997 9.001 L 13.038 9.001 L 13.011 5.002 L 15.01 5.016 L 15.01 14.986 L 12.997 15 L 13.025 11.014 L 10.983 11 L 10.997 14.958 L 9.011 14.944 L 9.053 5.016 L 10.997 5.002 z"/></g></svg>'
                    } else if (d.value === "Average") {
                        return '<svg class="difficulty-banner-svg" difficulty="Average" width="24" height="24"><g fill="none"><path fill="rgb(22, 158, 211)" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M 13.245 11.003 L 11.025 11 L 10.997 15.014 L 9.095 14.986 L 9.112 6.041 L 10.233 4.974 L 13.762 4.988 L 15.038 6.015 L 15.055 14.956 L 13.05 14.956 L 13.086 6.984 L 12.694 6.607 L 11.405 6.607 L 10.997 7.031 L 11.011 9.029 L 13.287 8.999 z"/></g></svg>'
                    } else if (d.value === "Easy") {
                        return '<svg class="difficulty-banner-svg" difficulty="Easy" width="24" height="24"><g fill="none"><path fill="rgb(150, 150, 148)" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M 14.983 15 L 8.998 15.027 L 9.039 5.029 L 15.01 5.016 L 15.01 6.974 L 10.997 6.987 L 11.011 9.001 L 15.01 9.001 L 14.996 11 L 10.997 10.987 L 11.011 12.972 L 14.983 12.972 z"/></g></svg>'
                    }
                }
                else {
                    return d.value;
                }
            });

        d3.selectAll(".tier-banner-svg").on("mouseover", function (event, d) {
            tier = this.attributes.tier.value;
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 1).html("Tier " + tier)
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        }).on("mouseout", function () {
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 0);
        });

        d3.selectAll(".difficulty-banner-svg").on("mouseover", function (event, d) {
            difficulty = this.attributes.difficulty.value;
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 1).html(difficulty)
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        }).on("mouseout", function () {
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 0);
        });

        d3.selectAll(".position-svg").on("mouseover", function (event, d) {
            position = this.attributes.alt.value;
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 1).html(position)
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        }).on("mouseout", function () {
            var tooltip = d3.select(".tooltip");
            tooltip.style("opacity", 0);
        });
    });
}

function displayBubbleChart(position, rank, sortWith, sortOrder) {
    d3.select("#bubble-chart-container").html("");
    Promise.all([
        d3.csv("../data/champions/" + rank + ".csv"),
        d3.csv("../data/championDifficulty.csv")
    ]).then(function (files) {

        var data = files[0];
        var difficultyData = files[1];

        data.forEach(function (d) {
            var difficulty = difficultyData.find(function (dd) { return dd.championName === d.name; });
            if (difficulty) {
                d.difficulty = difficulty.difficulty;
            }
        });

        data = data.map(function (d) {
            if (sortWith === "difficulty") {
                d[sortWith] = difficultyOrder[d[sortWith]];
            } else {
                d[sortWith] = +d[sortWith];
            }
            return d;
        });

        console.log(data);

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
                minRadius = 10;
                maxRadius = 35;
                break;
            case "banRate":
                minRadius = 10;
                maxRadius = 45;
                break;
            case "difficulty":
                minRadius = 10;
                maxRadius = 25;
                break;
            default:
                minRadius = 5;
                maxRadius = 35;
                break;
        }

        if (position != "ALL") {
            minRadius = minRadius * 1.4;
            maxRadius = maxRadius * 1.4;
        }

        if ((sortWith == "pickRate" || sortWith == "banRate") && (sortOrder == "asc")) {
            minRadius = 5
            maxRadius = 20
        }

        const tooltip = d3.select(".tooltip");

        const radiusScale = d3.scalePow()
            .exponent(0.68) // Controls the curvature of the scale
            .domain(sortOrder == "desc" ?
                (sortWith == "tier" || sortWith == "difficulty") ? [d3.max(data, d => d[sortWith]), d3.min(data, d => d[sortWith])] : [d3.min(data, d => d[sortWith]), d3.max(data, d => d[sortWith])] :
                (sortWith == "tier" || sortWith == "difficulty") ? [d3.min(data, d => d[sortWith]), d3.max(data, d => d[sortWith])] : [d3.max(data, d => d[sortWith]), d3.min(data, d => d[sortWith])]
            )
            .range([minRadius, maxRadius]);

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
            boundingBoxForce();
        });

        function ticked() {
            const minShowRadius = 7;
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
                        .html(d.name + "<br>" + sortWith + ": " + (sortWith == "difficulty" ? getKeyByValue(difficultyOrder, d[sortWith]) : d[sortWith].toLocaleString()) + (sortWith == "tier" || sortWith == "difficulty" ? "" : "%"))
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", () => tooltip.style("opacity", 0))
                .on("click", function (event, d) {
                    rank = d3.select("#dropdownSelect").text().replace(/(\r\n|\n|\r|\s)/gm, "").toLowerCase();
                    window.open("champion.html?name=" + encodeURIComponent(d.name) + "&tier=" + encodeURIComponent(d.tier) + "&rank=" + encodeURIComponent(rank), "_self");
                })
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

            tooltip.style("opacity", 0);
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        function boundingBoxForce() {
            for (let node of simulation.nodes()) {
                node.x = Math.max(radiusScale(node[sortWith]), Math.min(width - radiusScale(node[sortWith]), node.x));
                node.y = Math.max(radiusScale(node[sortWith]), Math.min(height - radiusScale(node[sortWith]), node.y));
            }
        }

    });
}

d3.selectAll("#champions-table .hoverable").on("click", function () {
    var rank = d3.select("#dropdownSelect").text().replace(/(\r\n|\n|\r|\s)/gm, "").toLowerCase();
    var position = d3.select(".nav-link.active").text().replace(/(\r\n|\n|\r|\s)/gm, "").toUpperCase();
    if (d3.select(this).attr("id") === "tier-th") {
        if (nowSort === "tier") {
            nowOrder = nowOrder === "desc" ? "asc" : "desc";
        } else {
            nowOrder = "desc";
        }
        nowSort = "tier";
        displayAllInfo(position, rank, "tier", nowOrder);
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);

        console.log(nowOrder)
    } else if (d3.select(this).attr("id") === "wr-th") {
        if (nowSort === "winRate") {
            nowOrder = nowOrder === "desc" ? "asc" : "desc";
        } else {
            nowOrder = "desc";
        }
        nowSort = "winRate";
        displayAllInfo(position, rank, "winRate", nowOrder);
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
        console.log(nowOrder)
    } else if (d3.select(this).attr("id") === "pr-th") {
        if (nowSort === "pickRate") {
            nowOrder = nowOrder === "desc" ? "asc" : "desc";
        } else {
            nowOrder = "desc";
        }
        nowSort = "pickRate";
        displayAllInfo(position, rank, "pickRate", nowOrder);
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    } else if (d3.select(this).attr("id") === "br-th") {
        if (nowSort === "banRate") {
            nowOrder = nowOrder === "desc" ? "asc" : "desc";
        } else {
            nowOrder = "desc";
        }
        nowSort = "banRate";
        displayAllInfo(position, rank, "banRate", nowOrder);
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    } else if (d3.select(this).attr("id") === "df-th") {
        if (nowSort === "difficulty") {
            nowOrder = nowOrder === "desc" ? "asc" : "desc";
        } else {
            nowOrder = "desc";
        }
        nowSort = "difficulty";
        displayAllInfo(position, rank, "difficulty", nowOrder);
        d3.selectAll(".nowSort").classed("nowSort", false);
        d3.select(this).classed("nowSort", true);
    }
});

function displayAllInfo(position, rank, sortWith, sortOrder) {
    displayChampions(position, rank, sortWith, sortOrder);
    displayBubbleChart(position, rank, sortWith, sortOrder);
}

displayAllInfo("ALL", "all", "tier", "desc");