<script setup>
import { ref } from "vue";

const props = defineProps({
    'title': String, 
    'visible': Boolean,
    'expanded': Boolean
});

const emit = defineEmits(["visibilityChanged"])

const isExpanded = ref(props.expanded == null ? false : props.expanded);

function toggle(){
    isExpanded.value = !isExpanded.value
}

</script>

<template>
    <p>
        <input type="checkbox" 
                class="form-check-input"
               :checked="visible" 
               @click="$emit('visibilityChanged')" >
        {{ title }}
        <button @click="toggle" class="btn btn-secondary ms-1 float-end">-</button>
    </p>
    <div v-if="isExpanded">
        <slot></slot>
    </div>
</template>


