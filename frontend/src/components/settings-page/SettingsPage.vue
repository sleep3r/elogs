<template>
  <div class="settings-page">
    <button @click="isShowHelp = true">Help</button>
    <settings-list></settings-list>

    <modal v-show="isShowHelp" @close="isShowHelp = false">
        <pre>
          <code>
            API get
            API post
            API put
          </code>
        </pre>
    </modal>
  </div>
</template>

<script>
import SettingsList from './SettingsList.vue'
import Modal from "../Modal.vue";

export default {
  name: 'settings-page',
  props: {

  },
  data() {
    return {
        isShowHelp: false
    }
  },
  components: {
      Modal,
      SettingsList
  }
}
</script>
<style scoped lang="scss">
  .settings-page {
    border: 1px solid #548CB7;
    vertical-align: middle;
    min-height: 400px;
    padding: 10px;
    display: flex;
    flex-direction: column;
  }
  a {
    color: #42b983;
  }
</style>
