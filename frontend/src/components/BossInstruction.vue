<template>
    <div class="modal fade pdf__modal" id="BossInstruction" tabindex="-1" role="dialog" aria-labelledby="BossInstruction" aria-hidden="true">
        <div class="modal-dialog modal-dialog-large" role="document">
            <div class="modal-content modal-content-large">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Инструкция для руководства </h5>
                </div>
                <div class="modal-body">
                    <embed :src="require('../assets/pdf/boss.pdf')" width="100%" height="100%"></embed>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: "BossInstruction"
    }
</script>

<style scoped>

</style>
