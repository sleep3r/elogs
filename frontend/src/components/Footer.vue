<template>
    <div>
        <footer>
            <button class="btn" data-toggle="modal" data-target="#MessageToDevelopersModal">
                <span>Оставить отзыв разработчикам</span>
                <i class="fab fa-optin-monster"></i>
            </button>
        </footer>
        <message-modal></message-modal>
        <scheme-modal></scheme-modal>
        <add-mode-modal></add-mode-modal>
        <resp-modal></resp-modal>
        <graph-modal></graph-modal>
        <full-calendar-modal></full-calendar-modal>
        <cell-comment
            :table-name="cellComment.tableName"
            :field-name="cellComment.fieldName"
            :row-index="cellComment.rowIndex"
            :onlyChat="cellComment.onlyChat"
            :x="cellComment.coordX" 
            :y="cellComment.coordY" 
            :show="cellComment.isShowPopover"
        />
    </div>
</template>

<script>
    import MessageModal from './MessageModal.vue';
    import SchemeModal from './SchemeModal.vue';
    import AddModeModal from './AddModeModal.vue';
    import ResponsibleModal from './ResponsibleModal.vue';
    import GraphModal from './GraphModal.vue';
    import FullCalendarModal from './FullCalendarModal.vue';
    import CellComment from './CellComment.vue'

    import EventBus from '../EventBus'

    export default {
        name: "Footer",
        components: {
            'message-modal': MessageModal,
            'schemeModal': SchemeModal,
            'add-mode-modal': AddModeModal,
            'resp-modal': ResponsibleModal,
            'graph-modal': GraphModal,
            'full-calendar-modal': FullCalendarModal,
            'cell-comment': CellComment
        },
        data () {
            return {
                cellComment: {
                    tableName: null,
                    fieldName: null,
                    rowIndex: null,
                    onlyChat: false,
                    coordX: null,
                    coordY: null,
                    isShowPopover: false
                }
            }
        },
        mounted () {
            EventBus.$on('show-cell-comment', (props) => {
                this.cellComment.tableName = props.tableName,
                this.cellComment.fieldName = props.fieldName,
                this.cellComment.rowIndex = props.rowIndex,
                this.cellComment.onlyChat = props.onlyChat,
                this.cellComment.coordX = props.coordX,
                this.cellComment.coordY = props.coordY,
                this.cellComment.isShowPopover = props.show

                if (props.show) {
                    EventBus.$emit('scroll-to-bottom')
                }
            })
            EventBus.$on('close-cell-comment', () => {
                this.cellComment.isShowPopover = false
            })
        }
    }
</script>

<style scoped>

</style>