import $ from 'jquery'
import 'jquery-ui-bundle';
import Plotly from 'plotly.js-dist'

let json = '{"data": [{"x": [1999, 2000, 2001, 2002], "y": [10, 15, 13, 17], "type": "scatter", "uid": "c4a0f6c8-abc2-11e8-968a-4a0004e53b00"}, {"x": [1999, 2000, 2001, 2002], "y": [16, 5, 11, 9], "type": "scatter", "uid": "c4a0f91e-abc2-11e8-bca0-4a0004e53b00"}], "layout": {"autosize": true, "title": "Sales Growth", "xaxis": {"showgrid": false, "title": "Year", "zeroline": false}, "yaxis": {"showline": false, "title": "Percent"}}}'
window.plot = JSON.parse(json)

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

$(document).ready(() => {
   window.Visualization = Visualization;
   window.Visualization.init()
});

export {Visualization}
