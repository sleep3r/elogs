<script>
import * as d3 from 'd3'

export default {
  name: 'LineChart',
  template: '<svg/>',
  props: {
    points: {
      type: Array,
      required: true
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 400
    }
  },
  mounted() {
    this.render()
  },
  watch: {
    points() {
      this.render()
    }
  },
  methods: {
    render() {
      let margin = {top: 70, right: 20, bottom: 50, left: 40}
      let width = this.width - margin.left - margin.right
      let height = this.height - margin.top - margin.bottom

      let svg = d3.select(this.$el)
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)

      let parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S.%f%Z");

      var ru_RU = d3.timeFormatDefaultLocale({
        "decimal": ",",
        "thousands": "\xa0",
        "grouping": [3],
        "currency": ["", " руб."],
        "dateTime": "%A, %e %B %Y г. %X",
        "date": "%d.%m.%Y",
        "time": "%H:%M:%S",
        "periods": ["AM", "PM"],
        "days": ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"],
        "shortDays": ["вс", "пн", "вт", "ср", "чт", "пт", "сб"],
        "months": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        "shortMonths": ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июль", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    })
      // d3.formatDefaultLocale(ru_RU)

      svg.selectAll('g').remove()

      let data = this.points

      var x = d3.scaleTime()
        .rangeRound([0, width]);

      var y = d3.scaleLinear()
          .rangeRound([height, 0]);

      var line = d3.line()
          .x(function(d) { return x(parseTime(d[0])) })
          .y(function(d) { return y(d[1]) })

      let g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      x.domain(d3.extent(data, function(d) { return parseTime(d[0]) }))
      y.domain(d3.extent(data, function(d) { return d[1] }))

      g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%d %b")))
        .select(".domain")
          .remove();

      g.append("g")
          .call(d3.axisLeft(y))
        // .append("text")
        //   .attr("fill", "#000")
        //   .attr("transform", "rotate(-90)")
        //   .attr("y", 6)
        //   .attr("dy", "0.71em")
        //   .attr("text-anchor", "end")
        //   .text("Price ($)");

      g.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 1.5)
          .attr("d", line)
    }
  }
}
</script>
