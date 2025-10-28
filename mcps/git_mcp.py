"""
Git MCP - Model Context Protocol for Git and GitHub operations
"""
import os
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime
from mcps.mcp_manager import BaseMCP


class GitMCP(BaseMCP):
    """MCP for Git operations (local repository management)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.repo_path = config.get("repo_path", ".")
        self.user_name = config.get("git_user_name", "")
        self.user_email = config.get("git_user_email", "")
        self._initialized = False
    
    async def initialize(self):
        """Initialize Git repository if needed"""
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            self.logger.info("Initializing Git repository")
            await self._run_command(["git", "init"])
        
        # Configure user if provided
        if self.user_name:
            await self._run_command(["git", "config", "user.name", self.user_name])
        if self.user_email:
            await self._run_command(["git", "config", "user.email", self.user_email])
        
        self._initialized = True
    
    async def execute(self, operation: str, **kwargs) -> Any:
        """Execute Git operation"""
        if not self._initialized:
            await self.initialize()
        
        operations = {
            "status": self.get_status,
            "add": self.add_files,
            "commit": self.commit,
            "push": self.push,
            "pull": self.pull,
            "create_branch": self.create_branch,
            "checkout": self.checkout_branch,
            "log": self.get_log,
            "diff": self.get_diff
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown Git operation: {operation}")
        
        return await operations[operation](**kwargs)
    
    async def _run_command(
        self,
        command: List[str],
        cwd: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run a Git command"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            self.logger.error(f"Git command timed out: {' '.join(command)}")
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            self.logger.error(f"Git command failed: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get repository status"""
        result = await self._run_command(["git", "status", "--porcelain"])
        
        if result["success"]:
            lines = result["stdout"].strip().split("\n") if result["stdout"].strip() else []
            return {
                "success": True,
                "modified": [line[3:] for line in lines if line.startswith(" M")],
                "added": [line[3:] for line in lines if line.startswith("A ")],
                "deleted": [line[3:] for line in lines if line.startswith(" D")],
                "untracked": [line[3:] for line in lines if line.startswith("??")],
                "clean": len(lines) == 0
            }
        
        return {"success": False, "error": result["stderr"]}
    
    async def add_files(self, files: List[str] = None) -> Dict[str, Any]:
        """Add files to staging area"""
        if files is None:
            files = ["."]  # Add all files
        
        command = ["git", "add"] + files
        result = await self._run_command(command)
        
        return {
            "success": result["success"],
            "files_added": files if result["success"] else [],
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def commit(
        self,
        message: str,
        add_all: bool = True
    ) -> Dict[str, Any]:
        """Commit changes"""
        if add_all:
            await self.add_files()
        
        result = await self._run_command(["git", "commit", "-m", message])
        
        return {
            "success": result["success"],
            "message": message,
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def push(
        self,
        remote: str = "origin",
        branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """Push changes to remote"""
        command = ["git", "push", remote]
        if branch:
            command.append(branch)
        
        result = await self._run_command(command)
        
        return {
            "success": result["success"],
            "remote": remote,
            "branch": branch,
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def pull(
        self,
        remote: str = "origin",
        branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pull changes from remote"""
        command = ["git", "pull", remote]
        if branch:
            command.append(branch)
        
        result = await self._run_command(command)
        
        return {
            "success": result["success"],
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def create_branch(self, branch_name: str) -> Dict[str, Any]:
        """Create a new branch"""
        result = await self._run_command(["git", "branch", branch_name])
        
        return {
            "success": result["success"],
            "branch": branch_name,
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def checkout_branch(
        self,
        branch_name: str,
        create: bool = False
    ) -> Dict[str, Any]:
        """Checkout a branch"""
        command = ["git", "checkout"]
        if create:
            command.append("-b")
        command.append(branch_name)
        
        result = await self._run_command(command)
        
        return {
            "success": result["success"],
            "branch": branch_name,
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def get_log(self, max_count: int = 10) -> Dict[str, Any]:
        """Get commit log"""
        result = await self._run_command([
            "git", "log",
            f"-{max_count}",
            "--pretty=format:%H|%an|%ae|%ai|%s"
        ])
        
        if result["success"]:
            commits = []
            for line in result["stdout"].strip().split("\n"):
                if line:
                    parts = line.split("|")
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    })
            
            return {"success": True, "commits": commits}
        
        return {"success": False, "error": result["stderr"]}
    
    async def get_diff(self, cached: bool = False) -> Dict[str, Any]:
        """Get diff of changes"""
        command = ["git", "diff"]
        if cached:
            command.append("--cached")
        
        result = await self._run_command(command)
        
        return {
            "success": result["success"],
            "diff": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }
    
    async def health_check(self) -> bool:
        """Check if Git is available"""
        try:
            result = await self._run_command(["git", "--version"])
            return result["success"]
        except:
            return False


class GitHubMCP(BaseMCP):
    """MCP for GitHub operations (remote repository management)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.token = config.get("github_token", "")
        self.username = config.get("github_username", "")
        self.default_repo = config.get("github_default_repo", "")
    
    async def execute(self, operation: str, **kwargs) -> Any:
        """Execute GitHub operation"""
        operations = {
            "create_repo": self.create_repository,
            "add_remote": self.add_remote,
            "create_issue": self.create_issue,
            "create_pr": self.create_pull_request
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown GitHub operation: {operation}")
        
        return await operations[operation](**kwargs)
    
    async def create_repository(
        self,
        name: str,
        private: bool = False,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a GitHub repository using gh CLI or API"""
        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            data = {
                "name": name,
                "private": private,
                "description": description
            }
            
            response = requests.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    "success": True,
                    "repo_url": repo_data["html_url"],
                    "clone_url": repo_data["clone_url"]
                }
            else:
                return {
                    "success": False,
                    "error": response.json().get("message", "Unknown error")
                }
        
        except Exception as e:
            self.logger.error(f"Failed to create repository: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_remote(
        self,
        repo_path: str,
        remote_name: str = "origin",
        remote_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add remote to local repository"""
        if not remote_url and self.default_repo:
            remote_url = f"https://github.com/{self.default_repo}.git"
        
        if not remote_url:
            return {"success": False, "error": "No remote URL provided"}
        
        try:
            result = subprocess.run(
                ["git", "remote", "add", remote_name, remote_url],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "remote_name": remote_name,
                "remote_url": remote_url,
                "error": result.stderr if result.returncode != 0 else None
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_issue(
        self,
        title: str,
        body: str,
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a GitHub issue"""
        # Placeholder - would use GitHub API
        return {"success": False, "error": "Not implemented yet"}
    
    async def create_pull_request(
        self,
        title: str,
        body: str,
        head: str,
        base: str = "main",
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a pull request"""
        # Placeholder - would use GitHub API
        return {"success": False, "error": "Not implemented yet"}
    
    async def health_check(self) -> bool:
        """Check if GitHub API is accessible"""
        if not self.token:
            return False
        
        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
        except:
            return False
