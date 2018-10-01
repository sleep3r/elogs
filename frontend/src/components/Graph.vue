<template>
    <div :id="idx">
        {{ message }}
    </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import VueGridLayout from 'vue-grid-layout';
import Plotly from 'plotly.js-dist'

export default {
    name: 'Graph',
    props: ["idx", "type"],
    data: function() {
        return {
            message: "Loading graph..."
        }
    },

    methods: {
        render: function(data) {
            console.log(data)
            this.message = ""
            let id = this.idx
            let width = $("#" + 'vue-grid-item-' + id).width()
            let height = $("#" + 'vue-grid-item-' + id).height()
            console.log(width, height)
            data.layout.width = width;
            data.layout.height = height - 30;
            // window.graphs_data[id] = data

            Plotly.newPlot(id, data.data, data.layout)
        },
        get_data: function() {
            let self = this
            let data = {
                id: this.idx,
                type: this.type
            }
            console.log(data)
            axios.post(
                "http://localhost:8000/dashboard/get-graph-data/",
                data,
                {withCredentials: true}
             )
                .then(function (response) {
                    self.render(response.data)
                })
        },
    },
    created() {
        this.get_data()
    }
}
</script>

<style>

.vue-grid-item {
    background: grey;
}

.vue-grid-item {
    border: solid grey 2px;
}

#app {
    width: 100%
}

.dashboard {
    width: 100%
}

</style>
