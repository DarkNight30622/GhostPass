@echo off
echo 🚀 Quick GHOST PASS Push to GitHub
echo.

echo 📦 Adding all files...
git add .

echo 📝 Committing...
git commit -m "🚀 Cleaned up GhostPass, finalized code & docs"

echo 🔗 Adding remote...
set /p username=Enter GitHub username: 
git remote add origin https://github.com/%username%/ghostpass.git

echo ⬆️ Pushing to GitHub...
git push -u origin main

echo ✅ Done!
pause 