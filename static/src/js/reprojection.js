import GeoJSON from 'ol/format/GeoJSON.js';
import GML3 from 'ol/format/GML3.js';
import WKT from 'ol/format/WKT.js';
import { transform, transformExtent } from 'ol/proj.js';
import { overpassJsonToGeojson } from './converters';

export const backendSRID = 'EPSG:4326';
export const mapSRID = 'EPSG:3857'

const formatters = {
  'geojson': new GeoJSON(),
  'gml': new GML3(),
}

const wktWriter = new WKT();

export function reproject(coords){
    return transform(coords, backendSRID, mapSRID);
}

export function reprojectExtent(extent){
  return transformExtent(extent, backendSRID, mapSRID);
}

export function readFeatures(source, sourceFormat, sourceSrid){
  if(sourceFormat == 'overpass'){
    source = overpassJsonToGeojson(source);
    sourceFormat = 'geojson';
  }
  return formatters[sourceFormat].readFeatures(source, {
    'dataProjection': sourceSrid,
    'featureProjection': mapSRID,
  });
}

export function featureToWKT(feature){
  return wktWriter.writeFeature(feature, {
    'dataProjection': backendSRID, 
    'featureProjection': mapSRID,
  });
}

export function reprojectGeometryToMap(geometry){
  return geometry.transform(backendSRID, mapSRID)
}

