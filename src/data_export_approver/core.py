"""Monkey Patch 核心引擎"""

import pandas as pd
from functools import wraps
from typing import Dict, Callable

_ORIGINAL_METHODS: Dict[str, Callable] = {}
_PATCHED = False

EXPORT_METHODS = [
    'to_csv', 'to_excel', 'to_json', 'to_parquet',
    'to_pickle', 'to_sql', 'to_hdf', 'to_feather',
    'to_stata', 'to_gbq', 'to_html', 'to_xml',
    'to_markdown', 'to_clipboard'
]


def create_wrapper(method_name: str, original_method: Callable):
    """创建带审批流程的包装函数"""
    @wraps(original_method)
    def wrapper(self, *args, **kwargs):
        from .cli import request_approval, show_approval_success, show_approval_denied
        from .utils import validate_approval_code

        # 请求审批
        code = request_approval(method_name)

        # 验证审批码
        if not validate_approval_code(code):
            show_approval_denied(method_name)
            raise PermissionError(f"Invalid approval code for {method_name}")

        # 显示成功并执行原始方法
        show_approval_success(method_name)
        return original_method(self, *args, **kwargs)

    return wrapper


def patch_pandas():
    """应用 Monkey Patch 到 pandas DataFrame"""
    global _PATCHED
    if _PATCHED:
        return

    for method_name in EXPORT_METHODS:
        if hasattr(pd.DataFrame, method_name):
            original = getattr(pd.DataFrame, method_name)
            _ORIGINAL_METHODS[method_name] = original
            wrapper = create_wrapper(method_name, original)
            setattr(pd.DataFrame, method_name, wrapper)

    _PATCHED = True


def unpatch_pandas():
    """移除 Monkey Patch"""
    global _PATCHED
    if not _PATCHED:
        return

    for method_name, original in _ORIGINAL_METHODS.items():
        setattr(pd.DataFrame, method_name, original)
    _ORIGINAL_METHODS.clear()
    _PATCHED = False
