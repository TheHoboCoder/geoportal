<script setup>
import FloatingPanel from './FloatingPanel.vue';
import LayerControl from './LayerControl.vue';
defineProps(["layers"])

</script>

<template>
    <FloatingPanel title="Слои">
        <ul class="list-group list-group-flush">
            <li v-for="l in layers" class="list-group-item">
                <LayerControl :layer="l" :id="l.name"/>
            </li>
        </ul>
    </FloatingPanel>
</template>