import yt_dlp
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
from datetime import timedelta
import random
import time

# VIDEO DOWNLOADER V4 - @scrxtch & @Claude.ai

MATRIX_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*<>[]{}|~"

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VDL//v3 — NEURAL_FETCH")
        self.root.geometry("1600x800")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0a0a')

        self.urls_file = None
        self.output_dir = None
        self.is_downloading = False
        self.downloaded_items = []
        self.failed_items = []
        self._matrix_after = None

        self._setup_styles()
        self._create_widgets()
        self._start_matrix_effect()
        self._animate_scanline()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Hack.TButton',
                        background='#0a0a0a',
                        foreground='#00ff41',
                        borderwidth=1,
                        focuscolor='none',
                        padding=(14, 8),
                        font=('Courier', 10, 'bold'),
                        relief='flat')
        style.map('Hack.TButton',
                  background=[('active', '#001a00'), ('disabled', '#0a0a0a')],
                  foreground=[('disabled', '#1a4a1a')])

        style.configure('Dim.TButton',
                        background='#0a0a0a',
                        foreground='#005510',
                        borderwidth=1,
                        focuscolor='none',
                        padding=(10, 6),
                        font=('Courier', 9),
                        relief='flat')
        style.map('Dim.TButton',
                  background=[('active', '#001200')],
                  foreground=[('active', '#00ff41')])

        style.configure('Hack.Horizontal.TProgressbar',
                        troughcolor='#0d0d0d',
                        background='#00ff41',
                        bordercolor='#003300',
                        lightcolor='#00ff41',
                        darkcolor='#00aa28')

    def _create_widgets(self):
        # ── HEADER ─────────────────────────────────────────────────────────
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(fill='x', padx=0, pady=0)

        top_bar = tk.Frame(header_frame, bg='#001a00', height=2)
        top_bar.pack(fill='x')

        title_row = tk.Frame(header_frame, bg='#0a0a0a')
        title_row.pack(fill='x', padx=20, pady=(10, 0))

        title_lbl = tk.Label(title_row,
                             text="VDL//v3",
                             font=('Courier', 28, 'bold'),
                             bg='#0a0a0a', fg='#00ff41')
        title_lbl.pack(side='left')

        sub_lbl = tk.Label(title_row,
                           text="  NEURAL_FETCH  //  MEDIA EXTRACTION SYSTEM  //  BUILD 2025.03",
                           font=('Courier', 9),
                           bg='#0a0a0a', fg='#1a5a1a')
        sub_lbl.pack(side='left', pady=(12, 0))

        self.status_dot = tk.Label(title_row,
                                   text="● READY",
                                   font=('Courier', 9, 'bold'),
                                   bg='#0a0a0a', fg='#00ff41')
        self.status_dot.pack(side='right', pady=(12, 0))

        sep = tk.Frame(header_frame, bg='#003300', height=1)
        sep.pack(fill='x', pady=(8, 0))

        # ── MAIN BODY ──────────────────────────────────────────────────────
        body = tk.Frame(self.root, bg='#0a0a0a')
        body.pack(fill='both', expand=True, padx=0, pady=0)

        # LEFT PANEL (controls + log)
        left = tk.Frame(body, bg='#0a0a0a', width=660)
        left.pack(side='left', fill='both', expand=True, padx=(20, 10), pady=10)
        left.pack_propagate(False)

        # divider canvas for matrix rain
        self.canvas = tk.Canvas(body, width=2, bg='#001a00',
                                highlightthickness=0, bd=0)
        self.canvas.pack(side='left', fill='y', pady=10)

        # RIGHT PANEL (status board)
        right = tk.Frame(body, bg='#0a0a0a', width=490)
        right.pack(side='right', fill='both', padx=(10, 20), pady=10)
        right.pack_propagate(False)

        self._build_left(left)
        self._build_right(right)

        # ── FOOTER ─────────────────────────────────────────────────────────
        foot_sep = tk.Frame(self.root, bg='#003300', height=1)
        foot_sep.pack(fill='x')
        foot = tk.Frame(self.root, bg='#0a0a0a')
        foot.pack(fill='x', padx=20)
        self.footer_lbl = tk.Label(foot,
                                   text="> SYSTEM IDLE  //  AWAITING INPUT",
                                   font=('Courier', 8),
                                   bg='#0a0a0a', fg='#1a5a1a')
        self.footer_lbl.pack(side='left', pady=4)

    def _build_left(self, parent):
        # ── FILE INPUT ─────────────────────────────────────────────────────
        self._section_label(parent, "01 // TARGET FILE  [.txt with URLs]")

        row1 = tk.Frame(parent, bg='#0a0a0a')
        row1.pack(fill='x', pady=(2, 8))

        self.file_entry = self._hacker_entry(row1)
        self.file_entry.pack(side='left', fill='x', expand=True, ipady=7)

        ttk.Button(row1, text="[ BROWSE ]",
                   style='Dim.TButton',
                   command=self.browse_file).pack(side='right', padx=(8, 0))

        # ── OUTPUT DIR ─────────────────────────────────────────────────────
        self._section_label(parent, "02 // OUTPUT DIRECTORY")

        row2 = tk.Frame(parent, bg='#0a0a0a')
        row2.pack(fill='x', pady=(2, 8))

        self.output_entry = self._hacker_entry(row2)
        self.output_entry.pack(side='left', fill='x', expand=True, ipady=7)

        ttk.Button(row2, text="[ BROWSE ]",
                   style='Dim.TButton',
                   command=self.browse_output).pack(side='right', padx=(8, 0))

        # ── PROGRESS ───────────────────────────────────────────────────────
        self._section_label(parent, "03 // TRANSFER STATUS")

        prog_row = tk.Frame(parent, bg='#0a0a0a')
        prog_row.pack(fill='x', pady=(2, 4))

        self.progress_label = tk.Label(prog_row,
                                       text="> STANDBY",
                                       font=('Courier', 9),
                                       bg='#0a0a0a', fg='#00ff41')
        self.progress_label.pack(side='left')

        self.pct_label = tk.Label(prog_row,
                                  text="",
                                  font=('Courier', 9),
                                  bg='#0a0a0a', fg='#005510')
        self.pct_label.pack(side='right')

        self.progress_bar = ttk.Progressbar(parent,
                                            style='Hack.Horizontal.TProgressbar',
                                            mode='indeterminate',
                                            length=580)
        self.progress_bar.pack(pady=(0, 8), fill='x')

        # ── LOG ────────────────────────────────────────────────────────────
        self._section_label(parent, "04 // SYSTEM LOG")

        log_frame = tk.Frame(parent, bg='#060606',
                             highlightbackground='#003300',
                             highlightthickness=1)
        log_frame.pack(fill='both', expand=True, pady=(2, 8))

        self.log_text = tk.Text(log_frame,
                                bg='#060606', fg='#00cc33',
                                font=('Courier', 9),
                                relief='flat', wrap='word',
                                insertbackground='#00ff41',
                                selectbackground='#003300',
                                selectforeground='#00ff41',
                                padx=8, pady=6)
        self.log_text.pack(side='left', fill='both', expand=True)
        self.log_text.tag_config('ok',  foreground='#00ff41')
        self.log_text.tag_config('err', foreground='#ff3333')
        self.log_text.tag_config('inf', foreground='#00aaff')
        self.log_text.tag_config('dim', foreground='#1a5a1a')
        self.log_text.tag_config('warn', foreground='#ffaa00')

        sb = tk.Scrollbar(log_frame, bg='#0a0a0a',
                          troughcolor='#060606',
                          activebackground='#003300',
                          highlightthickness=0, bd=0)
        sb.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=sb.set)
        sb.config(command=self.log_text.yview)

        # ── DOWNLOAD BUTTON ────────────────────────────────────────────────
        self.download_btn = ttk.Button(parent,
                                       text="▶  EXECUTE DOWNLOAD SEQUENCE",
                                       style='Hack.TButton',
                                       command=self.start_download)
        self.download_btn.pack(fill='x', ipady=4)

    def _build_right(self, parent):
        # Header
        hdr = tk.Frame(parent, bg='#0a0a0a')
        hdr.pack(fill='x')

        tk.Label(hdr, text="STATUS BOARD",
                 font=('Courier', 11, 'bold'),
                 bg='#0a0a0a', fg='#00ff41').pack(side='left')

        self.board_stats = tk.Label(hdr, text="",
                                    font=('Courier', 8),
                                    bg='#0a0a0a', fg='#1a5a1a')
        self.board_stats.pack(side='right', pady=2)

        sep = tk.Frame(parent, bg='#003300', height=1)
        sep.pack(fill='x', pady=(4, 6))

        # ── SUCCESS LIST ───────────────────────────────────────────────────
        ok_header = tk.Frame(parent, bg='#0a0a0a')
        ok_header.pack(fill='x')
        tk.Label(ok_header, text="✓ DOWNLOADED",
                 font=('Courier', 9, 'bold'),
                 bg='#0a0a0a', fg='#00ff41').pack(side='left')
        self.ok_count = tk.Label(ok_header, text="[0]",
                                  font=('Courier', 9),
                                  bg='#0a0a0a', fg='#005510')
        self.ok_count.pack(side='right')

        ok_frame = tk.Frame(parent, bg='#060606',
                            highlightbackground='#003300',
                            highlightthickness=1)
        ok_frame.pack(fill='both', expand=True, pady=(4, 8))

        self.ok_text = tk.Text(ok_frame,
                               bg='#060606', fg='#00ff41',
                               font=('Courier', 8),
                               relief='flat', wrap='word',
                               state='disabled',
                               padx=6, pady=4,
                               selectbackground='#003300')
        self.ok_text.pack(side='left', fill='both', expand=True)
        ok_sb = tk.Scrollbar(ok_frame, bg='#0a0a0a',
                              troughcolor='#060606',
                              activebackground='#003300',
                              highlightthickness=0, bd=0)
        ok_sb.pack(side='right', fill='y')
        self.ok_text.config(yscrollcommand=ok_sb.set)
        ok_sb.config(command=self.ok_text.yview)

        # ── FAILED LIST ────────────────────────────────────────────────────
        sep2 = tk.Frame(parent, bg='#330000', height=1)
        sep2.pack(fill='x', pady=(0, 6))

        err_header = tk.Frame(parent, bg='#0a0a0a')
        err_header.pack(fill='x')
        tk.Label(err_header, text="✗ FAILED",
                 font=('Courier', 9, 'bold'),
                 bg='#0a0a0a', fg='#ff3333').pack(side='left')
        self.err_count = tk.Label(err_header, text="[0]",
                                   font=('Courier', 9),
                                   bg='#0a0a0a', fg='#4a0000')
        self.err_count.pack(side='right')

        err_frame = tk.Frame(parent, bg='#060606',
                             highlightbackground='#330000',
                             highlightthickness=1)
        err_frame.pack(fill='both', expand=True, pady=(4, 0))

        self.err_text = tk.Text(err_frame,
                                bg='#060606', fg='#ff4444',
                                font=('Courier', 8),
                                relief='flat', wrap='word',
                                state='disabled',
                                padx=6, pady=4,
                                selectbackground='#330000')
        self.err_text.pack(side='left', fill='both', expand=True)
        err_sb = tk.Scrollbar(err_frame, bg='#0a0a0a',
                               troughcolor='#060606',
                               activebackground='#330000',
                               highlightthickness=0, bd=0)
        err_sb.pack(side='right', fill='y')
        self.err_text.config(yscrollcommand=err_sb.set)
        err_sb.config(command=self.err_text.yview)

    # ── HELPERS ───────────────────────────────────────────────────────────

    def _section_label(self, parent, text):
        tk.Label(parent, text=text,
                 font=('Courier', 8),
                 bg='#0a0a0a', fg='#1a6a1a').pack(anchor='w', pady=(6, 0))

    def _hacker_entry(self, parent):
        e = tk.Entry(parent,
                     font=('Courier', 9),
                     bg='#0d0d0d', fg='#00ff41',
                     insertbackground='#00ff41',
                     selectbackground='#003300',
                     selectforeground='#00ff41',
                     relief='flat',
                     highlightbackground='#003300',
                     highlightcolor='#00ff41',
                     highlightthickness=1)
        return e

    # ── EFFECTS ───────────────────────────────────────────────────────────

    def _start_matrix_effect(self):
        """Animate the thin divider strip with random chars."""
        self._matrix_tick()

    def _matrix_tick(self):
        self.canvas.delete('all')
        h = 660
        for y in range(0, h, 14):
            char = random.choice(MATRIX_CHARS)
            alpha = random.choice(['#001a00', '#002a00', '#003a00',
                                   '#00aa28', '#00cc33', '#00ff41'])
            self.canvas.create_text(1, y, text=char,
                                    font=('Courier', 8),
                                    fill=alpha, anchor='nw')
        self._matrix_after = self.root.after(120, self._matrix_tick)

    def _animate_scanline(self):
        """Blink the status dot."""
        cur = self.status_dot.cget('fg')
        nxt = '#00ff41' if cur == '#003300' else '#003300'
        if not self.is_downloading:
            self.status_dot.config(fg=nxt)
        self.root.after(800, self._animate_scanline)

    # ── BROWSE ────────────────────────────────────────────────────────────

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="SELECT URL FILE",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.urls_file = filename
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.log(f"FILE LOADED  →  {filename}", 'inf')

    def browse_output(self):
        directory = filedialog.askdirectory(title="SELECT OUTPUT DIRECTORY")
        if directory:
            self.output_dir = directory
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, directory)
            self.log(f"OUTPUT DIR   →  {directory}", 'inf')

    # ── LOGGING ───────────────────────────────────────────────────────────

    def log(self, message, tag='dim'):
        ts = time.strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{ts}] ", 'dim')
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.root.update()

    def _board_append(self, widget, text):
        widget.config(state='normal')
        widget.insert(tk.END, text + "\n")
        widget.see(tk.END)
        widget.config(state='disabled')

    def _add_ok(self, title, url):
        self.downloaded_items.append((title, url))
        n = len(self.downloaded_items)
        self.ok_count.config(text=f"[{n}]")
        short = title[:46] + "…" if len(title) > 47 else title
        self._board_append(self.ok_text, f"  ✓  {short}")
        self._update_board_stats()

    def _add_fail(self, url, reason):
        self.failed_items.append((url, reason))
        n = len(self.failed_items)
        self.err_count.config(text=f"[{n}]")
        short = url[:44] + "…" if len(url) > 45 else url
        self._board_append(self.err_text, f"  ✗  {short}")
        self._update_board_stats()

    def _update_board_stats(self):
        ok = len(self.downloaded_items)
        err = len(self.failed_items)
        total = ok + err
        self.board_stats.config(
            text=f"OK:{ok}  FAIL:{err}  TOTAL:{total}")

    # ── DOWNLOAD ──────────────────────────────────────────────────────────

    def start_download(self):
        if self.is_downloading:
            return

        urls_file = self.file_entry.get()
        output_dir = self.output_entry.get()

        if not urls_file:
            messagebox.showerror("INPUT ERROR", "No URL file selected.")
            return
        if not output_dir:
            messagebox.showerror("INPUT ERROR", "No output directory specified.")
            return
        if not os.path.exists(urls_file):
            messagebox.showerror("INPUT ERROR", "URL file not found on disk.")
            return

        # Reset board
        self.downloaded_items.clear()
        self.failed_items.clear()
        for w in (self.ok_text, self.err_text):
            w.config(state='normal')
            w.delete('1.0', tk.END)
            w.config(state='disabled')
        self.ok_count.config(text="[0]")
        self.err_count.config(text="[0]")
        self._update_board_stats()

        self.is_downloading = True
        self.download_btn.config(state='disabled', text="⏳  SEQUENCE RUNNING…")
        self.status_dot.config(text="● ACTIVE", fg='#00ff41')
        self.progress_bar.start(12)

        thread = threading.Thread(target=self._download_thread,
                                  args=(urls_file, output_dir),
                                  daemon=True)
        thread.start()

    def _download_thread(self, urls_file, output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = [l.strip() for l in f if l.strip()]

            if not urls:
                self.log("NO URLS FOUND IN FILE", 'err')
                self._finish()
                return

            total = len(urls)
            self.log(f"TARGETS LOADED  →  {total} URL(s)", 'ok')
            self.footer_lbl.config(text=f"> DOWNLOADING  0/{total}")

            for idx, url in enumerate(urls, 1):
                self.log("─" * 56, 'dim')
                self.log(f"[{idx}/{total}]  FETCHING  →  {url}", 'inf')
                self.progress_label.config(
                    text=f"> DOWNLOADING {idx}/{total}")
                self.pct_label.config(
                    text=f"{int((idx-1)/total*100)}%")
                self.footer_lbl.config(
                    text=f"> DOWNLOADING  {idx}/{total}  |  OK:{len(self.downloaded_items)}  FAIL:{len(self.failed_items)}")

                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                }

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        if not info:
                            raise ValueError("Could not extract video info")

                        title = info.get('title', 'Unknown')
                        self.log(f"TITLE    →  {title}", 'ok')

                        dur = info.get('duration', 0)
                        if dur:
                            self.log(f"DURATION →  {str(timedelta(seconds=dur))}", 'dim')

                        size = info.get('filesize') or info.get('filesize_approx', 0)
                        if size:
                            if size >= 1_073_741_824:
                                sz = f"{size/1_073_741_824:.2f} GB"
                            else:
                                sz = f"{size/1_048_576:.2f} MB"
                            self.log(f"SIZE     →  {sz}", 'dim')

                        ydl.download([url])
                        self.log(f"STATUS   →  COMPLETE", 'ok')
                        self._add_ok(title, url)

                except Exception as e:
                    err_msg = str(e)[:80]
                    self.log(f"STATUS   →  FAILED  [{err_msg}]", 'err')
                    self._add_fail(url, err_msg)

            ok = len(self.downloaded_items)
            fail = len(self.failed_items)
            self.log("═" * 56, 'dim')
            self.log(f"SEQUENCE COMPLETE  //  OK:{ok}  FAIL:{fail}", 'ok')
            self.pct_label.config(text="100%")

        except Exception as e:
            self.log(f"CRITICAL FAULT: {e}", 'err')
        finally:
            self._finish()

    def _finish(self):
        self.is_downloading = False
        self.progress_bar.stop()
        self.download_btn.config(state='normal',
                                 text="▶  EXECUTE DOWNLOAD SEQUENCE")
        self.status_dot.config(text="● READY", fg='#00ff41')
        self.progress_label.config(text="> STANDBY")
        self.footer_lbl.config(
            text=f"> SEQUENCE IDLE  //  OK:{len(self.downloaded_items)}  FAIL:{len(self.failed_items)}")


def main():
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()