<template>
  <div class="container">
    <div class="editor-container">
        <froala id="editor" :tag="'textarea'" :config="config" v-model="model"></froala>
    </div>
    <div class="btns">
        <btn :onClick="onHandleBack" style="margin-right: 14px">Назад</btn>
        <btn :onClick="onHandleSend">Отправить</btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditPage',
  data () {
    return {
      config: {
        events: {
          'froalaEditor.initialized': function () {
            console.log('initialized')
          }
        },
        toolbarButtons: ['fullscreen', '|', 'insertTable', '|', 'undo', 'redo'],
        charCounterCount: false
      },
      model: ''
    }
  },
  methods: {
      onHandleBack () {
        this.$router.back()
      },
      onHandleSend () {
        console.log($('#editor').froalaEditor('html.get'))
      }
  }
}
</script>

<style lang="scss">
.container {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}
.editor-container {
    margin-bottom: 20px;
}
.btns {
  display: flex;
  justify-content: center;
}
</style>
