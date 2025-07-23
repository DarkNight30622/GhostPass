#!/usr/bin/env python3
"""
GHOST PASS GitHub Push Script

Automatically pushes the GHOST PASS codebase to GitHub.
"""

import os
import sys
import subprocess
import getpass


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def main():
    """Main function to push code to GitHub."""
    print("🚀 GHOST PASS GitHub Push Script")
    print("=" * 50)
    
    # Check if git is available
    if not run_command("git --version", "Checking git availability"):
        print("❌ Git is not available. Please install Git first.")
        return False
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("📁 Initializing git repository...")
        if not run_command("git init", "Initializing git repository"):
            return False
    
    # Stage all files
    if not run_command("git add .", "Staging all files"):
        return False
    
    # Check status
    if not run_command("git status", "Checking git status"):
        return False
    
    # Commit changes
    commit_message = "🚀 Cleaned up GhostPass, finalized code & docs"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return False
    
    # Get GitHub username
    print("\n🔗 Setting up GitHub remote...")
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("❌ Username is required.")
        return False
    
    # Add remote
    remote_url = f"https://github.com/{username}/ghostpass.git"
    if not run_command(f"git remote add origin {remote_url}", "Adding remote repository"):
        # If remote already exists, set the URL
        run_command(f"git remote set-url origin {remote_url}", "Updating remote URL")
    
    # Verify remote
    if not run_command("git remote -v", "Verifying remote"):
        return False
    
    # Push to GitHub
    print("\n⬆️ Pushing to GitHub...")
    print("Note: You may be prompted for your GitHub credentials.")
    
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        return False
    
    print("\n✅ Push completed successfully!")
    print(f"🎉 GHOST PASS is now live on GitHub!")
    print(f"📍 Repository: https://github.com/{username}/ghostpass")
    print("\n📋 Next steps:")
    print("1. Go to your GitHub repository")
    print("2. Create a new release (v0.1.0)")
    print("3. Add release notes from CHANGELOG.md")
    print("4. Build executables with: python build.py")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 