<template>
    <div class="load-journal-content">
        <form enctype="multipart/form-data">
            <h3 style="margin-bottom: 30px;">Загрузка журнала</h3>
            <span :style="{display: errorText ? 'block' : 'none'}" class="alert alert-danger">{{errorText}}</span>
            <template v-if="!hash">
                <p>
                    <input accept=".jrn" id="journal_upload_button" type="file" value="Обзор" name="journal_file"
                           @change="handleFileUpload"/>
                </p>
            </template>
            <template v-if="altered">
                <h5><b>{{this.journalVerboseName}}</b> будет изменен.</h5>

                <p style="text-align: left;">
                    <button v-if="hash" class="btn" style="margin-right: 10px;" @click.prevent="hash = ''; file = ''">
                        Отмена
                    </button>
                    <button class="btn" type="submit" @click.prevent="onAlterJournal()">Изменить</button>
                </p>
            </template>
            <!--<template v-else-if="hash">-->
            <template>
                <p>
                    <select name="plant" v-model="plant">
                        <option disabled selected value="">Выберите цех</option>
                        <option v-for="plant in plants" :value="plant.name">{{plant.verbose_name}}</option>
                    </select>
                </p>
                <p>
                    <select name="type" v-model="type">
                        <option disabled selected value="">Выберите тип журнала</option>
                        <option value="shift">Посменный</option>
                        <option value="equipment">Журнал оборудования</option>
                        <option value="month">Помесячный</option>
                        <option value="year">Погодовой</option>
                    </select>
                </p>
                <p v-if="type === 'shift'">
                    <select name="number-of-shifts" v-model="shifts">
                        <option disabled selected value="">Выберите количество смен</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                    </select>
                </p>
            </template>

            <h5 v-if="hash && !altered"><b>Новый журнал будет загружен</b></h5>

            <p style="text-align: left;">
                <button v-if="hash && !altered" class="btn" style="margin-right: 10px;" @click.prevent="hash = ''; file = ''">
                    Отмена
                </button>

                <button v-if="!altered" class="btn" type="submit" @click.prevent="hash ? onLoadJournalData() : onLoadJournalFile()">
                    {{hash ? 'Загрузить' : 'Продолжить'}}
                </button>
            </p>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import VueCookies from 'vue-cookies'

    export default {
        name: "SettingsPage",
        data() {
            return {
                errorText: '',
                plant: '',
                journal: '',
                type: '',
                shifts: '',
                file: '',
                hash: '',
                altered: false,
            }
        },
        computed: {
            plants() {
                return this.$store.getters['journalState/plants']
            },
            plantVerboseName() {
                return this.plants.filter((item) => (item.name === this.plant))[0].verbose_name;
            },
            journalVerboseName() {
                return this.$store.getters['journalState/plants'].filter(item => item.name === this.plant)[0].journals.filter(item => item.name === this.journal)[0].verbose_name;
            }
        },
        methods: {
            onLoadJournalFile() {
                if (this.file) {
                    let formData = new FormData();

                    formData.append("journal_file", this.file);

                    axios.post(window.HOSTNAME + '/api/constructor/journal/', this.file,
                        {
                            headers: {
                                Authorization: 'Token ' + VueCookies.get('Authorization'),
                                'content-type': "application/json"
                            }
                        }
                    )
                        .then((res) => {
                            this.errorText = ''
                            this.hash = res.data.hash
                        })
                        .catch(err => {
                            this.$notify({
                                text: 'Не удалось загрузить файл!',
                                duration: 3000,
                                type: 'error'
                            })
                        })
                } else {
                    this.errorText = 'Выберите файл!'
                }
            },
            onAlterJournal() {
                let formData = new FormData();

                formData.append("plant", this.plant);
                formData.append("journal_name", this.journal);
                formData.append("hash", this.hash);

                axios.post(window.HOSTNAME + '/api/constructor/alter/', formData,
                    {
                        headers: {
                            Authorization: 'Token ' + VueCookies.get('Authorization')
                        }
                    }
                )
                    .then((res) => {
                        this.$notify({
                            text: `Журнал успешно изменен!`,
                            duration: 3000,
                            type: 'success'
                        })
                    })
                    .catch(err => {
                        this.$notify({
                            text: 'Не удалось изменить журнал!',
                            duration: 3000,
                            type: 'error'
                        })
                    })
            },
            onLoadJournalData() {

                let formData = new FormData();

                formData.append("plant", this.plant);
                formData.append("type", this.type);
                formData.append("number_of_shifts", this.shifts);
                formData.append("hash", this.hash);

                axios.post(window.HOSTNAME + '/api/constructor/upload/', formData,
                    {
                        headers: {
                            Authorization: 'Token ' + VueCookies.get('Authorization')
                        }
                    }
                )
                    .then((res) => {
                        this.$notify({
                            text: `Журнал успешно загружен!`,
                            duration: 3000,
                            type: 'success'
                        });
                        this.$store.dispatch('journalState/loadPlants');
                    })
                    .catch(err => {
                        this.$notify({
                            text: 'Не удалось загрузить журнал!',
                            duration: 3000,
                            type: 'error'
                        })
                    })
            },
            handleFileUpload(e) {
                var reader = new FileReader();
                let self = this;
                reader.onload = function(e) {
                    self.file = reader.result;
                    if (self.file) {
                        self.errorText = ''
                    }
                }
                reader.readAsText(e.target.files[0]);
            },
            getURLParameter(paramName) {
                let url = window.location.search.substring(1);
                let urlParams = url.split('&');
                for (let i = 0; i < urlParams.length; i++) {
                    let parameterName = urlParams[i].split('=');
                    if (parameterName[0] === paramName) {
                        return parameterName[1];
                    }
                }
                return "";
            }
        },
        mounted() {
            if (this.getURLParameter('hash')) {
                this.hash = this.getURLParameter('hash');
                if ((this.getURLParameter('plant'))) {
                    this.plant = this.getURLParameter('plant');
                    this.journal = this.getURLParameter('journalName');
                    this.altered = true;
                }
            }
        }
    }
</script>

<style type="scss" scoped>
    .load-journal-content {
        padding: 20px;
    }
</style>

