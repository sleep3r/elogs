<script>
import * as d3 from 'd3'
import { map } from 'lodash'

export default {
  name: "BarChart",
  template: `<svg/>`,
  props: {
      minSizes: {
          type: Array,
          required: true
      },
      masses: {
          type: Array,
          required: true
      }
  },
  computed: {
    sizes() {
      return map(this.minSizes, s => +s) // Ensure numbers
    },
    chartData() {
      return d3.zip(this.sizes, this.masses)
    }
  },
  watch: {
    chartData() {
      this.render()
    }
  },

  mounted() {
    this.render()
  },
  methods: {
    render() {
    let margin = {top: 20, right: 20, bottom: 30, left: 40}
    let width = 800 - margin.left - margin.right
    let height = 600 - margin.top - margin.bottom

    let svg = d3.select(this.$el).attr('width', 800).attr('height', 600)

    svg.selectAll('g').remove()

    let data = this.chartData

     var x = d3.scaleLinear()
      .domain([data[0][0], data[data.length - 1][0]])
      .range([0, width]);
    
    var y = d3.scaleLinear()
    .domain([0, d3.max(data, function(d) { return d[1] })])
    .range([height, 0]);


    let g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)

    var bar = g.selectAll(".bar")
      .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d[0]) + "," + y(d[1]) + ")"; });

    bar.append("rect")
        .attr("x", 1)
        .attr("width", function(d, i) { 
          console.log('w', d, i, x(data[i][0]))
          return (i < data.length - 1 ? x(data[i + 1][0]) - x(data[i][0] ) : x(data[1][0] - data[0][0])) - 1
        })
        .attr("height", function(d) { 
          console.log('h', d, d[0])
          return height - y(d[1])
          });

    bar.append("text")
        .attr("dy", ".75em")
        .attr("y", 6)
        .attr("x", function(d, i) {
          return ((i < data.length - 1 ? x(data[i + 1][0]) - x(data[i][0] ) : x(data[1][0] - data[0][0])) / 2)
        })
        .attr("text-anchor", "middle")
        .text(function(d) { return d3.format(".2f")(d[1]) });


    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).ticks(10, ",f"))
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")

    }
  }
}
</script>

<style>
.bar rect {
  fill: steelblue;
}
.bar text {
  fill: #fff;
  font: 10px sans-serif;
}
</style>