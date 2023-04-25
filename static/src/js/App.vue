<script setup>
import { ref } from "vue";
import { reproject } from "./reprojection";
import DateControl from "./components/DateControl.vue";
import MainMapControl from "./components/map/MainMapControl.vue";
import CommandsControl from "./components/map/CommandsControl.vue";


const center = ref(reproject([34, 68]));
const zoom = ref(7);
const view = ref(null);


function dateChanged(date){
  console.log(date);
}

</script>

<template>


    <ol-map
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      style="height: 100%"
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

      <MainMapControl mount-to="#main-block" :view="view"/>

      <CommandsControl mount-to="#command-block" />

    </ol-map>

  <Teleport to="footer">
    <DateControl @dateChanged="dateChanged"/>
  </Teleport>
  
</template>
 