<template>
    <div class="alert-modal">
        <div class="alert-modal-content">
            <h2 class="alert-modal-title">Продолжить?</h2>
            <p class="alert-modal-sub-title">{{text}}</p>
            <div class="alert-modal-btns">
                <button class="btn" @click="() => {onOk(); closeModal()}">Да</button>
                <button class="btn" @click="onCancelClick">Нет ( {{expTime}} )</button>
            </div>
        </div>
    </div>
</template>

<script>
    import EventBus from '../EventBus'

    export default {
        name: "AlertModal",
        data () {
            return {
                timer: null,
                expTime: 60,
                text: '',
                onOk: () => {}
            }
        },
        methods: {
            startTicking () {
                this.timer = setInterval(() => {
                    if (!this.expTime) {
                        this.onCancelClick()
                    }
                    else this.expTime--
                }, 1000)
            },
            stopTicking () {
                this.timer = clearInterval(this.timer)
            },
            onCancelClick () {
                this.closeModal()
            },
            closeModal () {
                console.log('closed', this.expTime, this.timer)
                $('.alert-modal').removeClass('alert-modal__open')
                this.stopTicking()
                setTimeout(() => this.expTime = 60, 200)
            }
        },
        mounted () {
            EventBus.$on('open-alert', ({text, onOk}) => {
                $('.alert-modal').addClass('alert-modal__open')
                this.text = text
                this.onOk = onOk
                this.startTicking()
            })
            EventBus.$on('close-alert', () => {
                this.closeModal()
            })
        }
    }
</script>

<style lang='scss' scoped>
.alert-modal {
    display: flex;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #008BB9;
    color: white;
    padding: 200px 10px;
    visibility: hidden;
    opacity: 0;
    transition: 0.2s;
    z-index: 100;
}

.alert-modal__open {
    visibility: visible;
    opacity: 0.9;
}

.alert-modal-content {
    max-width: 600px;
    text-align: center;
}

.alert-modal-title {
    margin-bottom: 30px;
}

.alert-modal-sub-title {
    font-size: 20px;
}

.alert-modal-btns {
    display: flex;
    justify-content: center;
}

.alert-modal-btns .btn {
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
