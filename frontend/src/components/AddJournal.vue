<template>
    <div class="load-journal-content">
        <!--<form action="journal_upload/" method="post" enctype="multipart/form-data">-->
        <form>
            <h3 style="margin-bottom: 30px;">Загрузить журнал:</h3>
            <span v-if="errorText" style="color: red">{{errorText}}</span>
            <p><input accept=".journal" id="journal_upload_button" type="file" value="Обзор" name="journal_file" @change="(e) => {file = e.target.files[0]}"/></p>
            <p>
                <select name="plant" v-model="plant">
                    <option disabled selected value="">Выберите цех</option>
                    <option value="furnace">Обжиг</option>
                    <option value="leaching">Выщелачивание</option>
                    <option value="electrolysis">Электролиз</option>
                </select>
            </p>
            <p>
                <select name="type" v-model="journal">
                    <option disabled selected value="">Выберите тип журнала</option>
                    <option value="shift">Смена</option>
                    <option value="equipment">Оборудование</option>
                    <option value="measurement">Измерение</option>
                </select>
            </p>
            <p style="text-align: right;"><input class="btn" type="submit" value="Загрузить" @click.prevent="onLoadJournal"/></p>
        </form>

        <!--{% if user.is_superuser or user|in_group:"Big boss" or user|in_group:"Boss" %}-->
        <!--{#<h2>Настройки системы</h2>#}-->
        <!--{% endif %}-->
    </div>
</template>

<script>
    export default {
        name: "SettingsPage",
        data () {
            return {
                errorText: '',
                plant: '',
                journal: '',
                file: null
            }
        },
        methods: {
            onLoadJournal () {
                console.dir(this.file)
            }
        }
    }
</script>

<style type="scss" scoped>
    .load-journal-content {
        padding: 20px;
    }
</style>