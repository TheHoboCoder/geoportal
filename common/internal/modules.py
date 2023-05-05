import importlib
from .module_filesystem import unzip_file, remove_module_dir
from zipfile import BadZipfile, LargeZipFile

class ModuleLoadException(Exception):
    pass

# информация о модуле
class Module:
    def __init__(self, name, command_list, layer_style_functions, schema):
        self.name = name
        self.command_list = command_list
        self.layer_style_functions = layer_style_functions
        self.schema = schema

class ModulesList:
    def __init__(self):
        self.__module_dict = {}
    
    def install_module(self, module_name):
        config = importlib.import_module(f"{module_name}.module_config", package=None)
        f_l = filter(lambda layer: layer.layer_content is not None 
                                   and layer.layer_content.styling_function is not None, 
                     config.SCHEMA.layers)
        style_functions = {l: l.layer_content.styling_function for l in f_l}
        self.__module_dict[module_name] = Module(module_name, config.COMMANDS,
                                                 style_functions, config.SCHEMA)
        
    def load_module(self, file, module_name):
        try:
            unzip_file(file, module_name)
        except BadZipfile as zip_error:
            remove_module_dir(module_name)
            raise ModuleLoadException(f"Невозможно открыть архив. Проверьте, что файл не поврежден. ({zip_error})") \
                from zip_error
        except OSError as os_error:
            remove_module_dir(module_name)
            raise ModuleLoadException(f"Ошибка при создании файлов: {os_error}") from os_error
        except Exception as err:
            remove_module_dir(module_name)
            raise ModuleLoadException(f"Неизвестная ошибка при распаковке архива: {err}") from err
        
        try:
            importlib.invalidate_caches()
            self.install_module(module_name)
        except ModuleNotFoundError as not_found:
            remove_module_dir(module_name)
            raise ModuleLoadException(f'Невозможно открыть файл конфигурации module_config.py: {not_found}') \
                  from not_found
        except AttributeError as att:
            remove_module_dir(module_name)
            raise ModuleLoadException(f'Ошибка при чтении COMMANDS and SCHEMA: {att}') from att
        except Exception as err:
            remove_module_dir(module_name)
            raise ModuleLoadException(f"Неизвестная ошибка при импортировании конфигурации: {err}") from err
        
    def contains(self, module_name):
        return module_name in self.__module_dict
    
    def __getitem__(self, module_name):
        if module_name not in self.__module_dict:
            self.install_module(module_name)
        return self.__module_dict[module_name]
    
MODULES = ModulesList()
        
