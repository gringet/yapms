from typing import ClassVar
from nicegui import ui


class Colors:
  PRIMARY: ClassVar[str] = 'bg-black text-white'
  SECONDARY: ClassVar[str] = 'bg-white text-black border border-black'
  GRAY: ClassVar[str] = 'bg-gray-100'
  GRAY_LIGHT: ClassVar[str] = 'bg-gray-50'
  SUCCESS: ClassVar[str] = 'bg-green-500 text-white'
  ERROR: ClassVar[str] = 'bg-red-500 text-white'
  WARNING: ClassVar[str] = 'bg-yellow-500 text-black'


class Button:
  PRIMARY: ClassVar[str] = 'bg-black text-white border border-black rounded-none hover:bg-gray-800'
  SECONDARY: ClassVar[str] = 'bg-white text-black border border-black rounded-none hover:bg-gray-100'
  CANCEL: ClassVar[str] = 'bg-white text-black border border-black rounded-none hover:bg-gray-100'
  DATE_SELECT: ClassVar[str] = 'bg-white text-black border border-black rounded-none hover:bg-gray-100 ml-2'
  CANCEL_MR: ClassVar[str] = 'bg-white text-black border border-black rounded-none hover:bg-gray-100 mr-2'


class Card:
  DEFAULT: ClassVar[str] = 'bg-white border-2 border-black rounded-none shadow-none'
  DRAGGABLE: ClassVar[str] = 'w-full min-h-[120px] max-h-[120px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col justify-between break-words p-3 overflow-hidden'
  DIALOG: ClassVar[str] = 'bg-white border-2 border-black rounded-none shadow-none'
  STAKEHOLDER: ClassVar[str] = 'min-h-[100px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col flex-1 min-w-[250px] max-w-[calc(25%-1rem)] p-3'


class Input:
  DEFAULT: ClassVar[str] = 'w-full'
  OUTLINED: ClassVar[str] = 'outlined'
  FLEX_GROW: ClassVar[str] = 'flex-grow'


class KanbanColumn:
  BASE: ClassVar[str] = 'flex-1 basis-1/4 min-w-0 h-[calc(100vh-100px)] p-3 rounded-none overflow-y-auto'
  HIGHLIGHTED: ClassVar[str] = 'bg-gray-100 border-2 border-black'
  UNHIGHLIGHTED: ClassVar[str] = 'bg-white border border-gray-300'


class Kanban:
  COLUMN_HEADER: ClassVar[str] = 'text-bold ml-1 text-black font-bold uppercase tracking-wide sticky top-0 bg-white z-10 -mx-3 px-3 py-2 mb-2 break-words'
  TASK_TITLE: ClassVar[str] = 'text-h6 font-semibold break-words'
  TASK_DESCRIPTION: ClassVar[str] = 'text-sm text-grey-8 -mt-2 break-words line-clamp-2'
  TASK_ROW: ClassVar[str] = 'w-full justify-between items-end mt-0 p-0 pt-0 flex-shrink-0 overflow-hidden'
  TASK_ICON_ROW: ClassVar[str] = 'items-center gap-1 flex-shrink-0'
  TASK_ICON: ClassVar[str] = 'text-grey-6 flex-shrink-0'
  TASK_LABEL: ClassVar[str] = 'text-sm text-grey-8 break-words'


class Layout:
  FULL_HEIGHT: ClassVar[str] = 'h-[calc(100vh-100px)]'
  DIALOG_WIDTH: ClassVar[str] = 'w-[48rem]'
  DIALOG_MIN_WIDTH: ClassVar[str] = 'min-width: 400px'
  FULL_WIDTH: ClassVar[str] = 'w-full'
  COLUMN: ClassVar[str] = 'w-full p-4'
  ROW: ClassVar[str] = 'w-full justify-end'
  ROW_END: ClassVar[str] = 'w-full justify-end mt-4'
  ROW_ITEMS_END: ClassVar[str] = 'w-full items-end'
  GRID_4_RESPONSIVE: ClassVar[str] = 'w-full flex flex-wrap gap-4'


class Text:
  H6: ClassVar[str] = 'text-h6 mb-4'
  H6_BOLD: ClassVar[str] = 'text-h6 font-semibold'
  LARGE: ClassVar[str] = 'text-lg font-bold text-black mb-4'
  DATE_LABEL: ClassVar[str] = 'text-lg font-bold text-black mb-4'
  SMALL_GRAY: ClassVar[str] = 'text-sm text-grey-8'
  CENTER_GRAY: ClassVar[str] = 'text-grey-6 text-center mt-8'
  LARGE_GRAY: ClassVar[str] = 'text-lg text-gray-500'
  SMALL_LIGHT_GRAY: ClassVar[str] = 'text-sm text-gray-400'


class Table:
  DEFAULT: ClassVar[str] = 'w-full'
  PROPS: ClassVar[str] = 'flat bordered'


def applyGlobalStyles() -> None:
  ui.add_head_html("""
<style>
.dragging * {
  pointer-events: none !important;
}
.kanban-column {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}
.kanban-column::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}


</style>
""")
