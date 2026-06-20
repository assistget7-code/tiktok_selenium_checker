#!/bin/bash
pip install -r requirements.txt
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
