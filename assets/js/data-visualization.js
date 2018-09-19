import $ from 'jquery'
import Vue from 'vue/dist/vue.esm.js'
import Plotly from 'plotly.js-dist'
import VueGridLayout from 'vue-grid-layout';


var testLayout = {
    "313": {"x":0,"y":0,"w":5,"h":6},
    "314": {"x":0,"y":0,"w":6,"h": 10},
};

class Visualization {
    static get_graphs_list() {
        $.ajax({
            type: 'GET',
            url: "/visualization/get-graphs-list",
            success: (data) => {
                this.graphs_list = data["graphs"]
                console.log(this.graphs_list)
                this.render_containers()
                this.render_graphs()
            },
            dataType: "json"
        });
    }

    static get_graph_data(id) {
        // return window.plot;
        let response;
        let data = JSON.stringify(id)
        $.ajax({
            type: 'POST',
            url: "/visualization/get-graph-data/",
            data: data,
            contentType: "application/json; charset=utf-8",
            success: (data) => {
                response = data;
                this.render_graph(id, data)
            },
            dataType: "json"
        });
    }

    static add_graph(cell_info){
        let data = JSON.stringify(cell_info)
        $.ajax({
            type: 'POST',
            url: "/visualization/add-graph",
            data: data,
            contentType: "application/json; charset=utf-8",
            success: console.log("Graph added"),
            dataType: "json"
        });
    }

    static render_containers() {
        let container = $("#dashboard-container")
        this.graphs_list.forEach(function(graph_name) {
            let graph_container = document.createElement("div")
            graph_container.setAttribute("id", graph_name)
            graph_container.setAttribute("class", "graph")
            container.append(graph_container)
            $("#" + graph_name).draggable()
        })
    }

    static render_graph(id, data) {
        let width = $("#" + 'vue-grid-item-' + id).width()
        let height = $("#" + 'vue-grid-item-' + id).height()
        console.log(width, height)
        data.layout.width = width;
        data.layout.height = height - 50;
        window.graphs_data[id] = data

        Plotly.newPlot(id, data.data, data.layout)
    }

    static render_graphs() {
        let graph_containers = $(".vue-grid-layout").children(".vue-grid-item:not(.vue-grid-placeholder)")
        graph_containers.each((index, element) => {
            let id = $(element).attr('id')
            id = id.split("-")[3]
            console.log(id)
            let data = this.get_graph_data(id)
            // this.render_graph(id, data)
        })
    }

    static init() {
        console.log(1)
        window.graphs_data = {};
        this.get_graphs_list()
    }
}

var GridLayout = VueGridLayout.GridLayout;
var GridItem = VueGridLayout.GridItem;

$(document).ready(() => {
    window.Visualization = Visualization;
    // window.Visualization.init()
    console.log("test")
    window.graphs_data = {}
    window.Plotly = Plotly
    window.dashboard = new Vue({
        el: '#vue-dashboard-container',
        components: {
            "GridLayout": GridLayout,
            "GridItem": GridItem,
        },
        data: {
            layout: testLayout,
            draggable: true,
            resizable: true,
            dragIgnoreFrom: ".plotly",
            index: 0
        },
        methods: {
            resizedEvent: function(i, newH, newW, newHpx, newWpx) {
                Plotly.relayout(i, {
                    autosize: false,
                    width: newWpx - 4,
                    height: newHpx - 50,
                })
            },
        }
    });
    Visualization.render_graphs();
});

export {Visualization}
