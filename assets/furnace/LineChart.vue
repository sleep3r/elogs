<template>
  <div>
    <div class="filters-box">
      <div 
        class="filters" 
        @click="setFilters('day')">Д</div>
      <div 
        class="filters" 
        @click="setFilters('week')">Н</div>
      <div 
        class="filters" 
        @click="setFilters('month')">М</div>
      <div 
        class="filters" 
        @click="setFilters('year')">Г</div>
      <div 
        class="filters" 
        @click="setFilters()">Все</div>

      <div style="float:right;">
        <datetime
          input-class="form-control input-sm"
          v-model="date_from"
          placeholder="От"
          type="datetime"
          input-format="DD.MM.YYYY HH:mm"
          moment-locale="ru" />

        <datetime
          input-class="form-control input-sm"
          v-model="date_to"
          placeholder="До"
          type="datetime"
          input-format="DD.MM.YYYY HH:mm"
          moment-locale="ru" />
      </div>
    </div>    
    <svg class="line-chart">
      <defs>
        <linearGradient id="gradBlue" x1="0%" y1="100%" x2="0%" y2="0%">
          <stop offset="0%" style="stop-color:rgba(135,123,237,1);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgba(26,7,135,1);stop-opacity:1" />
        </linearGradient>
        <linearGradient id="gradOrange" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
        </linearGradient>
      </defs>
    </svg>
  </div>
</template>


<script>
import * as d3 from 'd3'
import filter from 'lodash/filter'

export default {
  name: 'LineChart',
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
  data() {
    return {
      filter_from: 0,
      filter_to: 0
    }
  },
  computed: {
    orderedPoints() {
      return _.orderBy(this.points, o => o[0])
    },
    filteredPoints() {
      return filter(this.orderedPoints, d => {
        return d[0] * 1000 >= this.filter_from 
            && d[0] * 1000 <= this.filter_to
      })
    },
    date_from: {
      get() {
        return new Date(this.filter_from).toISOString()
      },
      set(val) {
        this.filter_from = +moment(val)
      }
    },
    date_to: {
      get() {
        return new Date(this.filter_to).toISOString()
      },
      set(val) {
        this.filter_to = +moment(val)
      }
    }
  },
  mounted() {
    this.setFilters()
  },
  watch: {
    filteredPoints() {
      this.render(this.filteredPoints)
    }
  },
  methods: {
    setFilters(from, to) {
      switch (from) {
        case 'day':
          from = +moment().subtract(1, 'days')
          break
        case 'week':
          from = +moment().subtract(1, 'weeks')
          break
        case 'month':
          from = +moment().subtract(1, 'months')
          break
        case 'year':
          from = +moment().subtract(1, 'years')
          break
      }

      this.filter_from = from || d3.min(this.points, d => d[0] * 1000)
      this.filter_to = to || Date.now()
    },
    render(data) {
      let margin = {top: 20, right: 20, bottom: 50, left: 40}
      let width = this.width - margin.left - margin.right
      let height = this.height - margin.top - margin.bottom

      let svg = d3.select(this.$el).select('.line-chart')
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)

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
      svg.selectAll('g').remove()

      var x = d3.scaleTime()
        .rangeRound([0, width]);

      var y = d3.scaleLinear()
          .rangeRound([height, 0]);

      var line = d3.line()
          .x(function(d) { return x(d[0] * 1000) })
          .y(function(d) { return y(d[1]) })

      let g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      x.domain(d3.extent(data, function(d) { return d[0] * 1000 }))
      y.domain(d3.extent(data, function(d) { return d[1] }))

      g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%d %b")))
        .select(".domain")
          .remove();

      g.append("g").call(d3.axisLeft(y))

      g.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "url('#gradBlue')")
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 1.5)
          .attr("stroke-opacity", 0.5)
          .attr("d", line)
    }
  }
}
</script>

<style lang="scss">
  div.filters {
    cursor: pointer;
    display: inline-block;
    background-color: #efefef;
    width: 2em;
    text-align: center;

    &:hover {
     background-color: #f4f4f4;
    }
  }
</style>
