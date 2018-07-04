<template>
  <div class="furnace-dashboard">
    <div class="x_panel">
      <div class="x_title"><h4>Фракционный состав шихты и огарка</h4></div>
      <div class="x_content">
        <div class="date-control">
          <datetime 
            v-model="selected_time"
            input-class="form-control"
            placeholder="Выбор даты и времени"
            type="datetime"
            input-format="DD.MM.YYYY HH:mm"
            moment-locale="ru" />
          <button
            @click="toCurrent()"
            class="btn btn-default"
            type="button">Текущее время</button>
        </div>
        <br>
        <div class="carousel">
          <div class="carousel-labels">
            <span>ОГАРОК</span>
            <span>ШИХТА</span>
          </div>
          <i 
            class="glyphicon glyphicon-chevron-left carousel-chevron"
            @click="prevFrame"/>
          <transition-group 
            :name="slideTransition"
            tag="div"
            class="carousel-inner">
            <div 
              class="timeframe" 
              :class="{prediction: is_prediction(timeframe.cinder.time)}"
              v-for="timeframe in current_timeframes" 
              :key="timeframe.cinder.time">
              <div 
                class="carousel-chart" 
                @click="modalChart(timeframe.cinder)">
                <bar-chart 
                  :min-sizes="timeframe.cinder.min_sizes"
                  :masses="timeframe.cinder.masses"
                  :prediction="is_prediction(timeframe.cinder.time)"/>
                <div class="time-label">{{ timeframe.cinder.time | datetime }}</div>
              </div>
              <div class="spacer"/>
              <div 
                class="carousel-chart" 
                @click="modalChart(timeframe.schieht)">
                <bar-chart
                  :min-sizes="timeframe.schieht.min_sizes"
                  :masses="timeframe.schieht.masses"
                  :prediction="is_prediction(timeframe.schieht.time)"/>
                <div class="time-label">{{ timeframe.schieht.time | datetime }}</div>
              </div>
            </div>
          </transition-group>
          <i 
            class="glyphicon glyphicon-chevron-right carousel-chevron"
            @click="nextFrame"/>
        </div>
      </div>
    </div>
    <div class="tablewrapper gaphs">
      <div class="x_panel">
        <div class="x_title"><h4>График среднего размера огарка</h4></div>
        <div 
          class="x_content" 
          v-if="gaphsData['cinder']">
          <line-chart :points="gaphsData.cinder"/>
        </div>
      </div>
    </div>
    <div class="tablewrapper gaphs">
      <div class="x_panel">
        <div class="x_title"><h4>График среднего размера шихты</h4></div>
        <div 
          class="x_content" 
          v-if="gaphsData['schieht']">
          <line-chart :points="gaphsData.schieht"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import barChart from "./BarChart.vue";
  import lineChart from "./LineChart.vue";

  export default {
    name: "FurnaceDashboard",
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
        current_time: Date.now(),
        selected_time: '',
        slideTransition: 'slide-left'
      }
    },
    mounted() {
      this.toCurrent()
      window.addEventListener('keydown', this.keyDownFrame)
    },
    destroyed() {
      window.removeEventListener('keydown', this.keyDownFrame)
    },
    watch: {
      selected_time(val) {
        this.moveToTime(val)
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
        return time * 1000 > this.current_time;
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
            height: "auto"
          }
        );
      },
      moveToTime(val) {
        let time = Date.parse(val)
        this.gallery_index = this.closest(this.fracData, time)
      },
      toCurrent() {
        let time = new Date(this.current_time).toISOString()
        this.moveToTime(time)
        // this.selected_time = time
      },
      keyDownFrame(e) {
        if (e.keyCode === 37) // left
          this.prevFrame()
        else if (e.keyCode === 39) // right
          this.nextFrame()
      },
      prevFrame() {
        if (this.gallery_index > 2) {
          this.slideTransition = 'slide-right'
          this.gallery_index -= 3;
        }
      },
      nextFrame() {
        if (this.gallery_index < this.fracData.length - 3) {
          this.slideTransition = 'slide-left'
          this.gallery_index += 3;
        }
      },
      closest(array, num) {
        var i=0;
        var minDiff = array[array.length - 1].cinder.time * 1000
        var ans;
        for(i in array){
            var m = Math.abs(num - array[i].cinder.time * 1000)
            // console.log(num, Date.parse(array[i].cinder.time), i, m)
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
        return new Date(value * 1000).toLocaleString("ru-RU", {
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

<style lang="scss">
.x_panel {
  margin-bottom: 10px;
}

.tablewrapper.gaphs {
  width: calc(50% - 10px);
}

.date-control {
  display: flex;

  .vdatetime {
    flex-grow: 1;
  }

}

.carousel, .carousel-inner {
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
  font-size: 20px;
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

.slide-left-move,
.slide-right-move {
  transition: transform 1s;
}

.slide-left-leave-active,
.slide-left-enter-active,
.slide-right-leave-active,
.slide-right-enter-active {
  transition: 1s;
}
.slide-left-enter {
  opacity: 0;
  transform: translate(300%, 0);
}

.slide-right-enter {
  transform: translate(-300%, 0);
  opacity: 0;
}

.slide-left-leave-to
{
  transform: translate(-100%, 0);
  opacity: 0;
}

.slide-right-leave-to {
  opacity: 0;
  transform: translate(500%, 0);
}

.slide-left-leave-active,
.slide-left-leave,
.slide-right-leave-active,
.slide-right-leave {
  max-width: 20%;
  position: absolute;
}



.timeframe:not(.prediction) + .timeframe.prediction {
  border-left: 1px dotted gray;
  padding-left: 5px;
  margin-left: 5px;
}

.carousel .spacer {
  min-height: 25px;
}

.time-label {
  text-align: center;
}

.furnace-dashboard {
  .vdatetime-popup__header,
  .vdatetime-popup__date-picker__item--selected:hover>span>span,
  .vdatetime-popup__date-picker__item--selected>span>span
  {
    background: rgb(28, 187, 156);
  }
}
</style>
