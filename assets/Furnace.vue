<template>
    <div class="x_panel">
      <div class="x_title">Furmace</div>
      <div class="x_content">
        <select name="center_data" class="form-control" v-model="gallery_index">
          <option v-for="({ cinder }, index) in fracData" :key="cinder.time" :value="index">{{ cinder.time }}</option>
        </select>
      
      <div class="carousel">
        <div class="carousel-labels">
          <span>CINDER</span>
          <span>SCHIEHT</span>
        </div>
                    
        <div class="timeframe" v-for="timeframe in current_timeframes" :key="timeframe.cinder.time">
          <div class="time-label">{{ timeframe.cinder.time | datetime }}</div>
          <div class="carousel-chart" @click="modalChart(timeframe.cinder)">
            <bar-chart 
              :min-sizes="timeframe.cinder.min_sizes"
              :masses="timeframe.cinder.masses"></bar-chart>
          </div>
          <div class="carousel-chart" @click="modalChart(timeframe.schieht)">
            <bar-chart
              :min-sizes="timeframe.schieht.min_sizes"
              :masses="timeframe.schieht.masses"></bar-chart>
          </div>
          <div class="time-label">{{ timeframe.schieht.time | datetime }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import barChart from './BarChart.vue'

export default {
  name: 'Furnace',
  props: {
    fracData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      gallery_index: 2
    }
  },
  computed: {
    current_timeframes() {
      let frame = 5
      let index = this.gallery_index
      return this.fracData.slice(Math.max(0, index - 2), Math.min(this.fracData.length - 1, index ? index + 3 : 5))
    }
  },
  methods: {
    modalChart(val) {
      console.log("click", val)
      this.$modal.show(barChart, {
        minSizes: val.min_sizes,
        masses: val.masses,
        labels: true
      }, {
        width: "800",
        height: "600"
      })
    }
  },
  components: {
    barChart
  },
  filters: {
    datetime(value) {
      return new Date(value).toLocaleString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false
        })
    }
  }
}
</script>

<style>
  .carousel {
    display: flex;
  }

  .carousel-chart {
    cursor: pointer;
  }

  .carousel .carousel-labels {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
  }

  .carousel .carousel-labels span {
    display: block;
    transform: rotate(-90deg);
  }

  .carousel .timeframe {
    display: flex;
    flex-direction: column;
    align-items: center;
  }


</style>
