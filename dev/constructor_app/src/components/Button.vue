<template>
    <button class="btn" v-on:click="onClick">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "Button",
    props: ['onClick']
}
</script>

<style scoped>
.btn {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px 20px;
    height: auto;
    color: #fff;
    border-radius: 6px;
    font-size: 14px;
    background-color: #409eff;
    border: none;
    outline: none;
    transition: 0.2s;
    cursor: pointer;
}
.btn:hover {
    background-color: #3b88e3;
}
</style>