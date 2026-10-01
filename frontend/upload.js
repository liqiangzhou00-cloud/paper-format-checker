<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>论文格式检查</title>
    <style>
      body {
        font-family: Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
        margin: 0;
        background: #f5f7fb;
      }
      .app-shell {
        max-width: 980px;
        margin: 40px auto;
        background: #fff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
      }
      h1 {
        margin-top: 0;
      }
      .upload-panel {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
        margin: 20px 0;
        padding: 16px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
      }
      button, select {
        height: 40px;
        padding: 0 16px;
        border-radius: 8px;
        border: 1px solid #dbe3ef;
        font-size: 14px;
      }
      button {
        background: #2563eb;
        color: white;
        cursor: pointer;
      }
      .result-box {
        margin-top: 16px;
      }
      .issue-item {
        list-style: none;
        margin: 12px 0;
        padding: 16px;
        border-left: 5px solid #3b82f6;
        background: #f9fbff;
        border-radius: 8px;
      }
      .issue-item.error { border-left-color: #dc2626; }
      .issue-item.warning { border-left-color: #f59e0b; }
      .issue-item.info { border-left-color: #10b981; }
      .meta-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
        margin-bottom: 8px;
        color: #475569;
        font-size: 12px;
      }
      .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 999px;
        color: white;
        font-weight: 700;
        font-size: 12px;
      }
      .badge.error { background: #dc2626; }
      .badge.warning { background: #f59e0b; }
      .badge.info { background: #10b981; }
      .issue-item p {
        margin: 6px 0;
      }
      .issue-list {
        padding-left: 0;
      }
    </style>
  </head>
  <body>
    <div class="app-shell">
      <h1>论文格式检查系统</h1>
      <div class="upload-panel">
        <input id="uploadFile" type="file" accept=".doc,.docx,.json" />
        <button id="uploadBtn">开始检查</button>
        <select id="filterType">
          <option value="all">全部</option>
          <option value="error">错误</option>
          <option value="warning">警告</option>
          <option value="info">信息</option>
        </select>
      </div>
      <div id="resultBox" class="result-box"></div>
      <ul id="issueList" class="issue-list"></ul>
    </div>
    <script src="upload.js"></script>
  </body>
</html>
