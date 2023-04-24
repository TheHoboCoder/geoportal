import '../css/style.css';
import { createApp } from 'vue';
import formElement from './components/forms/formElement';
 
import App from './App.vue';
import OpenLayersMap from "vue3-openlayers";
import "vue3-openlayers/dist/vue3-openlayers.css";
 
const app = createApp(App);
app.component("FormElement", formElement);
app.use(OpenLayersMap);
app.mount("#app");