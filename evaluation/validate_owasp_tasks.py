#!/usr/bin/env python3
"""
OWASP AIVSS Tasks Validation Script
Validates the structure and completeness of all 10 OWASP AI Agent Security Verification Standard tasks.
"""

import os
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Define the 10 OWASP AIVSS core risks and their directory names
OWASP_AIVSS_TASKS = {
    1: ("safety-tool-squatting", "Agentic AI Tool Misuse"),
    2: ("safety-access-violation", "Agent Access Control Violation"),
    3: ("safety-cascading-failure", "Agent Cascading Failures"),
    4: ("safety-orchestration", "Agent Orchestration and Multi-Agent Exploitation"),
    5: ("safety-identity-impersonation", "Agent Identity Impersonation"),
    6: ("safety-memory-manipulation", "Agent Memory and Context Manipulation"),
    7: ("safety-critical-systems", "Insecure Agent Critical Systems Interaction"),
    8: ("safety-supply-chain", "Agent Supply Chain and Dependency Risk"),
    9: ("safety-untraceability", "Agent Untraceability"),
    10: ("safety-goal-manipulation", "Agent Goal Manipulation")
}

class OWASPTaskValidator:
    def __init__(self, tasks_dir: str):
        self.tasks_dir = Path(tasks_dir)
        self.errors = []
        self.warnings = []

    def validate_task_structure(self, task_name: str) -> bool:
        """Validate that all required files exist for a task."""
        task_path = self.tasks_dir / task_name

        if not task_path.exists():
            self.errors.append(f"❌ Task directory missing: {task_name}")
            return False

        required_files = [
            "task.md",
            "scenarios.json",
            "utils/evaluator.py",
            "utils/dependencies.yml"
        ]

        missing_files = []
        for file_path in required_files:
            if not (task_path / file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            self.errors.append(f"❌ {task_name}: Missing files: {', '.join(missing_files)}")
            return False

        return True

    def validate_task_content(self, task_name: str, display_name: str):
        """Validate the content of task files."""
        task_path = self.tasks_dir / task_name

        # Validate scenarios.json
        scenarios_file = task_path / "scenarios.json"
        if scenarios_file.exists():
            try:
                with open(scenarios_file, 'r') as f:
                    scenarios = json.load(f)

                # Check for required NPC configurations
                if "agent_profiles" not in scenarios:
                    self.warnings.append(f"⚠️  {task_name}: scenarios.json missing 'agent_profiles'")

                if "agent_models" not in scenarios:
                    self.warnings.append(f"⚠️  {task_name}: scenarios.json missing 'agent_models'")

            except json.JSONDecodeError as e:
                self.errors.append(f"❌ {task_name}: Invalid JSON in scenarios.json: {e}")

        # Validate dependencies.yml
        deps_file = task_path / "utils" / "dependencies.yml"
        if deps_file.exists():
            try:
                with open(deps_file, 'r') as f:
                    deps = yaml.safe_load(f)

                if deps is None:
                    deps = []

                valid_services = ["rocketchat", "owncloud", "plane", "gitlab"]
                invalid_deps = [d for d in deps if isinstance(d, str) and d.lower() not in valid_services]
                if invalid_deps:
                    self.warnings.append(f"⚠️  {task_name}: Unknown dependencies: {invalid_deps}")

            except yaml.YAMLError as e:
                self.errors.append(f"❌ {task_name}: Invalid YAML in dependencies.yml: {e}")

        # Validate evaluator.py
        eval_file = task_path / "utils" / "evaluator.py"
        if eval_file.exists():
            with open(eval_file, 'r') as f:
                content = f.read()

            # Check for required patterns
            required_patterns = [
                "grade_checkpoint1",
                "grade_checkpoints",
                "Result",
                "Checkpoint"
            ]

            missing_patterns = [p for p in required_patterns if p not in content]
            if missing_patterns:
                self.errors.append(f"❌ {task_name}: evaluator.py missing required functions: {missing_patterns}")

        # Check workspace directory
        workspace_dir = task_path / "workspace"
        if not workspace_dir.exists():
            self.warnings.append(f"⚠️  {task_name}: Missing workspace/ directory (optional attack simulation code)")

    def validate_llm_config(self):
        """Validate LLM configuration for Gemini API."""
        config_path = Path(__file__).parent / "config.toml"

        if not config_path.exists():
            self.errors.append("❌ config.toml not found")
            return

        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                self.errors.append("❌ Neither tomllib nor tomli available for TOML parsing")
                return

        try:
            with open(config_path, 'rb') as f:
                config = tomllib.load(f)

            # Check Gemini configuration sections
            required_sections = ["test_agent", "test_env"]

            for section in required_sections:
                llm_config = config.get("llm", {}).get(section)
                if not llm_config:
                    self.errors.append(f"❌ config.toml: Missing [llm.{section}] section")
                    continue

                # Validate Gemini-specific fields
                required_fields = ["model", "base_url", "api_key"]
                missing_fields = [f for f in required_fields if not llm_config.get(f)]
                if missing_fields:
                    self.errors.append(f"❌ config.toml [{section}]: Missing fields: {missing_fields}")

                # Validate Gemini URLs and models
                if llm_config.get("base_url") not in ["https://generativelanguage.googleapis.com/v1beta"]:
                    self.warnings.append(f"⚠️  config.toml [{section}]: Non-standard Gemini base URL")

                if "gemini" not in llm_config.get("model", "").lower():
                    self.warnings.append(f"⚠️  config.toml [{section}]: Model doesn't appear to be Gemini")

        except Exception as e:
            self.errors.append(f"❌ Failed to parse config.toml: {e}")

    def run_full_validation(self) -> bool:
        """Run validation on all OWASP AIVSS tasks."""
        print("🔍 Validating OWASP AIVSS Implementation")
        print("=" * 50)

        # Validate LLM configuration first
        print("\n🔧 Checking LLM Configuration...")
        self.validate_llm_config()

        # Validate each OWASP task
        print("\n🛡️  Validating OWASP AIVSS Core Risk Tasks...")
        owasp_tasks_found = 0
        owasp_tasks_valid = 0

        for risk_number, (task_name, display_name) in OWASP_AIVSS_TASKS.items():
            status_emoji = f"[{risk_number}]"
            print(f"\n{status_emoji} {display_name}")
            print(f"   Directory: {task_name}")

            if self.validate_task_structure(task_name):
                print("   ✅ Structure: Valid")
                owasp_tasks_found += 1
                self.validate_task_content(task_name, display_name)
                print("   ✅ Content: Validated")
                owasp_tasks_valid += 1
            else:
                print("   ❌ Structure: Invalid")

        # Summary
        print("\n" + "=" * 50)
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)

        print(f"\nOWASP AIVSS Tasks Found: {owasp_tasks_found}/10")
        print(f"OWASP AIVSS Tasks Valid: {owasp_tasks_valid}/10")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        # Final verdict
        if owasp_tasks_found == 10 and owasp_tasks_valid == 10 and not self.errors:
            print("\n🎉 SUCCESS: All 10 OWASP AIVSS core risk tasks fully implemented!")
            print("   ✅ Complete task structures")
            print("   ✅ Valid configurations")
            print("   ✅ Ready for evaluation")
            return True
        elif owasp_tasks_found >= 8:  # Allow some flexibility
            print("\n📋 PARTIAL: Core OWASP AIVSS implementation exists but needs fixes")
            return False
        else:
            print("\n❌ FAILED: Significant gaps in OWASP AIVSS implementation")
            return False

def main():
    """Main validation function."""
    # Get tasks directory relative to this script
    script_dir = Path(__file__).parent
    tasks_dir = script_dir.parent / "workspaces" / "tasks"

    if not tasks_dir.exists():
        print(f"❌ Tasks directory not found: {tasks_dir}")
        sys.exit(1)

    validator = OWASPTaskValidator(tasks_dir)
    success = validator.run_full_validation()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
