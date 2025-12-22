"""
Pytest fixtures for test data
"""
import pytest


# Removed database seeding auto-fixture - create users manually via Django admin or backend script


@pytest.fixture(scope="function")
def test_student_credentials():
    """Test student credentials"""
    return {
        "username": "test_student",
        "password": "test_password_123",
        "role": "student"
    }


@pytest.fixture(scope="function")
def test_mentor_credentials():
    """Test mentor credentials"""
    return {
        "username": "test_mentor",
        "password": "test_password_123",
        "role": "mentor"
    }


@pytest.fixture(scope="function")
def test_floorwing_credentials():
    """Test floor wing credentials"""
    return {
        "username": "test_floorwing",
        "password": "test_password_123",
        "role": "floor_wing"
    }


@pytest.fixture(scope="function")
def test_admin_credentials():
    """Test admin credentials"""
    return {
        "username": "test_admin",
        "password": "test_password_123",
        "role": "admin"
    }


@pytest.fixture(scope="function")
def invalid_credentials():
    """Invalid credentials for negative testing"""
    return {
        "username": "invalid_user",
        "password": "wrong_password",
    }
