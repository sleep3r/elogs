<template>
    <section class="tabs">
        <ul class="nav nav-tabs">
            <li v-for="item in items" :key="item.id" role="presentation" :class="getClasses(item.id)" @click="selectTab(item.id)">
                <a href="javascript:;">{{item.title}}</a>
            </li>
        </ul>
        <slot/>
    </section>
</template>

<script>
    export default {
        name: "tabs",
        props: [
            'items'
        ],
        data: function () {
            return {
                activeIndex: 0,
                tabs: []
            }
        },
        mounted() {
            this.tabs[0].isActive = true;
        },
        created() {
          this.tabs = this.$children;
        },
        methods: {
            getClasses(id) {
              if (this.activeIndex === id ) {
                  return 'active';
              } else {
                  return '';
              }
            },
            selectTab: function(id) {
                console.log(id);
                let sid = "" + id;
                let selectedTab = this.tabs.find( tab => { return (tab.id === sid) });
                console.log(" selected: ", selectedTab);
                selectedTab.isActive = true;
                this.activeIndex = id;

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