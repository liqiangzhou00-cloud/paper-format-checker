* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Segoe UI", sans-serif;
  background: #f4f7fb;
  color: #1d2736;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.topbar {
  margin-bottom: 16px;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 20px;
}

.left-panel,
.right-panel {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 8px;
  font-weight: 600;
}

input, textarea, button {
  font: inherit;
}

input, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dfe7f1;
  border-radius: 8px;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

button {
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 11px 14px;
  cursor: pointer;
  font-weight: 600;
}

.summary-box {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.issue-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.issue-item {
  border: 1px solid #e5e7eb;
  background: #f8fafc;
  padding: 12px 14px;
  border-radius: 8px;
}

.issue-item.error {
  border-left: 5px solid #dc2626;
}

.issue-item.warning {
  border-left: 5px solid #f59e0b;
}

.issue-item.info {
  border-left: 5px solid #10b981;
}

.issue-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 0.8rem;
  color: #475569;
  margin-bottom: 6px;
}

.badge {
  border-radius: 999px;
  padding: 4px 8px;
  font-weight: 700;
  color: white;
  font-size: 0.7rem;
}

.badge.error { background: #dc2626; }
.badge.warning { background: #f59e0b; }
.badge.info { background: #10b981; }

@media (max-width: 768px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
