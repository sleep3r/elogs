<template>
    <div class="modal fade" id="SchemeModal" tabindex="-1" role="dialog" aria-labelledby="SchemeModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-large" role="document">
            <div class="modal-content modal-content-large">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Схема цехов </h5>
                </div>
                <div class="modal-body">
                    <embed :src="require('../assets/pdf/scheme.pdf')" width="100%" height="100%"></embed>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: "SchemeModal"
    }
</script>

<style scoped>
    #scheme {
        width: 100%;
    }
</style>