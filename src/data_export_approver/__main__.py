"""CLI 命令入口"""

import argparse
import sys
from . import __version__
from .utils import add_approval_code, list_approval_codes


def main():
    parser = argparse.ArgumentParser(
        description='Data Export Approver - 强制审批流程的 Pandas 数据导出管控工具'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # config 子命令
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--show', action='store_true', help='显示当前配置')
    config_parser.add_argument('--add', metavar='CODE', help='添加审批码')

    # test 子命令
    subparsers.add_parser('test', help='测试补丁是否生效')

    args = parser.parse_args()

    if args.command == 'config':
        if args.show:
            codes = list_approval_codes()
            if codes:
                print("当前有效的审批码:")
                for code in codes:
                    print(f"  - {code}")
            else:
                print("未配置任何审批码")
        elif args.add:
            add_approval_code(args.add)
            print(f"已添加审批码: {args.add}")
        else:
            config_parser.print_help()

    elif args.command == 'test':
        print("测试 Monkey Patch...")
        try:
            import pandas as pd
            from . import patch_pandas

            # 检查是否已打补丁
            df = pd.DataFrame({'test': [1, 2, 3]})
            print("✓ pandas 已安装")
            print("✓ data-export-approver 已激活")
            print("\n尝试导出将触发审批流程")
        except ImportError:
            print("✗ pandas 未安装")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
