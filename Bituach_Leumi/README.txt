==========================
	PROJECT README
==========================
creating a Lambda layer should be in the following format:

(*)python -> lib -> python{version} -> site_packages
(*)to access the file search in the search bar for "\\wsl$"
(*)zip the python dir and save into s3

** example for a pip install:
pip install --target=/home/sassgabai/python/lib/python3.10/site-packages PyPDF2

