<script setup>
import { ref, watch, computed } from "vue";
import { loadAreas, loadLayers, loadLayerContent } from "../../api.js"
import { reprojectGeometryToMap, readFeatures } from "../../reprojection.js"
import { getTopLeft } from 'ol/extent';
import LayerMapControl from "./LayerMapControl.vue";
import Polygon from 'ol/geom/Polygon.js';
import Feature from 'ol/Feature.js';

const props = defineProps(["view", "mountTo"]);

const areas = ref(null);
const currentAreaName = ref("");
const vectorLayers = ref([]);

loadAreas().then(json => {

    let res = {};
    let name = "";
    json.forEach((area, index) => {
        res[area.name] = {
            'name': area.name,
            'alias': area.alias,
            'feature': new Feature({
                'geometry': reprojectGeometryToMap(new Polygon(area.bbox.coordinates)),
                'name': area.name,
            })
        };
        if(index == 0){
            name = area.name;
        }
    });

    areas.value = res;
    currentAreaName.value = name;

});

const currentArea = computed(() => {
    return areas.value != null ? areas.value[currentAreaName.value] : null;
});


watch(currentArea, async (newArea) => {

    if(newArea == null){
        return;
    }

    // TODO: check view is not null, maybe fire event instead
    props.view.fit(newArea.feature.getGeometry(), {duration: 800});
    let layers_json = await loadLayers(newArea.name);
    let result_layers = [];
    for(const l of layers_json){
        if(l.layer_type == 'V'){
            let geojson = await loadLayerContent(newArea.name, l.name);
            l.visible = true;
            l.features = readFeatures(geojson);
            result_layers.push(l);
        }
        else{
        //TODO
        }
    }
    vectorLayers.value = result_layers;
});

const areaFeatures = computed(() => {
  return areas.value != null ? Object.values(areas.value).map(area => area.feature) : [];
});

</script>

<template>

    <SafeTeleport :to="mountTo">
        <div class="m-2">
            <label for="areaSelect"><b>Выбор области</b></label>
            <select id="areaSelect" class="form-select m-1" v-model="currentAreaName">
                <option v-for="area in areas" :key="area.name" :value="area.name">
                    {{  area.alias }}
                </option>
            </select>
        </div>
    </SafeTeleport>

    <LayerMapControl :vectorLayers="vectorLayers" :mount-to="mountTo" title="Слои карты"/>

    <ol-vector-layer v-if="areas != null">
        <ol-source-vector :features="areaFeatures">
        </ol-source-vector>
        <ol-style>
          <ol-style-stroke color="orange" :width="7" :lineDash="[10, 12]"></ol-style-stroke>
        </ol-style>
        <ol-overlay v-for="(value, k) in areas" 
                    :key="value.feature.getId()"
                    :position="getTopLeft(value.feature.getGeometry().getExtent())">
            <div class="p-2 area-caption">
                <b>{{ value.alias }}</b>
            </div>
        </ol-overlay>
    </ol-vector-layer>
    
</template>

<style>
.area-caption{
    background-color: white;
}
</style>