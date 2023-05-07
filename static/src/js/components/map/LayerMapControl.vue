<script setup>
import { ref, computed, watch } from "vue";
import VisibilityControl from '../utils/VisibilityControl.vue';
import CardExpand from '../utils/CardExpand.vue';
import { getTopLeft } from 'ol/extent';
import { readFeatures,  backendSRID, mapSRID } from "../../reprojection.js"
import { createStyles, MyCircle } from "../../converters.js"
import { circular } from 'ol/geom/Polygon';
import { transform } from 'ol/proj.js';

const props = defineProps({
    "title": String,
    'layers': Array,
    "mountTo": String
});

const vectorLayers = ref([]);

watch(() => props.layers, async (newLayers) => {
    let result_layers = [];
    for(const l of newLayers){
        l.visible = true;
        if(l.layer_type == 'V'){
            let source = [];
            let sourceProjection = 'EPSG:4326';
            let sourceFormat = 'geojson';
            if(l.layer_content.type == 'url'){
                sourceProjection = `EPSG:${l.layer_content.srid}`;
                sourceFormat = l.layer_content.format;
                const supportedFormats = ["geojson", "gml", "overpass"];
                if(!supportedFormats.includes(sourceFormat)){
                    throw new Error(`unsupported format: ${sourceFormat}`)
                }
                const response = await fetch(l.layer_content.url);
                if(!response.ok){
                    throw new Error(`unable to load ${l.layer_content.url}, error ${response.status}`);
                }
                if(sourceFormat == 'geojson' || sourceFormat == 'overpass'){
                    source = await response.json();
                }
                else{
                    source = await response.text();  
                }
            }
            else if(l.layer_content.type == 'internal'){
                source = l.layer_content.geojson;
            }
            else{
                throw new Error(`unsupported type: ${l.layer_content.type}`)
            }
            l.features = readFeatures(source, sourceFormat, sourceProjection);
            const layerStyles = createStyles(l.styles);
            l.features.forEach(feature => {
                const featureStyles = createStyles(feature.get('styles'));
                if(layerStyles != null || featureStyles != null){
                    const style = featureStyles != null ? featureStyles : layerStyles;
                    feature.setStyle(style);
                    // поддержка точных окружностей
                    const exactCircle = style.find(value => value.getImage() instanceof MyCircle && value.getImage().isExact());
                    if(exactCircle != undefined){
                        const geometries = feature.getGeometry()
                                                  .getGeometries()
                                                  .map(geom => {
                                if (geom.getType() == 'Point'){
                                    const center = transform(geom.getFirstCoordinate(), mapSRID, backendSRID);
                                    const circle = circular(center,
                                                    exactCircle.getImage().getRadius(),
                                                    32);
                                    circle.transform(backendSRID, mapSRID);
                                    return circle;
                                }
                                return geom;
                            }
                        );
                        feature.getGeometry().setGeometries(geometries);

                    }
                    
                }
            });
            result_layers.push(l);
        }
        else{
        //TODO
        }
    }
    vectorLayers.value = result_layers;
}, { immediate: true });


const visibleVectorLayers = computed(() => {
    return vectorLayers.value.filter(layer => layer.visible);
});

const vectorsIsVisible = ref(true);

function changeGroupVisibility(){
    vectorsIsVisible.value = !vectorsIsVisible.value;
    vectorLayers.value.forEach(l => l.visible = vectorsIsVisible.value);
}

</script>

<template>

    <SafeTeleport :to="mountTo">
        <CardExpand :title="title" class="mt-2">

            <VisibilityControl 
                title="Векторные слои"
                :expanded="true"
                :visible="vectorsIsVisible"
                @visibilityChanged="changeGroupVisibility">

                <ul class="list-group list-group-flush">
                    <li v-for="l in vectorLayers" :key="l.name" class="list-group-item">
                        <VisibilityControl 
                             :title="l.alias" 
                             :visible="l.visible"
                             :expanded="false"
                             @visibilityChanged="() => l.visible = !l.visible">

                             <ul class="list-group list-group-flush">
                                <li v-for="feature in l.features" :key="feature.getId()" class="list-group-item">
                                    <VisibilityControl :title="feature.get('name')" :visible="true">
                                        <ul class="list-group list-group-flush">
                                            <li v-for="(value, key) in feature.getProperties()" class="list-group-item" >
                                                <div v-if="key != 'geometry'" >
                                                    <b>{{ key }}:</b> {{ value }}
                                                </div>
                                            </li>
                                        </ul>
                                        
                                    </VisibilityControl>
                                 </li>
                             </ul>
                                

                        </VisibilityControl>
                    </li>
                </ul>
            </VisibilityControl>

        </CardExpand>
    </SafeTeleport>

    <ol-vector-layer v-for="layer in visibleVectorLayers" :key="layer.name">
        <ol-source-vector :features="layer.features">
            <ol-overlay v-for="feature in layer.features" 
                        :key="feature.getId()"
                        :position="getTopLeft(feature.getGeometry().getExtent())">
                <div class="p-2">
                    <b>{{ feature.get("name") }}</b>
                </div>
            </ol-overlay>
        </ol-source-vector>
    </ol-vector-layer>

</template>