<script setup>
import { ref } from "vue";

defineProps(['title', "class"])
const emit = defineEmits(["visibilityChanged"])

const isExpanded = ref(true);

function toggle(){
    isExpanded.value = !isExpanded.value
}
</script>

<template>
    <div class="card floating" :class="class">
        <div class="card-header">
            {{  title }}
            <button class="btn btn-secondary float-end" @click="toggle">-</button>
        </div>
        <div v-if="isExpanded" class="card-body">
            <slot></slot>
        </div>
    </div>
</template>