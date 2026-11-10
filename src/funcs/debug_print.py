import config as cfg
from src.classes.TerminalColors import TerminalColors


def debug_print(*args, color=TerminalColors.WHITE, **kwargs):
    """
    Функция для вывода информации для разработчиков в косноль.\n
    Выполняется только при условии, что в конфигурации включено значение NEED_DEBUG.\n
    Фактически просто выводит информацию в консоль из всех методов бота, чтобы видеть как он работает.
    """

    if cfg.NEED_DEBUG:
        print(
            TerminalColors.GREEN,
            TerminalColors.BOLD,
            "[CRMBotDebug]:",
            color,
            *args,
            TerminalColors.END,
        )
