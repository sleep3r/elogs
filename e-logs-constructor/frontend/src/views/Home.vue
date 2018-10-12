<template>
  <div class="home">
    <h1 class="title">
      <span>Реальный конструктор</span>
      <span>для нереальных таблиц</span>
    </h1>
    <form class="form" @submit.prevent="onHandleCreate">
      <div class="form-group">
        <input type="text" class="form-control" v-model="title" placeholder="Заголовок" @input="onHandleChange" style="margin-bottom: 20px">
      </div>
      <div v-show="error" class="error">
        Введите заголовок
      </div>
      <button class="btn btn-primary" @click="onHandleCreate">Создать журнал</button>
    </form>
  </div>
</template>

<script>
import slugify from 'slugify'
export default {
  name: "HomePage",
  data () {
      return {
          title: '',
          error: ''
      }
  },
  methods: {
      onHandleBack () {
          this.$router.back()
      },
      onHandleCreate (e) {
          if (this.title) {
              this.$store.commit('journalState/setJournal', {title: this.title, name: slugify(this.title, '_')})
              this.$router.push(`/journal/${slugify(this.title, '_')}`)
          }
          else this.error = true
      },
      onHandleChange (data) {
          data.target.value ? this.error = '' : this.error = true
      }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding-top: 130px;
  height: 100%;
  box-sizing: border-box;
}
.title {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 130px;
}
.title span:first-child {
  font-size: 40px;
  opacity: 0.9;
}
.title span:last-child {
  font-size: 44px;
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
.form {
  width: 300px;
  margin: 10px 0 0 0;
  text-align: center;
}
</style>