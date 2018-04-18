<template>
  <svg :class="{ labels, prediction }"></svg>
</template>

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
        default: 1200
      },
      height: {
        type: Number,
        default: 800
      },
      labels: {
        type: Boolean,
        default: false
      },
      prediction: {
        type: Boolean,
        default: false
      }
  },
  computed: {
    chartData() {
      return d3.zip(this.minSizes, this.masses)
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
    let margin = {top: 70, right: 20, bottom: 50, left: 40}
    let width = this.width - margin.left - margin.right
    let height = this.height - margin.top - margin.bottom

    let svg = d3.select(this.$el)
      .attr('viewBox', `0 0 ${this.width} ${this.height}`)

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

      if (this.labels) {
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
            .call(d3.axisBottom(x))
            .append("text")
              .attr("x", width - 6)
              .attr("dy", "3.5em")
              .attr("text-anchor", "end")
              .text("Размер")

          g.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y).ticks(10, ",f"))
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", "-1.75em")
              .attr("text-anchor", "end")
              .text("Фракция")
      }
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

svg.prediction .bar rect {
  fill: brown;
}

svg.labels .bar rect:hover {
  fill: rgb(28, 187, 156);
}

.bar text, .axis text {
  fill: #000;
  font: 16px sans-serif;
  font-weight: bold;
}
</style>