<template>
    <section class="tabs">
        <ul class="nav nav-tabs">
            <li v-for="item in items" :key="item.id"  class="nav-item" @click="selectTab(item.id)">
                <a href="#" :class="getClasses(item.id)" >{{item.title}}</a>
            </li>
        </ul>
        <slot/>
    </section>
</template>

<script>
    export default {
        name: "tabs",
        props: [
            'items',
            'first'
        ],
        data: function () {
            return {
                activeIndex: 0,
                tabs: []
            }
        },
        mounted() {
            // console.log("mounted");
            this.selectTab(this.first);
        },
        created() {
          this.tabs = this.$children;
          // console.log("created");
        },
        methods: {
            getClasses(id) {
              if (this.activeIndex === (id*1) ) {
                  return 'nav-link active';
              } else {
                  return 'nav-link ';
              }
            },
            selectTab: function(id) {
                // console.log(id);
                let sid = "" + id;
                let selectedTab = this.tabs.find( tab => { return (tab.id === sid) });
                // console.log(" selected: ", selectedTab);
                selectedTab.isActive = true;
                this.activeIndex = +id;
                this.tabs.forEach(tab => {
                    tab.isActive = (tab.id === sid);
                });
            }
        }
    }
</script>

<style scoped>
    .tab {
        padding: 10px;
        border: 1px solid #eeeeee;
        /*display: none;*/
    }
</style>