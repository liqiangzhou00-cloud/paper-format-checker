from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI


class CheckerAPI:
    def __init__(self, app: FastAPI):
        self.app = app

    def register_routes(self):
        @self.app.get("/api/summary")
        def summary() -> Dict[str, Any]:
            return {"status": "ready", "modules": ["parser", "rule_engine", "report_service"]}
