<template>
  <div class="settings-page">
    <settings-list></settings-list>
  </div>
</template>

<script>
import SettingsList from './SettingsList.vue'

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
      SettingsList
  }
}
</script>
<style scoped lang="scss">
  .settings-page {
    border: 1px solid #548CB7;
    vertical-align: middle;
    min-height: 400px;
    padding: 20px;
    display: flex;
    flex-direction: column;
  }
  a {
    color: #42b983;
  }
</style>
