ol.proj.useGeographic();

var vectorGroup = new ol.layer.Group({
    title: 'Векторные слои',
    layers: new ol.Collection()
});

var areaLayer = new ol.layer.Vector({
    title: 'Область',
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'orange',
          width: 7,
          lineDash: [10, 12]
        }),
      }),
    source: new ol.source.Vector()
})

var mapView = new ol.View({
    center: [34, 68],
    zoom: 7,
});

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Group({
            title: 'Подложка',
            type: 'base',
            layers: [
                new ol.layer.Tile({
                    title: 'OSM',
                    source: new ol.source.OSM()
                })
            ]
        }), 
        vectorGroup,
        areaLayer
    ],
    view: mapView
  });

map.addControl(new ol.control.LayerSwitcher({
    startActive: true,
    activationMode: 'click'
}));

$.getJSON("modules/", function (data){
    uploadAreas(data[0].name)
    for(var module of data){
        $("#modules").append(`<option value='${module.name}'>${module.alias}</option>`)
    }
});

function uploadAreas(name){
    $.getJSON(`modules/${name}/areas/`, function (data){
        zoomToArea(data[0])
        uploadVectorLayers(name, data[0].name)
        for(var area of data){
            $("#areas").append(`<option value='${area.name}'>${area.alias}</option>`)
        }  
    });
}

function zoomToArea(area){
    areaLayer.getSource().clear();
    var poly = new ol.geom.Polygon(area.bbox.coordinates)
    areaLayer.getSource().addFeature(new ol.Feature({
        geometry: poly,
        name: area.alias
    }));
    mapView.fit(poly, {duration: 800})
}

function uploadVectorLayers(module_name, area_name){
    $.getJSON(`modules/${module_name}/areas/${area_name}/`, function (data){
        for(var layer of data){
            if (layer.layer_type == 'V'){
                $.getJSON(`modules/${module_name}/areas/${area_name}/${layer.name}/`, function (json){
                    // mapView.fit(json.features[0].bbox, {duration: 800})
                    var mapLayer = new ol.layer.Vector({
                        title: layer.alias,
                        source: new ol.source.Vector({
                            features: new ol.format.GeoJSON().readFeatures(json)
                        })
                    });
                    if (vectorGroup.layers == undefined){
                        vectorGroup.setLayers(new ol.Collection([mapLayer]))
                    }
                    else{
                        vectorGroup.layers.append(mapLayer)
                    }
                    
                })
            } 
        } 
    });
}