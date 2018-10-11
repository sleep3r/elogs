<template>
  <div class="edit-data">
    <h2 class="title">Заполнение данными</h2>
    <editor class="editor"></editor>
    <div class="btns">
        <button class="btn btn-secondary" @click="onHandleBack" style="margin-right: 14px">Назад</button>
        <button class="btn btn-primary" @click.prevent="onHandleSave" type="submit">Сохранить</button>
    </div>
  </div>
</template>

<script>
import Editor from '../components/Editor.vue'
import formatFactory from '../utils/formatFactory.js'

export default {
  name: 'EditTableDataPage',
  data () {
    return {

    }
  },
  methods: {
      onHandleBack () {
        this.$router.back()
      },
      onHandleSave () {
        $('.editor .cell').removeClass("selected")
        this.$store.commit('journalState/setTable',
            {
                tableName: this.$route.params.tableName,
                data: {
                    html: formatFactory($('#editor-content').html())
                }
            }
        )
        this.$router.push(`/journal/${this.$route.params.journalName}`)
      }
  },
  components: { Editor },
}
</script>

<style scoped>
.edit-data {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}
.edit-data .title{
    margin-top: 0;
    margin-bottom: 20px;
}
.editor {
    margin-bottom: 20px;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
</style>
