from typing import Dict, List, Set

# Department to role mapping
ROLE_DEPARTMENTS: Dict[str, Set[str]] = {
    "admin": {"engineering", "finance", "hr", "marketing", "general"},
    "engineering": {"engineering", "general"},
    "finance": {"finance", "general"},
    "hr": {"hr", "general"},
    "marketing": {"marketing", "general"},
    "user": {"general"}
}

# Department to data directory mapping
DEPARTMENT_DIRS: Dict[str, str] = {
    "engineering": "engineering",
    "finance": "finance",
    "hr": "hr",
    "marketing": "marketing",
    "general": "general"
}

def get_allowed_departments(role: str) -> Set[str]:
    """Get the set of departments a role can access."""
    return ROLE_DEPARTMENTS.get(role, {"general"})

def is_department_allowed(role: str, department: str) -> bool:
    """Check if a role has access to a specific department."""
    return department in get_allowed_departments(role) 