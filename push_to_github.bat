@echo off
echo 🚀 Pushing GHOST PASS to GitHub...
echo.

echo 📋 Checking git status...
git status
echo.

echo 📦 Staging all files...
git add .
echo.

echo 📝 Committing changes...
git commit -m "🚀 Cleaned up GhostPass, finalized code & docs"
echo.

echo 🔗 Setting up remote repository...
echo Please enter your GitHub username:
set /p username=
git remote add origin https://github.com/%username%/ghostpass.git
echo.

echo 🔍 Verifying remote...
git remote -v
echo.

echo ⬆️ Pushing to GitHub...
git push -u origin main
echo.

echo ✅ Push completed!
echo.
echo 🎉 GHOST PASS is now live on GitHub!
echo 📍 Repository: https://github.com/%username%/ghostpass
echo.
pause 