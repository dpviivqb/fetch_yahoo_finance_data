import sys
import yfinance as yf 
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import re
import webbrowser

def validate_date(date_str):
    return re.match(r"^\d{4}-\d{2}-\d{2}$", date_str)

def fetch_data():
    tickers = entry_ticker.get().strip()
    start_date = entry_start.get().strip()
    end_date = entry_end.get().strip()
    interval = interval_var.get().strip()
    output_format = format_var.get().strip()

    # 内容为空 或仍处于 placeholder 状态（灰色）
    if not tickers or not start_date or not end_date or \
        entry_ticker.cget("fg") == 'grey' or \
        entry_start.cget("fg") == 'grey' or \
        entry_end.cget("fg") == 'grey':
        messagebox.showerror("错误", "请填写所有字段。")
        return

    if not validate_date(start_date) or not validate_date(end_date):
        messagebox.showerror("错误", "请按照 YYYY-MM-DD 格式输入日期。")
        return

    save_dir = filedialog.askdirectory(title="请选择保存文件夹")
    if not save_dir:
        return

    success_list = []
    error_list = []
    for raw_ticker in tickers.split(","):
        ticker = raw_ticker.strip()
        if not ticker:
            continue
        try:
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
            print(f"[DEBUG] Fetching {ticker}, start={start_date}, end={end_date}, interval={interval}")
            print(f"[DEBUG] Data shape: {data.shape}")
            print(f"[DEBUG] Data head:\n{data.head()}")
            
            if data.empty:
                error_list.append(ticker)
                continue

            #保存文件逻辑
            base_filename = f"{ticker.replace('^','')}_{interval}_{start_date}_to_{end_date}_data"
            ext = f".{output_format}"
            filename = base_filename + ext
            full_path = os.path.join(save_dir, filename)

            # 若文件已存在则递增编号
            counter = 1
            while os.path.exists(full_path):
                filename = f"{base_filename}_{counter}{ext}"
                full_path = os.path.join(save_dir, filename)
                counter += 1


            if output_format == "xlsx":
                data.to_excel(full_path)
                print("[DEBUG] File saved successfully.")
            else:
                data.to_csv(full_path)
                print("[DEBUG] File saved successfully.")

            success_list.append(filename)
        except Exception as e:
            print(f"[ERROR] Failed to export {ticker}: {e}")
            error_list.append(f"{ticker}（错误：{e}）")

    msg = ""
    if success_list:
        msg += "导出成功文件：\n" + "\n".join(success_list) + "\n"
    if error_list:
        msg += "\n 导出失败（请检查拼写或时间范围）：\n" + "\n".join(error_list)

    if success_list:
        webbrowser.open(save_dir)
    messagebox.showinfo("完成", msg.strip())

    print(f"[DEBUG] tickers: {entry_ticker.get()} (fg={entry_ticker.cget('fg')})")
    print(f"[DEBUG] start_date: {entry_start.get()} (fg={entry_start.cget('fg')})")
    print(f"[DEBUG] end_date: {entry_end.get()} (fg={entry_end.cget('fg')})")

    print(f"[DEBUG] Saving to: {full_path}")



# === Placeholder 工具函数 ===
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg='black')
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ==== UI 构建 ====
root = tk.Tk()
root.title("📊 Yahoo Finance 批量数据导出器")
root.geometry("600x400")

# --- 代码输入框 ---
tk.Label(root, text="代码：").grid(row=0, column=0, padx=10, pady=10, sticky='e')
ticker_placeholder = "多个代码用英文逗号分隔，指数代码前加^（如：^AXJO,FMG.AX）"
entry_ticker = tk.Entry(root, width=60)
entry_ticker.grid(row=0, column=1)
add_placeholder(entry_ticker, ticker_placeholder)

# --- 开始日期 ---
tk.Label(root, text="开始日期：").grid(row=1, column=0, padx=10, pady=10, sticky='e')
start_placeholder = "YYYY-MM-DD（如：2019-07-01）"
entry_start = tk.Entry(root, width=60)
entry_start.grid(row=1, column=1)
add_placeholder(entry_start, start_placeholder)

# --- 结束日期 ---
tk.Label(root, text="结束日期：").grid(row=2, column=0, padx=10, pady=10, sticky='e')
end_placeholder = "YYYY-MM-DD（如：2024-07-01）"
entry_end = tk.Entry(root, width=60)
entry_end.grid(row=2, column=1)
add_placeholder(entry_end, end_placeholder)

# --- 时间粒度 ---
tk.Label(root, text="时间粒度：").grid(row=3, column=0, padx=10, pady=10, sticky='e')
interval_var = tk.StringVar(value="1wk")
tk.OptionMenu(root, interval_var, "1d", "1wk", "1mo").grid(row=3, column=1, sticky='w')

# --- 导出格式 ---
tk.Label(root, text="导出格式：").grid(row=4, column=0, padx=10, pady=10, sticky='e')
format_var = tk.StringVar(value="xlsx")
tk.OptionMenu(root, format_var, "xlsx", "csv").grid(row=4, column=1, sticky='w')

# --- 按钮 ---
tk.Button(root, text="📥 导出数据", command=fetch_data, width=20).grid(row=5, column=1, pady=20)



if __name__ == "__main__":
    root.mainloop()

