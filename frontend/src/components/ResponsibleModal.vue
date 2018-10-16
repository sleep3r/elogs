<template>
    <div class="resp-modal">
        <div class="resp-modal-content">
            <h2 class="resp-modal-title">Продолжить?</h2>
            <p class="resp-modal-sub-title">Вы будете назначены ответственным за этот журнал после начала его редактирования</p>
            <div class="resp-modal-btns">
                <button class="btn" @click="onOkClick">Да</button>
                <button class="btn" @click="onCancelClick">Нет ( {{expTime}} )</button>
            </div>
        </div>
    </div>
</template>

<script>
    import EventBus from '../EventBus'

    export default {
        name: "ResponsibleModal",
        data () {
            return {
                timer: null,
                expTime: 60
            }
        },
        methods: {
            startTicking () {
                this.timer = setInterval(() => {
                    if (this.expTime === 0) {
                        this.onCancelClick()
                    }

                    this.expTime--
                }, 1000)
            },
            stopTicking () {
                this.timer = clearInterval(this.timer)
            },
            onOkClick () {
                this.onCancelClick()
            },
            onCancelClick () {
                $('.resp-modal').removeClass('resp-modal__open')
                this.stopTicking()
                this.expTime = 60
            }
        },
        mounted () {
            EventBus.$on('open-resp-modal', () => {
                this.startTicking()
            })
        }
    }
</script>

<style lang='scss' scoped>
.resp-modal {
    display: flex;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #548CB7;
    color: white;
    padding: 200px 10px;
    visibility: hidden;
    opacity: 0;
    transition: 0.2s;
    z-index: 100;
}

.resp-modal__open {
    visibility: visible;
    opacity: 0.9;
}

.resp-modal-content {
    max-width: 600px;
    text-align: center;
}

.resp-modal-title {
    margin-bottom: 30px;
}

.resp-modal-sub-title {
    font-size: 20px;
}

.resp-modal-btns {
    display: flex;
    justify-content: center;
}

.resp-modal-btns .btn {
    min-width: 120px;
    background-color: #386486;

    &:first-child {
        margin-right: 10px;
    }

    &:hover {
        background-color: #24435a;
    }
}
</style>