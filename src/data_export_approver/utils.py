"""配置和验证工具"""

import os
import json
from pathlib import Path
from typing import List, Optional

_CONFIG_CACHE: Optional[List[str]] = None


def load_approval_codes() -> List[str]:
    """从环境变量或配置文件加载审批码"""
    global _CONFIG_CACHE

    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    codes = []

    # 优先级 1: 环境变量
    env_codes = os.getenv('DATA_EXPORT_APPROVAL_CODES', '')
    if env_codes:
        codes.extend([c.strip() for c in env_codes.split(',') if c.strip()])

    # 优先级 2: 配置文件
    config_path = Path.home() / '.data-export-approver.json'
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
                codes.extend(config.get('approval_codes', []))
        except Exception:
            pass

    _CONFIG_CACHE = codes
    return codes


def validate_approval_code(code: str) -> bool:
    """验证审批码是否有效"""
    valid_codes = load_approval_codes()
    return code in valid_codes


def clear_config_cache():
    """清除配置缓存（用于测试）"""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None


def add_approval_code(code: str):
    """添加审批码到配置文件"""
    config_path = Path.home() / '.data-export-approver.json'

    # 读取现有配置
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {'approval_codes': []}

    # 添加新审批码
    if code not in config['approval_codes']:
        config['approval_codes'].append(code)

    # 保存配置
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # 清除缓存
    clear_config_cache()


def list_approval_codes() -> List[str]:
    """列出所有有效审批码"""
    return load_approval_codes()
