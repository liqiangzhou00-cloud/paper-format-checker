from __future__ import annotations

from typing import Dict, List


class ReportExporter:
    def export_html(self, summary: Dict[str, int], issues: List[Dict[str, str]]) -> str:
        rows = "".join(
            f"<li><strong>{item.get('rule_id', 'UNKNOWN')}</strong> [{item.get('severity', 'info')}] - {item.get('message', '')}</li>"
            for item in issues
        )
        return f"""
        <html>
        <head><title>论文格式检查报告</title></head>
        <body>
          <h1>论文格式检查报告</h1>
          <p>错误: {summary.get('error', 0)} / 警告: {summary.get('warning', 0)} / 信息: {summary.get('info', 0)}</p>
          <ul>{rows}</ul>
        </body>
        </html>
        """

    def export_json(self, summary: Dict[str, int], issues: List[Dict[str, str]]) -> Dict[str, object]:
        return {"summary": summary, "issues": issues}
