import pytest


@pytest.fixture
def auth_headers(client):
    client.post(
        "/auth/register", json={"username": "researcher", "password": "password123"}
    )
    login_response = client.post(
        "/auth/token", data={"username": "researcher", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_participant_crud_lifecycle(client, auth_headers):
    # 1. List participants (initially empty)
    list_response = client.get("/participants/", headers=auth_headers)
    assert list_response.status_code == 200
    assert list_response.json() == []

    # 2. Create a participant
    participant_data = {
        "subject_id": "SUB-001",
        "study_group": "treatment",
        "enrollment_date": "2026-06-12",
        "status": "active",
        "age": 45,
        "gender": "F",
    }
    create_response = client.post(
        "/participants/", json=participant_data, headers=auth_headers
    )
    assert create_response.status_code == 201
    created = create_response.json()
    participant_id = created["participant_id"]
    assert created["subject_id"] == "SUB-001"
    assert created["age"] == 45

    # 3. Create duplicate participant subject_id (should fail)
    duplicate_response = client.post(
        "/participants/", json=participant_data, headers=auth_headers
    )
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"]

    # 4. Get the created participant
    get_response = client.get(
        f"/participants/{participant_id}", headers=auth_headers
    )
    assert get_response.status_code == 200
    assert get_response.json()["subject_id"] == "SUB-001"

    # 5. Update participant (PUT)
    update_data = {
        "subject_id": "SUB-001",
        "study_group": "control",
        "enrollment_date": "2026-06-12",
        "status": "completed",
        "age": 46,
        "gender": "F",
    }
    update_response = client.put(
        f"/participants/{participant_id}", json=update_data, headers=auth_headers
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["study_group"] == "control"
    assert updated["status"] == "completed"
    assert updated["age"] == 46

    # 6. Check metrics
    metrics_response = client.get("/participants/metrics", headers=auth_headers)
    assert metrics_response.status_code == 200
    metrics = metrics_response.json()
    assert metrics["total_participants"] == 1
    assert metrics["study_groups"]["control"] == 1
    assert metrics["study_groups"]["treatment"] == 0
    assert metrics["statuses"]["completed"] == 1
    assert metrics["average_age"] == 46.0

    # 7. Delete participant
    delete_response = client.delete(
        f"/participants/{participant_id}", headers=auth_headers
    )
    assert delete_response.status_code == 204

    # 8. Retrieve deleted participant (should be 404)
    get_deleted_response = client.get(
        f"/participants/{participant_id}", headers=auth_headers
    )
    assert get_deleted_response.status_code == 404
