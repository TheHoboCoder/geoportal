<script setup>
import { ref } from "vue";

const emit = defineEmits(['dateChanged'])

const currentDate = ref((new Date(Date.now())).toISOString())

emit("dateChanged", currentDate.value)
function setDate(event){
    currentDate.value = event.target.value
    emit("dateChanged", currentDate.value)
}
</script>

<template>
    <div class="dc">
        <input class="datepicker" :value="currentDate" @input="setDate" type="datetime-local">
    </div>
</template>

<style>
.dc{
    height: 50px;
}
</style>