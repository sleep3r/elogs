<template>
    <div class="modal fade" id="GraphModal" tabindex="-1" role="dialog" aria-labelledby="GraphModal" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Построение графика </h5>
                </div>
                <div v-if="idx" class="modal-body">
                     <graph :idx='idx' :type='type'></graph>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn" @click.prevent="onAddGraph">Добавить</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import ajax from '../axios.config'
    import EventBus from '../EventBus'
    import Graph from './Graph.vue'

    export default {
        name: "GraphModal",
        components: {
            'graph': Graph
        },
        data () {
            return {
                idx: null,
                type: null,
            }
        },
        computed: {
            
        },
        methods: {
            onAddGraph () {
                EventBus.$emit('add-to-dashboard', $('#GraphModal').attr('data-type'))
                this.closeModal()
            },
            closeModal () {
                $('#GraphModal').find('button[aria-label=Close]').click()
            },
            showGraph(payload) {
                this.idx = payload.idx
                this.type = payload.type
            }
        },
        mount() {
            EventBus.$on("show-graph-in-modal", (payload) => this.showGraph(payload))
        }

    }
</script>

<style lang='scss' scoped>
#GraphModal {
    .modal-dialog {
        max-width: 55%;
    }
}
</style>