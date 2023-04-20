let path = window.location.pathname.split('/');
path.shift()
path.pop();
const MODULE = path[path.length - 1];
path.pop();
path.pop();
let last = path.length > 0 ? "/" + path[path.length - 1] : "";
const HOST = window.location.protocol + "//" + window.location.host + last;

export async function loadAreas(){
    let response = await fetch(`${HOST}/modules/${MODULE}/areas/`);
    if(response.ok){
        return await response.json()
    }
    else{
        console.log("error load areas")
        return {};
    }
}

export async function loadLayers(area_name){
    let response = await fetch(`${HOST}/modules/${MODULE}/areas/${area_name}/layers/`);
    if(response.ok){
        return await response.json()
    }
    else{
        console.log("error load areas")
        return {};
    }
}


