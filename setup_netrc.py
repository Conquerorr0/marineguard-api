"""
Setup .netrc file for NASA Earthdata authentication
Run this script to configure credentials for OPeNDAP access
"""

import os
import stat
from pathlib import Path


def setup_netrc(username, password):
    """
    Creates ~/.netrc file with NASA Earthdata credentials.
    
    Args:
        username: FatihAltuntas
        password: F@tih11031103
    """
    netrc_path = Path.home() / '.netrc'
    
    netrc_content = f"""machine urs.earthdata.nasa.gov
    login {username}
    password {password}
"""
    
    # Write .netrc file
    with open(netrc_path, 'w') as f:
        f.write(netrc_content)
    
    # Set proper permissions (read/write for owner only)
    os.chmod(netrc_path, stat.S_IRUSR | stat.S_IWUSR)
    
    print(f"✅ .netrc file created at: {netrc_path}")
    print(f"   Permissions: {oct(os.stat(netrc_path).st_mode)[-3:]}")


def setup_from_env():
    """Setup .netrc from environment variables."""
    username = os.environ.get('EARTHDATA_USERNAME')
    password = os.environ.get('EARTHDATA_PASSWORD')
    
    if not username or not password:
        print("❌ EARTHDATA_USERNAME and EARTHDATA_PASSWORD environment variables not set")
        print("\nPlease set them:")
        print("  export EARTHDATA_USERNAME=your_username")
        print("  export EARTHDATA_PASSWORD=your_password")
        print("\nOr create a .env file with:")
        print("  EARTHDATA_USERNAME=your_username")
        print("  EARTHDATA_PASSWORD=your_password")
        return False
    
    setup_netrc(username, password)
    return True


def setup_interactive():
    """Interactive setup for .netrc."""
    print("="*70)
    print("NASA EARTHDATA .netrc SETUP")
    print("="*70)
    print("\nYou need a NASA Earthdata account to access OPeNDAP data.")
    print("Sign up at: https://urs.earthdata.nasa.gov/\n")
    
    username = input("Enter your Earthdata username: ").strip()
    password = input("Enter your Earthdata password: ").strip()
    
    if not username or not password:
        print("❌ Username and password cannot be empty")
        return False
    
    setup_netrc(username, password)
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("NASA EARTHDATA AUTHENTICATION SETUP")
    print("="*70 + "\n")
    
    # Try environment variables first
    if not setup_from_env():
        # Fall back to interactive
        print("\nSwitching to interactive mode...\n")
        setup_interactive()
    
    print("\n" + "="*70)
    print("Setup complete! You can now access NASA OPeNDAP data.")
    print("="*70 + "\n")

