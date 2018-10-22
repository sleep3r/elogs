<template>
  <div class="cell-popup tooltip-content">
    <div class="header"><i v-close-popover class="btn--close fas fa-times"></i>
      <div class="title">
        <!-- {{$store.getters['journalState/plantVerboseName']}}
      </br>
        {{$store.getters['journalState/journalVerboseName']}}
      </br> -->
        {{$store.getters['journalState/tableVerboseName'](tableName)}}
      </br>
        {{$store.getters['journalState/fieldVerboseName'](tableName, fieldName)}}
      </div>
      <div class="header__icon"><i class="fas fa-receipt"></i></div>
    </div>
    <div class="body">
      <ul class="list" v-if="!onlyChat">
        <li v-if="cellValue" class="item"><i class="item__icon fas fa-pencil-alt"></i><span class="item__text">{{ cellValue }}</span></li>
        <li v-if="cellCreatedTime" class="item"><i class="item__icon far fa-clock"></i><span class="item__text">{{cellCreatedTime}}</span></li>
        <li v-if="((minNormal)||(maxNormal))" class="item"><i class="item__icon fas fa-info-circle"></i><span class="item__text">Допустимые значения <template v-if="minNormal">от {{minNormal}} </template>  <template v-if="maxNormal"> до {{maxNormal}}</template> </span></li>
        <li v-if="responsible" class="item"><i class="item__icon fas fa-user-tie"></i><span class="item__text">{{responsible}}</span></li>
        <li v-if="cellCreatedDate" class="item"><i class="item__icon fas fa-calendar-alt"></i><span class="item__text">{{ cellCreatedDate }}</span></li>
      </ul>
      <ul class="comments">
        <li v-for="comment in comments">
          <div style="float: left"><b>{{ Object.values(comment.user)[0] }}</b> ({{ prettyDate(comment.created) }}):</div> {{ comment.text }}
        </li>
      </ul>
      <textarea style="width: 80%" v-model="commentText">
      </textarea>
    </br>
      <button class="btn" @click="addComment">Добавить комментарий</button>
    </br>
    </br>
      <div class="buttons-panel"  v-if="!onlyChat">
        <!-- <div v-if="graphNotAdded"> -->
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-chart-line"></i>
                Построить график
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <!-- <a class="dropdown-item" href="javascript:;" data-toggle="modal" data-target="#GraphModal" @click.prevent="showGraphModal('ShiftTimeline')">ShiftTimeline</a>
                <a class="dropdown-item" href="javascript:;" data-toggle="modal" data-target="#GraphModal" @click.prevent="showGraphModal('ShiftHistogram')">ShiftHistogram</a> -->
                <a class="dropdown-item" href="" @click.prevent="addToDashboard('ShiftTimeline')">ShiftTimeline</a>
                <a class="dropdown-item" href="" @click.prevent="addToDashboard('ShiftHistogram')">ShiftHistogram</a>
              </div>
            </div>
        <!-- </div> -->
        <!-- <div v-else>
            График добавлен в панель аналитики
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import ajax from '../axios.config'
import GraphModal from './GraphModal.vue'
import EventBus from '../EventBus'
import { setTimeout } from 'timers';

export default {
  name: 'CellComment',
  props: [
    'tableName',
    'fieldName',
    'rowIndex',
    'onlyChat'
  ],
  data: function() {
      return {
          commentText: '',
          graphs: []
      }
  },
  computed: {
    cellValue: function () {
        return this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['value']
    },
    cellCreatedDate: function () {
        let created = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['created']
        if (created) {
            let date = new Date(created);
            return date.getFullYear()+'-' + (date.getMonth()+1) + '-'+date.getDate();
        }
        else {
            return ''
        }
    },
    cellCreatedTime: function () {
        let created = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['created']
        if (created) {
            let date = new Date(created);
            return date.getHours() + ':' + (date.getMinutes()<10?'0':'') + date.getMinutes();
        }
        else {
            return ''
        }
    },
    responsible: function () {
      let responsible = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['responsible']
      if (responsible) {
        return Object.values(responsible)[0]
      }
      else {
        return ''
      }
    },
    minNormal: function () {
      return this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName)['min_normal'];
    },
    maxNormal: function () {
      return this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName)['max_normal'];
    },
    units: function () {
      return this.$store.getters['journalState/fieldDescription'](this.tableName, this.fieldName)['units'];
    },
    comments: function () {
        return this.$store.getters['journalState/cellComments'](this.tableName, this.fieldName, this.rowIndex);
    },
  },
  methods: {
    prettyDate(date) {
      date = new Date(date);
      return date.getFullYear()+'-' + (date.getMonth()+1) + '-'+date.getDate();//prints expected format.
    },
    showGraphModal (type) {
      this.getConfig()
      $('.tooltip.popover').css({'visibility': 'hidden'})
      $('#GraphModal').attr('data-type', type)
    },
    addComment() {
      let date = new Date();
      this.$store.commit('journalState/SAVE_CELL_COMMENT', {
        tableName: this.tableName,
        fieldName: this.fieldName,
        index: this.rowIndex,
        comment: {'text': this.commentText, 'created': date.toISOString(), 'user': {'self': this.$store.getters['userState/username']}}
      });
      this.send();
      this.commentText = ''
    },
    send() {
      this.$socket.sendObj({
        'type': 'messages',
        'cell_location': {
          'group_id': this.$store.getters['journalState/journalInfo'].id,
          'table_name': this.tableName,
          'field_name': this.fieldName,
          'index': this.rowIndex
        },
        'message': {
          'text': this.commentText,
          'link': 'lalala',
          'type': 'comment'
        },
        'crud': 'add'
      });
    },
    addToDashboard(selectedGraphType) {
        ajax.post(
            window.HOSTNAME+"/dashboard/add-graph",
            {
                'cell_info': {
                    'journal_name': this.$store.state.journalState.journalInfo.journal.name,
                    'table_name': this.tableName,
                    'field_name': this.fieldName,
                },
                'graph_info': {
                    'type': selectedGraphType
                },
            },
            {withCredentials: true}
        )
        .then(() => {
          $('.tooltip.popover').css({'visibility': 'hidden'})
        })
    },
    getConfig () {
      let self = this;
      ajax.get(
          window.HOSTNAME + '/dashboard/get-config',
          {withCredentials: true},
      )
        .then(function (response) {
            let config = response.data.config
            for (var id in config) {
                self.graphs.push(id)
            }
        })
    }
  },
  mounted () {
      EventBus.$on('add-to-dashboard', (type) => {
        console.log(1232131313)
        this.addToDashboard(type)
      })
  }
}
</script>

<style lang="scss">
.content {
  .btn {
    display: none;
  }
}

.popup {
  margin: 150px auto;
}

$popup-width: 450px;
$color-bg: #008BB9;

.v-popover {
  span {
    width: 100%;
  }
}

.popover:not(.clockpicker-popover){
  max-width: 0;
  height: 0;
  border: none;

  .wrapper {
    width: 450px;
  }
}

.cell-popup {
   width: $popup-width;
   box-shadow: 0 24px 38px 3px rgba(0,0,0,0.14), 0 9px 46px 8px rgba(0,0,0,0.12), 0 11px 15px -7px rgba(0,0,0,0.2);
   font-family: 'Ubuntu', sans-serif;

  .header {
    position: relative;
    background-color: $color-bg;
    box-shadow: 0 3px 4px #e5e5e5;
    min-height: 80px;

    .btn--close {
      color: #ffffff !important;
      position: relative !important;
      top: -20px;
      cursor: pointer;
    }

    .title {
      color: #FFFFFF;
      position: relative;
      top: 0px;
      left: 63px;
      width: 300px;
    }

    .header__icon {
      color: #ffffff;
      width: 40px;
      height: 40px;
      border-radius: 20px;
      background-color: #008BB9;
      text-align: center;
      position: absolute;
      top: 60px;
      left: 30px;
      box-shadow: 0 6px 10px 0 rgba(0,0,0,0.14), 0 1px 18px 0 rgba(0,0,0,0.42), 0 3px 5px -1px rgba(0,0,0,0.2);

      i {
        line-height: 40px;
      }
    }
  }

  .body {
    padding-bottom: 20px;

    .list {
      margin: 40px 0 0 0;
      list-style: none;
      padding: 0;
    }
    .item {
      //padding: 10px;
      display: flex;
      margin-bottom: 10px;
    }
    .item__icon {
      width: 30px;
      height: 30px;
      line-height: 30px;
      text-align: center;
      margin-left: 21px;
      color: #959595;
    }
    .item__text {
      color: #252525;
      font-size: 14px;
      padding-left: 15px;
      line-height: 30px;
    }

    .comments {
      height: 150px;
      background-color: #fff;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 20px;
      color: #353535;
      list-style: none;
      border-top: 1px solid #c5c5c5;
      border-bottom: 1px solid #c5c5c5;
      box-shadow: inset 0 4px 5px #e5e5e5;

      li {
        margin-bottom: 10px;
      }
    }

    .buttons-panel {
      text-align: center;

      .btn {
        i {
          color: #ffffff;
          margin-right: 5px;

        }
      }

    }


  }

}
</style>
