"""
Version Control Agent - Manages Git and GitHub operations for the project
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.base_agent import BaseAgent


class VersionControlAgent(BaseAgent):
    """
    Agent responsible for version control operations
    - Commits code changes
    - Creates branches for experiments
    - Pushes to GitHub
    - Manages project history
    """
    
    def __init__(
        self,
        name: str,
        agent_id: str,
        config: Dict[str, Any],
        shared_memory: Any,
        mcp_manager: Any
    ):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
        self.auto_commit = config.get("auto_commit", True)
        self.auto_push = config.get("auto_push", False)
        self.branch_prefix = config.get("branch_prefix", "linguistic-bridges")
        self.commit_message_template = config.get(
            "commit_message_template",
            "[{agent}] {action}: {description}"
        )
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute version control task"""
        task_type = task.get("type", "unknown")
        
        if task_type == "commit_changes":
            return await self.commit_changes(task)
        elif task_type == "create_experiment_branch":
            return await self.create_experiment_branch(task)
        elif task_type == "push_changes":
            return await self.push_changes(task)
        elif task_type == "sync_repository":
            return await self.sync_repository(task)
        elif task_type == "get_status":
            return await self.get_repository_status()
        elif task_type == "get_history":
            return await self.get_commit_history(task)
        else:
            self.logger.warning(f"Unknown task type: {task_type}")
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def commit_changes(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Commit changes to the repository
        
        Args:
            task: {
                "agent_name": name of the agent making changes,
                "action": action performed (e.g., "implemented", "fixed", "added"),
                "description": description of changes,
                "files": optional list of specific files to commit,
                "auto": whether to auto-commit (overrides config)
            }
        """
        self.state = "committing"
        
        agent_name = task.get("agent_name", "system")
        action = task.get("action", "updated")
        description = task.get("description", "project files")
        files = task.get("files", None)
        auto = task.get("auto", self.auto_commit)
        
        # Generate commit message
        commit_message = self.commit_message_template.format(
            agent=agent_name,
            action=action,
            description=description
        )
        
        self.logger.info(f"Committing changes: {commit_message}")
        
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            
            # Check status first
            status = await git_mcp.get_status()
            
            if status.get("clean", True):
                self.logger.info("No changes to commit")
                self.state = "idle"
                return {
                    "success": True,
                    "message": "No changes to commit",
                    "committed": False
                }
            
            # Add files
            if files:
                add_result = await git_mcp.add_files(files=files)
            else:
                add_result = await git_mcp.add_files()  # Add all
            
            if not add_result["success"]:
                self.state = "idle"
                return {
                    "success": False,
                    "error": "Failed to add files",
                    "details": add_result.get("error")
                }
            
            # Request approval if not auto-commit
            if not auto:
                approved = await self.request_human_approval(
                    decision=f"Commit changes: {commit_message}",
                    context={
                        "message": commit_message,
                        "modified": status.get("modified", []),
                        "added": status.get("added", []),
                        "deleted": status.get("deleted", [])
                    }
                )
                
                if not approved:
                    self.state = "idle"
                    return {
                        "success": False,
                        "message": "Commit cancelled by user"
                    }
            
            # Commit
            commit_result = await git_mcp.commit(
                message=commit_message,
                add_all=False  # Already added
            )
            
            if commit_result["success"]:
                # Store commit info in memory
                await self.store_in_memory(
                    content=commit_message,
                    metadata={
                        "type": "git_commit",
                        "agent": agent_name,
                        "action": action,
                        "timestamp": datetime.now().isoformat()
                    },
                    collection="version_control"
                )
                
                self.logger.info(f"✅ Changes committed: {commit_message}")
                self.state = "idle"
                
                return {
                    "success": True,
                    "message": commit_message,
                    "committed": True,
                    "output": commit_result.get("output")
                }
            else:
                self.state = "idle"
                return {
                    "success": False,
                    "error": "Commit failed",
                    "details": commit_result.get("error")
                }
        
        except Exception as e:
            self.logger.error(f"Commit failed: {e}")
            self.state = "idle"
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_experiment_branch(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new branch for an experiment
        
        Args:
            task: {
                "experiment_name": name of the experiment,
                "base_branch": base branch to create from (default: current)
            }
        """
        self.state = "creating_branch"
        
        experiment_name = task.get("experiment_name", "experiment")
        base_branch = task.get("base_branch", None)
        
        # Generate branch name
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"{self.branch_prefix}/{experiment_name}-{timestamp}"
        
        self.logger.info(f"Creating branch: {branch_name}")
        
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            
            # Checkout base branch if specified
            if base_branch:
                await git_mcp.checkout_branch(base_branch)
            
            # Create and checkout new branch
            result = await git_mcp.checkout_branch(
                branch_name=branch_name,
                create=True
            )
            
            if result["success"]:
                self.logger.info(f"✅ Branch created: {branch_name}")
                self.state = "idle"
                
                return {
                    "success": True,
                    "branch_name": branch_name,
                    "message": f"Created experiment branch: {branch_name}"
                }
            else:
                self.state = "idle"
                return {
                    "success": False,
                    "error": "Failed to create branch",
                    "details": result.get("error")
                }
        
        except Exception as e:
            self.logger.error(f"Branch creation failed: {e}")
            self.state = "idle"
            return {
                "success": False,
                "error": str(e)
            }
    
    async def push_changes(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Push changes to remote repository
        
        Args:
            task: {
                "remote": remote name (default: "origin"),
                "branch": branch to push (default: current),
                "auto": whether to auto-push (overrides config)
            }
        """
        self.state = "pushing"
        
        remote = task.get("remote", "origin")
        branch = task.get("branch", None)
        auto = task.get("auto", self.auto_push)
        
        self.logger.info(f"Pushing to {remote}/{branch or 'current branch'}")
        
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            
            # Request approval if not auto-push
            if not auto:
                approved = await self.request_human_approval(
                    decision=f"Push changes to {remote}/{branch or 'current branch'}",
                    context={
                        "remote": remote,
                        "branch": branch
                    }
                )
                
                if not approved:
                    self.state = "idle"
                    return {
                        "success": False,
                        "message": "Push cancelled by user"
                    }
            
            # Push
            result = await git_mcp.push(remote=remote, branch=branch)
            
            if result["success"]:
                self.logger.info(f"✅ Changes pushed to {remote}")
                self.state = "idle"
                
                return {
                    "success": True,
                    "remote": remote,
                    "branch": branch,
                    "message": "Changes pushed successfully"
                }
            else:
                self.state = "idle"
                return {
                    "success": False,
                    "error": "Push failed",
                    "details": result.get("error")
                }
        
        except Exception as e:
            self.logger.error(f"Push failed: {e}")
            self.state = "idle"
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sync_repository(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sync repository (pull from remote)
        
        Args:
            task: {
                "remote": remote name (default: "origin"),
                "branch": branch to pull (default: current)
            }
        """
        self.state = "syncing"
        
        remote = task.get("remote", "origin")
        branch = task.get("branch", None)
        
        self.logger.info(f"Syncing with {remote}/{branch or 'current branch'}")
        
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            
            result = await git_mcp.pull(remote=remote, branch=branch)
            
            if result["success"]:
                self.logger.info(f"✅ Repository synced with {remote}")
                self.state = "idle"
                
                return {
                    "success": True,
                    "remote": remote,
                    "branch": branch,
                    "message": "Repository synced successfully",
                    "output": result.get("output")
                }
            else:
                self.state = "idle"
                return {
                    "success": False,
                    "error": "Sync failed",
                    "details": result.get("error")
                }
        
        except Exception as e:
            self.logger.error(f"Sync failed: {e}")
            self.state = "idle"
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_repository_status(self) -> Dict[str, Any]:
        """Get current repository status"""
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            status = await git_mcp.get_status()
            
            return {
                "success": True,
                "status": status
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_commit_history(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get commit history"""
        max_count = task.get("max_count", 10)
        
        try:
            git_mcp = self.mcp_manager.get_mcp("git")
            result = await git_mcp.get_log(max_count=max_count)
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
