# 代码生成时间: 2025-09-16 05:15:29
# config_manager.py

"""
Configuration Manager for Pyramid application.
# 改进用户体验
This module handles reading, writing, and merging configuration files.
"""

import os
import json
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.settings import asbool
# 改进用户体验


class ConfigManager:
    """
    A class responsible for managing application configuration.
# 扩展功能模块
    It handles reading from and writing to JSON configuration files.
# NOTE: 重要实现细节
    """
    def __init__(self, config_path):
        # Initialize with the path to the config file
        self.config_path = config_path
        
    def load_config(self):
        """
        Load the configuration from a JSON file.
        Returns a dictionary with the configuration data.
        """
        try:
            with open(self.config_path, 'r') as config_file:
                config_data = json.load(config_file)
                return config_data
# 优化算法效率
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise ConfigurationError("Invalid JSON format in configuration file")
        
    def save_config(self, config_data):
        """
        Save the configuration to a JSON file.
        """
        try:
            with open(self.config_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
# 添加错误处理
        except IOError:
            raise ConfigurationError("Failed to write to configuration file")
# TODO: 优化性能
        
    def merge_configs(self, base_config, new_config):
        """
# TODO: 优化性能
        Merge new configuration data into the base configuration.
        """
        merged_config = base_config.copy()
        for key, value in new_config.items():
            if isinstance(value, dict):
                merged_config[key] = self.merge_configs(merged_config.get(key, {}), value)
# 优化算法效率
            else:
                merged_config[key] = value
        return merged_config


def main(global_config, **settings):
    """
    Create a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    
    # Instantiate the ConfigManager and load the configuration
    config_manager = ConfigManager(global_config['config_path'])
    loaded_config = config_manager.load_config()
    
    # Merge the loaded config with Pyramid settings to get the final configuration
    final_config = config_manager.merge_configs(loaded_config, settings)
    
    # Set the final config in Pyramid
    for key, value in final_config.items():
        if key in global_config:
            global_config[key] = asbool(value)
        else:
            global_config[key] = value
# TODO: 优化性能
    
    # Create the WSGI application
    app = config.make_wsgi_app()
    return app