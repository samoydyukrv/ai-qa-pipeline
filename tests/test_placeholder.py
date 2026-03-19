import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


class TestGetPostById:
    
    def test_get_post_by_valid_id_returns_200_with_correct_fields(self):
        """Test that GET /posts/{id} returns 200 with correct response fields for valid post ID."""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert "userId" in data
        
        assert isinstance(data["id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["body"], str)
        assert isinstance(data["userId"], int)
        
        assert data["id"] == post_id

    def test_get_post_by_nonexistent_id_returns_404(self):
        """Test that GET /posts/{id} returns 404 for non-existent post ID."""
        post_id = 999999
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_by_zero_id_returns_404(self):
        """Test that GET /posts/0 returns 404 since post IDs start from 1."""
        response = requests.get(f"{BASE_URL}/posts/0")
        
        assert response.status_code == 404

    def test_get_post_by_negative_id_returns_404(self):
        """Test that GET /posts/{negative_id} returns 404 for negative post ID."""
        response = requests.get(f"{BASE_URL}/posts/-1")
        
        assert response.status_code == 404

    def test_get_post_by_string_id_returns_404(self):
        """Test that GET /posts/{string} returns 404 for non-numeric post ID."""
        response = requests.get(f"{BASE_URL}/posts/abc")
        
        assert response.status_code == 404

    def test_get_post_by_float_id_returns_404(self):
        """Test that GET /posts/{float} returns 404 for float post ID."""
        response = requests.get(f"{BASE_URL}/posts/1.5")
        
        assert response.status_code == 404

    def test_get_post_by_very_large_id_returns_404(self):
        """Test that GET /posts/{large_id} returns 404 for very large post ID."""
        response = requests.get(f"{BASE_URL}/posts/9999999999999999")
        
        assert response.status_code == 404

    def test_get_post_with_special_characters_in_id_returns_404(self):
        """Test that GET /posts/{special_chars} returns 404 for ID with special characters."""
        response = requests.get(f"{BASE_URL}/posts/1@#$")
        
        assert response.status_code == 404

    def test_get_post_response_content_type_is_json(self):
        """Test that GET /posts/{id} returns response with JSON content type."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_get_post_response_fields_not_empty_for_valid_post(self):
        """Test that GET /posts/{id} returns non-empty title and body for valid post."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["title"]) > 0
        assert len(data["body"]) > 0
        assert data["userId"] > 0

    def test_get_multiple_different_posts_have_different_content(self):
        """Test that different post IDs return different content."""
        response1 = requests.get(f"{BASE_URL}/posts/1")
        response2 = requests.get(f"{BASE_URL}/posts/2")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1["id"] != data2["id"]
        assert data1["title"] != data2["title"]
        assert data1["body"] != data2["body"]

    def test_get_post_id_matches_requested_id(self):
        """Test that the returned post ID matches the requested ID."""
        test_ids = [1, 5, 10, 50]
        
        for post_id in test_ids:
            response = requests.get(f"{BASE_URL}/posts/{post_id}")
            if response.status_code == 200:
                data = response.json()
                assert data["id"] == post_id

    def test_get_post_user_id_is_positive_integer(self):
        """Test that userId field is a positive integer for valid posts."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data["userId"], int)
        assert data["userId"] > 0

    def test_get_post_with_empty_id_returns_all_posts(self):
        """Test that GET /posts/ (without ID) returns all posts with 200 status."""
        response = requests.get(f"{BASE_URL}/posts/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify first post has required fields
        if data:
            post = data[0]
            assert "id" in post
            assert "title" in post
            assert "body" in post
            assert "userId" in post