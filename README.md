attendance_system/
├── main.py                 # Entry point with CLI menu
├── config.py              # Configuration & database setup
├── modules/
│   ├── __init__.py
│   ├── attendance.py      # Attendance marking & retrieval
│   ├── database.py        # Database operations
│   ├── csv_handler.py     # CSV export/import
│   ├── reports.py         # Report generation
│   ├── validation.py      # Input validation
│   └── sync.py            # CSV-Database sync
├── gui/
│   └── gui_app.py         # Tkinter GUI interface
├── backup/                # Auto-backup directory
├── reports/               # Generated reports directory
├── data/                  # CSV & Database files
└── requirements.txt       # Dependencies