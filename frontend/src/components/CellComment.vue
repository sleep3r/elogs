<template>
  <div>
    <div class="cell-popup-wrapper" @click="closePopover"></div>
    <div class="cell-popup" v-bind:style="{left: x + 'px', top: y + 'px'}">
      <div class="header">
        <div class="btn-close" @click="closePopover" >&times;</div>
        <div class="title">{{tableName}}</div>
        <div class="subtitle">{{fieldName}}</div>
        <div class="dash" v-if="!onlyChat">
            <div class="item user-name" v-if="responsible"><i class="material-icons">account_circle</i><span>&nbsp{{ responsible }}</span></div>
            <div class="item time" v-if="cellCreatedTime"><i class="material-icons">watch_later</i><span>&nbsp;{{cellCreatedTime}}</span></div>
            <div class="item units" v-if="maxNormal"><i class="material-icons">assignment_turned_in</i><span>&nbsp;to {{maxNormal}} m<sup>2</sup></span></div>
        </div>
      </div>
      <div class="comments">
        <div class="date">{{currentDate}}</div>
        <div class="comments-list">
          <div class="comment" v-for="(comment, index) in comments" :key="comment.text + '_' + comment.created + '_' + index">
            <div class="comment-cloud" v-if="comment.text">
              <div class="author">{{commentUserName(comment)}}</div>
              <div class="body">{{comment.text}}</div>
            </div>
            <div class="time">{{prettyTime(comment.created)}}</div>
          </div>
        </div>
      </div>
      <div class="footer">
        <textarea placeholder="Введите текст комментария" class="comment-text" v-model="commentText"></textarea>
        <div class="btns">
          <div class="btn btn-add" @click="addComment" >Добавить комментарий</div>
          <div class="btn btn-graph dropdown dropdown-toggle" v-if="!onlyChat" id="graphMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <span><i class="fas fa-chart-line"></i>&nbsp;Построить график</span>
            <div class="dropdown-menu" aria-labelledby="graphMenuButton">
              <a class="dropdown-item" href="" @click.prevent="addToDashboard('ShiftTimeline')">Временной ряд</a>
              <a class="dropdown-item" href="" @click.prevent="addToDashboard('ShiftHistogram')">Гистограмма</a>
            </div>
          </div>
        </div>
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
    'onlyChat',
    'x',
    'y'
  ],
  data: function() {
      return {
          commentText: '',
          graphs: []
      }
  },
  computed: {
    currentDate: function() {
      return this.cellCreatedDate;
    },
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
      let responsible = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['responsible'];
      if (responsible) {
        return Object.values(responsible)[0];
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
    closePopover () {
      EventBus.$emit('close-cell-comment')
    },
    scrollToBottom () {
      let commentList = $('.comments-list')
      if (commentList.length) commentList.scrollTop(commentList[0].scrollHeight);
    },
    commentUserName(comment) {
      let name = Object.values(comment.user)[0];
      return name;
    },
    prettyDate(date) {
      date = new Date(date);
      return date.getFullYear()+'-' + (date.getMonth()+1) + '-'+date.getDate();//prints expected format.
    },
    prettyTime(date) {
      date = new Date(date);
      return date.getHours() +':' + date.getMinutes();
    },
    showGraphModal (type) {
      this.getConfig();
      $('.tooltip.popover').css({'visibility': 'hidden'});
      $('#GraphModal').attr('data-type', type)
    },
    addComment() {
      let date = new Date();
      this.$store.commit('journalState/SAVE_CELL_COMMENT', {
        tableName: this.tableName,
        fieldName: this.fieldName,
        index: this.rowIndex,
        comment: {'text': this.commentText, 'created': date.toISOString(), 'user': {'self': this.$store.getters['userState/fullname']}}
      });
      this.send();
      this.commentText = '';
      setTimeout(() => this.scrollToBottom(), 0)
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
            window.HOSTNAME + "/api/dashboard/add-graph",
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
            this.$notify({
                text: 'График успешно создан!',
                duration: 3000,
                type: 'success'
            })
        })
    },
    getConfig () {
      let self = this;
      ajax.get(
          window.HOSTNAME + '/api/dashboard/get-config',
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
      setTimeout(() => this.scrollToBottom(), 0);

      EventBus.$on('add-to-dashboard', (type) => {
        this.addToDashboard(type)
      });

      EventBus.$on('scroll-to-bottom', () => {
        setTimeout(() => this.scrollToBottom(), 0)
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

.cell-popup-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 100;
}

.cell-popup {
   width: $popup-width;
   box-shadow: 0 24px 38px 3px rgba(0,0,0,0.14), 0 9px 46px 8px rgba(0,0,0,0.12), 0 11px 15px -7px rgba(0,0,0,0.2);
   font-family: 'Ubuntu', sans-serif;

  .header {
    position: relative;
    background-color: $color-bg;
    box-shadow: 0 3px 4px #e5e5e5;
    min-height: 95px;
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

/* ---------------------------------------- */
$color-header: #218DBA;
$color-footer: #E6E6E6;
$color-comment: #f5f5f5;
$color-comment-text: #A5A5A5 ;

.cell-popup {
  font-family: 'Roboto Condensed', sans-serif;
  font-size: 13px;
  background-color: white;
  width: 450px;
  height: 386px;
  position: absolute;
  z-index: 101;

  .header {
    background-color: $color-header;
    color: white;
    padding: 10px;
    display: flex;
    flex-direction: column;

    .btn-close {
        text-align: right;
        font-weight: bold;
        font-size: 20px;
        position: absolute;
        right: 10px;
        top: 1px;
        cursor: pointer;
    }

    .title {
      font-size: 14px;
      font-weight: bold;
    }

    .subtitle {
      font-size: 13px;
    }

    .dash {
      margin-top: 10px;
      display: flex;
      justify-content: space-evenly;
      height: 30px;

      .item {
        line-height: 20px;
        span, sup {
          vertical-align: top;
          line-height: 24px;
        }
      }

      .user-name {
      }

      .time {
      }

      .units {

      }
    }
  }
  .comments {
    .date {
      padding: 4px;
      font-size: 10px;
      font-style: italic;
      color: $color-comment-text;
      text-align: center;
    }

    .comments-list {
      height: 150px;
      min-height: 101%;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
      padding-right: 20px;
      padding-left: 100px;

      .comment {
        display: flex;
        flex-direction: row-reverse;
        margin-bottom: 20px;

        .time {
          color: $color-comment-text;
          margin-right: 10px;
          font-size: 11px;
        }

        .comment-cloud {
          width: 84%;
          background-color: $color-comment;
          padding: 5px;
          text-align: left;

          .author {
              color: $color-comment-text;
              font-style: italic;
            }

          .body {
              color: #353535;

            }
        }

      }
    }

  }
  .footer {
      background-color: $color-footer;
      padding: 10px;
      textarea.comment-text {
        color: #151515;
        width: 100%;
        border: none;
        resize: none;
        height: 60px;
        padding: 5px;
        font-size: 13px;
      }
      .btns {
        display: flex;
        justify-content: space-evenly;
        padding-top: 10px;

          .btn {
            background-color: $color-header;
            color: white;
            width: 50%;

          }
          .btn-add {
            margin-right: 10px;
          }
          .btn-graph {
          }
      }
    }
}
</style>
