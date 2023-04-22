<script setup>
import { ref, watch } from "vue";
import {transform} from 'ol/proj.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import DateControl from "./components/DateControl.vue";
import LayersInspector from "./components/LayersInspector.vue";
import {loadAreas, loadLayers, loadLayerContent} from "./api.js"
import AreaSwitcher from "./components/AreaSwitcher.vue";
import Feature from 'ol/Feature.js';
import Polygon from 'ol/geom/Polygon.js';
import { computed } from "@vue/reactivity";

const sourceSRID = 'EPSG:4326';
const distanitionSRID = 'EPSG:3857'
const geoJsonReader = new GeoJSON({
  'dataProjection': sourceSRID, 
  'featureProjection': distanitionSRID
});

const center = ref(transform([34, 68], sourceSRID, distanitionSRID));
const zoom = ref(7);
const view = ref(null)

const areas = ref([]);
const areaCurrent = ref({});
const vectorLayers = ref([]);

loadAreas().then(json => {

  let res = []
  json.forEach(area => {
    let poly = new Polygon(area.bbox.coordinates);
    poly.transform(sourceSRID, distanitionSRID)
    res.push({
      'name': area.name,
      'alias': area.alias,
      'feature': new Feature({
        'geometry': poly,
        'name': area.name,
      })
    });
  });

  areas.value = res;

  if (res.length > 0){
    areaCurrent.value = res[0];
  }

});

watch(areaCurrent, async (newArea) => {
  view.value.fit(newArea.feature.getGeometry(), {duration: 800});
  let layers_json = await loadLayers(newArea.name);
  let result_layers = [];
  for(const l of layers_json){
    if(l.layer_type == 'V'){
      let geojson = await loadLayerContent(newArea.name, l.name);
      l.features = geoJsonReader.readFeatures(geojson);
      result_layers.push(l);
    }
    else{
      //TODO
    }
  }
  vectorLayers.value = result_layers;
});

const areaFeatures = computed(() => {
  return areas.value.map(area => area.feature)
})



function dateChanged(date){
  console.log(date);
}

</script>

<template>

  <ol-map
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      class="flex-grow-1"
    >
      <ol-view
        ref="view"
        :center="center"
        :zoom="zoom"
      />

      <ol-zoom-control />
      <ol-attribution-control />

      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>

      <ol-vector-layer>
        <ol-source-vector :features="areaFeatures">
        </ol-source-vector>
        <ol-style>
          <ol-style-stroke color="orange" :width="7" :lineDash="[10, 12]"></ol-style-stroke>
        </ol-style>
      </ol-vector-layer>

      <ol-vector-layer v-for="layer in vectorLayers">
        <ol-source-vector :features="layer.features">
        </ol-source-vector>
      </ol-vector-layer>

  </ol-map>

  <LayersInspector :layers="vectorLayers"/>
  <AreaSwitcher :areas="areas" v-model="areaCurrent" />
  <DateControl @dateChanged="dateChanged"/>


</template>
 