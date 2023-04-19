<script setup>
import { ref } from "vue";
import {useGeographic, transform} from 'ol/proj.js';

const center = ref(transform([34, 68], 'EPSG:4326', 'EPSG:3857'));
const zoom = ref(7);

</script>

<template>
    <ol-map
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      style="height:100vh"
    >
      <ol-view
        ref="view"
        :center="center"
        :zoom="zoom"
      />
  
      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>

    </ol-map>
</template>
 

<script>
export default {
};
</script>