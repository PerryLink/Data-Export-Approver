"""端到端集成测试"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from data_export_approver import enable, disable
from data_export_approver.utils import clear_config_cache


@pytest.fixture
def temp_csv():
    """创建临时 CSV 文件"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        yield f.name
    # 清理
    if os.path.exists(f.name):
        os.unlink(f.name)


def test_full_export_flow_with_approval(temp_csv):
    """测试完整的导出流程（有审批）"""
    clear_config_cache()
    enable()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'TEST-APPROVED'}):
        with patch('data_export_approver.cli.request_approval', return_value='TEST-APPROVED'):
            with patch('data_export_approver.cli.show_approval_success'):
                df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
                df.to_csv(temp_csv, index=False)

                # 验证文件已创建
                assert os.path.exists(temp_csv)

                # 验证内容正确
                df_read = pd.read_csv(temp_csv)
                assert len(df_read) == 3
                assert list(df_read.columns) == ['col1', 'col2']

    disable()


def test_full_export_flow_without_approval(temp_csv):
    """测试完整的导出流程（无审批）"""
    clear_config_cache()
    enable()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'VALID-CODE'}):
        with patch('data_export_approver.cli.request_approval', return_value='WRONG-CODE'):
            df = pd.DataFrame({'col1': [1, 2, 3]})

            # 应该抛出 PermissionError
            with pytest.raises(PermissionError):
                df.to_csv(temp_csv, index=False)

            # 文件不应该被创建
            assert not os.path.exists(temp_csv)

    disable()


def test_enable_disable():
    """测试手动启用/禁用功能"""
    # 禁用
    disable()

    # 启用
    enable()

    # 验证补丁已应用
    from data_export_approver.core import _PATCHED
    assert _PATCHED is True

    # 禁用
    disable()

    # 验证补丁已移除
    assert _PATCHED is False


def test_multiple_export_methods():
    """测试多种导出方法"""
    clear_config_cache()
    enable()

    with patch.dict(os.environ, {'DATA_EXPORT_APPROVAL_CODES': 'TEST-CODE'}):
        with patch('data_export_approver.cli.request_approval', return_value='TEST-CODE'):
            with patch('data_export_approver.cli.show_approval_success'):
                df = pd.DataFrame({'a': [1, 2, 3]})

                # 测试 to_json
                json_str = df.to_json()
                assert json_str is not None

                # 测试 to_dict
                # 注意: to_dict 不在导出方法列表中，应该不受影响
                dict_result = df.to_dict()
                assert dict_result is not None

    disable()
