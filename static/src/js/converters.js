import { Circle, Fill, Stroke, Style } from 'ol/style.js';

function styleParams(obj){
    return {
        'fill': obj.fill ? new Fill(obj.fill) : null,
        'stroke': obj.stroke ? new Stroke(obj.stroke) : null
    };
}

export class MyCircle extends Circle{
    constructor(options){
        super(options);
        this.exact = options ? options.exact : false;
    }

    isExact(){
        return this.exact;
    }
}

export function createStyle(apiStyleObj){

    if(apiStyleObj == undefined || apiStyleObj == null){
        return null;
    }

    const resultParams = styleParams(apiStyleObj);

    if(apiStyleObj.point_style != null){
        const imgParams = styleParams(apiStyleObj.point_style);
        if(apiStyleObj.point_style.type == 'circle'){
            imgParams.exact = apiStyleObj.point_style.exact;
            imgParams.radius = apiStyleObj.point_style.radius;
            if(imgParams.exact){
                resultParams.fill = imgParams.fill;
                resultParams.stroke = imgParams.stroke;
            }
            resultParams.image = new MyCircle(imgParams);
        }
        else{
            // TODO: icons
        }
    }

    return new Style(resultParams);
}

export function createStyles(styles){
    if(styles == undefined || styles.length == 0){
        return null
    }
    return styles.map(value => createStyle(value))
}

// с помощью функции convert () можно заставить Overpass выводить данные,
// в формате, близком к GeoJson. Но его нужно довести до валидного GeoJson
export function overpassJsonToGeojson(json){
    json.type = 'FeatureCollection';
    json.features = json.elements.map(feature => {
        feature.type = "Feature";
        feature.properties = feature.tags;
        delete feature.tags;
        return feature;
    });
    delete json.elements;
    return json;
}