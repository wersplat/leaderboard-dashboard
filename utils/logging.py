# Ensure the directory for the log file exists only if a directory path is provided
if log_file and os.path.dirname(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)