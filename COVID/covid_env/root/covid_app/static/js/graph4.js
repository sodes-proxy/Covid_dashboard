var margin = {top: 60, right: 10, bottom: 120, left:170};
var width = 600;
var height = 400;

var svg = d3.select("#chart-area").append("svg")
	.attr("width", width + margin.right + margin.left)
	.attr("height", height + margin.top + margin.bottom);
var group= svg.append("g")
	.attr("transform","translate("+margin.left+","+margin.top+")");
var legend = group.append("g")
    .attr("transform", "translate(" + (width - 10) + "," + (height - 170) + ")");
    legend.append("g")
    .append("text")
    .attr("x", -25)
    .attr("y",-70)
    .attr("text-anchor", "end")
    .text("sectores")
	.style("font-size", "20px");

data.forEach((d) => {
    d.count = +d.count;
});
    months=data.map((d)=>{return d.sector});
    var sec = data.map((d) => {return d.sector;});
	var sectores = [...new Set(sec)];
    
    max_revenue=d3.max(data,(d)=>{return d.count});
    var x = d3.scaleBand()
	.domain(months)
	.range([0,400])
	.paddingInner(.3)
	.paddingOuter(.3);
    console.log(data);
    var y = d3.scaleLinear()
	.domain([max_revenue,0])
	.range([0,400]);
    var colors=d3.scaleOrdinal()
    .domain(months)
    .range(d3.schemeSet3);
	var revenues=group.selectAll("rect").data(data);
    revenues.enter()
        .append("rect")
	    .attr("x",(d)=>{return x(d.sector);})
	    .attr("y",(d)=>{return y(d.count);})
	    .attr("height", (d)=>{return height-y(d.count);})
        .attr("width",x.bandwidth())
	    .attr("fill",(d)=>{return colors(d.sector)});
		var bottomAxis = d3.axisBottom(x);
		group.append("g")
			.attr("class", "bottom axis")
			.attr("transform", "translate(0, " + height+ ")")
			.call(bottomAxis)
			.selectAll("text")
    		.attr("y", "30")
	    	.attr("x", "0")
    		.attr("text-anchor", "end")
        .attr("transform", "rotate(-20)");
		var leftAxis = d3.axisLeft(y)
			.ticks(11)
			.tickFormat((d)=>{return d;});
            
		group.append("g")
			.attr("class", "left-axis")
			.call(leftAxis);
		group.append("text")
			.attr("class", "x axis-label")
			.attr("x", (width / 2))
			.attr("y", height + 120)
			.style("font-size", "20px")
			.attr("text-anchor", "middle")
			.attr("transform", "translate(-120, -20)")
			.text("Sector");
		group.append("text")
			.attr("class", "y axis-label")
			.attr("x", - (height / 2))
			.attr("y", -60)
			.style("font-size", "20px")
			.attr("text-anchor", "middle")
			.attr("transform", "rotate(-90)")
			.text("Número de Personas");
            sectores.forEach((c, i) => {
                var paciente_row = legend.append("g")
                    .attr("transform", "translate(0, " + (i * 20) + ")");
        
                paciente_row.append("rect")
					.attr("x", -35)
                    .attr("y", -23)
                    .attr("width", 15)
                    .attr("height", 15)
                    .attr("fill", colors(c))
                    .attr("stroke", "white");
        
                paciente_row.append("text")
                    .attr("x", -50)
                    .attr("y", -10)
                    .attr("text-anchor", "end")
                    .text(c)
					.style("font-size", "18px");
                 });