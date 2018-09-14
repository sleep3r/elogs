<template>
    <div class="container">
        <h2 class="title">Создание таблицы</h2>
        <form>
            <form-input
                    @change="(value) => onHandleChange('name', value)"
                    :value="name"
                    :label="'Введите название таблицы'"
                    :placeholder="'Название'"
                    style="width: 300px;"
            />
            <form-input
                    @change="(value) => onHandleChange('latinName', value)"
                    :value="latinName"
                    :label="'Введите название таблицы на латинице'"
                    :placeholder="'Название на латинице'"
                    style="width: 300px;"
            />
            <div v-show="error" class="error">
                Заполните все поля
            </div>
        </form>
        <div class="btns">
            <btn :onClick="onHandleBack" style="margin-right: 14px">Назад</btn>
            <btn :onClick="onHandleCreate">Создать</btn>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CreateTablePage",
        data () {
            return {
                name: '',
                latinName: '',
                error: ''
            }
        },
        methods: {
            onHandleBack () {
                this.$router.back()
            },
            onHandleCreate () {
                if (this.latinName && this.name && this.$store.getters['journalState/getJournalName']) {
                    this.$store.commit('journalState/addTable',
                        {
                            name: this.name,
                            latinName: this.latinName,
                            fields: []
                        }
                    )
                    this.$router.push(`/journal/${this.$store.getters['journalState/getJournalName']}/table/${this.latinName}/edit`)
                }
                else if (!this.$store.getters['journalState/getJournalName']) {
                    this.$router.push('/journal/create')
                }
                else this.error = true
            },
            onHandleChange (data, value) {
                value ? this.error = '' : this.error = true
                this[data] = value
            }
        }
    }
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  padding-top: 130px;
  height: 100%;
  box-sizing: border-box;
}
.error {
    display: flex;
    align-items: center;
    background-color: rgb(245, 108, 108);
    color: rgb(255, 255, 255);
    height: 40px;
    border-radius: 6px;
    padding: 0px 15px;
    margin-bottom: 20px;
}
.btns {
  display: flex;
  justify-content: center;
}
</style>