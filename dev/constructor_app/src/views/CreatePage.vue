<template>
    <div class="container">
        <h2 class="title">Создание таблицы</h2>
        <form>
            <form-input
                    @change="(value) => onHandleChange('name', value)"
                    :value="name"
                    :label="'Введите название таблицы'"
                    :placeholder="'Название'"
            />
            <form-input
                    @change="(value) => onHandleChange('latinName', value)"
                    :value="latinName"
                    :label="'Введите название таблицы на латинице'"
                    :placeholder="'Название на латинице'"
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
        name: "CreatePage",
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
                this.latinName && this.name ?
                    this.$router.push(`/edit/${this.latinName}`)
                    : this.error = true
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