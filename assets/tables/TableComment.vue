<template>
    <div class="table__comment">
        <a href="javascript:;" onclick="Comment.collapse(this)">Комментарий </a>
        <i class="fas fa-envelope ico-comment"></i>
        <div class="comment__text collapse ">
            <textarea class="table-comment" name="comment" table-name="vsns" journal-page="1283" oninput="FormTable.onInput(this)" placeholder="Комментарий..." title="" readonly="readonly"></textarea>
        </div>
    </div>
</template>
<script>
export default {
  name: 'table-comment',
  props: {

  }
}
</script>