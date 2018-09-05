<template>
  <div class="container">
    <btn :onClick="onHandleClick">Создать таблицу</btn>
  </div>
</template>

<script>
export default {
  name: "JournalPage",
  methods: {
      onHandleClick () {
          this.$store.getters['journalState/getJournalName'] ?
              this.$router.push(`/journal/${this.$store.getters['journalState/getJournalName']}/table/create`)
              : this.$router.push('/journal/create')
      }
  }
}
</script>

<style scoped>
.container {
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
</style>