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
        <boss-instruction></boss-instruction>
        <no-boss-instruction></no-boss-instruction>
        <add-mode-modal></add-mode-modal>
        <alert-modal></alert-modal>
        <graph-modal></graph-modal>
        <full-calendar-modal></full-calendar-modal>
        <cell-comment
            :isShown="cellComment.isShowPopover"
            :table-name="cellComment.tableName"
            :field-name="cellComment.fieldName"
            :row-index="cellComment.rowIndex"
            :onlyChat="cellComment.onlyChat"
            :isNumber="cellComment.isNumber"
            :x="cellComment.coordX" 
            :y="cellComment.coordY" 
            :preshow="cellComment.preshow"
        />
        <clock-picker></clock-picker>
    </div>
</template>

<script>
    import MessageModal from './MessageModal.vue';
    import SchemeModal from './SchemeModal.vue';
    import BossInstruction from './BossInstruction.vue';
    import NoBossInstruction from './NoBossInstrucion.vue';
    import AddModeModal from './AddModeModal.vue';
    import AlertModal from './AlertModal.vue';
    import GraphModal from './GraphModal.vue';
    import FullCalendarModal from './FullCalendarModal.vue';
    import CellComment from './CellComment.vue'
    import ClockPicker from './ClockPicker.vue'

    import EventBus from '../EventBus'

    export default {
        name: "Footer",
        components: {
            'message-modal': MessageModal,
            'schemeModal': SchemeModal,
            'bossInstruction': BossInstruction,
            'noBossInstruction': NoBossInstruction,
            'add-mode-modal': AddModeModal,
            'alert-modal': AlertModal,
            'graph-modal': GraphModal,
            'full-calendar-modal': FullCalendarModal,
            'cell-comment': CellComment,
            'clock-picker': ClockPicker
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
                    isShowPopover: false,
                    preshow: false
                }
            }
        },
        mounted () {
            EventBus.$on('preshow-cell-comment', (props) => {
                console.log('preshow')
                this.cellComment.tableName = props.tableName
                this.cellComment.fieldName = props.fieldName
                this.cellComment.rowIndex = props.rowIndex
                this.cellComment.isNumber = props.isNumber
                this.cellComment.onlyChat = props.onlyChat
                this.cellComment.preshow = props.preshow
                this.cellComment.isShowPopover = props.show
            })

            EventBus.$on('show-cell-comment', (props) => {
                $('body').css({'overflow': 'hidden'})
                console.log('show')
                this.cellComment.tableName = props.tableName
                this.cellComment.fieldName = props.fieldName
                this.cellComment.rowIndex = props.rowIndex
                this.cellComment.isNumber = props.isNumber
                this.cellComment.onlyChat = props.onlyChat
                this.cellComment.coordX = props.coordX
                this.cellComment.coordY = props.coordY
                this.cellComment.isShowPopover = props.show
                this.cellComment.preshow = props.preshow
            
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
