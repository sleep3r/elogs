<template>
    <div class="container">
        <h2 class="title">Создание журнала</h2>
        <form>
            <form-input
                    @change="(value) => onHandleChange('name', value)"
                    :value="name"
                    :label="'Введите название журнала'"
                    :placeholder="'Название'"
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
        name: "CreateJournalPage",
        data () {
            return {
                name: '',
                error: ''
            }
        },
        methods: {
            onHandleBack () {
                this.$router.back()
            },
            onHandleCreate () {
                if (this.name) {
                    this.$store.commit('journalState/setJournal', {name: this.name})
                    this.$router.push(`/journal/${this.name}`)
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