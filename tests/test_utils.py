"""工具函数单元测试"""

import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from data_export_approver.utils import (
    load_approval_codes,
    validate_approval_code,
    clear_config_cache,
    add_approval_code,
    list_approval_codes
)


def test_load_from_env():
    """测试从环境变量加载审批码"""
    clear_config_cache()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'CODE1,CODE2,CODE3'}):
        codes = load_approval_codes()
        assert 'CODE1' in codes
        assert 'CODE2' in codes
        assert 'CODE3' in codes


def test_load_from_config_file():
    """测试从配置文件加载审批码"""
    clear_config_cache()

    config_data = json.dumps({'approval_codes': ['FILE-CODE1', 'FILE-CODE2']})

    with patch.dict(os.environ, {}, clear=True):
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=config_data)):
                codes = load_approval_codes()
                assert 'FILE-CODE1' in codes
                assert 'FILE-CODE2' in codes


def test_validate_approval_code():
    """测试审批码验证"""
    clear_config_cache()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'VALID-CODE'}):
        assert validate_approval_code('VALID-CODE') is True
        assert validate_approval_code('INVALID-CODE') is False


def test_config_cache():
    """测试配置缓存机制"""
    clear_config_cache()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'CODE1'}):
        codes1 = load_approval_codes()
        codes2 = load_approval_codes()

        # 应该返回相同的缓存对象
        assert codes1 is codes2


def test_clear_config_cache():
    """测试清除配置缓存"""
    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'CODE1'}):
        load_approval_codes()
        clear_config_cache()

        # 缓存应该被清除
        from data_export_approver.utils import _CONFIG_CACHE
        assert _CONFIG_CACHE is None
