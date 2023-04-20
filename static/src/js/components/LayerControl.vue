<script setup>
import { ref } from "vue";
const props = defineProps(['layer'])
const emit = defineEmits(["visibilityChanged"])

const visible = ref(true)

function flipVisibility(){
    visible.value = !visible.value;
    emit("visibilityChanged", props.layer.name, visible.value);
}
</script>

<template>
    <p>
        <input type="checkbox" :checked="visible" @input="flipVisibility" class="form-check-input">
        {{ layer.alias }}
    </p>
</template>