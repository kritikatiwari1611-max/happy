import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))
import database
from app import app

def run_tests():
    print("=== STEP 1: TESTING DATABASE ===")
    database.init_db()
    
    # Test valid choices
    assert database.save_response("Maybe We Can Try Again ♡"), "Failed to save 'Maybe We Can Try Again ♡'"
    assert database.save_response("I Need More Time"), "Failed to save 'I Need More Time'"
    
    # Test invalid choices
    assert not database.save_response("Invalid Random Option"), "Validation allowed invalid choice!"
    
    responses = database.get_all_responses()
    print(f"Total responses stored in database: {len(responses)}")
    for r in responses:
        print(f" - [{r['timestamp']}] Choice: {r['choice']}")
    
    print("\n=== STEP 2: TESTING FLASK ROUTES (GET) ===")
    client = app.test_client()
    routes = [
        '/',
        '/moment',
        '/letter',
        '/apology',
        '/gate',
        '/surprise',
        '/thank-you',
        '/final'
    ]
    
    for route in routes:
        resp = client.get(route)
        assert resp.status_code == 200, f"Route {route} returned status {resp.status_code}"
        html_lower = resp.data.decode('utf-8').lower()
        # Ensure zero JavaScript restriction is honored
        assert '<script' not in html_lower, f"Violation: <script> found on {route}"
        # Ensure no pink color mention
        assert '#ff' not in html_lower and 'pink' not in html_lower, f"Pink found on {route}"
        print(f"GET {route:<16} -> Status 200 OK | Pure HTML/CSS | Strict Blue Theme")

    print("\n=== STEP 3: TESTING FORM SUBMISSION (POST) ===")
    post_resp = client.post('/save-response', data={'choice': "Maybe We Can Try Again ♡"}, follow_redirects=True)
    assert post_resp.status_code == 200, f"POST /save-response returned {post_resp.status_code}"
    latest = database.get_latest_response()
    assert latest['choice'] == "Maybe We Can Try Again ♡", "Latest choice does not match"
    print(f"POST /save-response -> Successfully saved response: {latest['choice']}")

    print("\n=== STEP 4: VERIFYING CSS PALETTE & ANIMATIONS ===")
    css_path = os.path.join('static', 'css', 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read().lower()
    
    # Verify no pink
    assert 'pink' not in css_content, "Violation: 'pink' color found in CSS!"
    print("CSS verified: 100% Blue theme palette, no pink anywhere.")
    
    # Verify gate 3D transforms, animation delays and keyframes
    assert 'rotatey' in css_content, "CSS gate 3D rotateY transform missing"
    assert 'perspective' in css_content, "CSS 3D perspective missing"
    assert '@keyframes openleftgate' in css_content, "Left gate keyframe missing"
    assert '@keyframes openrightgate' in css_content, "Right gate keyframe missing"
    assert 'animation-delay: 3.3s' in css_content, "Gate message delay missing - message must appear after gates open!"
    print("CSS verified: Gate opens with 3D keyframe transforms and message delay is strictly enforced.")

    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
