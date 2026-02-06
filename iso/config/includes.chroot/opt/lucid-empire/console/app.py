#!/usr/bin/env python3
"""
LUCID EMPIRE TITAN - Web Console Dashboard
Provides REST API and web UI for profile management
Complements the PyQt6 TITAN Console GUI

Port: 8080
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from functools import wraps

try:
    from flask import Flask, render_template, jsonify, request, redirect, url_for
except ImportError:
    print("Flask not installed. Install with: pip install flask")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Paths
TITAN_HOME = Path(os.environ.get('TITAN_HOME', '/opt/lucid-empire'))
USER_HOME = Path.home()
PROFILES_DIR = USER_HOME / '.lucid-empire' / 'profiles'
ACTIVE_DIR = PROFILES_DIR / 'active'
BURNED_DIR = PROFILES_DIR / 'burned'
PRESETS_DIR = TITAN_HOME / 'presets'

# Ensure directories exist
PROFILES_DIR.mkdir(parents=True, exist_ok=True)
ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
BURNED_DIR.mkdir(parents=True, exist_ok=True)


def get_active_profile():
    """Get currently active profile data."""
    profile_file = ACTIVE_DIR / 'profile.json'
    if not profile_file.exists():
        return None
    
    try:
        with open(profile_file, 'r') as f:
            data = json.load(f)
        
        # Add time offset if present
        offset_file = ACTIVE_DIR / 'time_offset'
        if offset_file.exists():
            data['time_offset'] = offset_file.read_text().strip()
        
        return data
    except Exception as e:
        print(f"Error reading profile: {e}")
        return None


def list_profiles():
    """List all available profiles."""
    profiles = []
    
    for item in PROFILES_DIR.iterdir():
        if not item.is_dir():
            continue
        if item.name in ['active', 'burned', 'templates']:
            continue
        
        profile_file = item / 'profile.json'
        if profile_file.exists():
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                
                # Check if this is the active profile
                is_active = False
                active_profile = get_active_profile()
                if active_profile and active_profile.get('profile_name') == item.name:
                    is_active = True
                
                profiles.append({
                    'name': item.name,
                    'id': data.get('profile_id', 'N/A'),
                    'created': data.get('created', 'N/A'),
                    'aging_days': data.get('aging_days', 0),
                    'template': data.get('template', 'custom'),
                    'is_active': is_active
                })
            except Exception as e:
                print(f"Error reading profile {item.name}: {e}")
    
    return sorted(profiles, key=lambda x: x['name'])


def list_presets():
    """List available profile presets/templates."""
    presets = []
    
    if PRESETS_DIR.exists():
        for item in PRESETS_DIR.glob('*.json'):
            try:
                with open(item, 'r') as f:
                    data = json.load(f)
                presets.append({
                    'id': item.stem,
                    'name': data.get('preset_name', item.stem),
                    'description': data.get('description', '')
                })
            except Exception:
                pass
    
    return presets


def get_system_status():
    """Get system status information."""
    status = {
        'ebpf_loaded': False,
        'active_profile': None,
        'network_interface': 'eth0',
        'kernel_version': '',
        'uptime': '',
        'titan_version': '5.0-TITAN'
    }
    
    # Check eBPF status
    try:
        result = subprocess.run(['ip', 'link', 'show'], 
                              capture_output=True, text=True, timeout=5)
        status['ebpf_loaded'] = 'xdp' in result.stdout.lower()
    except Exception:
        pass
    
    # Get default interface
    try:
        result = subprocess.run(
            ['ip', 'route', 'show', 'default'],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            parts = result.stdout.split()
            if 'dev' in parts:
                idx = parts.index('dev')
                if idx + 1 < len(parts):
                    status['network_interface'] = parts[idx + 1]
    except Exception:
        pass
    
    # Get kernel version
    try:
        status['kernel_version'] = subprocess.check_output(
            ['uname', '-r'], text=True, timeout=5
        ).strip()
    except Exception:
        pass
    
    # Get uptime
    try:
        status['uptime'] = subprocess.check_output(
            ['uptime', '-p'], text=True, timeout=5
        ).strip()
    except Exception:
        pass
    
    # Active profile
    active = get_active_profile()
    if active:
        status['active_profile'] = active.get('profile_name')
    
    # TITAN version
    version_file = TITAN_HOME / 'VERSION'
    if version_file.exists():
        try:
            for line in version_file.read_text().splitlines():
                if line.startswith('TITAN_VERSION='):
                    status['titan_version'] = line.split('=')[1]
                    break
        except Exception:
            pass
    
    return status


# ==================== Routes ====================

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html',
                         active_profile=get_active_profile(),
                         profiles=list_profiles(),
                         presets=list_presets(),
                         system_status=get_system_status())


@app.route('/api/status')
def api_status():
    """API: Get system status."""
    return jsonify(get_system_status())


@app.route('/api/profiles')
def api_profiles():
    """API: List all profiles."""
    return jsonify({
        'profiles': list_profiles(),
        'active': get_active_profile()
    })


@app.route('/api/profile/active')
def api_active_profile():
    """API: Get active profile details."""
    profile = get_active_profile()
    if profile:
        return jsonify(profile)
    return jsonify({'error': 'No active profile'}), 404


@app.route('/api/profile/create', methods=['POST'])
def api_create_profile():
    """API: Create new profile."""
    data = request.json or {}
    name = data.get('name', '').strip()
    aging = data.get('aging_days', 90)
    template = data.get('template', 'us_ecom_premium')
    windsurf_token = data.get('windsurf_token', '').strip()
    
    if not name:
        return jsonify({'success': False, 'error': 'Profile name required'}), 400
    
    try:
        result = subprocess.run(
            ['/opt/lucid-empire/bin/lucid-profile-mgr', 'create', name, str(aging), template],
            capture_output=True, text=True, timeout=30
        )

        response = {
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr,
            'profile': name
        }

        # If creation succeeded and a Windsurf token was provided, store it per-profile
        if result.returncode == 0 and windsurf_token:
            try:
                profile_dir = PROFILES_DIR / name
                profile_dir.mkdir(parents=True, exist_ok=True)
                token_file = profile_dir / 'windsurf_token'
                token_file.write_text(windsurf_token)
                response['windsurf_token_saved'] = True
            except Exception as e:
                response['windsurf_token_saved'] = False
                response['windsurf_token_error'] = str(e)

        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/load/<name>', methods=['POST'])
def api_load_profile(name):
    """API: Load profile as active."""
    try:
        result = subprocess.run(
            ['/opt/lucid-empire/bin/lucid-profile-mgr', 'load', name],
            capture_output=True, text=True, timeout=30
        )
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/burn', methods=['POST'])
def api_burn_profile():
    """API: Burn active profile."""
    try:
        result = subprocess.run(
            ['/opt/lucid-empire/bin/lucid-burn', '-y'],
            capture_output=True, text=True, timeout=30
        )
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/delete/<name>', methods=['DELETE'])
def api_delete_profile(name):
    """API: Delete profile permanently."""
    profile_dir = PROFILES_DIR / name
    
    if not profile_dir.exists():
        return jsonify({'success': False, 'error': 'Profile not found'}), 404
    
    try:
        import shutil
        shutil.rmtree(profile_dir)
        return jsonify({'success': True, 'message': f'Profile {name} deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/browser/launch', methods=['POST'])
def api_launch_browser():
    """API: Launch browser with active profile.
    
    TITAN V5 FINAL - No-Fork Edition:
    Uses standard Firefox ESR / Chromium with Hardware Shield.
    """
    browser = data.get('browser', 'firefox')
    
    browser_map = {
        'firefox': '/opt/lucid-empire/bin/lucid-firefox',
        'chromium': '/opt/lucid-empire/bin/lucid-chromium',
        'default': '/opt/lucid-empire/bin/lucid-firefox'
    }
    
    cmd = browser_map.get(browser, browser_map['default'])
    
    if not os.path.exists(cmd):
        return jsonify({'success': False, 'error': f'Browser launcher not found: {cmd}'}), 404
    
    try:
        subprocess.Popen([cmd], start_new_session=True)
        return jsonify({'success': True, 'message': f'{browser} launched with Hardware Shield'})

def api_ebpf_status():
    """API: Get eBPF program status."""
    status = {'loaded': False, 'programs': [], 'interface': 'unknown'}
    
    try:
        # Check XDP
        result = subprocess.run(
            ['ip', 'link', 'show'],
            capture_output=True, text=True, timeout=5
        )
        status['loaded'] = 'xdp' in result.stdout.lower()
        
        # Check bpftool if available
        if os.path.exists('/usr/sbin/bpftool'):
            result = subprocess.run(
                ['bpftool', 'prog', 'list', '--json'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                status['programs'] = json.loads(result.stdout)
    except Exception as e:
        status['error'] = str(e)
    
    return jsonify(status)


@app.route('/api/ebpf/load', methods=['POST'])
def api_ebpf_load():
    """API: Load eBPF program."""
    data = request.json or {}
    os_profile = data.get('profile', 'windows')
    interface = data.get('interface', '')
    
    try:
        cmd = ['/opt/lucid-empire/bin/load-ebpf.sh']
        if interface:
            cmd.append(interface)
        cmd.extend([os_profile, 'load'])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Templates ====================

@app.route('/templates/dashboard.html')
def serve_template():
    """Serve dashboard template."""
    return redirect(url_for('dashboard'))


# ==================== Main ====================

if __name__ == '__main__':
    # Create templates directory
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║        LUCID EMPIRE TITAN - Web Console                   ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║  Dashboard: http://127.0.0.1:8080                         ║")
    print("║  API Docs:  http://127.0.0.1:8080/api/status              ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
