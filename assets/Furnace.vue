<template>
<div>
    <div class="x_panel">
      <div class="x_title"><h4>Фракционный состав шихты и огарка</h4></div>
      <div class="x_content">
        <!-- <select name="center_data" class="form-control" v-model="gallery_index">
          <option v-for="({ cinder }, index) in fracData" :key="cinder.time" :value="index">{{ cinder.time }}</option>
        </select> -->
        <datetime v-model="selected_time"
          type="datetime"
          input-format="DD-MM-YYYY HH:mm"
          moment-locale="ru" />
      <br/>
      <div class="carousel">
        <div class="carousel-labels">
          <span>ОГАРОК</span>
          <span>ШИХТА</span>
        </div>
        <i class="glyphicon glyphicon-chevron-left carousel-chevron"
          @click="prevFrame"></i>

        <div class="timeframe" v-for="timeframe in current_timeframes" :key="timeframe.cinder.time">
          <div class="carousel-chart" @click="modalChart(timeframe.cinder)">
            <bar-chart 
              :min-sizes="timeframe.cinder.min_sizes"
              :masses="timeframe.cinder.masses"
              :prediction="is_prediction(timeframe.cinder.time)"></bar-chart>
            <div class="time-label">{{ timeframe.cinder.time | datetime }}</div>
          </div>
          <div class="spacer"></div>
          <div class="carousel-chart" @click="modalChart(timeframe.schieht)">
            <bar-chart
              :min-sizes="timeframe.schieht.min_sizes"
              :masses="timeframe.schieht.masses"
              :prediction="is_prediction(timeframe.schieht.time)"></bar-chart>
            <div class="time-label">{{ timeframe.schieht.time | datetime }}</div>
          </div>
          
        </div>
        <i class="glyphicon glyphicon-chevron-right carousel-chevron"
          @click="nextFrame"></i>
      </div>
    </div>
      </div>
      <div class="tablewrapper" style="width:100%">
    <div class="x_panel">
      <div class="x_title"><h4>График среднего размера огарка</h4></div>
      <div class="x_content" style="display: flex;" v-if="gaphsData['cinder']">
        <line-chart :points="gaphsData.cinder"></line-chart>
      </div>
    </div>
    <div class="x_panel">
      <div class="x_title"><h4>График среднего размера шихты</h4></div>
      <div class="x_content" style="display: flex;" v-if="gaphsData['schieht']">
        <line-chart :points="gaphsData.schieht"></line-chart>
      </div>
    </div>
    </div>
</div>
</template>

<script>
  import barChart from "./BarChart.vue";
  import lineChart from "./LineChart.vue";

  export default {
    name: "Furnace",
    props: {
      fracData: {
        type: Array,
        required: true
      },
      gaphsData: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        gallery_index: 2,
        current_time: new Date(),
        selected_time: ''
      };
    },
    watch: {
      selected_time(val) {
        let time = Date.parse(val)
        this.gallery_index = this.closest(this.fracData, time)
      }
    },
    computed: {
      current_timeframes() {
        let frame = 5;
        let index = this.gallery_index;
        return this.fracData.slice(
          Math.max(0, index - 2),
          Math.min(this.fracData.length, index ? index + 3 : frame)
        );
      }
    },
    methods: {
      is_prediction(time) {
        return new Date(time) > this.current_time;
      },
      modalChart(val) {
        console.log("click", val);
        this.$modal.show(
          barChart,
          {
            minSizes: val.min_sizes,
            masses: val.masses,
            labels: true,
            prediction: this.is_prediction(val.time)
          },
          {
            width: "1200",
            height: "900"
          }
        );
      },
      prevFrame() {
        if (this.gallery_index > 1) {
          this.gallery_index--;
        }
      },
      nextFrame() {
        if (this.gallery_index < this.fracData.length - 4) {
          this.gallery_index++;
        }
      },
      closest(array,num){
        var i=0;
        var minDiff= Date.parse(array[array.length - 1].cinder.time)
        var ans;
        for(i in array){
            var m=Math.abs(num - Date.parse(array[i].cinder.time) )
            console.log(num, Date.parse(array[i].cinder.time), i, m)
            if(m<minDiff){ 
                    minDiff=m; 
                    ans=i; 
                }
          }
        return parseInt(ans)
}
    },
    components: {
      barChart,
      lineChart
    },
    filters: {
      datetime(value) {
        return new Date(value).toLocaleString("en-US", {
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          hour12: false
        });
      }
    }
  };
</script>

<style>
.x_panel {
  margin-bottom: 10px;
}

.carousel {
  display: flex;
}

.carousel-chart {
  cursor: pointer;
  margin: 0 5px;
  border: 1px solid #d5d5d5;
}

.carousel-chart:hover {
  border: 1px solid rgb(50, 150, 222);
}

.carousel .carousel-chevron {
  align-self: center;
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
  justify-content: space-evenly;
}

.carousel .spacer {
  min-height: 25px;
}

.time-label {
  text-align: center;
}

#furnacepicker {
  max-width: 1600px;
}
</style>
