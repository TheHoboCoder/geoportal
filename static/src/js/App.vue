<script setup>
import { ref } from "vue";
import { reproject } from "./reprojection";
import DateControl from "./components/DateControl.vue";
import MainMapControl from "./components/map/MainMapControl.vue";
import CommandsControl from "./components/map/CommandsControl.vue";
import CardExpand from "./components/utils/CardExpand.vue";

const center = ref(reproject([34, 68]));
const zoom = ref(7);
const view = ref(null);

const commandsExpanded = ref(false);
const panelExpanded = ref(true);

// TODO: maybe make common state to get current areas
const areaName = ref("");

function dateChanged(date){
  console.log(date);
}

</script>

<template>

    <div id="map-container">

      <div id="control-panel" class="px-2 pt-3 row">

        <div class="button-panel ms-auto p-1" style="width: 10%">
          <button class="btn btn-secondary" 
                  @click="panelExpanded = !panelExpanded"
                  :class="panelExpanded ? '' : 'float-end'">X</button>
        </div>
        
        <div v-if="panelExpanded" class="p-0" style="width: 90%">
          <CardExpand title="Карта">
            <TeleportTarget id="main-block"></TeleportTarget>
          </CardExpand>

          <CardExpand title="Функции" class="mt-3">
              <button class="btn btn-secondary" @click="commandsExpanded = true">Выполнить команду</button>
          </CardExpand>

          <CardExpand v-if="commandsExpanded" title="Команды" class="mt-3">
            <TeleportTarget id="command-block" class="mt-3"></TeleportTarget>
          </CardExpand>
        </div>
    
      </div>

      <ol-map
        :loadTilesWhileAnimating="true"
        :loadTilesWhileInteracting="true"
        id="map-view"
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

          <MainMapControl mount-to="#main-block" :view="view" @area-changed="(name) => areaName = name"/>

          <CommandsControl v-if="commandsExpanded" mount-to="#command-block" :area-name="areaName" />

      </ol-map>

    </div>
    

  <!-- <Teleport to="footer">
    <DateControl @dateChanged="dateChanged"/>
  </Teleport> -->
  
</template>
 