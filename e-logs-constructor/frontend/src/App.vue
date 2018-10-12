<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
@import '~bootstrap3/dist/css/bootstrap.min.css';
/*@import '~bootstrap3/dist/css/bootstrap-theme.min.css';*/
html, body {
  padding: 0;
  margin: 0;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  color: #2c3e50;
  box-sizing: border-box;
}
th {
  border: 1px solid #9d9d9d !important;
  background-color: #e6e6e6 !important;
  width: 145px !important;
  height: 35px !important;
}
td {
  border: 1px solid #9d9d9d !important;
  width: 145px !important;
  height: 35px !important;
}
</style>
