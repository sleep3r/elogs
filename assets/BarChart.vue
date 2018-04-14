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
      },
      width: {
        type: Number,
        default: 800
      },
      height: {
        type: Number,
        default: 600
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
    let margin = {top: 70, right: 20, bottom: 30, left: 40}
    let width = this.width - margin.left - margin.right
    let height = this.height - margin.top - margin.bottom

    let svg = d3.select(this.$el)
      .attr('viewBox', `0 0 ${this.width} ${this.height}`)
    // .attr('width', this.width).attr('height', this.height)

    svg.selectAll('g').remove()

    let data = this.chartData

     var x = d3.scaleLinear()
      .domain([data[0][0], data[data.length - 1][0] * (data.length + 1)/(data.length) ])
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
        .attr("x", 3)
        .attr("width", function(d, i) { 
          return (i < data.length - 1 
          ? x(data[i + 1][0]) - x(data[i][0])
          : x(data[data.length - 1][0] / data.length)
          ) - 3
        })
        .attr("height", function(d) { return height - y(d[1]) })

    bar.append("text")
        .attr("dy", "-.75em")
        .attr("y", 0)
        .attr("x", function(d, i) {
          return ((i < data.length - 1 
          ? x(data[i + 1][0]) - x(data[i][0] ) 
          : x(data[data.length - 1][0] / data.length)
          ) / 2)
        })
        .attr("text-anchor", "middle")
        .text(function(d) { return d3.format(".2f")(d[1]) })


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

svg {
  width: 100%;
  height: 100%;
}

.bar rect {
  fill: steelblue;
}

.bar rect:hover {
  fill: rgb(28, 187, 156);
}

.bar text {
  fill: #000;
  font: 10px sans-serif;
  font-weight: bold;
}
</style>