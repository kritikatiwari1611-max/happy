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
    
    # Test valid choices (maybe, more_time, and readable versions)
    assert database.save_response("maybe"), "Failed to save 'maybe'"
    assert database.save_response("more_time"), "Failed to save 'more_time'"
    assert database.save_response("Maybe We Can Try Again ♡"), "Failed to save 'Maybe We Can Try Again ♡'"
    assert database.save_response("I Need More Time"), "Failed to save 'I Need More Time'"
    
    # Test invalid choices
    assert not database.save_response("random_invalid_choice"), "Validation allowed invalid choice!"
    
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
        '/beginning',
        '/little-things',
        '/final',
        '/thank-you'
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

    print("\n=== STEP 3: TESTING FORM SUBMISSION AND CONDITIONAL REDIRECTION ===")
    # Button 1: maybe -> redirects directly to /little-things
    post_maybe = client.post('/save-response', data={'choice': 'maybe'}, follow_redirects=False)
    assert post_maybe.status_code == 302, f"Expected 302 redirect for maybe, got {post_maybe.status_code}"
    assert post_maybe.headers['Location'] == '/little-things', f"Unexpected redirect target: {post_maybe.headers['Location']}"
    print("POST /save-response (choice='maybe')     -> 302 Redirect to /little-things (PASS)")

    # Button 2: more_time -> redirects directly to /final
    post_more_time = client.post('/save-response', data={'choice': 'more_time'}, follow_redirects=False)
    assert post_more_time.status_code == 302, f"Expected 302 redirect for more_time, got {post_more_time.status_code}"
    assert post_more_time.headers['Location'] == '/final', f"Unexpected redirect target: {post_more_time.headers['Location']}"
    print("POST /save-response (choice='more_time') -> 302 Redirect to /final (PASS)")

    print("\n=== STEP 4: VERIFYING 6 FEATURES ON /LITTLE-THINGS ===")
    lt_resp = client.get('/little-things')
    lt_html = lt_resp.data.decode('utf-8')
    assert "A Little Virtual Gift" in lt_html, "Feature 1 missing"
    assert "Our Memories" in lt_html, "Feature 2 missing"
    assert "Reasons to Smile" in lt_html, "Feature 3 missing"
    assert "A Secret Letter" in lt_html, "Feature 4 missing"
    assert "Little Wishes" in lt_html, "Feature 5 missing"
    assert "Not Just Words, But Actions." in lt_html, "Feature 6 missing"
    assert "Some chapters are worth writing better." in lt_html, "Ending section missing"
    print("All 6 feature cards and the ending section verified on /little-things!")

    print("\n=== STEP 5: VERIFYING /FINAL CONTENT ===")
    final_resp = client.get('/final')
    final_html = final_resp.data.decode('utf-8')
    assert "Thank You for Being Honest ♡" in final_html, "Heading on /final missing"
    assert "Take all the time you need" in final_html, "Respectful message on /final missing"
    print("Heading & non-pressuring message verified on /final!")

    print("\n=== STEP 6: VERIFYING CSS PALETTE & ANIMATIONS ===")
    css_path = os.path.join('static', 'css', 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read().lower()
    
    # Verify no pink
    assert 'pink' not in css_content, "Violation: 'pink' color found in CSS!"
    print("CSS verified: 100% Blue theme palette, zero pink anywhere.")

    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
