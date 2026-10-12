import json
import os
import hmac
import tempfile
import secrets
from datetime import date
from functools import wraps
from pathlib import Path

from flask import current_app, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from wedding import wedding_bp


WEDDING_DATE = date(2027, 5, 22)


def _data_path():
    configured = current_app.config.get('WEDDING_DATA_FILE')
    if configured:
        return Path(configured)
    return Path(current_app.instance_path) / 'wedding_data.json'


def _load_wedding_data():
    path = _data_path()
    if not path.exists():
        return {
            'couple': 'Private Wedding Planner',
            'weekend': 'May 2027',
            'location': 'San Diego',
            'phase': 'Planning',
            'guest_count': '—',
            'budget': {},
            'tasks': [],
            'vendors': [],
            'payments': [],
            'events': [],
            'india_trip': [],
            'design': {},
        }
    with path.open(encoding='utf-8') as wedding_file:
        return json.load(wedding_file)


def _save_wedding_data(data):
    """Atomically save shared wedding data on the server for cross-device access."""
    path = _data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix='.wedding-data-', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            json.dump(data, output, ensure_ascii=False, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp_name, path)
        try:
            os.chmod(path, 0o600)
        except OSError:
            current_app.logger.warning('Could not restrict permissions on wedding data file.')
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def wedding_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('wedding_authenticated'):
            return redirect(url_for('wedding.login', next=request.path))
        return view(*args, **kwargs)
    return wrapped


@wedding_bp.route('/wedding/login', methods=['GET', 'POST'])
def login():
    if session.get('wedding_authenticated'):
        return redirect(url_for('wedding.index'))

    error = None
    if request.method == 'POST':
        password_hash = current_app.config.get('WEDDING_PASSWORD_HASH')
        if not password_hash:
            current_app.logger.error('WEDDING_PASSWORD_HASH is not configured.')
            error = 'Wedding login is not configured yet.'
        elif check_password_hash(password_hash, request.form.get('password', '')):
            session.clear()
            session['wedding_authenticated'] = True
            session.permanent = True
            return redirect(url_for('wedding.index'))
        else:
            error = 'Incorrect password. Please try again.'

    return render_template('wedding/login.html', error=error)


@wedding_bp.route('/wedding/logout', methods=['POST'])
def logout():
    session.pop('wedding_authenticated', None)
    return redirect(url_for('wedding.login'))


@wedding_bp.route('/wedding')
@wedding_login_required
def index():
    data = _load_wedding_data()
    # Keep a per-session CSRF token for checklist updates.
    if not session.get('wedding_csrf_token'):
        session['wedding_csrf_token'] = secrets.token_urlsafe(32)
    days_to_go = max((WEDDING_DATE - date.today()).days, 0)
    return render_template(
        'wedding/index.html',
        data=data,
        days_to_go=days_to_go,
        csrf_token=session['wedding_csrf_token'],
    )


@wedding_bp.route('/wedding/checklist/<task_id>', methods=['POST'])
@wedding_login_required
def update_checklist_task(task_id):
    supplied_token = request.headers.get('X-CSRF-Token', '')
    expected_token = session.get('wedding_csrf_token', '')
    if not expected_token or not hmac.compare_digest(supplied_token, expected_token):
        return jsonify({'ok': False, 'error': 'Security token expired. Refresh the page and try again.'}), 400

    payload = request.get_json(silent=True) or {}
    completed = payload.get('completed')
    if not isinstance(completed, bool):
        return jsonify({'ok': False, 'error': 'Invalid completion value.'}), 400

    data = _load_wedding_data()
    phases = data.get('checklist_phases', [])
    for phase in phases:
        for task in phase.get('tasks', []):
            if task.get('id') == task_id:
                task['completed'] = completed
                _save_wedding_data(data)
                return jsonify({'ok': True, 'task_id': task_id, 'completed': completed})

    return jsonify({'ok': False, 'error': 'Checklist task not found.'}), 404
