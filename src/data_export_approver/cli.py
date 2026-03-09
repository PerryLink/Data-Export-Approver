"""Rich 交互式 CLI 界面"""

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()


def request_approval(method_name: str) -> str:
    """显示锁定警告并请求审批码"""

    # 红色警告面板
    warning = Panel(
        Text.assemble(
            ("🔒 ", "red bold"),
            ("UNAUTHORIZED DATA EXPORT ATTEMPT\n\n", "red bold"),
            ("Method: ", "white"),
            (f"{method_name}\n", "yellow bold"),
            ("Status: ", "white"),
            ("BLOCKED - Approval Required", "red"),
        ),
        border_style="red bold",
        title="[red bold]⚠ SECURITY ALERT ⚠[/red bold]",
    )
    console.print(warning)

    # 提示输入审批码
    code = Prompt.ask(
        "[yellow]Enter approval code to proceed[/yellow]",
        password=False
    )

    return code


def show_approval_success(method_name: str):
    """显示绿色成功确认"""
    success = Panel(
        Text.assemble(
            ("✅ ", "green bold"),
            ("APPROVAL GRANTED\n\n", "green bold"),
            ("Method: ", "white"),
            (f"{method_name}\n", "yellow"),
            ("Status: ", "white"),
            ("Executing export...", "green"),
        ),
        border_style="green bold",
        title="[green bold]✓ AUTHORIZED ✓[/green bold]",
    )
    console.print(success)


def show_approval_denied(method_name: str):
    """显示拒绝消息"""
    console.print(f"[red bold]❌ Permission denied: Invalid approval code[/red bold]")
    console.print(f"[red]Export operation cancelled for {method_name}[/red]")
