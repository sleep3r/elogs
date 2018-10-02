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
    </div>
</template>

<script>
    import MessageModal from './MessageModal.vue';
    import SchemeModal from './SchemeModal.vue';
    import AddModeModal from './AddModeModal.vue';

    export default {
        name: "Footer",
        components: {
            'message-modal': MessageModal,
            'schemeModal': SchemeModal,
            'add-mode-modal': AddModeModal
        }
    }
</script>

<style scoped>

</style>