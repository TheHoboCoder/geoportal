<script setup>
import { ref, watch } from "vue";
import {useGeographic, transform} from 'ol/proj.js';
import DateControl from "./components/DateControl.vue";
import LayersInspector from "./components/LayersInspector.vue";
import {loadAreas, loadLayers} from "./api.js"
import AreaSwitcher from "./components/AreaSwitcher.vue";
import Feature from 'ol/Feature.js';
import Polygon from 'ol/geom/Polygon.js';
import { computed } from "@vue/reactivity";

const center = ref(transform([34, 68], 'EPSG:4326', 'EPSG:3857'));
const zoom = ref(7);
const view = ref(null)
const projection1 = ref("EPSG:4326")
const projection2 = ref("EPSG:3857")

const areas = ref([]);
const areaCurrent = ref({});
const layers = ref({});

loadAreas().then(json => {
  areas.value = json;
  if (json.length > 0){
    areaCurrent.value = json[0];
  }
});

const areaFeatures = computed(()=>{
  
})

watch(areaCurrent, (newArea)=>{
  //view.value.fit(newArea.bbox);
  loadLayers(newArea.name).then(json => layers.value = json)
})

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
        :projection="projection2"
      />

      <ol-zoom-control />
      <ol-attribution-control />

      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>

      <ol-vector-layer>
        <ol-source-vector :projection="projection1">
          <ol-feature v-for="area in areas">
            <ol-geom-polygon :coordinates="area.bbox.coordinates"></ol-geom-polygon>
            <ol-style>
              <ol-style-stroke color="red" :width="5"></ol-style-stroke>
              <ol-style-fill color="red"></ol-style-fill>
            </ol-style>
          </ol-feature>
        </ol-source-vector>
      </ol-vector-layer>

  </ol-map>

  <LayersInspector title="test" :layers="layers"/>
  <AreaSwitcher :areas="areas" v-model="areaCurrent" />
  <DateControl @dateChanged="test"/>


</template>
 