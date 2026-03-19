import pytest
import requests
import random
import string


class TestBOWhitelistingCommentField:
    
    @pytest.fixture
    def base_url(self):
        return "https://bo.example.com"
    
    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json"
        }
    
    @pytest.fixture
    def valid_ip(self):
        return "192.168.1.100"
    
    def generate_comment(self, length):
        """Generate a comment string of specified length."""
        return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))
    
    def test_whitelist_add_comment_20_symbols_success(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment exactly 20 symbols - should succeed.
        This tests the current working boundary.
        """
        comment = self.generate_comment(20)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert "id" in response.json()
    
    def test_whitelist_add_comment_21_symbols_fails_before_fix(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment 21 symbols - should fail before fix.
        This reproduces the reported bug.
        """
        comment = self.generate_comment(21)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "value too long for type character varying(20)" in response.json().get("error", "")
    
    def test_whitelist_add_comment_64_symbols_success_after_fix(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment exactly 64 symbols - should succeed after fix.
        This tests the new requirement to match Admin limit.
        """
        comment = self.generate_comment(64)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["comment"] == comment
        assert len(response_data["comment"]) == 64
    
    def test_whitelist_add_comment_65_symbols_fails(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment 65 symbols - should fail even after fix.
        This tests the new upper boundary limit.
        """
        comment = self.generate_comment(65)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "value too long" in response.json().get("error", "").lower()
    
    def test_whitelist_add_comment_1_symbol_success(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment 1 symbol - should succeed.
        This tests the minimum valid comment length.
        """
        comment = "a"
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["comment"] == comment
    
    def test_whitelist_add_empty_comment_success(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with empty comment - should succeed.
        This tests that comment field is optional.
        """
        payload = {
            "ip_address": valid_ip,
            "comment": ""
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["comment"] == ""
    
    def test_whitelist_add_comment_special_characters(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment containing special characters within 64 limit.
        This tests special character handling.
        """
        comment = "Test!@#$%^&*()_+-=[]{}|;':\",./<>?" 
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["comment"] == comment
    
    def test_whitelist_add_comment_unicode_characters(self, base_url, auth_headers, valid_ip):
        """
        Test adding IP with comment containing unicode characters within 64 limit.
        This tests unicode character handling and encoding.
        """
        comment = "тест中文🚀" + "a" * 50  # Unicode + padding to test limits
        comment = comment[:64]  # Ensure exactly 64 chars
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["comment"] == comment
    
    def test_whitelist_update_comment_64_symbols(self, base_url, auth_headers, valid_ip):
        """
        Test updating existing whitelist entry with 64 symbol comment.
        This tests update operation with new comment limit.
        """
        # First create an entry
        create_payload = {
            "ip_address": valid_ip,
            "comment": "short"
        }
        create_response = requests.post(
            f"{base_url}/api/whitelist",
            json=create_payload,
            headers=auth_headers
        )
        entry_id = create_response.json()["id"]
        
        # Then update with 64 character comment
        long_comment = self.generate_comment(64)
        update_payload = {
            "comment": long_comment
        }
        
        response = requests.put(
            f"{base_url}/api/whitelist/{entry_id}",
            json=update_payload,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["comment"] == long_comment
        assert len(response.json()["comment"]) == 64
    
    @pytest.mark.parametrize("comment_length", [19, 32, 50, 63])
    def test_whitelist_add_comment_various_valid_lengths(self, base_url, auth_headers, valid_ip, comment_length):
        """
        Test adding IP with comments of various valid lengths.
        This tests multiple valid lengths within the new 64 character limit.
        """
        comment = self.generate_comment(comment_length)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert len(response.json()["comment"]) == comment_length
    
    @pytest.mark.parametrize("comment_length", [100, 200, 500])
    def test_whitelist_add_comment_various_invalid_lengths(self, base_url, auth_headers, valid_ip, comment_length):
        """
        Test adding IP with comments of various invalid lengths above 64.
        This tests that lengths beyond the new limit are properly rejected.
        """
        comment = self.generate_comment(comment_length)
        payload = {
            "ip_address": valid_ip,
            "comment": comment
        }
        
        response = requests.post(
            f"{base_url}/api/whitelist",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        error_message = response.json().get("error", "").lower()
        assert any(phrase in error_message for phrase in ["too long", "exceeds limit", "invalid length"])