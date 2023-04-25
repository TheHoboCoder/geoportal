import GeoJSON from 'ol/format/GeoJSON.js';
import {transform} from 'ol/proj.js';

export const sourceSRID = 'EPSG:4326';
export const distanitionSRID = 'EPSG:3857'
export const geoJsonReader = new GeoJSON({
  'dataProjection': sourceSRID, 
  'featureProjection': distanitionSRID
});

export function reproject(coords){
    return transform(coords, sourceSRID, distanitionSRID);
}