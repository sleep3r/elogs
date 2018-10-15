<template>
    <div class="resp-modal">
        
    </div>
</template>

<script>
    export default {
        name: "ResponsibleModal"
    }
</script>

<style scoped>
.resp-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #ff6c6c;
    opacity: 0;
    transition: 0.2;
    z-index: 100;
}

.resp-modal__open{
    display: block;
    opacity: 0.8;
}
</style>