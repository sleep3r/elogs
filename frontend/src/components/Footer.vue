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
        <alert-modal></alert-modal>
        <graph-modal></graph-modal>
        <full-calendar-modal></full-calendar-modal>
        <cell-comment
            v-if="cellComment.isShowPopover"
            :table-name="cellComment.tableName"
            :field-name="cellComment.fieldName"
            :row-index="cellComment.rowIndex"
            :onlyChat="cellComment.onlyChat"
            :isNumber="cellComment.isNumber"
            :x="cellComment.coordX" 
            :y="cellComment.coordY" 
        />
    </div>
</template>

<script>
    import MessageModal from './MessageModal.vue';
    import SchemeModal from './SchemeModal.vue';
    import AddModeModal from './AddModeModal.vue';
    import AlertModal from './AlertModal.vue';
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
            'alert-modal': AlertModal,
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
                    isNumber: false,
                    coordX: null,
                    coordY: null,
                    isShowPopover: false
                }
            }
        },
        mounted () {
            EventBus.$on('show-cell-comment', (props) => {
                $('body').css({'overflow': 'hidden'})

                this.cellComment.tableName = props.tableName,
                this.cellComment.fieldName = props.fieldName,
                this.cellComment.rowIndex = props.rowIndex,
                this.cellComment.isNumber = props.isNumber,
                this.cellComment.onlyChat = props.onlyChat,
                this.cellComment.coordX = props.coordX,
                this.cellComment.coordY = props.coordY,
                this.cellComment.isShowPopover = props.show
            
                if (props.show) {
                    EventBus.$emit('scroll-to-bottom')
                }
            })
            EventBus.$on('close-cell-comment', () => {
                $('body').css({'overflow': ''})

                this.cellComment.isShowPopover = false
            })
        }
    }
</script>

<style scoped>

</style>