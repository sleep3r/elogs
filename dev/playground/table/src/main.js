import Vue from 'vue/dist/vue.esm.js'
import TableCommon from './components/TableCommon.vue'


Vue.config.errorHandler = function (err, vm, info) {
  // Обработка ошибки. В `info` подробности Vue-специфичной ошибки,
  // например, в каком хуке жизненного цикла произошла ошибка.
  // Доступно только в версиях 2.2.0+
    console.error("error: ", err);
    console.info(vm);
    console.info("hook name ->", info);
};



window.app = new Vue({
    el: '#elogs-app',
    template: "<div>" +
        '<TableCommon plant-name="furnace" journal-name="furnace_changed_fraction" table-name="table-ostatok"></TableCommon>' +
        '<TableCommon plant-name="furnace" journal-name="furnace_changed_fraction" table-name="first"></TableCommon>' +
        '<TableCommon plant-name="furnace" journal-name="furnace_changed_fraction" table-name="shit"></TableCommon>' +
        "</div>",
    components: { TableCommon },
    renderError (h, err) {
         return h('pre', { style: { color: 'red' }}, err.stack)
    }
});
