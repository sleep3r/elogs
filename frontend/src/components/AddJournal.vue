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
            <template v-if="hash && plant">
                <h5><b>{{this.journalVerboseName}}</b> будет изменен.</h5>
            </template>
            <template v-else="hash">
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
            <p v-if="hash && this.plant" style="text-align: left;">
                <button v-if="hash" class="btn" style="margin-right: 10px;" @click.prevent="hash = ''; file = ''">
                    Отмена
                </button>
                <button class="btn" type="submit" @click.prevent="onAlterJournal()">Изменить</button>
            </p>
            <p v-else-if="hash" style="text-align: left;">
                <button v-if="hash" class="btn" style="margin-right: 10px;" @click.prevent="hash = ''; file = ''">
                    Отмена
                </button>
                <button class="btn" type="submit" @click.prevent="hash ? onLoadJournalData() : onLoadJournalFile()">
                    {{hash ? 'Сохранить' : 'Загрузить'}}
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

                    axios.post(window.HOSTNAME + '/api/constructor/hash/', formData,
                        {
                            headers: {
                                Authorization: 'Token ' + VueCookies.get('Authorization'),
                                'content-type': "multipart/form-data"
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
                            text: `Журнал успешно загружен!
                            Обновите страницу.`,
                            duration: 3000,
                            type: 'success'
                        })
                    })
                    .catch(err => {
                        this.$notify({
                            text: 'Не удалось загрузить журнал!',
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

                // let data = {
                //     'plant': this.plant,
                //     'type': this.type,
                //     'number_of_shifts': this.shifts,
                //     'hash': this.hash
                // }

                axios.post(window.HOSTNAME + '/api/constructor/upload/', formData,
                    {
                        headers: {
                            Authorization: 'Token ' + VueCookies.get('Authorization')
                        }
                    }
                )
                    .then((res) => {
                        this.$notify({
                            text: `Журнал успешно загружен! 
                            Обновите страницу.`,
                            duration: 3000,
                            type: 'success'
                        })
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
                this.file = e.target.files[0];
                if (this.file) {
                    this.errorText = ''
                }
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
                    this.journal = this.getURLParameter('journalName')
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

