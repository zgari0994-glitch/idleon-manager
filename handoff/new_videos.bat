@echo off
cd /d %~dp0
py list_videos.py || goto :err
py new_videos.py || goto :err
py run_apify.py --list idleon_transcripts\new_video_list.csv --cap 3 || goto :err
echo Done. Zip the idleon_transcripts folder and tell Claude.
pause
exit /b
:err
echo Something failed above. Copy the message to Claude.
pause
