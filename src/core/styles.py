from nicegui import ui


class Colors:
  PRIMARY = 'bg-black text-white'
  SECONDARY = 'bg-white text-black border border-black'
  GRAY = 'bg-gray-100'
  GRAY_LIGHT = 'bg-gray-50'
  SUCCESS = 'bg-green-500 text-white'
  ERROR = 'bg-red-500 text-white'
  WARNING = 'bg-yellow-500 text-black'


class Button:
  PRIMARY = 'bg-black text-white border border-black rounded-none hover:bg-gray-800'
  SECONDARY = 'bg-white text-black border border-black rounded-none hover:bg-gray-100'
  CANCEL = 'bg-white text-black border border-black rounded-none hover:bg-gray-100'
  DATE_SELECT = 'bg-white text-black border border-black rounded-none hover:bg-gray-100 ml-2'
  CANCEL_MR = 'bg-white text-black border border-black rounded-none hover:bg-gray-100 mr-2'


class Card:
  DEFAULT = 'bg-white border-2 border-black rounded-none shadow-none'
  DRAGGABLE = 'w-full min-h-[160px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col'
  DIALOG = 'bg-white border-2 border-black rounded-none shadow-none'
  STAKEHOLDER = 'min-h-[160px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col flex-1 min-w-[250px] max-w-[calc(25%-1rem)]'


class Input:
  DEFAULT = 'w-full'
  OUTLINED = 'outlined'
  FLEX_GROW = 'flex-grow'


class KanbanColumn:
  BASE = 'flex-1 min-w-0 h-[calc(100vh-100px)] p-3 rounded-none overflow-y-auto'
  HIGHLIGHTED = 'bg-gray-100 border-2 border-black'
  UNHIGHLIGHTED = 'bg-white border border-gray-300'


class Kanban:
  COLUMN_HEADER = 'text-bold ml-1 text-black font-bold uppercase tracking-wide sticky top-0 bg-white z-10 -mx-3 px-3 py-2 mb-2'
  TASK_TITLE = 'text-h6 font-semibold'
  TASK_DESCRIPTION = 'text-sm text-grey-8 -mt-2 flex-1'
  TASK_ROW = 'w-full justify-between items-end mt-0 p-0 pt-0'
  TASK_ICON_ROW = 'items-center gap-1'
  TASK_ICON = 'text-grey-6'
  TASK_LABEL = 'text-sm text-grey-8'


class Layout:
  FULL_HEIGHT = 'h-[calc(100vh-100px)]'
  DIALOG_WIDTH = 'w-[48rem]'
  DIALOG_MIN_WIDTH = 'min-width: 400px'
  FULL_WIDTH = 'w-full'
  COLUMN = 'w-full p-4'
  ROW = 'w-full justify-end'
  ROW_END = 'w-full justify-end mt-4'
  ROW_ITEMS_END = 'w-full items-end'
  GRID_4_RESPONSIVE = 'w-full flex flex-wrap gap-4'
  GANTT_SVG = 'w-full h-[50vh] min-h-[25rem]'


class Text:
  H6 = 'text-h6 mb-4'
  H6_BOLD = 'text-h6 font-semibold'
  LARGE = 'text-lg font-bold text-black mb-4'
  DATE_LABEL = 'text-lg font-bold text-black mb-4'
  SMALL_GRAY = 'text-sm text-grey-8'
  CENTER_GRAY = 'text-grey-6 text-center mt-8'
  LARGE_GRAY = 'text-lg text-gray-500'
  SMALL_LIGHT_GRAY = 'text-sm text-gray-400'


class Table:
  DEFAULT = 'w-full'
  PROPS = 'flat bordered'


def applyGlobalStyles():
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