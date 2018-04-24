<template>
  <div class="x_panel">
    <div class="x_title">
        <h2>{{lang.messages.title}}</h2>
        <ul class="nav navbar-right panel_toolbox">
            <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
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
                                <td><input type="text" v-model="denser.hs.ph"></td>
                                <td><input type="text" v-model="denser.hs.cu" ></td>
                                <td><input type="text" v-model="denser.hs.fe"></td>
                                <td><input type="text" v-model="denser.hs.liq_sol"></td>

                                <td><input type="text" v-model="denser.ls.ph"></td>
                                <td><input type="text" v-model="denser.ls.liq_sol"></td>
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
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>

                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>
                            <a class="btn btn-success" v-on:click="">
                                <i class="glyphicon glyphicon-plus"></i>
                            </a>
                        </td>
                        <td colspan="18"></td>
                    </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Densers',
  data() {
    return {
        state: '',
        editableId: '',
        items: [],
        errors: [],
        lang: {
            messages: {
                title: 'Сгустители'
            }
        },
        headers: {}
     }
  },
  created() {
       console.log('created:.....')
       this.headers = this.getTableHeaders()
       this.getDensers()
  },
  methods: {
      editRow(combineId) {
        console.log(combineId)
        this.editableId = combineId
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



  }
}
</script>