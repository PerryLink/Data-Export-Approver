"""核心功能单元测试"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_export_approver.core import patch_pandas, unpatch_pandas, EXPORT_METHODS


def test_patch_pandas():
    """测试 Monkey Patch 是否正确应用"""
    unpatch_pandas()  # 确保初始状态

    # 保存原始方法
    original_to_csv = pd.DataFrame.to_csv

    # 应用补丁
    patch_pandas()

    # 验证方法已被替换
    assert pd.DataFrame.to_csv != original_to_csv

    # 清理
    unpatch_pandas()


def test_unpatch_pandas():
    """测试移除 Monkey Patch"""
    patch_pandas()
    original_to_csv = pd.DataFrame.to_csv

    unpatch_pandas()

    # 验证方法已恢复
    assert pd.DataFrame.to_csv != original_to_csv


def test_export_with_valid_code():
    """测试使用有效审批码导出"""
    patch_pandas()

    with patch('data_export_approver.cli.request_approval', return_value='VALID-CODE'):
        with patch('data_export_approver.utils.validate_approval_code', return_value=True):
            with patch('data_export_approver.cli.show_approval_success'):
                df = pd.DataFrame({'a': [1, 2, 3]})
                # 应该成功导出
                result = df.to_csv(index=False)
                assert result is not None

    unpatch_pandas()


def test_export_with_invalid_code():
    """测试使用无效审批码导出"""
    patch_pandas()

    with patch('data_export_approver.cli.request_approval', return_value='INVALID'):
        with patch('data_export_approver.utils.validate_approval_code', return_value=False):
            df = pd.DataFrame({'a': [1, 2, 3]})

            # 应该抛出 PermissionError
            with pytest.raises(PermissionError):
                df.to_csv('test.csv')

    unpatch_pandas()


def test_all_export_methods_patched():
    """测试所有导出方法都被正确劫持"""
    patch_pandas()

    for method_name in EXPORT_METHODS:
        if hasattr(pd.DataFrame, method_name):
            method = getattr(pd.DataFrame, method_name)
            # 验证方法已被包装
            assert hasattr(method, '__wrapped__') or method.__name__ == 'wrapper'

    unpatch_pandas()
