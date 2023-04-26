import GeoJSON from 'ol/format/GeoJSON.js';
import WKT from 'ol/format/WKT.js';
import {transform} from 'ol/proj.js';

export const backendSRID = 'EPSG:4326';
export const mapSRID = 'EPSG:3857'

const params = {
  'dataProjection': backendSRID, 
  'featureProjection': mapSRID,
};

const geoJsonReader = new GeoJSON(params);
const wktWriter = new WKT();

export function reproject(coords){
    return transform(coords, backendSRID, mapSRID);
}

export function readFeatures(geojson){
  return geoJsonReader.readFeatures(geojson);
}

export function featureToWKT(feature){
  return wktWriter.writeFeature(feature, params);
}

export function reprojectGeometryToMap(geometry){
  return geometry.transform(backendSRID, mapSRID)
}

