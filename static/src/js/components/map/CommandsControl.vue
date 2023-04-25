<script setup>
import { ref, watch, computed } from "vue";
import { loadCommands, runCommand } from "../../api.js"
import GeoForm from "../forms/GeoForm.vue";

const props = defineProps(["mountTo"]);

const commands = ref({});
const errorFields = ref({});
const selectedCommandName = ref("");

const geoFields = ref({});

loadCommands().then(json => commands.value = json);

function submitForm(params){
  runCommand(currentCommand.value.name, params)
  .then(async (response) => {
    if(response.status == 400){
      errorFields.value = await response.json();
    }
    else{
      console.log(await response.json());
    }
  })
}

const currentCommand = computed(() => {
    if(selectedCommandName.value != "" && commands.value != {}){
        return commands.value[selectedCommandName.value];
    }
    return null;
});

const commandSchema = computed(() => {
    return currentCommand.value != null ? currentCommand.value.schema.properties : null;
})

const requiredFields = computed(() => {
    return currentCommand.value != null ? currentCommand.value.schema.required : null;
})


</script>

<template>

    <Teleport :to="mountTo">
        <div class="m-2">
            <label for="commandSelect"><b>Выберите команду</b></label>
            <select id="areaSelect" class="form-select m-1" v-model="selectedCommandName">
                <option></option>
                <option v-for="(command, name) in commands" 
                        :key="command.name" :value="command.name">
                    {{  command.alias }}
                </option>
            </select>
        </div>
        <div v-if="commandSchema != null" class="m-3">
            <GeoForm 
                :form-fields="commandSchema" 
                :requiredFields="requiredFields"
                :error-messages="errorFields"
                @submit="submitForm"/>
        </div>
    </Teleport>

</template>