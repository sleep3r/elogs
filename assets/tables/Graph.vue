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
    props: ["idx"],
    data: function() {
        return {
            idx: "",
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
            data.layout.height = height - 50;
            // window.graphs_data[id] = data

            Plotly.newPlot(id, data.data, data.layout)
        },
        get_data: function() {
            let self = this
            let data = JSON.stringify(this.idx)
            axios.post("/dashboard/get-graph-data/", data)
                .then(function (response) {
                    self.render(response.data)
                })
        }
    },
    created() {
        this.get_data()
    }
}
</script>
