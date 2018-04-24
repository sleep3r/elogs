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
                    <tr class="mini" v-for="(row, hour) in items">
                        <td>{{hour}}<sup>00</sup></td>
                        <template v-for="denser in row">
                            <td>{{denser.hs.ph }}</td>
                            <td>{{denser.hs.cu }}</td>
                            <td>{{denser.hs.fe }}</td>
                            <td>{{denser.hs.liq_sol }} :1</td>

                            <td>{{denser.ls.ph }}</td>
                            <td>{{denser.ls.liq_sol }} :1</td>
                        </template>
                    </tr>
                </template>
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
       this.headers = this.getTableHeaders()
       this.getDensers()
  },
  methods: {
      getTableHeaders() {
          return { densers: ["10", "11", "12"] }
      },
      getDensers() {
        let shiftId = 441
        axios.get('/leaching/api/densers?shift_id=' + shiftId)
            .then(({ data }) => {
                this.items = data.items
                console.log(data)

            })
            .catch(e => {
                this.errors.push(e)
            })
    }

  }
}
</script>