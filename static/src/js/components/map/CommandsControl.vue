<script setup>
import { ref, watch, computed, inject } from "vue";
import { loadCommands, runCommand } from "../../api.js"
import GeoForm from "../forms/GeoForm.vue";
import { featureToWKT, readFeatures } from "../../reprojection.js"
import LayerMapControl from "./LayerMapControl.vue";
import {getTopLeft} from 'ol/extent';

const props = defineProps(["mountTo"]);
const commands = ref({});
const errorFields = ref({});
const selectedCommandName = ref("");
const layers = ref([]);

loadCommands().then(json => commands.value = json);


const currentCommand = computed(() => {
    if(selectedCommandName.value != "" && commands.value != {}){
        return commands.value[selectedCommandName.value];
    }
    return null;
});

const commandSchema = computed(() => {
    return currentCommand.value != null ? currentCommand.value.schema.properties : null;
});

const requiredFields = computed(() => {
    return currentCommand.value != null ? currentCommand.value.schema.required : null;
});

const geoFields = ref({});
const currentGeomFieldName = ref("");

watch(commandSchema, (newSchema) => {

    if (newSchema == null){
        geoFields.value = {};
        return;
    }
       
    geoFields.value = Object.fromEntries(
        Object.entries(newSchema).filter(value => {
            return Object.hasOwn(value[1], 'geom_type');
        }).map(value => {
            const [key, val] = value;
            return [key, {
                'name': key,
                'alias': val.title,
                'visible': true,
                'drawEnabled': false,
                'editEnabled': false,
                'geom_type': val.geom_type,
                'features': []
            }];
        })
    );
});

function startAdd(field_name){
    currentGeomFieldName.value = field_name;
    if(geoFields.value[field_name].features.length > 0){
        geoFields.value[field_name].features = [];
    }
    geoFields.value[field_name].drawEnabled = true;
}

function drawEnded(event){
    geoFields.value[currentGeomFieldName.value].drawEnabled = false;
    geoFields.value[currentGeomFieldName.value].features.push(event.feature.clone())
    currentGeomFieldName.value = "";
}

function deleteField(field_name){
    geoFields.value[field_name].features = [];
    currentGeomFieldName.value = "";
}

function submitForm(params){

  Object.entries(geoFields.value).forEach(value => {
    const [key, val] = value;
    if(val.features.length > 0){
        params[key] = featureToWKT(val.features[0]);
        console.log(params[key]);
    }
  });
  
  runCommand(currentCommand.value.name, params)
  .then(async (response) => {
    if(response.status == 400){
      errorFields.value = await response.json();
    }
    else{
      const json = await response.json();
      errorFields.value = {};
      layers.value.push({
         'name': currentCommand.value.name+`_res_${layers.length + 1}`,
         'alias': `Результат выполнения команды ${currentCommand.value.name}`,
         'visible': true,
         'features': readFeatures(json.gis_data)
      });
    }
  })
}

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
                :current-geom-field-name="currentGeomFieldName"
                @startAdd="startAdd"
                @delete="deleteField"
                @submit="submitForm"/>
        </div>
    </Teleport>

    <ol-vector-layer v-for="(value, name) in geoFields" :key="name">
        <ol-source-vector :features="value.features">
            <ol-overlay v-for="feature in value.features" 
                        :key="feature.getId()"
                        :position="getTopLeft(feature.getGeometry().getExtent())">
                <div class="p-2">
                    <b>{{ value.alias }}</b>
                </div>
            </ol-overlay>
        </ol-source-vector>
    </ol-vector-layer>

    <template v-for="(value, name) in geoFields" :key="name">
        <ol-vector-layer v-if="value.drawEnabled">
            <ol-source-vector>
                <ol-interaction-draw
                    :type="value.geom_type"
                    @drawend="drawEnded"
                >
                </ol-interaction-draw>

            </ol-source-vector>
        </ol-vector-layer>
    </template>

    <LayerMapControl v-if="layers.length > 0" :vectorLayers="layers" :mount-to="mountTo" />
    

</template>

<!-- <style>
.geom-text{
    background-color: white;
}
</style> -->