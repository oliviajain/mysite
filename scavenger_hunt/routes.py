from flask import Blueprint, render_template, request, session, redirect, url_for
import json
import os

scavenger_hunt_bp = Blueprint('scavenger_hunt', __name__, url_prefix='/scavenger_hunt')

# Load clues from JSON file
def load_clues():
    clues_path = os.path.join(os.path.dirname(__file__), 'clues.json')
    with open(clues_path, 'r') as f:
        clues_dict = json.load(f)
    # Convert numeric string keys to integers, keep others as strings
    result = {}
    for k, v in clues_dict.items():
        try:
            result[int(k)] = v
        except ValueError:
            result[k] = v
    return result

CLUES = load_clues()


@scavenger_hunt_bp.route('/', methods=['GET'])
def index():
    # Show landing page with instructions
    return render_template('scavenger_hunt/landing.html')


@scavenger_hunt_bp.route('/start', methods=['GET'])
def start():
    # Initialize the session for a new game
    session['current_clue'] = 0
    session['error'] = None
    session['wrong_attempts'] = 0
    session['chosen_path'] = None
    session['path_clues'] = []
    session['show_correct'] = False
    return redirect(url_for('scavenger_hunt.hunt'))


@scavenger_hunt_bp.route('/hunt', methods=['GET', 'POST'])
def hunt():
    # Get current clue index from session
    current_clue_index = session.get('current_clue', 0)
    path_clues = session.get('path_clues', [])
    path_index = session.get('path_index', 0)
    wrong_attempts = session.get('wrong_attempts', 0)
    show_correct = session.get('show_correct', False)
    error = None
    reveal_answer = False
    
    # Determine which clue to show
    if current_clue_index <= 3:
        # Main clues (0, 1, 2, 3)
        clue_key = current_clue_index
        total_clues = 4 + 1  # 4 main clues + 1 bonus (representing the choice)
        clue_number = current_clue_index + 1
    elif path_clues:
        # Path clues (4a, 4b or 4c)
        if path_index >= len(path_clues):
            return redirect(url_for('scavenger_hunt.complete'))
        clue_key = path_clues[path_index]
        total_clues = 4 + len(path_clues)
        clue_number = 4 + path_index + 1
    else:
        # After main clues but no path chosen - redirect to choice
        return redirect(url_for('scavenger_hunt.choice'))
    
    if request.method == 'POST':
        # Check if this is a "next" button press after correct answer
        if request.form.get('action') == 'next':
            session['show_correct'] = False
            session['wrong_attempts'] = 0  # Reset wrong attempts for next clue
            
            if current_clue_index <= 3:
                # Move to next main clue
                current_clue_index += 1
                session['current_clue'] = current_clue_index
                
                # After clue 3, redirect to choice page
                if current_clue_index > 3:
                    return redirect(url_for('scavenger_hunt.choice'))
            else:
                # Move to next path clue
                path_index += 1
                session['path_index'] = path_index
                
                # Check if path is completed
                if path_index >= len(path_clues):
                    return redirect(url_for('scavenger_hunt.complete'))
            
            # Redirect to show next clue
            return redirect(url_for('scavenger_hunt.hunt'))
        
        # Otherwise, check the answer
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = CLUES[clue_key]['answer'].lower()
        
        if user_answer == correct_answer:
            # Show correct message
            session['show_correct'] = True
            show_correct = True
        else:
            # Wrong answer
            wrong_attempts += 1
            session['wrong_attempts'] = wrong_attempts
            
            if wrong_attempts >= 5:
                reveal_answer = True
                error = None
            else:
                attempts_left = 5 - wrong_attempts
                error = f"That's not correct. Try again! ({attempts_left} attempt{'s' if attempts_left != 1 else ''} left)"
    
    # Get current clue
    current_clue = CLUES[clue_key]
    correct_message = current_clue.get('correct_message', '')
    
    return render_template(
        'scavenger_hunt/hunt.html',
        clue=current_clue['clue'],
        clue_number=clue_number,
        total_clues=total_clues,
        error=error,
        reveal_answer=reveal_answer,
        correct_answer=current_clue['answer'] if reveal_answer else None,
        wrong_attempts=wrong_attempts,
        show_correct=show_correct,
        correct_message=correct_message
    )


@scavenger_hunt_bp.route('/choice', methods=['GET', 'POST'])
def choice():
    if request.method == 'POST':
        chosen_path = request.form.get('path')
        
        if chosen_path == 'A':
            session['path_clues'] = ['4a', '4b']
            session['chosen_path'] = 'A'
        elif chosen_path == 'B':
            session['path_clues'] = ['4c']
            session['chosen_path'] = 'B'
        
        session['path_index'] = 0
        session['wrong_attempts'] = 0
        session['show_correct'] = False
        return redirect(url_for('scavenger_hunt.hunt'))
    
    return render_template('scavenger_hunt/choice.html')


@scavenger_hunt_bp.route('/complete')
def complete():
    return render_template('scavenger_hunt/complete.html')

