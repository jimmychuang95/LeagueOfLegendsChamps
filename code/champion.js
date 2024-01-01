const params = new URLSearchParams(window.location.search);
const name = params.get("name");
const tier = params.get("tier");
var winRate
var pickRate
var banRate
var nowRank = params.get("rank");

var cleannedName = name.replace(/[\s.'"]/g, "");
switch (cleannedName) {
    case ("RenataGlasc"): cleannedName = "Renata";
    case ("Nunu&Willump"): cleannedName = "Nunu";
    case ("Wukong"): cleannedName = "MonkeyKing";
}
var lowerName = cleannedName.toLowerCase();

var dropdown = d3.select("#dropdownSelect");
dropdown.html("");
if (nowRank != "all") {
    dropdown.append("img")
        .attr("src", "../images/rank/Rank=" + nowRank + ".png")
        .attr("alt", "Rank")
        .attr("width", "25")
        .attr("height", "25")
        .attr("class", "me-1");
}
dropdown.append("span").text((nowRank == "all") ? "All" : nowRank);

d3.selectAll(".dropdown-item").on("click", function () {

    var rank = d3.select(this).text().replace(/(\r\n|\n|\r|\s)/gm, "");
    nowRank = rank;
    displayRate();
    
    dropdown = d3.select("#dropdownSelect");
    dropdown.html("");
    if (rank != "All") {
        dropdown.append("img")
            .attr("src", "../images/rank/Rank=" + rank + ".png")
            .attr("alt", "Rank")
            .attr("width", "25")
            .attr("height", "25")
            .attr("class", "me-1");
    }
    dropdown.append("span").text(rank);
});

d3.select(".image-box")
    .append("img")
    .attr("src", `../images/champion/${cleannedName}.png`)
    .attr("class", "champion-image")
    .attr("alt", `${name} image`)
    .attr("width", "90px")
    .attr("height", "90px");

d3.select(".tier-banner")
    .append("svg")
    .attr("width", "24px")
    .attr("height", "24px")
    .html(function (d) {
        if (tier === "0") {
            return '<g fill="none"><path fill="#E84057" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M6.666 15l-1.274-1.274V6.614L6.666 5.34h3.598l1.274 1.274v7.112L10.264 15H6.666zm1.12-1.54H9.13l.462-.462V7.342L9.13 6.88H7.786l-.462.462v5.656l.462.462zM12.854 15V5.34h4.802l1.26 1.274v3.654l-1.26 1.274H14.8V15h-1.946zm1.946-4.914h1.75l.42-.434V7.23l-.42-.434H14.8v3.29z"/></g>'
        } else if (tier === "1") {
            return '<g fill="none"><path fill="#0093FF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.148 15L10.148 13.446 11.632 13.446 11.632 6.894 10.148 6.894 10.148 5.34 13.564 5.34 13.564 13.446 15.02 13.446 15.02 15z"/></g>'
        } else if (tier === "2") {
            return '<g fill="none"><path fill="#00BBA3" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M9.165 15L9.165 10.702 10.229 9.638 12.707 9.638 13.015 9.33 13.015 7.188 12.693 6.88 11.447 6.88 11.125 7.188 11.125 8.238 9.193 8.238 9.193 6.572 10.411 5.34 13.715 5.34 14.961 6.586 14.961 10.226 13.897 11.29 11.419 11.29 11.111 11.598 11.111 13.376 14.947 13.376 14.947 15z"/></g>'
        } else if (tier === "3") {
            return '<g fill="none"><path fill="#FFB900" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.124 15L8.892 13.768 8.892 12.046 10.838 12.046 10.838 13.11 11.244 13.516 12.644 13.516 13.05 13.11 13.05 11.318 12.588 10.842 10.068 10.842 10.068 9.288 12.588 9.288 13.05 8.826 13.05 7.258 12.644 6.852 11.244 6.852 10.838 7.258 10.838 8.28 8.892 8.28 8.892 6.572 10.124 5.34 13.764 5.34 14.996 6.558 14.996 9.036 13.988 10.044 14.996 11.066 14.996 13.782 13.778 15z"/></g>'
        } else if (tier === "4") {
            return '<g fill="none"><path fill="#9AA4AF" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M12.672 15L12.672 12.452 8.64 12.452 8.64 11.192 9.998 5.34 11.72 5.34 10.628 10.842 12.672 10.842 12.672 5.34 14.604 5.34 14.604 10.842 15.318 10.842 15.318 12.452 14.604 12.452 14.604 15z"/></g>'
        } else if (tier === "5") {
            return '<g fill="none"><path fill="#A88A67" d="M2 0L22 0 22 18.056 12 23 2 18.056z"/><path fill="#FFF" d="M10.327 15L9.095 13.768 9.095 12.06 11.041 12.06 11.041 13.082 11.433 13.474 12.651 13.474 13.057 13.068 13.057 10.422 12.749 10.1 11.517 10.1 10.901 10.716 9.095 10.716 9.095 5.34 14.877 5.34 14.877 6.95 11.041 6.95 11.041 9.26 11.727 8.574 13.855 8.574 15.003 9.722 15.003 13.754 13.757 15z"/></g>'
        }
    })

d3.select(".champion-name-info").text(name);

d3.select(".tier-info").text("Tier " + tier);

d3.select(".skill-info-p")
    .append("img")
    .attr("src", `../images/passive/${cleannedName}P.png`)
    .attr("class", "skill-image me-2 rounded")
    .attr("alt", `${cleannedName}P`)
    .attr("width", "33px")
    .attr("height", "33px")

d3.select(".skill-info-q")
    .append("img")
    .attr("src", `../images/spell/${cleannedName}Q.png`)
    .attr("class", "skill-image me-2 rounded")
    .attr("alt", `${cleannedName}Q`)
    .attr("width", "33px")
    .attr("height", "33px")

d3.select(".skill-info-w")
    .append("img")
    .attr("src", `../images/spell/${cleannedName}W.png`)
    .attr("class", "skill-image me-2 rounded")
    .attr("alt", `${cleannedName}W`)
    .attr("width", "33px")
    .attr("height", "33px")

d3.select(".skill-info-e")
    .append("img")
    .attr("src", `../images/spell/${cleannedName}E.png`)
    .attr("class", "skill-image me-2 rounded")
    .attr("alt", `${cleannedName}E`)
    .attr("width", "33px")
    .attr("height", "33px")

d3.select(".skill-info-r")
    .append("img")
    .attr("src", `../images/spell/${cleannedName}R.png`)
    .attr("class", "skill-image me-2 rounded")
    .attr("alt", `${cleannedName}R`)
    .attr("width", "33px")
    .attr("height", "33px")


const skillTooltip = d3.select(".skill-tooltip");

d3.csv("../data/champion_abilities.csv").then(function (data) {
    data = data.map(function (d) {
        d.Champion = d.Champion.toLowerCase();
        return d;
    });
    const abilities = data;

    d3.selectAll(".skill-image")
        .on("mouseover", function (event, d) {
            const ability = abilities.filter(function (d) {
                return d.Champion == lowerName;
            });

            const hoverAbility = this.alt.split(cleannedName)[1];
            console.log(this.alt);

            skillTooltip.style("opacity", 1)
                .style("left", event.pageX + "px")
                .style("top", event.pageY + "px")
                .html(`
                    <div class="mb-2"><strong>${ability[0][hoverAbility + "Name"]}</strong></div>
                    <div class="lh-base">${ability[0][hoverAbility + "Description"]}</div>
                `);
        })
        .on("mouseout", function () {
            skillTooltip.style("opacity", 0);
        });
});

function displayRate() {

    d3.csv("../data/champions/" + nowRank + ".csv").then(function (data) {

        data = data.filter(function (d) {
            return d.name == name;
        });
        data.sort(function (a, b) {
            return b.pickRate - a.pickRate;
        });
        winRate = data[0].winRate;
        pickRate = data[0].pickRate;
        banRate = data[0].banRate;

        d3.select(".win-rate-text-span").select("strong").text(winRate + "%");
        d3.select(".pick-rate-text-span").select("strong").text(pickRate + "%");
        d3.select(".ban-rate-text-span").select("strong").text(banRate + "%");

        var winRateGradient = 100 - winRate;
        var pickRateGradient = 100 - pickRate;
        var banRateGradient = 100 - banRate;

        d3.select(".win-rate-bar").attr("style", "border-image: linear-gradient(to bottom, #28282F " + winRateGradient + "%, #62d979 " + winRateGradient + "%) 1;")
        d3.select(".pick-rate-bar").attr("style", "border-image: linear-gradient(to bottom, #28282F " + pickRateGradient + "%, #51b9ed " + pickRateGradient + "%) 1;")
        d3.select(".ban-rate-bar").attr("style", "border-image: linear-gradient(to bottom, #28282F " + banRateGradient + "%, #c22760 " + banRateGradient + "%) 1;")

    });
}

displayRate();
