<template>
    <tr class="setting-item">
        <td>
            <!--<i @click="markAsFavorite" :class="{ marked: isFavorite, 'material-icons': true }">star_rate</i>-->
        </td>
        <td>{{model.name}}</td>
        <td>{{title}}</td>
        <td>
            <button class="btn btn-info" style="font-size: 10px;"><i @click="editModel()" class="material-icons" >build</i></button>&nbsp;
            <code>{{model.value}}</code>
        </td>
        <td></td>
        <td>
            <code>{{model.scope}}</code>
        </td>
    </tr>
</template>

<script>
    export default {
        name: "setting-item",
        props: {
            model: Object
        },
        data() {
            return {
                type: 'text',
                isEditing: false
            }
        },
        computed: {
            title: function () {
                return this.model.scope.name;
            },
            isFavorite: function () {
                if (!this.model) return false;
                return this.model.isFavorite;
            }
        },
        methods: {
            editModel(){
                // console.log(this.$parent);

                this.$store.commit('settingsState/SET_CURRENT_MODEL', this.model);
                this.$parent.isEditing = true;
            },
            markAsFavorite(){
                console.log("mark as favorite");
                this.model.isFavorite = !this.model.isFavorite;
            },
        },
        mounted() {
            this.type = this.model.type;
        }
    }
</script>

<style scoped>
    .setting-item th:first-child, td:first-child {
        width: 130px;
    }

    label {
        margin-right: 10px;
        font-weight: bold;
    }
    .marked {
        color: #FF0000;
    }
</style>