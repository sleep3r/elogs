<template>
    <div class="input-container">
        <span class="label">{{ label }}</span>
        <input class="input" type="text" v-model="initialValue" @input="$emit('change', initialValue)" :placeholder="placeholder">
    </div>
</template>

<script>
    export default {
        name: "FormInput",
        props: ['label', 'placeholder', 'value'],
        data () {
            return {
                initialValue: this.value
            }
        }
    }
</script>

<style scoped>
.input-container {
    margin: 20px 0;
}
.label {
    display: block;
    opacity: 0.8;
    margin-bottom: 6px;
}
.input {
    width: 100%;
    background-color: #fff;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    box-sizing: border-box;
    color: #606266;
    display: inline-block;
    font-size: inherit;
    height: 40px;
    line-height: 40px;
    outline: none;
    padding: 0 15px;
    transition: 0.2s;
}
.input::placeholder {
    color: #b5b5b5
}
.input:focus {
    border-color: #409eff
}
</style>