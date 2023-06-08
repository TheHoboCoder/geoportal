import { h } from 'vue'

function formInput(fieldDef, defaultAttribs){

    let field_type = "";
    switch(fieldDef.type){
        case "integer":
        case "number":
            field_type = "number";
            break;

        case "boolean":
            field_type = "checkbox";
            break;

        case "string":
            field_type = "text";
            break;
    }

    if(fieldDef.type == "number"){
        defaultAttribs["step"] = "0.001"
    }

    defaultAttribs.type = field_type;
    defaultAttribs.class = field_type == "checkbox" ? "form-check-input" : "form-control";
    let mapping = {
        "minimum": "min",
        "maximum": "max",
        "minLength": "minlength",
        "maxLength": "maxlength",
    };

    for(const [key, value] in Object.entries(mapping)){
        if(Object.hasOwn(fieldDef, key)){
            defaultAttribs[value] = fieldDef[key];
        }
    }
    return h('input', defaultAttribs);
}

function select(fieldDef, defaultAttribs){
    let values = fieldDef.enum;
    if(Object.hasOwn(fieldDef, "enumNames")){
        values = fieldDef.enumNames;
    }
    return h('select', defaultAttribs, fieldDef.enum.map((value, index) => {
        return h('option', {'value': value}, values[index])
    }))
}

export default {
  props: ["fieldName", "fieldDef", "modelValue", "requiredArray"],
  emits: ['update:modelValue'],
  setup(props, {emit}) {
    return () => {

        let defaultAttribs = {
            "fieldName": props.fieldName, 
            "value": props.modelValue,
            'onInput': (event) => emit('update:modelValue', event.target.value),
            "class": "form-control"
        }

        if (props.requiredArray.includes(props.fieldName) && props.fieldDef.type != "boolean"){
            defaultAttribs.required = true;
        }

        if(props.fieldDef.type == "boolean"){
            delete defaultAttribs["onInput"];
            defaultAttribs["onClick"] = (event) => emit('update:modelValue', event.target.checked);
        }

        if(Object.hasOwn(props.fieldDef, "enum")){
            defaultAttribs.choices = props.fieldDef.choices;
            return select(props.fieldDef, defaultAttribs);
        }

        return formInput(props.fieldDef, defaultAttribs);

    }
  }
}

