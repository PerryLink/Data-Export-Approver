"""Data Export Approver - 强制审批流程的 Pandas 数据导出管控工具"""

__version__ = "0.1.0"

from .core import patch_pandas, unpatch_pandas

__all__ = ['enable', 'disable', 'patch_pandas', 'unpatch_pandas']


def enable():
    """手动启用补丁"""
    patch_pandas()


def disable():
    """手动禁用补丁"""
    unpatch_pandas()


# 导入时自动激活
try:
    patch_pandas()
except ImportError:
    import warnings
    warnings.warn("pandas not installed, data-export-approver will not be activated")
