<template>
    <div class="load-journal-content">
        <form>
            <h3 style="margin-bottom: 30px;">Загрузить журнал:</h3>
            <span v-if="errorText" style="color: red">{{errorText}}</span>
            <p><input accept=".jrn" id="journal_upload_button" type="file" value="Обзор" name="journal_file" @change="(e) => {file = e.target.files[0]}"/></p>
            <p>
                <select name="plant" v-model="plant">
                    <option disabled selected value="">Выберите цех</option>
                    <option value="furnace">Обжиг</option>
                    <option value="leaching">Выщелачивание</option>
                    <option value="electrolysis">Электролиз</option>
                </select>
            </p>
            <p>
                <select name="type" v-model="type">
                    <option disabled selected value="">Выберите тип журнала</option>
                    <option value="shift">Смена</option>
                    <option value="equipment">Оборудование</option>
                    <option value="measurement">Измерение</option>
                </select>
            </p>
            <p>
                <select name="number-of-shifts" v-model="shifts">
                    <option disabled selected value="">Выберите количество смен</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                </select>
            </p>
            <p style="text-align: right;"><input class="btn" type="submit" value="Загрузить" @click.prevent="onLoadJournal"/></p>
        </form>
    </div>
</template>

<script>
    import ajax from '../axios.config' 
    import VueCookies from 'vue-cookies'

    export default {
        name: "SettingsPage",
        data () {
            return {
                errorText: '',
                plant: '',
                type: '',
                shifts: '',
                file: null
            }
        },
        methods: {
            onLoadJournal () {
                ajax.post(window.HOSTNAME + '/api/load_journal/', 
                    {
                        'journal_file': this.file,
                        'plant': this.plant,
                        'type': this.type,
                        'number_of_shifts': this.shifts
                    }, 
                    {
                        headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
                    }
                )
                    .then((res) => {
                        console.log(res)
                    })
                    .catch(err => {
                        console.log(err)
                    })
            }
        }
    }
</script>

<style type="scss" scoped>
    .load-journal-content {
        padding: 20px;
    }
</style>