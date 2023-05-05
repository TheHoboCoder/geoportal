from unittest import TestCase
import common.internal.module_filesystem as utils
import os, shutil, sys
from zipfile import ZipFile, BadZipfile
from pathlib import Path

class TestModuleFilesystem(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_path = Path(__file__).resolve().parent
        cls.module_path = os.path.join(cls.base_path, 'modules')
        if os.path.exists(cls.module_path):
            shutil.rmtree(cls.module_path)
        os.mkdir(cls.module_path)
        open(os.path.join(cls.module_path, "__init__.py"), "x").close()
        if cls.module_path not in sys.path:
            sys.path.insert(0, cls.module_path)
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.module_path):
            shutil.rmtree(cls.module_path)
        if cls.module_path in sys.path:
            sys.path.remove(cls.module_path)

    def test_zip_corrupted(self):
        with open(os.path.join(self.base_path, "assets", "wrong_zipped.zip"), "r+b") as f:
            with self.assertRaises(BadZipfile):
                utils.unzip_file(f, 'test_zipped', path=self.module_path)
            utils.remove_module_dir('test_zipped')

    def test_no_config(self):
        with open(os.path.join(self.base_path, "assets" , "no_config.zip"), "r+b") as f:
            utils.unzip_file(f, 'test_no_config', path=self.module_path)
            with self.assertRaises(ModuleNotFoundError):
                utils.try_import('test_no_config')
            utils.remove_module_dir('test_no_config')

    def test_wrong_config(self):
        with open(os.path.join(self.base_path, "assets" , "wrong_config.zip"), "r+b") as f:
            utils.unzip_file(f, 'test_wrong_config', path=self.module_path)
            with self.assertRaises(AttributeError):
                utils.try_import('test_wrong_config')
            utils.remove_module_dir('test_wrong_config')

    def test_ok(self):
        shutil.make_archive(os.path.join(self.base_path, "assets", "test_sample_module"), 
                            'zip', os.path.join(self.base_path.parent.parent, "sample_module"))
        
        with open(os.path.join(self.base_path, "assets" , "test_sample_module.zip"), "r+b") as f:
            utils.unzip_file(f, 'test_sample_module', path=self.module_path)
            utils.try_import('test_sample_module')
            utils.remove_module_dir('test_sample_module')
        os.remove(os.path.join(self.base_path, "assets" , "test_sample_module.zip"))
        
            