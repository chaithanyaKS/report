# usr/bin/env bash
python -m celery -A report worker --uid=celery -l INFO -S django -E --pool=eventlet &