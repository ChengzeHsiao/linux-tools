#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FreeIPA User Password Expiration Reset Tool
CLI tool for automated management of FreeIPA user password expiration times
"""

import subprocess
import sys
import re
import os
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import argparse

class FreeIPAPasswordReset:
    def __init__(self, demo_mode=False):
        self.users_data = []
        self.demo_mode = demo_mode
    
    def install_to_system(self) -> bool:
        """
        Install the current executable to system path
        
        Returns:
            bool: True if installation successful, False otherwise
        """
        executable_name = "freeipa-password-reset"
        install_dir = "/usr/local/bin"
        
        # Get current executable path
        current_exe = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        
        # If running from Python script, inform user to use packaged version
        if not getattr(sys, 'frozen', False):
            print("❌ Error: Self-installation only works with packaged executable")
            print("Please use the packaged version created with PyInstaller")
            return False
        
        print("FreeIPA Password Reset Tool - Self Installation")
        print("=================================================")
        
        # Check if running as root or with sudo
        if os.geteuid() != 0:
            print("❌ Error: Installation requires root privileges")
            print(f"Usage: sudo {current_exe} --install")
            return False
        
        target_path = os.path.join(install_dir, executable_name)
        
        try:
            print(f"📦 Installing {executable_name} to {install_dir}...")
            
            # Create install directory if it doesn't exist
            os.makedirs(install_dir, exist_ok=True)
            
            # Copy executable to install directory
            shutil.copy2(current_exe, target_path)
            
            # Set proper permissions
            os.chmod(target_path, 0o755)
            
            # Verify installation
            if os.path.isfile(target_path):
                print("✅ Installation successful!")
                print(f"📍 Executable installed at: {target_path}")
                print(f"🚀 You can now run the tool from anywhere using: {executable_name}")
                print("")
                print("Usage examples:")
                print(f"  {executable_name} --help")
                print(f"  {executable_name} --demo --list-only")
                print(f"  {executable_name} --demo --users user1,user2 --expiration 2030-12-31T12:00:00Z")
                return True
            else:
                print("❌ Installation failed!")
                return False
                
        except PermissionError:
            print("❌ Error: Permission denied. Please run with sudo.")
            return False
        except Exception as e:
            print(f"❌ Error during installation: {e}")
            return False
    
    def execute_command(self, command: str) -> tuple:
        """
        Execute command directly on the system
        
        Args:
            command: Command to execute
            
        Returns:
            tuple: (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command execution timeout"
        except Exception as e:
            return 1, "", str(e)
    

    

    
    def get_users_list(self) -> bool:
        """
        Get user list information
        """
        print("Getting user list...")
        
        # Demo mode - use mock data
        if self.demo_mode:
            print("Running in demo mode with mock data...")
            mock_data = """
  User login: testuser1
  First name: Test
  Last name: User1
  UID: 1001
  Email address: testuser1@example.com
  User password expiration: 2024-03-15T12:00:00Z
  Member of groups: users, developers

  User login: testuser2
  First name: Test
  Last name: User2
  UID: 1002
  Email address: testuser2@example.com
  User password expiration: 2024-04-20T12:00:00Z
  Member of groups: users

  User login: admin
  First name: Administrator
  Last name: 
  UID: 1000
  Email address: admin@example.com
  User password expiration: 2030-12-31T12:00:00Z
  Member of groups: admins, users
            """
            self.parse_users_data(mock_data)
            print(f"Demo mode - Loaded {len(self.users_data)} mock users")
            return True
        
        # Use ipa user-find with structured output
        command = 'ipa user-find --all --raw'
        ret_code, stdout, stderr = self.execute_command(command)
        
        # If the structured command fails, try the basic command
        if ret_code != 0:
            print("Structured command failed, trying basic command...")
            command = 'ipa user-find --all'
            ret_code, stdout, stderr = self.execute_command(command)
            
            if ret_code != 0:
                print(f"Error: Failed to get user list - {stderr}")
                print("\nHint: If FreeIPA is not installed, try running with --demo flag for testing")
                return False
        
        # Parse user information
        self.parse_users_data(stdout)
        return True
    
    def parse_users_data(self, raw_data: str):
        """
        Parse user data - Enhanced to handle FreeIPA's actual output format
        """
        self.users_data = []
        
        # Try to parse structured output first (--raw format)
        if self.parse_structured_output(raw_data):
            return
        
        # Fallback to parsing standard output
        self.parse_standard_output(raw_data)
    
    def parse_structured_output(self, raw_data: str) -> bool:
        """
        Parse structured FreeIPA output (--raw format)
        """
        try:
            lines = raw_data.split('\n')
            current_user = {}
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    if current_user and ('uid' in current_user or 'login' in current_user):
                        self.users_data.append(current_user)
                        current_user = {}
                    continue
                
                if line.startswith('dn: uid='):
                    # Extract username from DN
                    try:
                        login = line.split('uid=')[1].split(',')[0]
                        current_user['login'] = login
                    except:
                        pass
                elif ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'givenName':
                        current_user['first_name'] = value
                    elif key == 'sn':
                        current_user['last_name'] = value
                    elif key == 'uidNumber':
                        current_user['uid'] = value
                    elif key == 'mail':
                        current_user['email'] = value
                    elif key == 'krbPasswordExpiration':
                        current_user['password_expiration'] = value
                    elif key == 'memberOf':
                        if 'groups' in current_user:
                            current_user['groups'] += f", {value.split(',')[0].split('=')[1]}"
                        else:
                            current_user['groups'] = value.split(',')[0].split('=')[1]
            
            # Add the last user
            if current_user and ('uid' in current_user or 'login' in current_user):
                self.users_data.append(current_user)
            
            return len(self.users_data) > 0
        except:
            return False
    
    def parse_standard_output(self, raw_data: str):
        """
        Parse standard FreeIPA output format
        """
        lines = raw_data.split('\n')
        
        # Collect all field data
        field_data = {
            'first_names': [],
            'last_names': [],
            'uids': [],
            'emails': [],
            'expirations': [],
            'groups': []
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'First name:' in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['first_names'].append(value)
            elif 'Last name:' in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['last_names'].append(value)
            elif 'UID:' in line and 'UID number:' not in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['uids'].append(value)
            elif 'Email address:' in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['emails'].append(value)
            elif 'User password expiration:' in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['expirations'].append(value)
            elif 'Member of groups:' in line:
                value = line.split(':', 1)[1].strip()
                if value:
                    field_data['groups'].append(value)
        
        # Try to reconstruct users from field data
        max_users = max(len(v) for v in field_data.values() if v)
        
        for i in range(max_users):
            user = {}
            
            # Generate a login name if we don't have one
            if i < len(field_data['first_names']) and i < len(field_data['last_names']):
                first = field_data['first_names'][i]
                last = field_data['last_names'][i]
                user['login'] = f"{first.lower()}.{last.lower()}"
                user['first_name'] = first
                user['last_name'] = last
            elif i < len(field_data['emails']):
                email = field_data['emails'][i]
                user['login'] = email.split('@')[0]
                user['email'] = email
            else:
                user['login'] = f"user{i+1}"
            
            if i < len(field_data['uids']):
                user['uid'] = field_data['uids'][i]
            if i < len(field_data['emails']):
                user['email'] = field_data['emails'][i]
            if i < len(field_data['expirations']):
                user['password_expiration'] = field_data['expirations'][i]
            if i < len(field_data['groups']):
                user['groups'] = field_data['groups'][i]
            
            self.users_data.append(user)
    
    def display_users(self):
        """
        Display user list
        """
        if not self.users_data:
            print("No user data found")
            return
            
        print("\n" + "="*120)
        print(f"{'序号':<4} {'用户名':<15} {'名':<12} {'姓':<12} {'UID':<8} {'邮箱':<25} {'密码过期时间':<20} {'用户组':<20}")
        print("="*120)
        
        for i, user in enumerate(self.users_data, 1):
            login = user.get('login', 'N/A')
            first_name = user.get('first_name', 'N/A')
            last_name = user.get('last_name', 'N/A')
            uid = user.get('uid', 'N/A')
            email = user.get('email', 'N/A')
            expiration = user.get('password_expiration', 'N/A')
            groups = user.get('groups', 'N/A')
            
            # Truncate long fields for display
            if len(email) > 24:
                email = email[:21] + "..."
            if len(groups) > 19:
                groups = groups[:16] + "..."
            
            print(f"{i:<4} {login:<15} {first_name:<12} {last_name:<12} {uid:<8} {email:<25} {expiration:<20} {groups:<20}")
        
        print("="*120)
    
    def get_user_selection(self) -> List[str]:
        """
        Get user selection
        """
        while True:
            print("\nPlease select users to modify:")
            print("1. Enter user numbers (e.g.: 1,3,5 or 1-5)")
            print("2. Enter usernames (e.g.: user1,user2)")
            print("3. Enter 'all' to select all users")
            
            selection = input("Please enter your selection: ").strip()
            
            if not selection:
                print("Input cannot be empty, please try again")
                continue
                
            if selection.lower() == 'all':
                return [user['login'] for user in self.users_data]
            
            # Try to parse as numbers
            if re.match(r'^[\d,-]+$', selection):
                try:
                    selected_users = []
                    for part in selection.split(','):
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            for i in range(start, end + 1):
                                if 1 <= i <= len(self.users_data):
                                    selected_users.append(self.users_data[i-1]['login'])
                        else:
                            i = int(part)
                            if 1 <= i <= len(self.users_data):
                                selected_users.append(self.users_data[i-1]['login'])
                    return list(set(selected_users))  # Remove duplicates
                except ValueError:
                    print("Invalid number format, please try again")
                    continue
            
            # Try to parse as usernames
            usernames = [name.strip() for name in selection.split(',')]
            valid_usernames = [user['login'] for user in self.users_data]
            selected_users = []
            
            for username in usernames:
                if username in valid_usernames:
                    selected_users.append(username)
                else:
                    print(f"Warning: User '{username}' does not exist")
            
            if selected_users:
                return selected_users
            else:
                print("No valid users selected, please try again")
    
    def get_expiration_date(self) -> str:
        """
        Get new expiration date
        """
        while True:
            print("\nPlease select password expiration time setting:")
            print("1. Enter specific date (format: YYYYMMDD, e.g.: 20301231)")
            print("2. Enter number of days (e.g.: 365 means expire after 365 days)")
            print("3. Use default value (June 30, 2030)")
            
            choice = input("Please enter your choice (1/2/3): ").strip()
            
            if choice == '3':
                return "2030-06-30T12:00:00Z"
            elif choice == '1':
                date_str = input("Please enter date (YYYYMMDD): ").strip()
                if re.match(r'^\d{8}$', date_str):
                    try:
                        # Validate date format
                        datetime.strptime(date_str, '%Y%m%d')
                        # Convert YYYYMMDD to YYYY-MM-DD format
                        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                        return f"{formatted_date}T12:00:00Z"
                    except ValueError:
                        print("Invalid date format, please try again")
                else:
                    print("Invalid date format, please enter 8 digits")
            elif choice == '2':
                days_str = input("Please enter number of days: ").strip()
                try:
                    days = int(days_str)
                    if days > 0:
                        future_date = datetime.now() + timedelta(days=days)
                        return future_date.strftime('%Y-%m-%dT12:00:00Z')
                    else:
                        print("Number of days must be greater than 0")
                except ValueError:
                    print("Please enter a valid number")
            else:
                print("Invalid choice, please enter 1, 2, or 3")
    
    def modify_user_expiration(self, username: str, expiration_date: str) -> bool:
        """
        Modify user password expiration time
        """
        if self.demo_mode:
            print(f"✓ [DEMO] Successfully modified user {username} password expiration time to {expiration_date}")
            return True
        
        command = f"ipa user-mod {username} --setattr=krbPasswordExpiration={expiration_date}"
        ret_code, stdout, stderr = self.execute_command(command)
        
        if ret_code != 0:
            print(f"Error: Failed to modify user {username} - {stderr}")
            return False
        
        print(f"✓ Successfully modified user {username} password expiration time to {expiration_date}")
        return True
    
    def run_interactive(self):
        """
        Run interactive mode
        """
        print("FreeIPA User Password Expiration Reset Tool")
        print("="*50)
        
        # Get user list
        if not self.get_users_list():
            return False
        
        # Display user list
        self.display_users()
        
        # Get user selection
        selected_users = self.get_user_selection()
        print(f"\nSelected users: {', '.join(selected_users)}")
        
        # Get expiration time
        expiration_date = self.get_expiration_date()
        print(f"Set expiration time to: {expiration_date}")
        
        # 确认操作
        confirm = input(f"\nConfirm to modify password expiration time for {len(selected_users)} users? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled")
            return False
        
        # Execute modification
        success_count = 0
        for username in selected_users:
            if self.modify_user_expiration(username, expiration_date):
                success_count += 1
        
        print(f"\nOperation completed: Successfully modified {success_count}/{len(selected_users)} users")
        return True
    
    def run_batch(self, users: List[str], expiration_date: str):
        """
        Run batch processing mode
        """
        print("FreeIPA User Password Expiration Reset Tool - Batch Mode")
        print("="*60)
        
        print(f"Batch modify users: {', '.join(users)}")
        print(f"Set expiration time to: {expiration_date}")
        
        # Execute modification
        success_count = 0
        for username in users:
            if self.modify_user_expiration(username, expiration_date):
                success_count += 1
        
        print(f"\nOperation completed: Successfully modified {success_count}/{len(users)} users")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='FreeIPA User Password Expiration Reset Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Interactive mode
  python3 freeipa_password_reset.py
  
  # Batch mode - specify users and expiration time
  python3 freeipa_password_reset.py --users user1,user2 --expiration 2030-12-31T12:00:00Z
  
  # Demo mode (when FreeIPA is not available)
  python3 freeipa_password_reset.py --demo --list-only
  python3 freeipa_password_reset.py --demo --users testuser1,testuser2 --expiration 2030-12-31T12:00:00Z
        """
    )
    

    
    parser.add_argument(
        '--users', '-u',
        help='List of usernames to modify, separated by commas (e.g.: user1,user2,user3)'
    )
    
    parser.add_argument(
        '--expiration', '-e',
        help='Password expiration time (format: YYYY-MM-DDTHH:MM:SSZ, e.g.: 2030-12-31T12:00:00Z)'
    )
    
    parser.add_argument(
        '--list-only', '-l',
        action='store_true',
        help='Only list user information, do not modify'
    )
    
    parser.add_argument(
        '--demo', '-d',
        action='store_true',
        help='Run in demo mode with mock data (useful when FreeIPA is not available)'
    )
    
    parser.add_argument(
        '--install',
        action='store_true',
        help='Install the executable to system path (/usr/local/bin) - requires sudo'
    )
    

    
    args = parser.parse_args()
    
    # Handle installation request
    if args.install:
        tool = FreeIPAPasswordReset()
        success = tool.install_to_system()
        sys.exit(0 if success else 1)
    
    # Create tool instance
    tool = FreeIPAPasswordReset(demo_mode=args.demo)
    
    try:
        if args.list_only:
            # Only list users
            if not tool.get_users_list():
                sys.exit(1)
            tool.display_users()
            
        elif args.users and args.expiration:
            # Batch processing mode
            users = [u.strip() for u in args.users.split(',')]
            if not tool.run_batch(users, args.expiration):
                sys.exit(1)
                
        else:
            # Interactive mode
            if not tool.run_interactive():
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Program execution error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()