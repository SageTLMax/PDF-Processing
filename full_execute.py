import subprocess

subprocess.run(["cmd.exe", "/c", "python", "merge_to_pdf.py"])
subprocess.run(["cmd.exe", "/c", "python", "compress_pdf.py"])
subprocess.run(["cmd.exe", "/c", "python", "ocr_pdf.py"])