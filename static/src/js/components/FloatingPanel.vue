<script setup>
import { ref } from "vue";

defineProps(['title'])

const isExpanded = ref(true);
var lastPos = null;

function toggle(){
    isExpanded.value = !isExpanded.value
}

function startMove(event){
    lastPos = [event.clientX, event.clientY];
    console.log(lastPos);
}

function moving(event){
    if(lastPos != null){
        var card = event.target.parentElement;
        card.style.left = (card.offsetLeft + event.clientX - lastPos[0]) + "px";
        card.style.top = (card.offsetTop + event.clientY - lastPos[1]) + "px";
        lastPos[0] = event.clientX;
        lastPos[1] = event.clientY;
    }
}

function endMove(event){
    lastPos = null;
}

</script>

<template>
    <div class="card floating">
        <div class="card-header"
            @mousedown="startMove"
            @mousemove="moving"
            @mouseup="endMove"
        >
            {{  title }}
            <button class="btn btn-secondary pull-right" @click="toggle">-</button>
        </div>
        <div v-if="isExpanded" class="card-body">
            <slot></slot>
        </div>
    </div>
</template>

<style>
.floating{
    position: absolute;
    min-width: 300px;
}
</style>