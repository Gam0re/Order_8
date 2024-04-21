from aiogram_dialog import Dialog
from src.dialogs_windows import windows

async def bot_catalog_dialogs():
    return [Dialog(
            await windows.first_category_window(),
            await windows.categories_window(1),
            await windows.categories_window(2),
            await windows.categories_window(3),
            await windows.categories_window(4),
            await windows.categories_window(5),
            on_process_result=windows.on_process_result
    ),
            Dialog(
                await windows.tovari_window()
            )
    ]


