<script setup>
import { ref, computed } from "@vue/reactivity";
const props = defineProps(['fieldName', 'geometryType', "disabled"])
const emit = defineEmits(["startAdd", "startEdit", "delete"]);

const selected = ref(false)
const status = computed(() => {
    return selected.value ? "Выбрано" : "Не выбрано"
});

const statusClass = computed(() => {
    return selected.value ? "text-success" : "text-danger"
});

function deleteFeature(){
    selected.value = false;
    emit("delete", props.fieldName);
}

</script>

<template>
    <div class="pb-2">
        <span :class="statusClass">
            {{ status }}
        </span>

        <input type="button" 
               :disabled="disabled"
               @click="deleteFeature"
               class="btn btn-primary ms-1 float-end" 
               value="✖">

        <input type="button" 
               :disabled="disabled"
               @click="$emit('startEdit', fieldName, geometryType)"
               class="btn btn-primary ms-1 float-end" 
               value="🖉">

        <input type="button"
               :disabled="disabled"
               @click="$emit('startAdd', fieldName, geometryType)"
               class="btn btn-primary ms-1 float-end" value="+">
        
    </div>
    
</template>