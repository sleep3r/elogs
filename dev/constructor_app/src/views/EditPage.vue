<template>
  <div class="container">
    <editor class="editor"></editor>
    <div class="btns">
        <btn :onClick="onHandleBack" style="margin-right: 14px">Назад</btn>
        <btn :onClick="onHandleSend">Отправить</btn>
    </div>
  </div>
</template>

<script>
import Editor from '../components/Editor'
export default {
  name: 'EditPage',
  data () {
    return {

    }
  },
  methods: {
      onHandleBack () {
        this.$router.back()
      },
      onHandleSend () {
        console.log($('#editor-content').html())
      }
  },
  components: { Editor }
}
</script>

<style scoped>
.container {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}
.editor {
    margin-bottom: 20px;
}
.btns {
  display: flex;
  justify-content: center;
}
</style>
