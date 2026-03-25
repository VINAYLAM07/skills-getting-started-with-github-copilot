import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    # Arrange
    expected_activities = activities
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities

def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = activities[activity_name]["participants"].copy()
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]
    # Cleanup
    activities[activity_name]["participants"] = initial_participants

def test_signup_activity_not_found():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_signup_already_signed():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_unregister_success():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already in participants
    initial_participants = activities[activity_name]["participants"].copy()
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]
    # Cleanup
    activities[activity_name]["participants"] = initial_participants

def test_unregister_activity_not_found():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_unregister_not_signed():
    # Arrange
    activity_name = "Chess Club"
    email = "notsigned@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}

def test_root_redirect():
    # Arrange
    client_no_redirect = TestClient(app, follow_redirects=False)
    
    # Act
    response = client_no_redirect.get("/")
    
    # Assert
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"
