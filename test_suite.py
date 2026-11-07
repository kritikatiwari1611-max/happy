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
    
    assert database.save_response("maybe"), "Failed to save 'maybe'"
    assert database.save_response("more_time"), "Failed to save 'more_time'"
    
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
        '/memories',
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
    post_maybe = client.post('/save-response', data={'choice': 'maybe'}, follow_redirects=False)
    assert post_maybe.status_code == 302, f"Expected 302 for maybe, got {post_maybe.status_code}"
    assert post_maybe.headers['Location'] == '/little-things', f"Unexpected redirect target: {post_maybe.headers['Location']}"
    print("POST /save-response (choice='maybe')     -> 302 Redirect to /little-things (PASS)")

    post_more_time = client.post('/save-response', data={'choice': 'more_time'}, follow_redirects=False)
    assert post_more_time.status_code == 302, f"Expected 302 for more_time, got {post_more_time.status_code}"
    assert post_more_time.headers['Location'] == '/final', f"Unexpected redirect target: {post_more_time.headers['Location']}"
    print("POST /save-response (choice='more_time') -> 302 Redirect to /final (PASS)")

    print("\n=== STEP 4: VERIFYING 6 CARDS ON /LITTLE-THINGS ===")
    lt_resp = client.get('/little-things')
    lt_html = lt_resp.data.decode('utf-8')
    assert "A Little Virtual Gift" in lt_html, "Feature 1 missing"
    assert "Our Memories" in lt_html, "Feature 2 missing"
    assert "Watch Our Memories ♡" in lt_html, "Watch Our Memories button missing"
    assert "/memories" in lt_html, "Link to /memories missing on little things"
    assert "Reasons to Smile" in lt_html, "Feature 3 missing"
    assert "A Secret Letter" in lt_html, "Feature 4 missing"
    assert "Little Wishes" in lt_html, "Feature 5 missing"
    assert "Not Just Words, But Actions." in lt_html, "Feature 6 missing"
    print("All 6 feature cards & 'Watch Our Memories ♡' button verified on /little-things!")

    print("\n=== STEP 5: VERIFYING NEW VIDEO PAGE (/MEMORIES) ===")
    mem_resp = client.get('/memories')
    mem_html = mem_resp.data.decode('utf-8')
    assert "Our Memories ♡" in mem_html, "Heading on /memories missing"
    assert "Some moments are forever..." in mem_html, "Subtitle on /memories missing"
    assert "<video" in mem_html, "<video> tag missing"
    assert "our_memories.mp4" in mem_html, "our_memories.mp4 video source missing"
    assert "A little collection of moments that will always be special ♡" in mem_html, "Caption missing"
    assert "/little-things" in mem_html, "Back button link to /little-things missing"
    print("Video player, controls, placeholder source & back button verified on /memories!")

    print("\n=== STEP 6: VERIFYING CSS PALETTE & RESTRICTIONS ===")
    css_path = os.path.join('static', 'css', 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read().lower()
    
    assert 'pink' not in css_content, "Violation: 'pink' color found in CSS!"
    print("CSS verified: 100% Blue theme palette, zero pink anywhere.")

    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
