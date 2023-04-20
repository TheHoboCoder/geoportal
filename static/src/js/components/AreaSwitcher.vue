<script setup>
import FloatingPanel from './FloatingPanel.vue';
const props = defineProps(["areas", "modelValue"])
defineEmits("update:modelValue")
</script>

<template>
    <FloatingPanel title="Области">
        <ul class="list-group list-group-flush">
            <li v-for="area in areas" 
                class="list-group-item list-group-item-action"
                :class="area == modelValue ? 'active' : ''"
                @click="$emit('update:modelValue', area)">
                {{ area.alias }}
            </li>
        </ul>
    </FloatingPanel>
</template>