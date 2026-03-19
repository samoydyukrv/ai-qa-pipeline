import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


class TestGetPostById:
    
    def test_get_valid_post_returns_200_with_correct_fields(self):
        """Test that a valid post ID returns 200 status with all required fields."""
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

    def test_get_post_with_maximum_valid_id(self):
        """Test retrieving a post with the highest valid ID (100)."""
        post_id = 100
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == post_id
        assert len(data["title"]) > 0
        assert len(data["body"]) > 0
        assert data["userId"] > 0

    def test_get_post_with_minimum_valid_id(self):
        """Test retrieving a post with the lowest valid ID (1)."""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == post_id
        assert len(data["title"]) > 0
        assert len(data["body"]) > 0
        assert data["userId"] > 0

    def test_get_post_with_nonexistent_id_returns_404(self):
        """Test that requesting a non-existent post ID returns 404."""
        post_id = 999
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_zero_id_returns_404(self):
        """Test that requesting post with ID 0 returns 404."""
        post_id = 0
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_negative_id_returns_404(self):
        """Test that requesting post with negative ID returns 404."""
        post_id = -1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_string_id_returns_404(self):
        """Test that requesting post with string ID returns 404."""
        post_id = "invalid"
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_float_id_returns_404(self):
        """Test that requesting post with float ID returns 404."""
        post_id = "1.5"
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_very_large_id_returns_404(self):
        """Test that requesting post with very large ID returns 404."""
        post_id = 999999999
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_special_characters_in_id_returns_404(self):
        """Test that requesting post with special characters in ID returns 404."""
        post_id = "1@#$"
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 404

    def test_get_post_with_empty_id_returns_different_endpoint(self):
        """Test that empty ID in path calls different endpoint (all posts)."""
        response = requests.get(f"{BASE_URL}/posts/")
        
        # This should return all posts, not a single post
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 1

    def test_get_post_response_content_type_is_json(self):
        """Test that the response content type is application/json."""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_get_post_response_has_no_extra_fields(self):
        """Test that response contains only expected fields."""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        
        data = response.json()
        expected_fields = {"id", "title", "body", "userId"}
        actual_fields = set(data.keys())
        
        assert actual_fields == expected_fields

    def test_get_post_field_values_are_not_empty_strings(self):
        """Test that title and body fields are not empty strings."""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"].strip() != ""
        assert data["body"].strip() != ""

    # def test_get_post_user_id_is_positive(self):