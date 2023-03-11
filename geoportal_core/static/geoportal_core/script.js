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

var layerSwitcher = new ol.control.LayerSwitcher({
    startActive: true,
    activationMode: 'click'
});

map.addControl(layerSwitcher);

var HOST = "http://"+window.location.host
var MODULE = window.location.pathname.split('/')[2]

uploadArea(MODULE, $("#areas").val())

$("#areas").change(function(){
   uploadArea(MODULE, $(this).val())
})

function uploadArea(module_name, name){
    $.ajax(`${HOST}/modules/${module_name}/areas/${name}/`)
    .done(function(data){
        zoomToArea(data);
        uploadVectorLayers(module_name, name)
    })
    .fail(function (t) {
        console.log(`error loading area ${name}`)
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
    $.getJSON(`${HOST}/modules/${module_name}/areas/${area_name}/layers/`, function (data){
        for(var layer of data){
            if (layer.layer_type == 'V'){
                var mapLayer = new ol.layer.Vector({
                    title: layer.alias,
                    source: new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        url: `${HOST}/modules/${module_name}/areas/${area_name}/layers/${layer.name}/`
                    })
                });

                if (vectorGroup.layers == undefined){
                    vectorGroup.setLayers(new ol.Collection([mapLayer]))
                }
                else{
                    vectorGroup.layers.append(mapLayer)
                }
            } 
        } 
        layerSwitcher.renderPanel();
    });
}

$(".command_form").each(function(form){
    $(this).submit(function(event){
        event.preventDefault();
        var command_name = $(this).attr("name")
        $.ajax({
            url: `${HOST}/modules/${MODULE}/commands/${command_name}/`,
            data: $(this).serialize()
        })
        .done(function (data){
            console.log(data);
        })
        .fail(function (data){
            console.log(data);
        })
    })
})

$("#commands").change(function(){
    var val = $(this).val();
    $(".command_form").hide();
    if(val != -1){
        $(`.command_form[name='${val}']`).show();
    }
})