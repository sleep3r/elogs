<template>
    <div class="modal fade" id="MessageToDevelopersModal" tabindex="-1" role="dialog" aria-labelledby="MessageToDevelopersModal" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Отзыв </h5>
                    <div>
                        Оставляйте здесь любые замечания и пожелания по работе системы и мы исправим их при первой возможности!
                    </div>
                </div>
                <div class="modal-body">
                    <div class="alert alert-danger" role="alert" id="message-modal-alert">
                        Введите корректную тему и сообщение!
                    </div>
                    <form>
                        <div class="form-group">
                            <label for="devs-message-theme" class="col-form-label">Тема:</label>
                            <input type="text" class="form-control bordered" id="devs-message-theme" placeholder="Не больше 200 символов" v-model="title">
                        </div>
                        <div class="form-group">
                            <label for="devs-message-text" class="col-form-label">Сообщение:</label>
                            <textarea class="form-control bordered" id="devs-message-text" placeholder="Не больше 1000 символов" v-model="message"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="devs-message-files" class="col-form-label">Изображения:</label>
                            <input type="file" class="form-control bordered" id="devs-message-files" ref="files" multiple accept="image/*" @change="handleFilesUploads()"></input>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn" @click.prevent="onSendMessage">Отправить</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import axios from 'axios';
    export default {
        name: "MessageModal",
        data () {
            return {
                title: '',
                message: '',
                files: '',
            }
        },
        methods: {
            onSendMessage () {
                let formData = new FormData();
                for( var i = 0; i < this.files.length; i++ ){
                      let file = this.files[i];
                      formData.append('file' + i, file);
                }
                formData.append("title", this.title)
                formData.append("message", this.message)
                formData.append("url", window.location.pathname)
                axios.post( 'http://localhost:8000/feedback/send-message',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        },
                        withCredentials: true,
                    })
                    .then(function(){console.log('SUCCESS!!');})
                    .catch(function(){console.log('FAILURE!!');});
            },
            handleFilesUploads() {
                this.files = this.$refs.files.files;
            }
        },
    }
</script>

<style scoped>

</style>
