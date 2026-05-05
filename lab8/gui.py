import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

try:
    from readLogLab3 import readLog
    from getEntriesInTimeRangeLab3 import getEntriesInTimeRange
except ImportError as e:
    print(f"Błąd importu: {e}")
    
    def readLog(stream): return []
    def getEntriesInTimeRange(logs, start, end): return logs


class LogBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log browser")
        self.root.geometry("900x500")
        
        self.allLogs = []
        self.dateLogs = []
        
        self.buildGui()

    def buildGui(self):
        mainFrame = ttk.Frame(self.root, padding="10")
        mainFrame.pack(fill=tk.BOTH, expand=True)

        topFrame = ttk.Frame(mainFrame)
        topFrame.pack(fill=tk.X, pady=(0, 15))
        
        self.filepathVar = tk.StringVar()
        ttk.Entry(topFrame, textvariable=self.filepathVar, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(topFrame, text="Open", command=self.openFile).pack(side=tk.RIGHT)

        midFrame = ttk.Frame(mainFrame)
        midFrame.pack(fill=tk.BOTH, expand=True)

        leftFrame = ttk.Frame(midFrame)
        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        filterFrame = ttk.Frame(leftFrame)
        filterFrame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filterFrame, text="From").pack(side=tk.LEFT)
        self.dateFromVar = tk.StringVar()
        ttk.Entry(filterFrame, textvariable=self.dateFromVar, width=12).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(filterFrame, text="To").pack(side=tk.LEFT)
        self.dateToVar = tk.StringVar()
        ttk.Entry(filterFrame, textvariable=self.dateToVar, width=12).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(filterFrame, text="Filter", command=self.applyFilter).pack(side=tk.LEFT)

        listFrame = ttk.Frame(leftFrame)
        listFrame.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(listFrame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.logListbox = tk.Listbox(listFrame, yscrollcommand=self.scrollbar.set, font=('Consolas', 9))
        self.logListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.logListbox.yview)
        self.logListbox.bind('<<ListboxSelect>>', self.onLogSelect)

        rightFrame = ttk.Frame(midFrame)
        rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.detailVars = {
            "Remote host": tk.StringVar(),
            "Date": tk.StringVar(),
            "Time": tk.StringVar(),
            "Timezone": tk.StringVar(),
            "Status code": tk.StringVar(),
            "Method": tk.StringVar(),
            "Resource": tk.StringVar(),
            "Size": tk.StringVar()
        }

        row = 0
        for labelText, var in self.detailVars.items():
            ttk.Label(rightFrame, text=labelText + ":", font=('', 9, 'bold')).grid(row=row, column=0, sticky=tk.E, padx=5, pady=8)
            
            if labelText in ["Status code", "Time", "Timezone", "Remote host", "Date"]:
                ttk.Entry(rightFrame, textvariable=var, state='readonly', width=20).grid(row=row, column=1, sticky=tk.W, padx=5, pady=8)
            else:
                ttk.Entry(rightFrame, textvariable=var, state='readonly', width=45).grid(row=row, column=1, sticky=tk.W, padx=5, pady=8)
            row += 1

        bottomFrame = ttk.Frame(mainFrame)
        bottomFrame.pack(fill=tk.X, pady=(15, 0))
        
        self.btnPrev = ttk.Button(bottomFrame, text="Previous", command=self.selectPrev, state=tk.DISABLED)
        self.btnPrev.pack(side=tk.LEFT)
        
        self.btnNext = ttk.Button(bottomFrame, text="Next", command=self.selectNext, state=tk.DISABLED)
        self.btnNext.pack(side=tk.RIGHT)

    def openFile(self):
        filepath = filedialog.askopenfilename(title="Wybierz plik z logami", filetypes=(("Log files", "*.log"), ("All files", "*.*")))
        if filepath:
            self.filepathVar.set(filepath)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.allLogs = readLog(f) 
                    
                self.currentDisplayLogs = self.allLogs
                self.updateListbox()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać pliku: {e}")

    def applyFilter(self):
        dFromStr = self.dateFromVar.get().strip()
        dToStr = self.dateToVar.get().strip()
        
        try:
            formatStr = '%Y-%m-%d %H:%M:%S'

            startDt = datetime.strptime(dFromStr, formatStr) if dFromStr else datetime.min
            endDt = datetime.strptime(dToStr, formatStr) if dToStr else datetime.max
            
            self.currentDisplayLogs = getEntriesInTimeRange(self.allLogs, startDt, endDt)
            self.updateListbox()
        except ValueError:
            messagebox.showwarning("Błąd formatu", "Użyj formatu daty: YYYY-MM-DD")

    def formatMasterItem(self, logEntry):
        try:
            ts = logEntry[0].strftime("%d/%b/%Y:%H:%M:%S") if isinstance(logEntry[0], datetime) else str(logEntry[0])
            ip = str(logEntry[2])
            method = str(logEntry[6])
            uri = str(logEntry[8])
            
            line = f'{ip} - - [{ts}] "{method} {uri}"'
            return line[:50] + "..." if len(line) > 50 else line
        except (IndexError, TypeError):
            return str(logEntry)[:50]

    def updateListbox(self):
        self.logListbox.delete(0, tk.END)
        for log in self.currentDisplayLogs:
            self.logListbox.insert(tk.END, self.formatMasterItem(log))
        self.updateNavButtons()

    def onLogSelect(self, event=None):
        selection = self.logListbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        log = self.currentDisplayLogs[index]
        
        for var in self.detailVars.values():
            var.set("")
            
        try:
            if isinstance(log[0], datetime):
                self.detailVars["Date"].set(log[0].strftime("%Y-%m-%d"))
                self.detailVars["Time"].set(log[0].strftime("%H:%M:%S"))
                self.detailVars["Timezone"].set("UTC")
            else:
                self.detailVars["Date"].set(str(log[0]))

            if len(log) > 2:
                self.detailVars["Remote host"].set(str(log[2]))
                
            if len(log) > 6:
                self.detailVars["Method"].set(str(log[6]))
                
            if len(log) > 8:
                self.detailVars["Resource"].set(str(log[8]))
                
            if len(log) > 9:
                self.detailVars["Status code"].set(str(log[9]))

            if len(log) > 10:
                self.detailVars["Size"].set(f"{log[10]} Bytes")
            else:
                self.detailVars["Size"].set("- Bytes")

        except IndexError:
            pass

        self.updateNavButtons()

    def updateNavButtons(self):
        selection = self.logListbox.curselection()
        if not selection or not self.currentDisplayLogs:
            self.btnPrev.config(state=tk.DISABLED)
            self.btnNext.config(state=tk.DISABLED)
            return

        index = selection[0]
        self.btnPrev.config(state=tk.NORMAL if index > 0 else tk.DISABLED)
        self.btnNext.config(state=tk.NORMAL if index < len(self.currentDisplayLogs) - 1 else tk.DISABLED)

    def selectPrev(self):
        selection = self.logListbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0] - 1
            self.logListbox.selection_clear(0, tk.END)
            self.logListbox.selection_set(index)
            self.logListbox.see(index)
            self.onLogSelect()

    def selectNext(self):
        selection = self.logListbox.curselection()
        if selection and selection[0] < len(self.currentDisplayLogs) - 1:
            index = selection[0] + 1
            self.logListbox.selection_clear(0, tk.END)
            self.logListbox.selection_set(index)
            self.logListbox.see(index)
            self.onLogSelect()

if __name__ == "__main__":
    root = tk.Tk()
    app = LogBrowserApp(root)
    root.mainloop()