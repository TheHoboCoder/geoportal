// TODO: find better way
// из url извлекаем имя текущего модуля (последний элемент)
// а также корневой адрес, относительно которого находится api
// для сервера может быть, что корневой адрес != хост
let path = window.location.pathname.split('/');
// удаляем пустые строки в начале и конце
path.shift()
path.pop();
const MODULE = path[path.length - 1];
// URL: <корневой_адрес>/map/<module_name>. 
// Удаляем последние два элемента, остается <корневой_адрес>
path.pop();
path.pop();
let last = path.length > 0 ? "/" + path[path.length - 1] : "";
const HOST = window.location.protocol + "//" + window.location.host + last;

const fetchParams = {
    method: 'GET',
    mode: 'same-origin',
    headers: {
        'Content-type': 'application/json'
    }
};

async function fetchApi(url, error_msg, params=null){
    if(params != null){
        url = url+"?"+URLSearchParams(params)
    }
    let response = await fetch(url, fetchParams);
    if(response.ok){
        return await response.json()
    }
    throw new Error(error_msg);
}

export async function loadAreas(){
    return fetchApi(`${HOST}/modules/${MODULE}/areas/`, "can't load areas")
}

export async function loadLayers(area_name){
    return fetchApi(`${HOST}/modules/${MODULE}/areas/${area_name}/layers/`, 
                    "can't load area layers")
}

export async function loadLayerContent(area_name, layer_name){
    console.log(`In api host: ${HOST}`);
    return fetchApi(`${HOST}/modules/${MODULE}/areas/${area_name}/layers/${layer_name}`, 
                    "can't load layer content")
}

export async function loadCommands(){
    console.log(`In api host: ${HOST}`);
    return fetchApi(`${HOST}/modules/${MODULE}/commands/`, 
                    "can't load commands")
}

export async function runCommand(commandName, params, area_name){
    params = { 
        ...params, 
        'area_name': area_name, 
    };
    return await fetch(`${HOST}/modules/${MODULE}/commands/${commandName}?`
                        + (new URLSearchParams(params)));
}

