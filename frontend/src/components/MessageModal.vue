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
                            <label for="recipient-name" class="col-form-label">Тема:</label>
                            <input type="text" class="form-control bordered" id="devs-message-theme" placeholder="Не больше 200 символов">
                        </div>
                        <div class="form-group">
                            <label for="message-text" class="col-form-label">Сообщение:</label>
                            <textarea class="form-control bordered" id="devs-message-text" placeholder="Не больше 1000 символов"></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" onclick="FeedBack.send()">Отправить</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: "MessageModal"
    }
</script>

<style scoped>

</style>