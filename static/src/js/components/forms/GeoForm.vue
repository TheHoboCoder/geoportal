<script setup>
import GeoField from './GeoField.vue';
const props = defineProps([
    'formFields', 
    'requiredFields', 
    'errorMessages', 
    "currentGeomFieldName"
]);
defineEmits(["submit", "startAdd", "startEdit", "delete"])
import { ref } from "vue";

let pam = {}
for (const key in props.formFields){
    pam[key] = "";
    if(props.formFields[key].type == "boolean"){
        pam[key] = false;
    }
}

const formVars = ref(pam);

function onSubmit(event){
    console.log(Object.entries(formVars.value))
}

let supportedTypes = ["integer", "number", "string", "boolean"]

function isSimple(field_value){
    return Array.isArray(field_value.type) || 
           supportedTypes.includes(field_value.type) && !Object.hasOwn(field_value, 'geom_type');
}

function isInvalid(fieldName){
    return props.errorMessages != null && Object.hasOwn(props.errorMessages, fieldName);
}

</script>

<template>
    <form @submit.prevent="$emit('submit', formVars)">
        <div class="form-group" v-for="(field_value, field_name) in formFields">
            <label :for="field_name">
                {{ field_value.title }}
            </label>

            <FormElement v-if="isSimple(field_value)"
                         :fieldName="field_name" 
                         :fieldDef="field_value"
                         v-model="formVars[field_name]"
                         :requiredArray="requiredFields"
                         :class="isInvalid(field_name) ? 'is-invalid' : ''"/>

            <GeoField v-else-if="Object.hasOwn(field_value, 'geom_type')"
                        :fieldName="field_name" 
                        :geometryType="field_value.geom_type"
                        :disabled="currentGeomFieldName != '' && currentGeomFieldName != field_name"
                        @startAdd="(name, type) => $emit('startAdd', name)"
                        @startEdit="(name, type) => $emit('startEdit', name)"
                        @delete="(name) => $emit('delete', name)"
                        :class="isInvalid(field_name) ? 'is-invalid' : ''"
            />
            <div v-else>
                unsupported yet
            </div>
            <div class="invalid-feedback" v-if="isInvalid(field_name)">
                {{ props.errorMessages[field_name].join() }}
            </div>
        </div>
        <button type="submit"  class="btn btn-primary">Submit</button>
    </form>
</template>