<script setup>
import { ref, computed } from "vue";

import VisibilityControl from '../utils/VisibilityControl.vue';
import CardExpand from '../utils/CardExpand.vue';
const props = defineProps({
    "vectorLayers": Array, 
    "mountTo": String
});

const visibleVectorLayers = computed(() => {
    return props.vectorLayers.filter(layer => layer.visible);
});

const vectorsIsVisible = ref(true);

function changeGroupVisibility(){
    vectorsIsVisible.value = !vectorsIsVisible.value;
    props.vectorLayers.forEach(l => l.visible = vectorsIsVisible.value);
}

</script>

<template>

    <Teleport :to="mountTo">
        <CardExpand title="Слои карты">

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
    </Teleport>

    <ol-vector-layer v-for="layer in visibleVectorLayers" :key="layer.name">
        <ol-source-vector :features="layer.features">
        </ol-source-vector>
    </ol-vector-layer>

</template>