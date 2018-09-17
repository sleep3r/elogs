import $ from 'jquery'
import 'jquery-ui-bundle';
import Plotly from 'plotly.js-dist'
import VueGridLayout from 'vue-grid-layout';


var testLayout = [
    {"x":0,"y":0,"w":2,"h":4,"i":"0"},
    {"x":2,"y":0,"w":2,"h":4,"i":"1"},
    {"x":4,"y":0,"w":2,"h":5,"i":"2"},
    {"x":6,"y":0,"w":2,"h":3,"i":"3"},
    {"x":8,"y":0,"w":2,"h":3,"i":"4"},
    {"x":10,"y":0,"w":2,"h":3,"i":"5"},
    {"x":0,"y":5,"w":2,"h":5,"i":"6"},
    {"x":2,"y":5,"w":2,"h":5,"i":"7"},
    {"x":4,"y":5,"w":2,"h":5,"i":"8"},
    {"x":6,"y":4,"w":2,"h":4,"i":"9"},
    {"x":8,"y":4,"w":2,"h":4,"i":"10"},
    {"x":10,"y":4,"w":2,"h":4,"i":"11"},
    {"x":0,"y":10,"w":2,"h":5,"i":"12"},
    {"x":2,"y":10,"w":2,"h":5,"i":"13"},
    {"x":4,"y":8,"w":2,"h":4,"i":"14"},
    {"x":6,"y":8,"w":2,"h":4,"i":"15"},
    {"x":8,"y":10,"w":2,"h":5,"i":"16"},
    {"x":10,"y":4,"w":2,"h":2,"i":"17"},
    {"x":0,"y":9,"w":2,"h":3,"i":"18"},
    {"x":2,"y":6,"w":2,"h":2,"i":"19"}
];

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
            url: "/visualization/get-graph-data",
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
        console.log(data)
        Plotly.newPlot(id, data["data"], data["layout"])
    }

    static render_graphs() {
        let graph_containers = $("#dashboard-container").children(".graph")
        graph_containers.each((index, element) => {
            let id = $(element).attr('id')
            let data = this.get_graph_data(id)
            // this.render_graph(id, data)
        })
    }

    static init() {
        console.log(1)
        this.get_graphs_list()
    }
}

var GridLayout = VueGridLayout.GridLayout;
var GridItem = VueGridLayout.GridItem;

$(document).ready(() => {
    window.Visualization = Visualization;
    // window.Visualization.init()

    new Vue({
        el: '#vue-dashboard-container',
        components: {
            "GridLayout": GridLayout,
            "GridItem": GridItem
        },
        data: {
            layout: testLayout,
            draggable: true,
            resizable: true,
            index: 0
        },
    });
});

export {Visualization}
