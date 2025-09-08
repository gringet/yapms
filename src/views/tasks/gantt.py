from __future__ import annotations

import json
import datetime as _dt
from typing import List
from nicegui import ui

from ...core.styles import applyGlobalStyles
from ...core.app_state import appState
from ...data.task import Task


def _ensure_frappe_assets() -> None:
  """Inject Frappe Gantt assets (CSS + JS) and hide progress UI."""
  ui.run_javascript(
    """
(function() {
  if (!document.getElementById('frappe-gantt-css')) {
    var l = document.createElement('link');
    l.id = 'frappe-gantt-css';
    l.rel = 'stylesheet';
    l.href = 'https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css';
    document.head.appendChild(l);
  }
  if (!document.getElementById('frappe-gantt-js')) {
    var s = document.createElement('script');
    s.id = 'frappe-gantt-js';
    s.src = 'https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js';
    document.head.appendChild(s);
  }
  if (!document.getElementById('frappe-gantt-hide-progress')) {
    var style = document.createElement('style');
    style.id = 'frappe-gantt-hide-progress';
    style.textContent = '.bar .bar-progress, .bar .handle.progress { display: none !important; }';
    document.head.appendChild(style);
  }
})();
"""
  )


def _map_tasks_for_gantt(tasks: List[Task]) -> list[dict]:
  rows: list[dict] = []
  for t in tasks:
    if not t.startdate:
      continue
    try:
      y, m, d = [int(x) for x in t.startdate.split('-')]
      start = _dt.date(y, m, d)
    except Exception:
      continue
    effort = int(t.effort or 1)
    if effort <= 0:
      effort = 1
    end = start + _dt.timedelta(days=effort)
    # Map status to progress percentage
    status = (t.status or '').strip().lower()
    if status in ('backlog', 'to do', 'to-do', 'todo'):
      progress = 0
    elif status in ('in progress', 'in-progress'):
      progress = 50
    elif status in ('done', 'completed', 'complete'):
      progress = 100
    else:
      progress = 0
    rows.append({
      'id': str(t.id),
      'name': t.title,
      'start': start.isoformat(),
      'end': end.isoformat(),
      'progress': progress,
      'dependencies': ''
    })
  return rows


@ui.refreshable
def build() -> None:
  """Build a simple Frappe Gantt with console logging on date changes."""

  applyGlobalStyles()
  _ensure_frappe_assets()

  # Prepare and filter tasks for the chart
  current_tasks: List[Task] = appState.filterTasks(appState.tasksList or [])
  data = _map_tasks_for_gantt(current_tasks)
  data_json = json.dumps(data)

  container_id = 'gantt-container'
  with ui.card().classes('w-full border-0 shadow-none p-0'):
    ui.html(f'<div id="{container_id}" style="width:100%; height: calc(100vh - 140px);"></div>')

    # Improve contrast: darker bars with bold labels scoped to this container
    ui.run_javascript(
      f"""
(function() {{
  var sid = 'frappe-gantt-contrast-{container_id}';
  if (!document.getElementById(sid)) {{
    var style = document.createElement('style');
    style.id = sid;
    style.textContent = `
#{container_id} .bar {{ fill: #1f2937 !important; }}               /* slate-800 */
#{container_id} .bar-wrapper:hover .bar {{ fill: #111827 !important; }} /* gray-900 */
#{container_id} .bar-label {{ fill: #ffffff !important; font-weight: 700; }}
#{container_id} .bar-label.outside {{ fill: #000000 !important; font-weight: 700; }}
`;
    document.head.appendChild(style);
  }}
}})();
"""
    )

    # Initialize the chart (wait until Frappe Gantt is available),
    # and POST changes to the NiceGUI backend with console logging.
    ui.run_javascript(
      f"""
(function() {{
  var tasks = {data_json};
  function init() {{
    if (!(window.Gantt)) {{ setTimeout(init, 50); return; }}
    var target = document.getElementById('{container_id}');
    if (!target) {{ setTimeout(init, 50); return; }}
    target.innerHTML = '';
    try {{
      var gantt = new Gantt(target, tasks, {{
        view_mode: 'Day',
        language: 'en',
        on_date_change: function(task, start, end) {{
          try {{
            var payload = {{
              id: task && task.id,
              start: (start && start.toISOString ? start.toISOString().slice(0,10) : null),
              end: (end && end.toISOString ? end.toISOString().slice(0,10) : null)
            }};
            console.log('[Gantt] on_date_change', payload);
            if (payload.id && payload.start && payload.end) {{
              fetch('/api/gantt/update', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
              }})
              .then(function(r) {{ return r.json(); }})
              .then(function(res) {{ console.log('[Gantt] backend ok', res); }})
              .catch(function(err) {{ console.warn('[Gantt] backend error', err); }});
            }} else {{
              console.warn('[Gantt] invalid payload; not posting', payload);
            }}
          }} catch (e) {{ console.warn('[Gantt] on_date_change failed', e); }}
        }}
      }});
    }} catch (e) {{ console.error('[Gantt] init failed', e); }}

    function styleLabels() {{
      var labels = target.querySelectorAll('.bar-label');
      labels.forEach(function(el) {{
        if (el.classList.contains('outside')) {{
          el.setAttribute('fill', '#000000');
          el.style.fill = '#000000';
          el.style.fontWeight = '700';
        }} else {{
          el.setAttribute('fill', '#ffffff');
          el.style.fill = '#ffffff';
          el.style.fontWeight = '700';
        }}
      }});
    }}
    // Initial pass and short delayed pass for layout
    styleLabels();
    setTimeout(styleLabels, 50);
  }}
  init();
}})();
"""
    )
