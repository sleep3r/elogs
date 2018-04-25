<template>
  <div class="x_panel">
    <div class="x_title">
        <h2>{{lang.messages.title}}</h2>
        <ul class="nav navbar-right panel_toolbox">
            <li>
                <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
            </li>
            <li><a class="close-link"><i class="fa fa-close"></i></a>
            </li>
        </ul>
        <div class="clearfix"></div>
    </div>
    <div class="x_content">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th rowspan="3" class="rotate"><div><span>Время</span></div></th>
                    <template v-for="denser, key in headers.densers">
                        <th colspan="6" > Сгуститель {{denser}}</th>
                    </template>
                </tr>
                <tr>
                    <template v-for="denser, key in headers.densers">
                        <th colspan="4">ВС {{denser}} сг.</th>
                        <th colspan="2">НС {{denser}} сг.</th>
                    </template>
                </tr>
                <tr>
                    <template v-for="denser, key in headers.densers">
                        <th class="rotate densers-header"><div><span>pH</span></div></th>
                        <th class="rotate"><div><span>Медь, мг/л</span></div></th>
                        <th class="rotate"><div><span>Железо, мг/л</span></div></th>
                        <th class="rotate"><div><span>Ж:Т</span></div></th>

                        <th class="rotate"><div><span>pH</span></div></th>
                        <th class="rotate"><div><span>Ж:Т</span></div></th>
                    </template>
                </tr>
            </thead>
            <tbody>
                <template v-if="items">
                    <tr class="mini" v-for="(row, combine_id) in items" v-on:click="editRow(combine_id)">
                        <td>{{row.hour}}<sup>00</sup></td>
                        <template v-for="denser in row.item">
                            <template v-if="editableId === combine_id">
                                <td><input type="text" class="form-control" v-model="denser.hs.ph"></td>
                                <td><input type="text" class="form-control" v-model="denser.hs.cu" ></td>
                                <td><input type="text" class="form-control" v-model="denser.hs.fe"></td>
                                <td><input type="text" class="form-control" v-model="denser.hs.liq_sol"></td>

                                <td><input type="text" class="form-control" v-model="denser.ls.ph"></td>
                                <td><input type="text" class="form-control" v-model="denser.ls.liq_sol"></td>
                            </template>
                            <template v-else>
                                <td>{{denser.hs.ph }}</td>
                                <td>{{denser.hs.cu }}</td>
                                <td>{{denser.hs.fe }}</td>
                                <td>{{denser.hs.liq_sol }} :1</td>

                                <td>{{denser.ls.ph }}</td>
                                <td>{{denser.ls.liq_sol }} :1</td>
                            </template>
                        </template>
                    </tr>

                </template>
                    <tr v-if="state == 'add' ">
                        <td>{{selectedHour}}<sup>00</sup></td>
                        <template v-for="denser in record">
                        <td><input type="text" class="form-control" v-model="denser.hs.ph"></td>
                        <td><input type="text" class="form-control" v-model="denser.hs.cu"></td>
                        <td><input type="text" class="form-control" v-model="denser.hs.fe"></td>
                        <td><input type="text" class="form-control" v-model="denser.hs.liq_sol"></td>

                        <td><input type="text" class="form-control" v-model="denser.ls.ph"></td>
                        <td><input type="text" class="form-control" v-model="denser.ls.liq_sol"></td>
                        </template>
                    </tr>

                    <tr>
                        <td colspan="1" style="width:80px">
                            <select-hours :current="paramSelectedHour" v-on:selectedHour="onSelectedHour" />
                        </td>
                        <td>
                            <a class="btn btn-success" v-on:click="newRecord()">
                                <i class="glyphicon glyphicon-plus"></i>
                            </a>
                        </td>
                        <td colspan="18"></td>
                    </tr>
                    <tr>
                        <td colspan="20" >
                            <template v-if=" editableId  != ''" >
                                <a class="btn btn-success" align="left" v-on:click="saveRecord()">
                                    <i class="glyphicon glyphicon-floppy-disk"></i>Сохранить
                                </a>
                            </template>
                            <template v-else >
                                    <a class="btn btn-success" align="left" v-on:click="addRecord()">
                                        <i class="glyphicon glyphicon-floppy-disk"></i>Добавить
                                    </a>
                            </template>
                        </td>
                    </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import selectHours from './Hours.vue'

export default {
  name: 'Densers',
  data() {
    return {
        state: '',
        editableId: '',
        selectedHour: 10,
        items: [],
        errors: [],
        initRecord: {'10':{'hs':{},'ls':{}}, '11':{'hs':{},'ls':{}}, '12':{'hs':{},'ls':{}}},
        record: {},
        saved: {},
        lang: {
            messages: {
                title: 'Сгустители'
            }
        },
        headers: {}
     }
  },
  computed: {
      paramSelectedHour: function() {
        return this.selectedHour
      },
      initalRecord: function() {
        return this.initRecord
      }

  },
  created() {
      this.init()
  },
  methods: {
      init() {
        console.log('init:.....')
        this.headers = this.getTableHeaders()
        this.getDensers()
      },
      editRow(combineId) {
        console.log(combineId)
        this.editableId = combineId
      },
      onSelectedHour(hour) {
          this.selectedHour = parseInt(hour)
      },
      getTableHeaders() {
          return { densers: ["10", "11", "12"] }
      },
      getShiftFromUrl() {
        let uri = window.location.search.substring(1);
        let params = new URLSearchParams(uri);
        let id = params.get('shift') ? params.get('shift') : 0
        return id
      },
      getDensers() {
        let shiftId = this.getShiftFromUrl()
        console.log(shiftId)
        axios.get('/leaching/api/densers?shift_id=' + shiftId)
            .then( ( responce ) => {
                this.items = responce.data.items
                console.info('responce')
                console.log(responce)

            })
            .catch(e => {
                this.errors.push(e)
            })
      },
      newRecord() {
        this.record =  JSON.parse(JSON.stringify(this.initRecord))
        this.state = 'add'
        this.editableId = ''
      },
      addRecord() {
        let shiftId = this.getShiftFromUrl()
        this.state = ''
        let forSave = new FormData()

        forSave.append('record', JSON.stringify(this.record))
        forSave.append('shift_id', shiftId)
        forSave.append('hour', this.selectedHour)

        axios.post('/leaching/densers/add', forSave )
            .then( (response) => {
                console.info(response.data)
                this.init()
            })
            .catch( e=>{
                this.errors.push(e)
            })

        this.saved = forSave
      },
      saveRecord() {
        let shiftId = this.getShiftFromUrl()
        this.state = ''
        let forSave = new FormData()
        let row = this.items[this.editableId]
          console.info("hour ")
        console.log(row.hour)
        forSave.append('record', JSON.stringify(row))
        forSave.append('hour', row.hour)
        forSave.append('shift_id', shiftId)

        axios.post('/leaching/densers/save', forSave )
            .then( (response) => {
                console.info(response.data)
                this.init()
            })
            .catch( e=>{
                this.errors.push(e)
            })


      }

  },
  components: {
      selectHours
  }
}
</script>