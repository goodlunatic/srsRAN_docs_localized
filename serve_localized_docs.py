#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import mimetypes
import posixpath
import socketserver
import threading
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path


ROOT = Path(__file__).resolve().parent

LANG_CONFIG = {
    "en": {
        "port": 8081,
        "title": "srsRAN Documentation",
        "subtitle": (
            "A local English documentation gateway for the landing page, "
            "srsRAN Project, and srsRAN 4G."
        ),
        "project_name": "srsRAN Project",
        "project_desc": "ORAN-native 5G CU/DU documentation with user manuals and dev guides.",
        "four_g_name": "srsRAN 4G",
        "four_g_desc": "End-to-end 4G suite documentation for UE, eNodeB, and EPC.",
        "feature_name": "srsRAN Features",
        "feature_desc": "Overview of the software suite and key feature highlights.",
        "issues_name": "Reporting Issues",
        "issues_desc": "Issue tracking, vulnerability reporting, and support guidance.",
    },
    "zh": {
        "port": 8082,
        "title": "srsRAN 文档",
        "subtitle": "本地中文文档入口，统一跳转到主页、srsRAN Project 和 srsRAN 4G。",
        "project_name": "srsRAN Project",
        "project_desc": "面向 5G ORAN-native CU/DU 的中文文档，包含用户手册和开发指南。",
        "four_g_name": "srsRAN 4G",
        "four_g_desc": "4G 端到端套件文档，覆盖 UE、eNodeB 和 EPC。",
        "feature_name": "srsRAN 功能特性",
        "feature_desc": "查看软件套件概览与关键能力说明。",
        "issues_name": "问题反馈",
        "issues_desc": "查看 issue、漏洞和支持相关说明。",
    },
}

DOC_ROOTS = {
    "en": {
        "project": ROOT / "srsran_project" / "en",
        "4g": ROOT / "srsran_4g" / "en",
    },
    "zh": {
        "project": ROOT / "srsran_project" / "zh",
        "4g": ROOT / "srsran_4g" / "zh",
    },
}


def build_homepage(lang: str) -> bytes:
    config = LANG_CONFIG[lang]
    other_lang = "zh" if lang == "en" else "en"
    other_port = LANG_CONFIG[other_lang]["port"]
    other_label = "中文" if lang == "en" else "English"
    feature_href = "/feature.html" if lang == "en" else "/feature.html"
    issues_href = "/reporting_issues.html" if lang == "en" else "/page_1.html"

    def card(title: str, desc: str, href: str) -> str:
        return (
            f'<a class="card" href="{html.escape(href, quote=True)}">'
            f"<h2>{html.escape(title)}</h2>"
            f"<p>{html.escape(desc)}</p>"
            f'<span class="cta">Open</span>'
            "</a>"
        )

    body = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(config["title"])}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4efe5;
      --panel: rgba(255, 252, 247, 0.9);
      --text: #1f2933;
      --muted: #52606d;
      --accent: #8c3b2f;
      --accent-2: #135d66;
      --border: rgba(31, 41, 51, 0.12);
      --shadow: 0 24px 60px rgba(31, 41, 51, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Noto Sans SC", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(19, 93, 102, 0.18), transparent 30%),
        radial-gradient(circle at bottom right, rgba(140, 59, 47, 0.16), transparent 28%),
        var(--bg);
      color: var(--text);
    }}
    .wrap {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 56px 24px 72px;
    }}
    .topbar {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      margin-bottom: 40px;
    }}
    .badge {{
      display: inline-flex;
      padding: 8px 14px;
      border-radius: 999px;
      background: rgba(19, 93, 102, 0.08);
      color: var(--accent-2);
      font-size: 14px;
      text-decoration: none;
      border: 1px solid rgba(19, 93, 102, 0.12);
    }}
    h1 {{
      margin: 0 0 16px;
      font-size: clamp(34px, 6vw, 64px);
      line-height: 0.95;
      letter-spacing: -0.03em;
    }}
    .subtitle {{
      max-width: 760px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
      margin: 0 0 32px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin-top: 28px;
    }}
    .card {{
      display: block;
      min-height: 210px;
      padding: 24px;
      border-radius: 22px;
      text-decoration: none;
      color: inherit;
      background: var(--panel);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      transition: transform 160ms ease, border-color 160ms ease;
    }}
    .card:hover {{
      transform: translateY(-3px);
      border-color: rgba(140, 59, 47, 0.28);
    }}
    .card h2 {{
      margin: 0 0 12px;
      font-size: 24px;
    }}
    .card p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
    }}
    .cta {{
      display: inline-block;
      margin-top: 22px;
      color: var(--accent);
      font-weight: 600;
    }}
    .ports {{
      margin-top: 28px;
      padding: 18px 20px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.55);
      border: 1px solid var(--border);
      color: var(--muted);
      line-height: 1.7;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      color: var(--text);
      background: rgba(19, 93, 102, 0.08);
      padding: 1px 6px;
      border-radius: 7px;
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="topbar">
      <span class="badge">Local Docs Gateway</span>
      <a class="badge" href="http://127.0.0.1:{other_port}/">{other_label}</a>
    </div>
    <h1>{html.escape(config["title"])}</h1>
    <p class="subtitle">{html.escape(config["subtitle"])}</p>
    <section class="grid">
      {card(config["project_name"], config["project_desc"], "/project/")}
      {card(config["four_g_name"], config["four_g_desc"], "/4g/")}
      {card(config["feature_name"], config["feature_desc"], feature_href)}
      {card(config["issues_name"], config["issues_desc"], issues_href)}
    </section>
    <section class="ports">
      <div>English: <code>http://127.0.0.1:{LANG_CONFIG["en"]["port"]}/</code></div>
      <div>中文: <code>http://127.0.0.1:{LANG_CONFIG["zh"]["port"]}/</code></div>
    </section>
  </main>
</body>
</html>
"""
    return body.encode("utf-8")


class DocsRequestHandler(BaseHTTPRequestHandler):
    server_version = "LocalizedDocsHTTP/1.0"

    def do_GET(self) -> None:
        self._handle_request(send_body=True)

    def do_HEAD(self) -> None:
        self._handle_request(send_body=False)

    def _handle_request(self, *, send_body: bool) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        raw_path = urllib.parse.unquote(parsed.path)
        path = posixpath.normpath(raw_path)
        if raw_path.endswith("/") and not path.endswith("/"):
            path += "/"

        if path in (".", ""):
            path = "/"

        if path == "/":
            self._send_bytes(build_homepage(self.server.lang), "text/html; charset=utf-8", send_body=send_body)
            return

        if path == "/feature.html":
            source = ROOT / "srsran_docs" / "docs" / ("source" if self.server.lang == "en" else "source_zh") / "feature.rst"
            self._send_bytes(
                render_rst_page(source, self.server.lang, "feature"),
                "text/html; charset=utf-8",
                send_body=send_body,
            )
            return

        if path in ("/reporting_issues.html", "/page_1.html"):
            source = ROOT / "srsran_docs" / "docs" / ("source" if self.server.lang == "en" else "source_zh") / "page_1.rst"
            self._send_bytes(
                render_rst_page(source, self.server.lang, "issues"),
                "text/html; charset=utf-8",
                send_body=send_body,
            )
            return

        for prefix, doc_root in self.server.doc_roots.items():
            route_prefix = f"/{prefix}"
            if path == route_prefix:
                self._redirect(f"{route_prefix}/")
                return
            if path.startswith(f"{route_prefix}/"):
                rel_path = path[len(route_prefix) + 1 :]
                self._serve_from_root(doc_root, rel_path, send_body=send_body)
                return

        self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.server.lang}:{self.server.server_address[1]}] {self.address_string()} - {fmt % args}")

    def _redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.MOVED_PERMANENTLY)
        self.send_header("Location", location)
        self.end_headers()

    def _serve_from_root(self, root: Path, rel_path: str, *, send_body: bool) -> None:
        relative = Path(rel_path.lstrip("/"))
        target = (root / relative).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
            return

        if target.is_dir():
            index_path = target / "index.html"
            if index_path.is_file():
                target = index_path
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return

        if not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(target.stat().st_size))
        self.end_headers()
        if send_body:
            with target.open("rb") as handle:
                self.wfile.write(handle.read())

    def _send_bytes(self, data: bytes, content_type: str, *, send_body: bool) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if send_body:
            self.wfile.write(data)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address: tuple[str, int], handler_cls, *, lang: str) -> None:
        super().__init__(server_address, handler_cls)
        self.lang = lang
        self.doc_roots = DOC_ROOTS[lang]


def render_rst_page(source: Path, lang: str, page_kind: str) -> bytes:
    text = source.read_text(encoding="utf-8")
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    title = "srsRAN Features" if page_kind == "feature" and lang == "en" else None
    if page_kind == "feature" and lang == "zh":
        title = "srsRAN 功能特性"
    if page_kind == "issues" and lang == "en":
        title = "Reporting Issues"
    if page_kind == "issues" and lang == "zh":
        title = "问题反馈"

    paragraphs: list[str] = []
    bullets: list[str] = []
    for line in lines:
        if line.startswith(".. _"):
            continue
        if set(line) <= {"=", "-", "*"}:
            continue
        if line.startswith("- "):
            bullets.append(line[2:])
            continue
        paragraphs.append(line)

    bullet_html = ""
    if bullets:
        bullet_items = "".join(f"<li>{html.escape(item)}</li>" for item in bullets)
        bullet_html = f"<ul>{bullet_items}</ul>"

    paragraph_html = "".join(f"<p>{html.escape(item)}</p>" for item in paragraphs if item != title)
    back_label = "Back to home" if lang == "en" else "返回主页"
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title or '')}</title>
  <style>
    body {{
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Noto Sans SC", sans-serif;
      background: #f6f3ed;
      color: #1f2933;
    }}
    main {{
      max-width: 920px;
      margin: 0 auto;
      padding: 48px 24px 72px;
      line-height: 1.8;
    }}
    a {{
      color: #8c3b2f;
      text-decoration: none;
    }}
    h1 {{
      margin: 0 0 20px;
      font-size: clamp(32px, 5vw, 54px);
    }}
    p, li {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <main>
    <p><a href="/">{html.escape(back_label)}</a></p>
    <h1>{html.escape(title or '')}</h1>
    {paragraph_html}
    {bullet_html}
  </main>
</body>
</html>
"""
    return body.encode("utf-8")


def serve_language(lang: str, port: int) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), DocsRequestHandler, lang=lang)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve localized srsRAN docs.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--en-port", type=int, default=LANG_CONFIG["en"]["port"])
    parser.add_argument("--zh-port", type=int, default=LANG_CONFIG["zh"]["port"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    servers = []
    for lang, port in (("en", args.en_port), ("zh", args.zh_port)):
        server = ThreadingHTTPServer((args.host, port), DocsRequestHandler, lang=lang)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        servers.append(server)
        print(f"{lang} docs: http://{args.host}:{port}/")

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
